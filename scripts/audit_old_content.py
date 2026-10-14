#!/usr/bin/env python3
"""Read-only provenance audit of the 29 previously authored content files.

Writes only doi_chieu_noi_dung_cu.{json,md}. A textual hit is not a claim
verification, and absence of a textual hit is not evidence that a claim is false.
"""
from __future__ import annotations
import ast
import bisect
import collections
import hashlib
import html
import json
from pathlib import Path
import re
import struct
import unicodedata
from urllib.parse import unquote, urlsplit
from datetime import datetime
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / 'kiem_tra_2026-10-12'
RAW = AUDIT / 'ban_chup_goc'
OLD = ROOT / 'du_lieu_noi_dung'


def rel(p):
    return str(p.relative_to(ROOT))


def norm(s):
    s = html.unescape(unicodedata.normalize('NFKC', str(s)))
    s = s.translate(str.maketrans({'“':'"', '”':'"', '‘':"'", '’':"'", '–':'-', '—':'-', '\u200b':''}))
    return re.sub(r'\s+', ' ', s).strip().casefold()


def leaves(obj, path='$'):
    if isinstance(obj, dict):
        for k,v in obj.items():
            yield from leaves(v, path+'['+json.dumps(k, ensure_ascii=False)+']')
    elif isinstance(obj,list):
        for i,v in enumerate(obj):
            yield from leaves(v, f'{path}[{i}]')
    else:
        yield path,obj


class Corpus:
    def __init__(self):
        self.records=[]
        self.index={}
        self.nindex={}

    def add(self, text, **meta):
        if not isinstance(text,str) or not text:
            return
        self.records.append({'text':text, **meta})
        self.index.setdefault(text,len(self.records)-1)
        self.nindex.setdefault(norm(text),len(self.records)-1)

    def build(self):
        self.starts=[]; self.nstarts=[]; chunks=[]; nchunks=[]; pos=npos=0
        for r in self.records:
            self.starts.append(pos); self.nstarts.append(npos)
            chunks.append(r['text']); nchunks.append(norm(r['text']))
            pos+=len(chunks[-1])+1; npos+=len(nchunks[-1])+1
        self.all='\x00'.join(chunks); self.nall='\x00'.join(nchunks)

    def result(self, i, kind, query):
        r=self.records[i]
        out={k:v for k,v in r.items() if k!='text'}
        out['match']=kind
        exact_pos=r['text'].find(query)
        if exact_pos>=0:
            out['match_in_record_offset_chars']=exact_pos
            if r.get('kind')=='raw_source_file':
                out['line']=r['text'].count('\n',0,exact_pos)+1
        else:
            out['match_in_normalized_record_offset_chars']=norm(r['text']).find(norm(query))
        if len(r['text'])<=700:
            out['source_excerpt']=r['text']
        else:
            j=r['text'].find(query)
            out['source_excerpt']=r['text'][max(0,j-90):max(0,j-90)+500] if j>=0 else None
        return out

    def lookup(self, text):
        if not isinstance(text,str) or not text.strip():
            return None
        if text in self.index:
            return self.result(self.index[text], 'exact_value',text)
        pos=self.all.find(text)
        if pos>=0:
            return self.result(bisect.bisect_right(self.starts,pos)-1,'exact_substring',text)
        n=norm(text)
        if n in self.nindex:
            return self.result(self.nindex[n],'normalized_value',text)
        pos=self.nall.find(n)
        if pos>=0:
            return self.result(bisect.bisect_right(self.nstarts,pos)-1,'normalized_substring',text)
        return None


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_sources():
    c=Corpus(); candidates=[]; inputs=[]
    manifest=json.loads((AUDIT/'manifest.json').read_text())
    urls={m.get('local_path'):m.get('url') for m in manifest if m.get('status')==200}
    astpath=AUDIT/'trich_xuat_js_ast.json'
    inputs.append({'file':rel(astpath),'sha256':sha(astpath)})
    astdata=json.loads(astpath.read_text())
    for unit in astdata:
        source='kiem_tra_2026-10-12/ban_chup_goc/_next/'+unit['file']
        is_app_content='/chunks/app/' in unit['file'] or Path(unit['file']).name.startswith(('369-','648.','761.','840-'))
        for i,item in enumerate(unit.get('strings',[])):
            v=item.get('value')
            meta={'file':source,'url':urls.get(source),'kind':'javascript_literal','ast_file':rel(astpath),'ast_pointer':f'{unit["file"]}/strings/{i}', 'line':item.get('line'),'column_zero_based':item.get('column'), 'start':item.get('start')}
            c.add(v,**meta)
            if is_app_content and isinstance(v,str) and 8<=len(v)<=4000 and re.search('[À-ỹđĐ]',v) and not v.lstrip().startswith(('[','{')) and '\n' not in v and 'return' not in v:
                candidates.append((v,meta))
        for field in ('json_parse','static_data','templates'):
            for i,item in enumerate(unit.get(field,[])):
                for lp,v in leaves(item.get('value',item.get('cooked',''))):
                    if isinstance(v,str):
                        meta={'file':source,'url':urls.get(source),'kind':'javascript_decoded_data','ast_file':rel(astpath),'ast_pointer':f'{unit["file"]}/{field}/{i}/value{lp[1:]}','start':item.get('start')}
                        c.add(v,**meta)
                        if is_app_content and 8<=len(v)<=4000 and re.search('[À-ỹđĐ]',v) and '\n' not in v:
                            candidates.append((v,meta))
    for p in sorted((AUDIT/'trich_xuat_html').glob('*.json')):
        inputs.append({'file':rel(p),'sha256':sha(p)})
        x=json.loads(p.read_text())
        for lp,v in leaves(x):
            if isinstance(v,str):
                meta={'file':rel(p),'url':x.get('url'),'kind':'html_extraction','json_path':lp}
                c.add(v,**meta)
                if lp.startswith('$["text_nodes"]') and len(v.strip())>=2:
                    candidates.append((v,meta))
        c.add(' '.join(x.get('text_nodes',[])),file=rel(p),url=x.get('url'),kind='html_joined_text_nodes')
    browser_count=0
    for p in sorted((AUDIT/'trinh_duyet').glob('*.json')):
        x=json.loads(p.read_text()); browser_count+=1
        inputs.append({'file':rel(p),'sha256':sha(p)})
        for lp,v in leaves(x):
            if isinstance(v,str):
                c.add(v,file=rel(p),url=x.get('url'),kind='browser_capture',json_path=lp)
        for i,line in enumerate(x.get('text','').splitlines(),1):
            if len(line.strip())>=2:
                candidates.append((line,{'file':rel(p),'url':x.get('url'),'kind':'browser_text_line','text_line':i}))
    glb=None
    raw_count=0
    for p in sorted(RAW.rglob('*')):
        if not p.is_file(): continue
        source=rel(p)
        if p.suffix in ('.js','.css','.html','.svg') or '.html.' in p.name or p.name=='news':
            t=p.read_text(errors='replace');raw_count+=1
            c.add(t,file=source,url=urls.get(source),kind='raw_source_file')
            inputs.append({'file':source,'sha256':sha(p)})
            if p.name=='news':
                for lp,v in leaves(json.loads(t)):
                    c.add(v,file=source,url=urls.get(source),kind='api_json',json_path=lp)
        if p.suffix=='.glb':
            b=p.read_bytes(); size,typ=struct.unpack_from('<II',b,12)
            glb=json.loads(b[20:20+size])
            inputs.append({'file':source,'sha256':sha(p)})
            for lp,v in leaves(glb):
                c.add(v,file=source,url=urls.get(source),kind='glb_json_chunk',json_path=lp)
            c.add(p.name,file=source,url=urls.get(source),kind='asset_filename')
    c.build()
    return c,candidates,inputs,glb,{'ast_files':len(astdata),'browser_json_files':browser_count,'raw_text_files':raw_count,'text_records':len(c.records)}


def writer_info(p, scripts):
    out=[]
    for sp,text in scripts.items():
        if p.name in text:
            linenos=[i for i,l in enumerate(text.splitlines(),1) if p.name in l]
            out.append({'file':rel(sp),'reference_lines':linenos})
    return out


def generator_hits(value,writers,scripts):
    if not isinstance(value,str) or len(value)<8:return []
    out=[]
    for w in writers:
        p=ROOT/w['file']; t=scripts[p]
        for i,line in enumerate(t.splitlines(),1):
            if value in line or norm(value) in norm(line):
                out.append({'file':rel(p),'line':i,'kind':'authored_literal_or_template'})
                break
    return out[:4]


def contextual_glb(lp,value,g):
    if not g:return None
    gp=None; expected=None
    m=re.match(r'\$\["mo_hinh_gltf"\]\["cay_nut_node_hierarchy"\]\[(\d+)\]\["(nut|mesh_id|con)"\](?:\[(\d+)\])?$',lp)
    if m:
        i,key,sub=m.groups(); i=int(i); k={'nut':'name','mesh_id':'mesh','con':'children'}[key]
        expected=g['nodes'][i].get(k);gp=f'$["nodes"][{i}]["{k}"]'
        if sub is not None: expected=expected[int(sub)];gp+=f'[{sub}]'
    m=re.match(r'\$\["mo_hinh_gltf"\]\["bang_vat_lieu_pbr"\]\[(\d+)\]\["(ten|base_color_factor|metallic_factor|roughness_factor)"\](?:\[(\d+)\])?$',lp)
    if m:
        i,key,sub=m.groups();i=int(i)
        if key=='ten':expected=g['materials'][i]['name'];gp=f'$["materials"][{i}]["name"]'
        else:
            k={'base_color_factor':'baseColorFactor','metallic_factor':'metallicFactor','roughness_factor':'roughnessFactor'}[key]
            expected=g['materials'][i]['pbrMetallicRoughness'][k];gp=f'$["materials"][{i}]["pbrMetallicRoughness"]["{k}"]'
            if sub is not None:expected=expected[int(sub)];gp+=f'[{sub}]'
    if lp=='$["mo_hinh_gltf"]["dung_luong_bytes"]':
        expected=(RAW/'models/vercel-lacquer-box.glb').stat().st_size;gp='file_size_bytes'
    if gp:
        if value==expected:status='contextual_source_equal'
        elif isinstance(value,(int,float)) and isinstance(expected,(int,float)) and abs(value-expected)<0.00011:status='contextual_numeric_approximation'
        else:status='contextual_source_differs'
        return {'file':rel(RAW/'models/vercel-lacquer-box.glb'),'json_path':gp,'value':expected,'assessment':status}
    return None


def strip_md(line):
    s=re.sub(r'^\s*(?:>\s*)?(?:[-+*]\s+|\d+\.\s+)?','',line.strip())
    s=re.sub(r'^#{1,6}\s+','',s)
    s=re.sub(r'!?\[([^]]*)\]\(([^)]*)\)',r'\1 \2',s)
    return s.replace('**','').replace('`','').strip('* ').strip()


def main():
    c,candidates,inputs,glb,source_counts=load_sources()
    retrieved_resources={}
    for i,item in enumerate(json.loads((AUDIT/'manifest.json').read_text())):
        if item.get('status')==200 and item.get('local_path'):
            resource={'assessment':'resource_retrieved_not_page_association','manifest_file':rel(AUDIT/'manifest.json'),'manifest_index':i,'url':item['url'],'file':item['local_path'],'status':200,'sha256':item.get('sha256'),'caution':'Successful retrieval proves the resource exists, not that a particular old document attached it to the correct paragraph or UI state.'}
            retrieved_resources[item['url']]=resource
            retrieved_resources.setdefault(unquote(urlsplit(item['url']).path),resource)
    scripts={p:p.read_text(errors='replace') for p in sorted((ROOT/'scripts').glob('*')) if p.suffix in ('.py','.js') and p.name!=Path(__file__).name}
    files=[]; json_by_stem={}; total=collections.Counter()
    for p in sorted(OLD.glob('*.json')):
        writers=writer_info(p,scripts)
        entries=[]; counts=collections.Counter()
        for lp,v in leaves(json.loads(p.read_text())):
            hit=c.lookup(v) if isinstance(v,str) else None
            context=contextual_glb(lp,v,glb) if p.name.startswith('11_') else None
            if not context and isinstance(v,str) and not hit:
                context=retrieved_resources.get(v)
            if hit:status='exact' if hit['match'].startswith('exact') else 'normalized'
            elif isinstance(v,str):status='no_text_match'
            else:status='non_text_scalar'
            entry={'json_path':lp,'value':v,'textual_status':status,'source_provenance':hit,'contextual_evidence':context}
            if hit and len(norm(v))<8:
                entry['caution']='Short string: match only proves token occurrence, not factual or contextual correctness.'
            if status=='no_text_match':
                entry['unsourced_leaf_flag']=True
                entry['meaning']='No full textual match in this source snapshot. May be paraphrase, editorial title, derived fact, changed live content, or unsupported addition; not automatically false.'
                entry['generation_provenance']=generator_hits(v,writers,scripts)
                if p.name.startswith('api_') and 'rss-news-' in v:
                    entry['caution']='Transient RSS id: compare article URL/title/date instead; snapshot identifiers can change.'
            if context:counts[context['assessment']]+=1
            counts[status]+=1;counts['leaf_total']+=1
            entries.append(entry)
        counts['string_total']=counts['exact']+counts['normalized']+counts['no_text_match']
        counts['matched_string_percent']=round(100*(counts['exact']+counts['normalized'])/counts['string_total'],2) if counts['string_total'] else None
        row={'file':rel(p),'sha256':sha(p),'type':'json','generator_references':writers,'counts':dict(counts),'leaves':entries}
        json_by_stem[p.stem]=row;files.append(row)
        total.update({k:v for k,v in counts.items() if k!='matched_string_percent'})
    for p in sorted(OLD.glob('*.md')):
        entries=[];counts=collections.Counter(); in_code=False
        sibling=json_by_stem.get(p.stem,{}); sibling_leaves=sibling.get('leaves',[])
        for line_number,line in enumerate(p.read_text().splitlines(),1):
            if not line.strip():continue
            if line.lstrip().startswith('```'):
                in_code=not in_code;continue
            if re.fullmatch(r'[\s|:\-]+',line):continue
            clean=strip_md(line)
            opts=[clean]
            if ':' in clean and len(clean.split(':',1)[0])<75:opts.append(clean.split(':',1)[1].strip())
            hit=None
            for v in opts:
                if len(v)>=3:
                    hit=c.lookup(v)
                    if hit:break
            inherited=[]
            for leaf in sibling_leaves:
                v=leaf['value']
                if isinstance(v,str) and len(v)>=8 and norm(v) in norm(clean):
                    inherited.append({'json_path':leaf['json_path'],'textual_status':leaf['textual_status'],'source_provenance':leaf.get('source_provenance'),'contextual_evidence':leaf.get('contextual_evidence')})
            if hit:status='direct_text_match'
            elif line.lstrip().startswith('#'):status='editorial_heading'
            elif inherited:status='contains_sibling_json_content'
            elif in_code:status='code_or_diagram_needs_contextual_review'
            else:status='no_full_text_match_needs_review'
            entries.append({'line':line_number,'text':line,'assessment':status,'source_provenance':hit,'sibling_json_references':inherited,'unsourced_line_flag':status in ('no_full_text_match_needs_review','code_or_diagram_needs_contextual_review')})
            counts[status]+=1;counts['nonblank_content_lines']+=1
        files.append({'file':rel(p),'sha256':sha(p),'type':'markdown','generator_references':writer_info(p,scripts),'assessment':'Presentation/edited document, not a verbatim page archive. See each line and its sibling JSON provenance; sibling membership alone does not prove web provenance.','counts':dict(counts),'lines':entries})

    # Reverse direction: source UI strings not reproduced verbatim by any old file.
    old_corpus=Corpus()
    for p in sorted(OLD.glob('*')):
        if p.suffix=='.json':
            for lp,v in leaves(json.loads(p.read_text())):old_corpus.add(v,file=rel(p),json_path=lp)
        elif p.suffix=='.md':old_corpus.add(strip_md(p.read_text()),file=rel(p))
    old_corpus.build(); unique={}
    for v,meta in candidates:
        n=norm(v)
        if not n or not re.search(r'[a-zà-ỹđ]',n) or len(n)<2:continue
        if n not in unique:unique[n]={'value':v,'source_provenance':meta,'additional_occurrences':0}
        else:unique[n]['additional_occurrences']+=1
    missing=[entry for entry in unique.values() if not old_corpus.lookup(entry['value'])]
    groups=collections.Counter(e['source_provenance']['file'] for e in missing)
    findings=manual_findings(c,glb)
    api_old=json.loads((OLD/'api_tin_tuc_bao_chi.json').read_text())
    api_new=json.loads((RAW/'api/news').read_text())
    old_by_url={r.get('url'):r for r in api_old};new_by_url={r.get('url'):r for r in api_new}
    api_compare={'old_count':len(api_old),'new_count':len(api_new),'matching_article_urls':len(set(old_by_url)&set(new_by_url)), 'old_only_urls':sorted(set(old_by_url)-set(new_by_url)), 'new_only_urls':sorted(set(new_by_url)-set(old_by_url)), 'field_changes_same_article':[]}
    for url in sorted(set(old_by_url)&set(new_by_url)):
        changes={k:{'old':old_by_url[url].get(k),'current':new_by_url[url].get(k)} for k in set(old_by_url[url])|set(new_by_url[url]) if old_by_url[url].get(k)!=new_by_url[url].get(k)}
        if changes:api_compare['field_changes_same_article'].append({'url':url,'changes':changes})
    report={
        'created_at':datetime.now(ZoneInfo('Asia/Ho_Chi_Minh')).isoformat(),
        'scope':'All 29 files in du_lieu_noi_dung; comparison against saved public source snapshots. Original files left untouched.',
        'normalization':'HTML entity decode, Unicode NFKC, casefold, whitespace collapse; curly quotes and en/em dashes standardized. No accent removal, stemming, semantic rewriting or translation.',
        'interpretation':['Exact/normalized coverage is old-document string provenance, not percentage of website crawled.', 'Full-string absence does not imply a false statement. Added titles, paraphrases, derived technical facts and transient API ids require separate assessment.', 'Numeric and boolean scalar coincidences in unrelated source text are not counted as matches. GLB numeric fields receive contextual mapping.', 'Source omissions are candidate UI/literary strings from HTML nodes, browser text lines and Vietnamese JavaScript literals. They prove incomplete verbatim reproduction; they are not a measure of every possible interactive state.', 'A matching short label or substring establishes occurrence only; source context must support any factual interpretation.'],
        'summary':{'old_files':len(files),'old_json_files':len(json_by_stem),'old_markdown_files':len(files)-len(json_by_stem), 'json_leaf_counts':dict(total),'source_counts':source_counts,'unique_source_candidate_strings':len(unique),'source_candidate_strings_missing_from_all_old_files':len(missing),'missing_by_first_source_file':dict(groups)},
        'manual_findings':findings,'api_snapshot_comparison':api_compare,'files':files,
        'source_candidate_strings_missing_from_old_files':missing,
        'input_source_checksums':inputs,
        'generator_script_checksums':[{'file':rel(p),'sha256':sha(p)} for p in scripts if any(p.name==Path(w['file']).name for f in files for w in f['generator_references'])]
    }
    (AUDIT/'doi_chieu_noi_dung_cu.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    write_markdown(report)
    print(json.dumps(report['summary'],ensure_ascii=False,indent=2))


def manual_findings(c,glb):
    findings=[]
    def add(id,files,assessment,detail,queries=()):
        findings.append({'id':id,'files':files,'assessment':assessment,'detail':detail,'evidence_searches':[{'query':q,'source_hit':c.lookup(q)} for q in queries]})
    add('F01',['00–07 JSON/MD'],'edited_summaries_not_verbatim_archive','Các chương cũ được dựng bằng script tạo tài liệu, thường là dict và văn bản gán cứng. 03 lấy nguyên văn mảng bài viết qua JSON.parse rồi ghép các mốc thời gian viết riêng. Vì vậy có cả bản chép nguồn, tóm tắt/đặt tên lại và nội dung bổ sung. Không được gọi toàn bộ 29 file là nội dung nguyên văn đã cào.')
    add('F02',['02_kham_pha.json','02_kham_pha.md'],'unverified_embellishment','Các đoạn chi tiết kỹ thuật có thêm vật liệu/công thức như độ ẩm 70–85%, phù sa/bột đá, vải màn, mài bằng lá chuối khô, trong khi nguồn giao diện nhấn mạnh năm chặng chỉ để giải thích và không phải công thức chế tác. Cần giữ bản nguyên văn riêng, không dùng bản diễn giải cũ làm bằng chứng web.',('Năm chặng để dễ hình dung, không phải công thức cứng','70-85%','lá chuối khô'))
    add('F03',['03_cau_chuyen_son_mai.json','03_cau_chuyen_son_mai.md'],'mixed_provenance','scripts/gen_03.js:3–15 đọc/giải mã mảng bài viết trong JS; dòng 16–60 tự gán các mốc/tóm tắt. Những mốc này không mặc nhiên là câu chữ của tác giả website. Báo cáo từng leaf cho biết câu nào trùng nguồn.')
    add('F04',['08_giai_ma_ky_thuat_chuyen_sau.json','08_giai_ma_ky_thuat_chuyen_sau.md'],'technical_interpretation_partial_support','Script build_extreme_deep_dive.py tạo 08 từ dữ liệu gán cứng, sau đó generate_ultimate_deep_dive.py bổ sung mô tả WebGL. Có dấu vết triển khai thực về hai Canvas 900×620, shader, localStorage, GLB. Bundle còn ghi version Next.js 14.2.35 và React 18.3.0-canary-178c267a4e-20241218, chi tiết hơn nhãn 14+/18 của tài liệu. Các nhãn thuật toán, ý nghĩa vật lý, runtime Edge và cách kể kiến trúc là diễn giải; browser bundle không tự chứng minh môi trường chạy server.',('ssms-applied-faces-v1','localStorage','width=900','height=620','bezierCurveTo(-53,-38,-47,-110,0,-164)','vercel-lacquer-box.glb','AudioContext','14.2.35','18.3.0-canary-178c267a4e-20241218'))
    add('F05',['09_he_thong_thiet_ke_design_system.json','09_he_thong_thiet_ke_design_system.md'],'css_tokens_supported_interpretation_separate','Tên CSS token có thật nhưng bảng màu cũ chưa mô tả cascade/override. Trong 58e70d5489b56972.css, --color-vermilion ban đầu #8c0e0e rồi đổi sang var(--red); --red tiếp tục có các giá trị #8c0e0e, #8b2a2a, #8b2922. --color-eggshell-white cũng đổi từ #ebeae9 sang var(--cream). Noto Serif và Inter có khai báo font; chuỗi tên Playfair Display không xuất hiện trong CSS/JS/HTML được xét. Một file font tồn tại riêng không chứng minh nó đang được dùng. Ý nghĩa văn hóa, nhận định thẩm mỹ và lời khẳng định “tái hiện chính xác” là diễn giải tác giả tài liệu.',('--color-black-lacquer','--color-vermilion','--color-gold','--color-eggshell-white','--color-mother-of-pearl','--color-lacquer-brown','--color-surface-card','Playfair Display','Noto Serif','Inter','feTurbulence'))
    css_path=RAW/'_next/static/css/58e70d5489b56972.css'
    css_text=css_path.read_text()
    findings[-1]['css_declarations_in_source_order']=[{'property':m.group(1),'value':m.group(2),'offset':m.start(),'file':rel(css_path)} for m in re.finditer(r'(--(?:color-(?:black-lacquer|vermilion|gold|eggshell-white|mother-of-pearl|lacquer-brown|surface-card)|red|gold|cream))\s*:\s*([^;}]+)',css_text)]
    add('F06',['10_nghien_cuu_van_hoa_va_khe_uoc_nghe_thuat.json','10_nghien_cuu_van_hoa_va_khe_uoc_nghe_thuat.md'],'research_additions_not_established_as_site_content','Tên khoa học cây sơn, enzyme, độ ẩm/nhiệt độ, niên đại và quy mô tranh xuất hiện trong script tạo chuyên luận. Báo cáo tìm chứng cứ trong toàn bộ nguồn công khai đã lưu; không xác minh độc lập tính đúng sai học thuật. Nhãn “trích xuất từ dự án” không đủ chứng minh từng phát biểu.',('Toxicodendron','Rhus succedanea','laccase','75–85%','25–30','104cm','Joseph Inguimberty'))
    add('F07',['11_giai_ma_mo_hinh_3d_va_shader_webgl.json','11_giai_ma_mo_hinh_3d_va_shader_webgl.md'],'binary_and_shader_evidence_supported_in_part','GLB tải về thực sự dài 449344 byte, glTF 2.0, 12 nodes, 10 meshes, 4 materials. Các tên node, children, mesh index, metallicFactor và roughnessFactor có thể đối chiếu ngữ cảnh trực tiếp. baseColorFactor trong tài liệu đã rút gọn số thập phân, không bảo toàn nguyên giá trị. Bộ lọc âm thanh có hệ số .99886, .0555179, .0750759, .153852 trong mã minify; bản cũ rút gọn hệ số .0555/.075/.153. Không tìm thấy dạng có số 0 trước dấu chấm không có nghĩa thuật toán vắng mặt. Ý nghĩa văn hóa/kích thước “chuẩn mực”, tên “Sobel”, “Paul Kellet” cần tách khỏi bằng chứng mã.',('rawDepth = texture2D(uMaskMap, vUv).r','revealThreshold','.99886*n+.0555179*t','.99332*i+.0750759*t','.969*l+.153852*t','Math.min(2200,Math.max(700,1e3+1200*e))','Paul Kellet','Sobel'))
    findings[-1]['glb_verified']={'file':rel(RAW/'models/vercel-lacquer-box.glb'),'bytes':(RAW/'models/vercel-lacquer-box.glb').stat().st_size,'asset':glb.get('asset'),'nodes':len(glb.get('nodes',[])),'meshes':len(glb.get('meshes',[])),'materials':len(glb.get('materials',[]))}
    add('F08',['12_kien_truc_ma_nguon_va_reverse_engineering.json','12_kien_truc_ma_nguon_va_reverse_engineering.md'],'reconstructed_not_recovered_source','Tên component và đường dẫn .tsx trong phần “reconstructed” là bản tái dựng đặt tên; không phải bằng chứng đã tải được mã nguồn TSX. Tên hash webpack và số lượng bundle chỉ đúng với snapshot cụ thể. Không nên coi mô tả 28 JS/9 CSS là định mức để chứng minh website đã cào đủ.',('HeaderNavigation','HeroCover','EightStepJourneyStateMachine','app/layout.tsx','_w6excJGTCRbJVHnNuGcc','dpl_6jQJ65uT65LPuzwTmJiqFs1xmLmA','webpack-f57e898f0a30f96c.js'))
    add('F09',['13_dai_bach_khoa_toan_thu_son_mai.json','13_dai_bach_khoa_toan_thu_son_mai.md'],'unsourced_encyclopedic_additions','Các công thức phân tử, tỉ lệ 65–70%, 20–25%, 5–7%, 2–3%, thời gian 40–60 giờ, 3–5 ngày và diễn giải phản ứng hóa học được gán cứng trong generate_ultimate_deep_dive.py. Không tìm thấy cả chuỗi hoặc thuật ngữ đặc thù tương ứng là dấu hiệu chưa có chứng cứ web trong snapshot, không phải kết luận khoa học sai.',('C23H36O2','C21H32O2','laccol','ortho-quinone','40-60','3-5 ngày','Polyphenol oxidase'))
    add('F10',['api_tin_tuc_bao_chi.json','04_tin_tuc_su_kien.json','04_tin_tuc_su_kien.md'],'live_api_snapshot_identity','API tin tức thay đổi id theo lần/snapshot dù URL bài, tiêu đề hoặc ngày có thể không đổi. Trong hai snapshot đang xét, cả 12 URL bài và các trường ngoài id trùng nhau. Phần api_snapshot_comparison đối chiếu theo URL, tránh gắn cờ id mới thành bài báo thiếu hoặc dữ liệu bịa.')
    return findings


def write_markdown(r):
    s=r['summary'];counts=s['json_leaf_counts']; lines=[
        '# Đối chiếu 29 tài liệu nội dung cũ với nguồn website đã lưu',
        '',f'Kiểm tra lúc: {r["created_at"]}. Các file gốc được giữ nguyên.',
        '', '**Kết luận: 29 file cũ không phải bản lưu nguyên văn đầy đủ của website.** Có nội dung chép đúng nguồn, nội dung tóm tắt/đặt tên lại và nội dung nghiên cứu hoặc phân tích được bổ sung. Đặc biệt 08–13 cần phân biệt dữ kiện có chứng cứ trong CSS/JS/GLB với lời diễn giải của tài liệu.',
        '', f'- Phạm vi: {s["old_json_files"]} JSON và {s["old_markdown_files"]} Markdown.',
        f'- Tổng {counts["leaf_total"]} JSON leaf; {counts["string_total"]} là chuỗi. Khớp nguyên văn: {counts["exact"]}; chỉ khớp sau chuẩn hóa: {counts["normalized"]}; chưa có toàn chuỗi trong nguồn: {counts["no_text_match"]}.',
        f'- {s["source_candidate_strings_missing_from_all_old_files"]}/{s["unique_source_candidate_strings"]} chuỗi ứng viên lấy từ giao diện/JS không được giữ nguyên văn trong bất kỳ file cũ nào. Danh sách đầy đủ kèm vị trí nguồn nằm trong JSON báo cáo.',
        '', 'Các số trên đo khả năng truy nguồn của tài liệu cũ; **không phải phần trăm website đã cào**. Không khớp chữ không đồng nghĩa sai: có thể do tóm tắt, tiêu đề biên tập, tính toán, thay đổi dữ liệu trực tiếp hoặc phát biểu chưa có nguồn. Chuỗi ngắn trùng nhau cũng không xác nhận một phát biểu đúng ngữ cảnh.',
        '', '## Kiểm tra từng file JSON', '',
        '| File | Leaf | Chuỗi | Nguyên văn | Chuẩn hóa | Chưa có toàn chuỗi | % chuỗi khớp |',
        '| --- | ---: | ---: | ---: | ---: | ---: | ---: |']
    for f in r['files']:
        if f['type']!='json':continue
        q=f['counts'];lines.append(f'| {Path(f["file"]).name} | {q["leaf_total"]} | {q["string_total"]} | {q.get("exact",0)} | {q.get("normalized",0)} | {q.get("no_text_match",0)} | {q["matched_string_percent"]}% |')
    lines+=['','Các số/boolean không được xác nhận bằng cách tìm một con số bất kỳ trong bundle. Riêng chương 11 có đối chiếu GLB theo đúng node/material; chi tiết và các phép rút gọn thập phân nằm tại `contextual_evidence` của từng leaf.', '', '## Nguồn gốc và phát hiện cần lưu ý','']
    for f in r['manual_findings']:
        lines+=[f'### {f["id"]} — {", ".join(f["files"])}','',f['detail'],'']
        if f['evidence_searches']:
            lines+=['| Từ khóa kiểm tra | Kết quả trong snapshot |','| --- | --- |']
            for q in f['evidence_searches']:
                h=q['source_hit']; answer=f'Có: `{h["file"]}`' if h else 'Chưa tìm thấy chuỗi này'
                lines.append(f'| `{q["query"]}` | {answer} |')
            lines.append('')
    lines+=['## Kiểm tra từng file Markdown','','Mỗi dòng có chữ được đánh giá trong JSON. “Có nội dung JSON” chỉ chỉ ra quan hệ giữa hai tài liệu, không tự xác nhận nguồn web. Dòng tiêu đề/bố cục được phân loại riêng. Các dòng mã/sơ đồ cần đọc đúng ngữ cảnh; không gắn nhãn sai chỉ vì khác tên biến hoặc định dạng.', '', '| File | Dòng nội dung | Khớp nguồn trực tiếp | Có nội dung JSON cùng chương | Tiêu đề | Cần đối chiếu thêm |','| --- | ---: | ---: | ---: | ---: | ---: |']
    for f in r['files']:
        if f['type']!='markdown':continue
        q=f['counts']; lines.append(f'| {Path(f["file"]).name} | {q.get("nonblank_content_lines",0)} | {q.get("direct_text_match",0)} | {q.get("contains_sibling_json_content",0)} | {q.get("editorial_heading",0)} | {q.get("no_full_text_match_needs_review",0)+q.get("code_or_diagram_needs_contextual_review",0)} |')
    a=r['api_snapshot_comparison'];lines+=['','## API tin tức','',f'Bản cũ: {a["old_count"]} mục; snapshot mới: {a["new_count"]} mục; cùng URL bài: {a["matching_article_urls"]}. URL chỉ có ở bản cũ: {len(a["old_only_urls"])}; URL chỉ có ở bản mới: {len(a["new_only_urls"])}. Xem thay đổi từng trường trong JSON để phân biệt id thay đổi với bài báo thay đổi.', '', '## Ví dụ nguyên văn nguồn chưa có trong tài liệu cũ', '', 'Đây là mẫu từ danh sách đối chiếu ngược, không phải toàn bộ các phần thiếu. Tất cả chuỗi tìm thấy được lưu trong trường `source_candidate_strings_missing_from_old_files` của JSON.','']
    selected=[];seen=collections.Counter()
    for e in r['source_candidate_strings_missing_from_old_files']:
        src=e['source_provenance']['file']
        if 45<=len(e['value'])<=650 and seen[src]<3:
            selected.append(e);seen[src]+=1
        if len(selected)>=36:break
    for e in selected:
        v=e['value'].replace('\n',' ')
        lines+=[f'- **Nguồn:** `{e["source_provenance"]["file"]}` — {v}']
    lines+=['','## Cách tái kiểm tra','','Chạy `python3 scripts/audit_old_content.py` tại thư mục dự án. Script chỉ đọc các file cũ và nguồn đã lưu; chỉ ghi hai file báo cáo của lần kiểm tra. Không gọi mạng, không sửa tài liệu gốc. SHA-256 của đầu vào được lưu để biết báo cáo ứng với snapshot nào.', '', 'Chuẩn hóa gồm HTML entity, Unicode NFKC, chữ hoa/thường, khoảng trắng và dấu ngoặc kép/gạch ngang kiểu chữ. Không bỏ dấu tiếng Việt, không đổi nghĩa câu. Phần xác minh kỹ thuật GLB là riêng biệt với phép đối chiếu chuỗi.','']
    (AUDIT/'doi_chieu_noi_dung_cu.md').write_text('\n'.join(lines))


if __name__=='__main__':
    main()
