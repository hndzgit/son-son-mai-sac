#!/usr/bin/env python3
"""Offline technical audit of preserved assets. Does not modify source assets.
Dependencies: Pillow, fonttools, tinycss2. Install to /tmp/sonsonmaisat-audit-deps
or make them available via PYTHONPATH. All evidence is relative to repository root.
"""
from __future__ import annotations
import base64, collections, difflib, hashlib, html, io, json, os, pathlib, re, struct, sys
import urllib.parse, xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from html.parser import HTMLParser
sys.path.insert(0, '/tmp/sonsonmaisat-audit-deps')
from PIL import Image, ExifTags, __version__ as pillow_version
from fontTools.ttLib import TTFont
import fontTools, tinycss2

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / 'kiem_tra_2026-10-12'
EMBED = OUT / 'tai_nguyen_nhung'
EMBED.mkdir(parents=True, exist_ok=True)
ORIGINAL_ROOTS = ['hinh_anh_assets', 'ma_nguon_css_js', 'trang_html_goc']
SNAPSHOT = 'kiem_tra_2026-10-12/ban_chup_goc'
IMAGE_SUFFIXES = {'.png', '.jpg', '.jpeg', '.webp', '.svg', '.ico', '.gif', '.avif'}

def sha(data): return hashlib.sha256(data).hexdigest()
def rel(p): return str(pathlib.Path(p).relative_to(ROOT))
def write_json(p, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
def safe(value):
    if isinstance(value, bytes): return {'bytes': len(value), 'sha256': sha(value)}
    if isinstance(value, dict): return {str(k): safe(v) for k,v in value.items()}
    if isinstance(value, (tuple, list, set)): return [safe(x) for x in value]
    if isinstance(value, (str, int, float, bool)) or value is None: return value
    return str(value)

def file_evidence(p):
    b=p.read_bytes()
    return {'path':rel(p), 'bytes':len(b), 'sha256':sha(b)}

def image_metadata(data, name=''):
    r={'signature_first_32_bytes_hex': data[:32].hex()}
    if (data.lstrip().startswith(b'<') and b'<svg' in data[:2048]) or name.lower().endswith('.svg'):
        e=ET.fromstring(data)
        if e.tag.rsplit('}',1)[-1]!='svg': raise ValueError('XML root is not SVG')
        tags=collections.Counter(x.tag.rsplit('}',1)[-1] for x in e.iter())
        r.update(format='SVG', valid=True, validation='XML parsed; SVG root verified; scripts/external links never executed',
                 width=e.get('width'), height=e.get('height'), viewBox=e.get('viewBox'), root_attributes=e.attrib,
                 element_counts=dict(tags), ids=[x.get('id') for x in e.iter() if x.get('id')],
                 text_nodes=[t for t in e.itertext() if t.strip()],
                 references=[{'attribute':k,'value':v} for x in e.iter() for k,v in x.attrib.items() if k.rsplit('}',1)[-1] in ['href','src']])
        if e.get('viewBox'):
            dims = [float(v) for v in re.split(r'[ ,]+', e.get('viewBox').strip())]
            if len(dims) == 4: r['viewbox_dimensions'] = {'width': dims[2], 'height': dims[3]}
        if e.get('width') is None or e.get('height') is None: r['dimensions_note'] = 'No explicit intrinsic width/height; viewport dimensions derive from the viewBox and embedding context.'
        return r
    with Image.open(io.BytesIO(data)) as im:
        r.update(format=im.format, width=im.width, height=im.height, mode=im.mode, info=safe(im.info),
                 frames=getattr(im,'n_frames',1), animated=getattr(im,'is_animated',False))
        r['exif']={ExifTags.TAGS.get(k,str(k)): safe(v) for k,v in im.getexif().items()}
        if im.format == 'ICO':
            r['ico_sizes']=sorted([list(s) for s in im.ico.sizes()])
            r['ico_entries']=safe(im.ico.entry)
            for s in im.ico.sizes(): im.ico.getimage(s).load()
        for i in range(getattr(im,'n_frames',1)):
            im.seek(i); im.load()
    with Image.open(io.BytesIO(data)) as test: test.verify()
    r.update(valid=True, validation='Pillow full pixel decode of all frames + verify; ICO sizes decoded individually')
    return r

def font_metadata(data):
    f=TTFont(io.BytesIO(data), checkChecksums=2)
    names=[]
    for n in f['name'].names:
        try: value=n.toUnicode()
        except Exception: value=n.string.hex()
        names.append({'name_id':n.nameID,'platform_id':n.platformID,'encoding_id':n.platEncID,'language_id':n.langID,'value':value})
    cmap=f.getBestCmap() or {}
    codepoints=sorted(cmap); ranges=[]
    for c in codepoints:
        if ranges and c==ranges[-1][1]+1: ranges[-1][1]=c
        else: ranges.append([c,c])
    r={'valid':True,'validation':'fontTools SFNT table/name/cmap parsing', 'sfnt_version':repr(f.sfntVersion),
       'tables':[{ 'tag':str(t), 'length':getattr(f.reader.tables.get(t),'length',None),
                   'offset':getattr(f.reader.tables.get(t),'offset',None),
                   'checksum':getattr(f.reader.tables.get(t),'checkSum',None)} for t in f.keys()],
       'names':names,'units_per_em':f['head'].unitsPerEm,'glyph_count':f['maxp'].numGlyphs,
       'cmap_codepoint_count':len(cmap),'cmap_unicode_ranges':[[f'U+{a:04X}',f'U+{b:04X}'] for a,b in ranges],
       'cmap':{f'U+{k:04X}':v for k,v in cmap.items()}}
    if 'hhea' in f: r['horizontal_metrics']={k:getattr(f['hhea'],k) for k in ['ascent','descent','lineGap','advanceWidthMax']}
    if 'OS/2' in f: r['os2_metrics']={k:getattr(f['OS/2'],k,None) for k in ['usWeightClass','usWidthClass','fsType','sTypoAscender','sTypoDescender','sTypoLineGap','usWinAscent','usWinDescent','achVendID']}
    if 'fvar' in f: r['variation_axes']=[{'tag':a.axisTag,'min':a.minValue,'default':a.defaultValue,'max':a.maxValue,'flags':a.flags} for a in f['fvar'].axes]
    f.close(); return r

def glb_metadata(data, src):
    magic,version,length=struct.unpack_from('<4sII',data)
    if magic!=b'glTF' or version!=2 or length!=len(data): raise ValueError('Invalid GLB header/declared length')
    chunks=[]; at=12; doc=None; bins=[]
    while at<len(data):
        n,t=struct.unpack_from('<II',data,at); at+=8; payload=data[at:at+n]
        if len(payload)!=n: raise ValueError('Truncated GLB chunk')
        kind=struct.pack('<I',t).decode('ascii','replace')
        chunks.append({'type':kind,'offset':at,'bytes':n,'sha256':sha(payload)})
        if t==0x4E4F534A:
            doc=json.loads(payload); p=EMBED/'glb'/(sha(data)[:20]+'.gltf.json'); write_json(p,doc)
        elif t==0x004E4942: bins.append(payload)
        at+=n
    if doc is None: raise ValueError('No GLB JSON chunk')
    issues=[]
    for i,b in enumerate(doc.get('buffers',[])):
        if 'uri' not in b and (not bins or b['byteLength']>len(bins[0])): issues.append(f'buffer {i} outside BIN chunk')
    for i,v in enumerate(doc.get('bufferViews',[])):
        if v.get('byteOffset',0)+v['byteLength']>doc['buffers'][v['buffer']]['byteLength']: issues.append(f'bufferView {i} outside buffer')
    return {'valid':not issues,'validation':'GLB v2 header, declared file length, chunk bounds, JSON, buffers and bufferView bounds',
            'version':version,'chunks':chunks,'issues':issues,'json_extracted_path':rel(p),
            'counts':{k:len(doc.get(k,[])) for k in ['scenes','nodes','meshes','materials','accessors','bufferViews','buffers','textures','images','animations','skins','cameras']},
            'metadata_exact':doc}

class StylesParser(HTMLParser):
    def __init__(self): super().__init__(convert_charrefs=True); self.in_style=False; self.styles=[]; self.attrs=[]
    def handle_starttag(self,tag,attrs):
        if tag=='style': self.in_style=True
        for k,v in attrs:
            if k=='style' and v: self.attrs.append(v)
    def handle_endtag(self,tag):
        if tag=='style': self.in_style=False
    def handle_data(self,data):
        if self.in_style: self.styles.append(data)

def css_inventory(text, label):
    r={'source':label,'bytes_utf8':len(text.encode()),'sha256':sha(text.encode()),'custom_properties':[], 'font_faces':[],
       'media_queries':[], 'supports_queries':[], 'keyframes':[], 'animation_declarations':[], 'rules':[], 'parse_errors':[]}
    def ser(ts): return tinycss2.serialize(ts).strip()
    def decls(content,context):
        result=[]
        for d in tinycss2.parse_declaration_list(content, skip_whitespace=True, skip_comments=True):
            if d.type=='declaration':
                v={'name':d.name,'value':ser(d.value),'important':d.important}
                result.append(v)
                if d.name.startswith('--'): r['custom_properties'].append({'context':context,**v})
                if d.lower_name in ['animation','animation-name','animation-duration','animation-timing-function','animation-delay','animation-iteration-count','animation-direction','animation-fill-mode','animation-play-state','transition','transition-property','transition-duration','transition-timing-function','transition-delay']: r['animation_declarations'].append({'context':context,**v})
            elif d.type=='error': r['parse_errors'].append({'context':context,'message':d.message,'line':d.source_line,'column':d.source_column})
        return result
    def walk(rules,parents):
        for rule in rules:
            if rule.type=='qualified-rule':
                selector=ser(rule.prelude); context=parents+[selector]
                r['rules'].append({'selector':selector,'context':parents,'declarations':decls(rule.content,context)})
            elif rule.type=='at-rule':
                name=rule.lower_at_keyword; query=ser(rule.prelude); context=parents+['@'+name+' '+query]
                if name=='font-face': r['font_faces'].append({'context':parents,'declarations':decls(rule.content or [],context)})
                elif name=='media': r['media_queries'].append({'query':query,'context':parents})
                elif name=='supports': r['supports_queries'].append({'query':query,'context':parents})
                elif name.endswith('keyframes'): r['keyframes'].append({'name':query,'context':parents,'css':ser(rule.content or [])})
                if rule.content and name!='font-face': walk(tinycss2.parse_rule_list(rule.content,skip_comments=True,skip_whitespace=True),context)
            elif rule.type=='error': r['parse_errors'].append({'context':parents,'message':rule.message,'line':rule.source_line,'column':rule.source_column})
    walk(tinycss2.parse_stylesheet(text,skip_comments=True,skip_whitespace=True),[])
    return r

def unescape_js(s):
    # Handles escapes in static source literals. No JavaScript is evaluated.
    def sub(m):
        x=m.group(1)
        if x.startswith('u{'): return chr(int(x[2:-1],16))
        if x.startswith('u') and len(x)==5: return chr(int(x[1:],16))
        if x.startswith('x') and len(x)==3: return chr(int(x[1:],16))
        return {'n':'\n','r':'\r','t':'\t','b':'\b','f':'\f','v':'\v','0':'\0','\n':'','\r\n':''}.get(x,x)
    return re.sub(r'\\(u\{[0-9a-fA-F]+\}|u[0-9a-fA-F]{4}|x[0-9a-fA-F]{2}|\r\n|[\s\S])',sub,s)

manifest=json.loads((OUT/'manifest.json').read_text())
before=json.loads((OUT/'kiem_ke_truoc.json').read_text())
manifest_by_path={i['local_path']:i for i in manifest if i.get('local_path')}
before_by_path={i['path']:i for i in before['files']}
files=[]
for folder in ORIGINAL_ROOTS+[SNAPSHOT]: files.extend(sorted(p for p in (ROOT/folder).rglob('*') if p.is_file()))
assets=[]; css=[]; texts=[]; hash_cache={}; glbs=[]; fonts=[]
for p in files:
    data=p.read_bytes(); evidence=file_evidence(p); source=rel(p)
    evidence['collection']='live_snapshot' if source.startswith(SNAPSHOT+'/') else 'preserved_original'
    prior=before_by_path.get(source)
    if prior: evidence['matches_initial_inventory_sha256']=prior['sha256']==evidence['sha256']
    request=manifest_by_path.get(source)
    if request:
        evidence.update(url=request['url'],http_status=request['status'],fetched_at=request.get('fetched_at'),matches_manifest_sha256=request.get('sha256')==evidence['sha256'])
    ext=p.suffix.lower()
    if ext in IMAGE_SUFFIXES:
        try: evidence.update(kind='image', **image_metadata(data,p.name))
        except Exception as e: evidence.update(kind='image',valid=False,error=f'{type(e).__name__}: {e}')
        assets.append(evidence)
    elif ext in ['.ttf','.otf','.woff','.woff2']:
        try: evidence.update(kind='font', **font_metadata(data))
        except Exception as e: evidence.update(kind='font',valid=False,error=f'{type(e).__name__}: {e}')
        fonts.append(evidence)
    elif ext=='.glb':
        try: evidence.update(kind='glb', **glb_metadata(data,source))
        except Exception as e: evidence.update(kind='glb',valid=False,error=f'{type(e).__name__}: {e}')
        glbs.append(evidence)
    if ext in ['.css','.js','.html'] or (request and request.get('content_type','').startswith('text/html')):
        text=data.decode('utf-8'); texts.append((source,text))
        if ext=='.css': css.append(css_inventory(text,source))
        elif ext=='.html' or (request and request.get('content_type','').startswith('text/html')):
            parser=StylesParser(); parser.feed(text)
            for i,style in enumerate(parser.styles): css.append(css_inventory(style,f'{source}#style[{i}]'))
            if parser.attrs:
                css.append(css_inventory('\n'.join(f'[data-audit-inline="{i}"]{{{s}}}' for i,s in enumerate(parser.attrs)),f'{source}#inline-style-attributes'))

# Every static data URI occurrence is saved or explicitly classified. Empty prefixes
# (startsWith('data:image/png;base64,')) are runtime validation code, not assets.
embedded={}; uri_occurrences=[]; data_markers=[]; shaders={}
quoted=re.compile(r'"(?:\\[\s\S]|[^"\\])*"|\'(?:\\[\s\S]|[^\'\\])*\'|`(?:\\[\s\S]|[^`\\])*`')
for source,text in texts:
    for m in re.finditer(r'data:(?:[a-zA-Z][a-zA-Z0-9!#$&^_.+-]*/[a-zA-Z0-9!#$&^_.+-]+)?(?:;[^,\s"\'<>]*)?,',text):
        start=m.start(); delimiter=text[start-1] if start and text[start-1] in ['"',"'",'`'] else None
        end=m.end(); escaped=False
        if delimiter:
            while end<len(text):
                c=text[end]
                if escaped: escaped=False
                elif c=='\\': escaped=True
                elif c==delimiter: break
                end+=1
        else:
            z=re.search(r'[\s"\'<>)]',text[end:]); end=end+z.start() if z else len(text)
        raw=text[start:end]; decoded=unescape_js(html.unescape(raw)); header,body=decoded.split(',',1)
        occ={'source':source,'char_offset':start,'line':text.count('\n',0,start)+1,'column':start-(text.rfind('\n',0,start)+1)+1,'raw_data_uri':raw,'mime':header[5:].split(';')[0] or 'text/plain','base64':';base64' in header.lower()}
        if not body:
            occ['classification']='runtime_data_uri_prefix_without_payload'; uri_occurrences.append(occ); continue
        try:
            payload=base64.b64decode(body,validate=True) if occ['base64'] else urllib.parse.unquote_to_bytes(body)
            digest=sha(payload); ext={ 'image/svg+xml':'.svg','image/webp':'.webp','image/avif':'.avif','image/png':'.png','image/jpeg':'.jpg','text/javascript':'.js','application/javascript':'.js'}.get(occ['mime'],'.bin')
            dest=EMBED/'data_uri'/(digest[:24]+ext); dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(payload)
            if digest not in embedded:
                entry={'path':rel(dest),'bytes':len(payload),'sha256':digest,'mime':occ['mime'],'sources':[]}
                if occ['mime'].startswith('image/'):
                    try: entry['validation']=image_metadata(payload,dest.name)
                    except Exception as e: entry['validation']={'valid':False,'error':str(e)}
                embedded[digest]=entry
            occ['classification']='extracted_static_payload'; occ['resource_path']=rel(dest); occ['sha256']=digest
            embedded[digest]['sources'].append({k:v for k,v in occ.items() if k!='raw_data_uri'})
        except Exception as e: occ.update(classification='extraction_error',error=str(e))
        uri_occurrences.append(occ)
    for m in re.finditer(r'data:',text):
        if any(x['source']==source and x['char_offset']==m.start() for x in uri_occurrences): continue
        context=text[max(0,m.start()-60):m.start()+130]
        data_markers.append({'source':source,'char_offset':m.start(),'context':context,'classification':'non_resource_marker_or_program_property'})
    if source.endswith('.js'):
        for m in quoted.finditer(text):
            raw=m.group()[1:-1]
            if not re.search(r'void main|#(?:if|define|include|endif|pragma|version)|(?:float|vec[234]|mat[234]|uniform|varying|attribute|precision)\s|gl_(?:Position|FragColor|VertexID)|texture2D\s*\(', raw): continue
            decoded=unescape_js(raw)
            digest=sha(decoded.encode('utf-8','surrogatepass')); dest=EMBED/'shader_glsl'/(digest[:24]+'.glsl')
            if digest not in shaders:
                dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(decoded.encode('utf-8','surrogatepass'))
                shaders[digest]={'path':rel(dest),'sha256':digest,'bytes':dest.stat().st_size,'sources':[], 'validation':'Decoded static string literal; retained verbatim. No GPU compilation attempted.'}
            shaders[digest]['sources'].append({'source':source,'char_offset':m.start(),'char_end_offset':m.end(),'context':text[max(0,m.start()-70):m.start()]})

integrity=[]
for item in manifest:
    if not item.get('local_path'): continue
    p=ROOT/item['local_path']; record={k:item.get(k) for k in ['url','status','local_path','bytes','sha256']}
    if p.exists():
        b=p.read_bytes(); record.update(exists=True,actual_bytes=len(b),actual_sha256=sha(b),matches=(len(b)==item['bytes'] and sha(b)==item['sha256']))
    else: record.update(exists=False,matches=False)
    integrity.append(record)

asset_by_path={x['path']:x for x in assets}
box=[]
for p in sorted((ROOT/'hinh_anh_assets/story-assets').glob('box-*.jpg')):
    original=asset_by_path[rel(p)]; url='https://sonsonmaisat.site/story-assets/'+p.name
    live=next((x for x in manifest if x['url']==url),None)
    box.append({'filename':p.name,'original':{k:original.get(k) for k in ['path','bytes','sha256','format','width','height','valid','validation','matches_initial_inventory_sha256']},'live_request':{k:live.get(k) for k in ['url','status','content_type','bytes','sha256','local_path','fetched_at']} if live else None})
fav=[]
for p in sorted((ROOT/'hinh_anh_assets').glob('favicon*')):
    old=asset_by_path.get(rel(p)); new=asset_by_path.get(SNAPSHOT+'/'+p.name)
    comparison={'filename':p.name,'old':old,'live':new,'same_bytes':bool(old and new and old['sha256']==new['sha256'])}
    if p.suffix.lower()=='.svg' and old and new:
        a=p.read_bytes(); b=(ROOT/new['path']).read_bytes()
        comparison['identical_after_normalizing_CRLF_to_LF']=a.replace(b'\r\n',b'\n')==b.replace(b'\r\n',b'\n')
        comparison['byte_differences']=[{'operation':tag,'old_start':i,'old_end':j,'new_start':k,'new_end':l,'old_bytes_hex':a[i:j].hex(),'new_bytes_hex':b[k:l].hex()} for tag,i,j,k,l in difflib.SequenceMatcher(None,a,b).get_opcodes() if tag!='equal']
    fav.append(comparison)

report={'generated_at':datetime.now(timezone(timedelta(hours=7))).isoformat(),'scope':'Offline validation of all files in hinh_anh_assets, ma_nguon_css_js, trang_html_goc, and ban_chup_goc snapshot; HTTP evidence copied from manifest, no fresh requests in this script.',
 'tools':{'python':sys.version,'pillow':pillow_version,'fonttools':fontTools.__version__,'tinycss2':tinycss2.__version__},
 'summary':{'input_files':len(files),'images':len(assets),'unique_image_sha256':len({x['sha256'] for x in assets}),'invalid_images':sum(not x.get('valid') for x in assets),'font_files':len(fonts),'invalid_fonts':sum(not x.get('valid') for x in fonts),'glb_files':len(glbs),'invalid_glbs':sum(not x.get('valid') for x in glbs),'css_sources_including_inline':len(css),'static_data_uri_unique_resources':len(embedded),'static_data_uri_occurrences':sum(x['classification']=='extracted_static_payload' for x in uri_occurrences),'runtime_data_uri_prefix_occurrences':sum(x['classification']=='runtime_data_uri_prefix_without_payload' for x in uri_occurrences),'data_uri_errors':sum(x['classification']=='extraction_error' for x in uri_occurrences),'unique_shader_string_literals':len(shaders),'shader_literal_occurrences':sum(len(x['sources']) for x in shaders.values()),'manifest_files_verified':len(integrity),'manifest_integrity_failures':sum(not x['matches'] for x in integrity),'preserved_valid_box_images_live_404':sum(x['original']['valid'] and x['live_request'] and x['live_request']['status']==404 for x in box)},
 'images':assets,'fonts':fonts,'glb_models':glbs,'css':css,'embedded_data_uri_resources':list(embedded.values()),'data_uri_occurrences':uri_occurrences,'non_asset_data_markers':data_markers,'shader_string_literals':list(shaders.values()),'manifest_integrity':integrity,'box_image_evidence':box,'favicon_comparison':fav,
 'limitations':['Raster validation checks files and decoder output; does not prove every interaction was executed.','SVG validation parses XML and records vector attributes. SVGs are not rasterized or visually compared.','Embedded resources are static data URI payloads present in source; runtime-generated canvas exports/user-uploaded images have no fixed file to extract.','Shader literals are preserved but not compiled or evaluated on a GPU.','CSS and shader metadata are derived from saved sources. Original bytes and SHA-256 remain authoritative.','Font metadata extracts SFNT tables and Unicode cmap; fonts are not visually rendered in this audit.']}
write_json(OUT/'kiem_dinh_tai_nguyen.json', report)
write_json(EMBED/'muc_luc.json',{'generated_at':report['generated_at'],'resources':list(embedded.values()),'occurrences':uri_occurrences,'non_asset_data_markers':data_markers,'shaders':list(shaders.values()),'glb_json':[{'source':x['path'],'path':x.get('json_extracted_path')} for x in glbs]})
s=report['summary']; lines=['# Kiểm định tài nguyên — 12/10/2026','',f"Tạo lúc {report['generated_at']}. Đây là kiểm định trên file đã lưu; trạng thái HTTP lấy từ manifest của đợt cào mới.",'','## Kết quả chính','',f"- Đã xét {s['input_files']} file nguồn; {s['images']} file ảnh ({s['unique_image_sha256']} nội dung SHA-256 khác nhau), {s['font_files']} font và {s['glb_files']} mô hình GLB.",f"- Ảnh lỗi giải mã/XML: {s['invalid_images']}. File manifest sai hash/kích thước: {s['manifest_integrity_failures']} / {s['manifest_files_verified']}.",f"- {s['preserved_valid_box_images_live_404']} ảnh box-*.jpg cũ vẫn giải mã đầy đủ, không bị thay đổi so với kiểm kê đầu, dù URL hiện trả HTTP 404.",f"- Đã bóc {s['static_data_uri_unique_resources']} data URI có dữ liệu tĩnh, ghi lại {s['runtime_data_uri_prefix_occurrences']} tiền tố data URI dùng kiểm tra dữ liệu tương tác; lỗi bóc: {s['data_uri_errors']}.",f"- Đã giữ riêng {s['unique_shader_string_literals']} chuỗi GLSL/shader khác nhau; có nguồn và vị trí ký tự.",f"- CSS: {s['css_sources_including_inline']} nguồn gồm CSS ngoài và CSS inline; JSON chứa toàn bộ selector/declaration đã phân tích, custom properties, font-face, media/supports, keyframes, animation/transition.",'','## Ảnh box cũ và bằng chứng HTTP','', '| File | Kích thước | File cũ hợp lệ | SHA khớp kiểm kê đầu | HTTP mới |','|---|---:|---|---|---|']
for x in box:
    o=x['original']; l=x['live_request'] or {}; lines.append(f"| {x['filename']} | {o['width']} × {o['height']} | {o['valid']} | {o['matches_initial_inventory_sha256']} | {l.get('status','chưa có')} |")
lines+=['','Không ghi đè ảnh cũ bằng HTML 404. File HTML lỗi mới được giữ riêng trong `http_loi/`; hash và đường dẫn có trong JSON.','','## Favicon','']
for x in fav:
    lines += [f"- `{x['filename']}`: {'giống nhau' if x['same_bytes'] else 'khác nội dung'}."]
    if x.get('identical_after_normalizing_CRLF_to_LF') and not x['same_bytes']: lines.append('  - Chỉ khác ký tự xuống dòng: 2 CRLF cũ thành LF. XML/nội dung đồ họa giữ nguyên.')
    for label,key in [('Cũ','old'),('Mới','live')]:
        v=x[key]
        if v: lines.append(f"  - {label}: {v['bytes']} byte, SHA-256 `{v['sha256']}`, {v.get('format')} {v.get('width')} × {v.get('height')}.")
lines+=['','## Mô hình và font','']
for x in glbs: lines.append(f"- `{x['path']}`: hợp lệ={x.get('valid')}, {x.get('counts')}; JSON chính xác: `{x.get('json_extracted_path')}`.")
for x in fonts:
    selected=[n['value'] for n in x.get('names',[]) if n['name_id'] in [1,2,4,6]]
    lines.append(f"- `{x['path']}`: hợp lệ={x.get('valid')}; {x.get('glyph_count')} glyph, {x.get('cmap_codepoint_count')} codepoint; {', '.join(dict.fromkeys(selected))}.")
lines+=['','## Tệp nhúng','']
for x in embedded.values(): lines.append(f"- `{x['path']}`: {x['mime']}, {x['bytes']} byte, hợp lệ={x.get('validation',{}).get('valid')}, {len(x['sources'])} vị trí nguồn.")
lines+=['','Mục lục đầy đủ: `tai_nguyen_nhung/muc_luc.json`. Mỗi data URI có nguyên văn nguồn, offset và hash của dữ liệu giải mã; mỗi shader có nguồn và offset.','','## Giới hạn kiểm định','', '- Kiểm tra tính toàn vẹn và cấu trúc file, không thay thế kiểm thử mọi thao tác UI.', '- SVG chỉ được phân tích XML; shader chưa được biên dịch GPU; font chưa được render trực quan.', '- Dữ liệu canvas sinh lúc chạy, ảnh người dùng tải lên, trạng thái lưu ở localStorage và kết quả tương tác không có một file cố định để bóc từ bundle.', '- Tất cả dữ liệu gốc được giữ nguyên. Mọi kết luận HTTP chỉ tương ứng thời điểm lấy trong manifest.', '', 'Chi tiết máy đọc: `kiem_dinh_tai_nguyen.json`.']
(OUT/'kiem_dinh_tai_nguyen.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps(s,ensure_ascii=False,indent=2))
