set -euo pipefail
rm -f pdlc-run-build-before.json pdlc-run-build-receipt.json
# Quoted heredoc + json_string: feature/context values are DATA, never shell code.
cat > pdlc-run-build-input.json <<'HG_INPUT_JSON'
{"change_id":"CHG-ticket-priority-a1b2c3","attempt":1,"node_id":"command-build"}
HG_INPUT_JSON
: > pdlc-run-build.log
rc=0
node tools/hg/verify.mjs snapshot pdlc-run-build-input.json pdlc-run-build-before.json >> pdlc-run-build.log 2>&1 || rc=$?
if [ "$rc" -eq 0 ]; then
  timeout 900 bash tools/hg/build.sh - >> pdlc-run-build.log 2>&1 || rc=$?
fi

# Receipt creation records result; it does not know the graph or select a next node.
node tools/hg/verify.mjs receipt build pdlc-run-build-input.json pdlc-run-build-before.json pdlc-run-build-receipt.json "$rc" pdlc-run-build.log -
# Only HG SDLC interprets route and controls the transition.
node --input-type=module - pdlc-run-build-receipt.json <<'HG_STEP_JS'
import fs from 'node:fs';
const r = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const s = {step_id:r.node_id, attempt:r.attempt, status:'done',
  route:r.passed ? 'on_success' : 'on_rework', exit_code:r.exit_code,
  actions:['Executed build check; actual evidence: pdlc-run-build-receipt.json'],
  rework_instruction:r.passed ? '' : 'build failed. Read pdlc-run-build-receipt.json and pdlc-run-build.log; fix the cause, never suppress exit or weaken acceptance.',
  feedback_id:r.node_id+':'+r.attempt, basis_hash:r.contract_hash};
console.log('STEP_SUMMARY:\n```json\n'+JSON.stringify(s,null,2)+'\n```');
HG_STEP_JS
