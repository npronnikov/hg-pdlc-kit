set -euo pipefail
rm -f pdlc-run-contract-before.json pdlc-run-contract-receipt.json
# Quoted heredoc + json_string: feature/context values are DATA, never shell code.
cat > pdlc-run-contract-input.json <<'HG_INPUT_JSON'
{"change_id":"${((step["ai-context"].change_id)!"")?json_string}","attempt":${(((step["command-contract-check"].attempt)!0)+1)?c},"node_id":"command-contract-check"}
HG_INPUT_JSON
: > pdlc-run-contract.log
rc=0
node tools/hg/verify.mjs snapshot pdlc-run-contract-input.json pdlc-run-contract-before.json >> pdlc-run-contract.log 2>&1 || rc=$?
if [ "$rc" -eq 0 ]; then
  node tools/hg/verify.mjs spec pdlc-run-contract-input.json >> pdlc-run-contract.log 2>&1 || rc=$?
fi

# Receipt creation records result; it does not know the graph or select a next node.
node tools/hg/verify.mjs receipt contract pdlc-run-contract-input.json pdlc-run-contract-before.json pdlc-run-contract-receipt.json "$rc" pdlc-run-contract.log -
# Only HG SDLC interprets route and controls the transition.
node --input-type=module - pdlc-run-contract-receipt.json <<'HG_STEP_JS'
import fs from 'node:fs';
const r = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const s = {step_id:r.node_id, attempt:r.attempt, status:'done',
  route:r.passed ? 'on_success' : 'on_rework', exit_code:r.exit_code,
  actions:['Executed contract check; actual evidence: pdlc-run-contract-receipt.json'],
  rework_instruction:r.passed ? '' : 'contract failed. Read pdlc-run-contract-receipt.json and pdlc-run-contract.log; fix the cause, never suppress exit or weaken acceptance.',
  feedback_id:r.node_id+':'+r.attempt, basis_hash:r.contract_hash};
console.log('STEP_SUMMARY:\n```json\n'+JSON.stringify(s,null,2)+'\n```');
HG_STEP_JS
