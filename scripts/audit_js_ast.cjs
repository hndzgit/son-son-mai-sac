// Parse downloaded JavaScript as data. Never execute code from the website.
const fs = require('node:fs');
const path = require('node:path');
const acorn = require(process.env.ACORN_PATH || '/tmp/ssms-audit-tools/node_modules/acorn');
const dir = process.argv[2];
const output = process.argv[3];
function files(p) {return fs.readdirSync(p,{withFileTypes:true}).flatMap(e=>e.isDirectory()?files(path.join(p,e.name)):[path.join(p,e.name)]);}
const missing = Symbol('dynamic');
function value(n) {
  if (!n) return missing;
  if (n.type==='Literal') return n.regex || typeof n.value==='bigint' ? missing : n.value;
  if (n.type==='UnaryExpression') {const v=value(n.argument);if(v===missing)return missing; if(n.operator==='!')return !v;if(n.operator==='-')return -v;if(n.operator==='+')return +v;return missing;}
  if (n.type==='ArrayExpression') {const a=n.elements.map(value);return a.includes(missing)?missing:a;}
  if (n.type==='ObjectExpression') {const o={};for(const p of n.properties){if(p.type!=='Property'||p.kind!=='init'||p.method)return missing;const k=p.computed?value(p.key):(p.key.name??p.key.value),v=value(p.value);if(k===missing||v===missing)return missing;Object.defineProperty(o,k,{value:v,enumerable:true,configurable:true});}return o;}
  if (n.type==='BinaryExpression' && n.operator==='+'){const a=value(n.left),b=value(n.right);return a===missing||b===missing?missing:a+b;}
  if (n.type==='TemplateLiteral' && !n.expressions.length) return n.quasis[0].value.cooked;
  return missing;
}
const result=[];
for(const f of files(dir).filter(f=>f.endsWith('.js'))){
  const s=fs.readFileSync(f,'utf8'),row={file:path.relative(dir,f),strings:[],json_parse:[],static_data:[],templates:[]};
  try {
    const ast=acorn.parse(s,{ecmaVersion:'latest',sourceType:'script',locations:true,allowReturnOutsideFunction:true});
    function walk(n,parent,key){
      if(!n||!n.type)return;
      if(n.type==='Literal' && typeof n.value==='string')row.strings.push({start:n.start,end:n.end,line:n.loc.start.line,column:n.loc.start.column,value:n.value,parent_type:parent?.type,property:parent?.type==='Property'?(parent.key.name??parent.key.value):key});
      if(n.type==='TemplateLiteral')row.templates.push({start:n.start,end:n.end,raw:s.slice(n.start,n.end),parts:n.quasis.map(q=>q.value.cooked)});
      if(n.type==='CallExpression' && n.callee.type==='MemberExpression' && n.callee.object.name==='JSON' && n.callee.property.name==='parse'){
        const v=value(n.arguments[0]);if(typeof v==='string'){try{row.json_parse.push({start:n.start,end:n.end,value:JSON.parse(v)});}catch(e){row.json_parse.push({start:n.start,error:e.message});}}
      }
      if(n.type==='ObjectExpression'||n.type==='ArrayExpression'){
        const v=value(n);if(v!==missing){row.static_data.push({start:n.start,end:n.end,value:v});/* Strings inside still need exact provenance. */}
      }
      for(const [k,v]of Object.entries(n)){if(['loc','start','end'].includes(k))continue;if(Array.isArray(v)){for(const x of v)if(x?.type)walk(x,n,k);}else if(v?.type)walk(v,n,k);}
    }
    walk(ast);
    // Keep maximal static structures; child values remain included in the parent.
    row.static_data=row.static_data.filter((n,i,a)=>!a.some((p,j)=>i!==j&&p.start<=n.start&&p.end>=n.end));
  }catch(e){row.parse_error=e.message;}
  result.push(row);
}
fs.mkdirSync(path.dirname(output),{recursive:true});fs.writeFileSync(output,JSON.stringify(result,null,2));
console.log(JSON.stringify({files:result.length,errors:result.filter(r=>r.parse_error),strings:result.reduce((a,r)=>a+r.strings.length,0),json_blocks:result.reduce((a,r)=>a+r.json_parse.length,0),static_data:result.reduce((a,r)=>a+r.static_data.length,0)}));
