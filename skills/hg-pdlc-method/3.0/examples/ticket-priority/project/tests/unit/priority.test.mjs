import test from 'node:test';
import assert from 'node:assert/strict';
import {parsePriority} from '../../apps/api/priority.mjs';
test('accepts all documented enum values',()=>{for(const priority of ['low','normal','high'])assert.deepEqual(parsePriority({priority,expectedVersion:1}),{priority,expectedVersion:1});});
test('rejects unknown priority',()=>assert.throws(()=>parsePriority({priority:'urgent',expectedVersion:1}),/invalid_priority/));
test('rejects missing or non-integer version',()=>{for(const expectedVersion of [undefined,0,-1,1.5,'1'])assert.throws(()=>parsePriority({priority:'high',expectedVersion}),/invalid_version/);});
test('rejects unknown fields and non-object body',()=>{assert.throws(()=>parsePriority({priority:'high',expectedVersion:1,owner:'bob'}),/unknown_field/);assert.throws(()=>parsePriority([]),/object_required/);});
