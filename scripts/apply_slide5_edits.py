# -*- coding: utf-8 -*-
"""
Cập nhật Slide Khám Phá (Top Hero Banner) theo hình ảnh Canva người dùng gửi:
1. Đổi tiêu đề:
   'Năm chặng.<br/>Một bề mặt nhiều lớp.'
   -> 'QUA TỪNG LỚP,<br/>VẺ ĐẸP DẦN HIỆN RA.'
2. Đổi nút bấm:
   'Tự tạo một bề mặt sơn mài ⟶'
   -> 'TRẢI NGHIỆM NGAY ⟶'
3. Giữ / thêm chú thích bên cạnh nút bấm:
   'Trải nghiệm khoảng 3–5 phút · Có tương tác'
Cập nhật đồng bộ cả HTML tĩnh và RSC serialization stream để tránh React hydration mismatch.
"""

def apply_kham_pha_edits():
    # 1. Update kham-pha/index.html
    html_path = 'kham-pha/index.html'
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Static HTML replacements
    old_h1_static = '<h1>Năm chặng.<br/>Một bề mặt nhiều lớp.</h1>'
    new_h1_static = '<h1>QUA TỪNG LỚP,<br/>VẺ ĐẸP DẦN HIỆN RA.</h1>'
    assert old_h1_static in html, "old_h1_static not found"
    html = html.replace(old_h1_static, new_h1_static)

    old_action_static = '<div class="explore_actions__K1B4A"><a class="btn red" href="/trai-nghiem#simulator">Tự tạo một bề mặt sơn mài <span aria-hidden="true">⟶</span></a></div>'
    new_action_static = '<div class="explore_actions__K1B4A"><a class="btn red" href="/trai-nghiem#simulator">TRẢI NGHIỆM NGAY <span aria-hidden="true">⟶</span></a><span>Trải nghiệm khoảng 3–5 phút · Có tương tác</span></div>'
    assert old_action_static in html, "old_action_static not found"
    html = html.replace(old_action_static, new_action_static)

    # Hydration stream (__next_f) replacements
    old_h1_stream = r'[\"Năm chặng.\",[\"$\",\"br\",null,{}],\"Một bề mặt nhiều lớp.\"]'
    new_h1_stream = r'[\"QUA TỪNG LỚP,\",[\"$\",\"br\",null,{}],\"VẺ ĐẸP DẦN HIỆN RA.\"]'
    assert old_h1_stream in html, "old_h1_stream not found"
    html = html.replace(old_h1_stream, new_h1_stream)

    old_action_stream = r'{\"className\":\"explore_actions__K1B4A\",\"children\":[\"$\",\"$L6\",null,{\"className\":\"btn red\",\"href\":\"/trai-nghiem#simulator\",\"children\":[\"Tự tạo một bề mặt sơn mài \",[\"$\",\"span\",null,{\"aria-hidden\":\"true\",\"children\":\"⟶\"}]]}]}'
    new_action_stream = r'{\"className\":\"explore_actions__K1B4A\",\"children\":[[\"$\",\"$L6\",null,{\"className\":\"btn red\",\"href\":\"/trai-nghiem#simulator\",\"children\":[\"TRẢI NGHIỆM NGAY \",[\"$\",\"span\",null,{\"aria-hidden\":\"true\",\"children\":\"⟶\"}]]}],[\"$\",\"span\",null,{\"children\":\"Trải nghiệm khoảng 3–5 phút · Có tương tác\"}]]}'
    assert old_action_stream in html, "old_action_stream not found"
    html = html.replace(old_action_stream, new_action_stream)

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Updated kham-pha/index.html successfully!")

    # 2. Update rsc_payloads/kham-pha.rsc
    rsc_path = 'rsc_payloads/kham-pha.rsc'
    with open(rsc_path, 'r', encoding='utf-8') as f:
        rsc = f.read()

    old_h1_rsc = '["Năm chặng.",["$","br",null,{}],"Một bề mặt nhiều lớp."]'
    new_h1_rsc = '["QUA TỪNG LỚP,",["$","br",null,{}],"VẺ ĐẸP DẦN HIỆN RA."]'
    assert old_h1_rsc in rsc, "old_h1_rsc not found"
    rsc = rsc.replace(old_h1_rsc, new_h1_rsc)

    old_action_rsc = '{"className":"explore_actions__K1B4A","children":["$","$L2",null,{"className":"btn red","href":"/trai-nghiem#simulator","children":["Tự tạo một bề mặt sơn mài ",["$","span",null,{"aria-hidden":"true","children":"⟶"}]]}]}'
    new_action_rsc = '{"className":"explore_actions__K1B4A","children":[["$","$L2",null,{"className":"btn red","href":"/trai-nghiem#simulator","children":["TRẢI NGHIỆM NGAY ",["$","span",null,{"aria-hidden":"true","children":"⟶"}]]}],["$","span",null,{"children":"Trải nghiệm khoảng 3–5 phút · Có tương tác"}]]}'
    assert old_action_rsc in rsc, "old_action_rsc not found"
    rsc = rsc.replace(old_action_rsc, new_action_rsc)

    with open(rsc_path, 'w', encoding='utf-8') as f:
        f.write(rsc)
    print("Updated rsc_payloads/kham-pha.rsc successfully!")

if __name__ == '__main__':
    apply_kham_pha_edits()
