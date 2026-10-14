import subprocess
import sys

def update_files():
    paths = [
        '_next/static/chunks/840-f19fdd306966b2e5.js',
        'ma_nguon_css_js/js/840-f19fdd306966b2e5.js'
    ]

    guide_old = 'Chọn một loại cốt để xem vật liệu ảnh hưởng ra sao đến việc chuẩn bị. Gỗ, tre, gốm và vật liệu khác cần cách xử lý phù hợp với cấu tạo tác phẩm.'
    guide_new = 'Chọn một loại cốt để xem vật liệu ảnh hưởng ra sao đến việc chuẩn bị. Gỗ, tre, gốm và vật liệu khác cần cách xử lý phù hợp với cấu tạo sản phẩm.'

    check_old = ')," Xem lớp vải cotton gia cố (khi phù hợp)"]})'
    check_new = ')," Thêm lớp vải/xơ/dặm gia cố (chỉ phù hợp)"]})'

    msg_old = 'if(e.target.checked)B("Đã bật xem lớp vải cotton gia cố bó cốt.")'
    msg_new = 'if(e.target.checked)B("Đã bật thêm lớp vải/xơ/dặm gia cố cốt.")'

    target = ':"Lớp vải chỉ là lựa chọn minh họa khi phù hợp với cấu tạo cốt; không phải bước bắt buộc cho mọi vật liệu."}),(0,a.jsxs)("button",{type:"button",className:g().advanceButton'
    replacement = ':"Lớp vải chỉ là lựa chọn minh họa khi phù hợp với cấu tạo cốt; không phải bước bắt buộc cho mọi vật liệu."}),(0,a.jsxs)("div",{className:"studio_stage_status",children:[(0,a.jsx)("span",{className:"studio_status_dot"}),(0,a.jsx)("span",{children:"Bề mặt đã được đặt ở trạng thái sẵn sàng để bắt đầu làm vóc."})]}),(0,a.jsxs)("button",{type:"button",className:g().advanceButton'

    for p in paths:
        with open(p, 'r', encoding='utf-8') as f:
            content = f.read()

        if guide_old in content:
            content = content.replace(guide_old, guide_new)

        if check_old in content:
            content = content.replace(check_old, check_new)

        if msg_old in content:
            content = content.replace(msg_old, msg_new)

        if target in content:
            content = content.replace(target, replacement)
        elif 'studio_stage_status' not in content:
            print(f"ERROR: target not found in {p}")
            return False

        with open(p, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Updated", p)

        res = subprocess.run(['node', '-c', p])
        if res.returncode != 0:
            print("Syntax error in", p)
            return False

    print("All chunks updated and syntax verified!")
    return True

if __name__ == '__main__':
    if not update_files():
        sys.exit(1)
