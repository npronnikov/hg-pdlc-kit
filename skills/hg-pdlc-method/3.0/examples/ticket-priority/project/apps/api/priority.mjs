export const priorities=Object.freeze(['low','normal','high']);
export function parsePriority(body){
 if(!body || typeof body!=='object' || Array.isArray(body))throw new Error('object_required');
 if(!priorities.includes(body.priority))throw new Error('invalid_priority');
 if(!Number.isSafeInteger(body.expectedVersion)||body.expectedVersion<1)throw new Error('invalid_version');
 if(Object.keys(body).some(k=>!['priority','expectedVersion'].includes(k)))throw new Error('unknown_field');
 return {priority:body.priority,expectedVersion:body.expectedVersion};
}
