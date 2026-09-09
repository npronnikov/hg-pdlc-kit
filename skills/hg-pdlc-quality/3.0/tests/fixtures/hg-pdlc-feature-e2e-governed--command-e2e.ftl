set -euo pipefail
rm -f pdlc-run-e2e-before.json pdlc-run-e2e-receipt.json
# Quoted heredoc + json_string: feature/context values are DATA, never shell code.
cat > pdlc-run-e2e-input.json <<'HG_INPUT_JSON'
{"change_id":"${((step["ai-context"].change_id)!"")?json_string}","attempt":${(((step["command-e2e"].attempt)!0)+1)?c},"node_id":"command-e2e"}
HG_INPUT_JSON
rm -f pdlc-run-e2e-report.json
: > pdlc-run-e2e.log
rc=0
node tools/hg/verify.mjs snapshot pdlc-run-e2e-input.json pdlc-run-e2e-before.json >> pdlc-run-e2e.log 2>&1 || rc=$?
if [ "$rc" -eq 0 ]; then
  rm -f pdlc-run-e2e-report.json
  timeout 900 bash tools/hg/e2e.sh pdlc-run-e2e-report.json >> pdlc-run-e2e.log 2>&1 || rc=$?
fi
if [ ! -f pdlc-run-e2e-report.json ]; then
  printf '%s\n' '{"runner":"not_started","cases":[],"error":"Fresh E2E report missing"}' > pdlc-run-e2e-report.json
fi
if [ "$rc" -eq 0 ]; then
  node tools/hg/verify.mjs e2e pdlc-run-e2e-input.json pdlc-run-e2e-report.json >> pdlc-run-e2e.log 2>&1 || rc=$?
fi
# Receipt creation records result; it does not know the graph or select a next node.
node tools/hg/verify.mjs receipt e2e pdlc-run-e2e-input.json pdlc-run-e2e-before.json pdlc-run-e2e-receipt.json "$rc" pdlc-run-e2e.log pdlc-run-e2e-report.json
# Only HG SDLC interprets route and controls the transition.
node --input-type=module - pdlc-run-e2e-receipt.json <<'HG_STEP_JS'
import fs from 'node:fs';
const r = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const s = {step_id:r.node_id, attempt:r.attempt, status:'done',
  route:r.passed ? 'on_success' : 'on_rework', exit_code:r.exit_code,
  actions:['Executed e2e check; actual evidence: pdlc-run-e2e-receipt.json'],
  rework_instruction:r.passed ? '' : 'e2e failed. Read pdlc-run-e2e-receipt.json and pdlc-run-e2e.log; fix the cause, never suppress exit or weaken acceptance.',
  feedback_id:r.node_id+':'+r.attempt, basis_hash:r.contract_hash};
console.log('STEP_SUMMARY:\n```json\n'+JSON.stringify(s,null,2)+'\n```');
HG_STEP_JS
