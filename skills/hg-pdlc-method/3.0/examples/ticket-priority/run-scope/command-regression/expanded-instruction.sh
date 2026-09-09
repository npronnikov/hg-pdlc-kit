set -euo pipefail
rm -f pdlc-run-regression-before.json pdlc-run-regression-receipt.json
# Quoted heredoc + json_string: feature/context values are DATA, never shell code.
cat > pdlc-run-regression-input.json <<'HG_INPUT_JSON'
{"change_id":"CHG-ticket-priority-a1b2c3","attempt":1,"node_id":"command-regression"}
HG_INPUT_JSON
rm -f pdlc-run-nfr-report.json
: > pdlc-run-regression.log
rc=0
node tools/hg/verify.mjs snapshot pdlc-run-regression-input.json pdlc-run-regression-before.json >> pdlc-run-regression.log 2>&1 || rc=$?
if [ "$rc" -eq 0 ]; then
  timeout 900 bash tools/hg/build.sh pdlc-run-nfr-report.json >> pdlc-run-regression.log 2>&1 || rc=$?
fi

# Receipt creation records result; it does not know the graph or select a next node.
node tools/hg/verify.mjs receipt regression pdlc-run-regression-input.json pdlc-run-regression-before.json pdlc-run-regression-receipt.json "$rc" pdlc-run-regression.log pdlc-run-nfr-report.json
# Only HG SDLC interprets route and controls the transition.
node --input-type=module - pdlc-run-regression-receipt.json <<'HG_STEP_JS'
import fs from 'node:fs';
const r = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const s = {step_id:r.node_id, attempt:r.attempt, status:'done',
  route:r.passed ? 'on_success' : 'on_rework', exit_code:r.exit_code,
  actions:['Executed regression check; actual evidence: pdlc-run-regression-receipt.json'],
  rework_instruction:r.passed ? '' : 'regression failed. Read pdlc-run-regression-receipt.json and pdlc-run-regression.log; fix the cause, never suppress exit or weaken acceptance.',
  feedback_id:r.node_id+':'+r.attempt, basis_hash:r.contract_hash};
console.log('STEP_SUMMARY:\n```json\n'+JSON.stringify(s,null,2)+'\n```');
HG_STEP_JS
