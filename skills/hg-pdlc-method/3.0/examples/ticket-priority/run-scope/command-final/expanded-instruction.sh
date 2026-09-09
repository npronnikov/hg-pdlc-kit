set -euo pipefail
rm -f pdlc-run-final-before.json pdlc-run-final-receipt.json
# Quoted heredoc + json_string: feature/context values are DATA, never shell code.
cat > pdlc-run-final-input.json <<'HG_INPUT_JSON'
{"change_id":"CHG-ticket-priority-a1b2c3","attempt":1,"node_id":"command-final"}
HG_INPUT_JSON
: > pdlc-run-final.log
rc=0
node tools/hg/verify.mjs snapshot pdlc-run-final-input.json pdlc-run-final-before.json >> pdlc-run-final.log 2>&1 || rc=$?
if [ "$rc" -eq 0 ]; then
  node tools/hg/verify.mjs final pdlc-run-final-input.json >> pdlc-run-final.log 2>&1 || rc=$?
fi

# Receipt creation records result; it does not know the graph or select a next node.
node tools/hg/verify.mjs receipt final pdlc-run-final-input.json pdlc-run-final-before.json pdlc-run-final-receipt.json "$rc" pdlc-run-final.log -
# Only HG SDLC interprets route and controls the transition.
node --input-type=module - pdlc-run-final-receipt.json <<'HG_STEP_JS'
import fs from 'node:fs';
const r = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const input=JSON.parse(fs.readFileSync('pdlc-run-final-input.json','utf8'));
if(!/^CHG-[a-z0-9-]{1,100}$/.test(input.change_id))throw new Error('Invalid change ID');
const target='docs/changes/'+input.change_id+'/evidence/final-check-receipt.json';
fs.mkdirSync('docs/changes/'+input.change_id+'/evidence',{recursive:true});
fs.writeFileSync(target,JSON.stringify(r,null,2)+'\n');
const s = {step_id:r.node_id, attempt:r.attempt, status:'done',
  route:r.passed ? 'on_success' : 'on_rework', exit_code:r.exit_code,
  actions:['Executed final check; actual evidence: pdlc-run-final-receipt.json'],
  rework_instruction:r.passed ? '' : 'final failed. Read pdlc-run-final-receipt.json and pdlc-run-final.log; fix the cause, never suppress exit or weaken acceptance.',
  feedback_id:r.node_id+':'+r.attempt, basis_hash:r.contract_hash};
console.log('STEP_SUMMARY:\n```json\n'+JSON.stringify(s,null,2)+'\n```');
HG_STEP_JS
