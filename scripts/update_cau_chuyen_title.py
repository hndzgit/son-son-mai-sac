# -*- coding: utf-8 -*-
"""
Script cập nhật tiêu đề và mô tả trang Câu chuyện sơn mài:
Từ:
  MỖI THỜI KỲ LẠI THÊM MỘT LỚP
  Từ vật dụng đời sống đến thực hành đương đại, một chất liệu đi qua nhiều bàn tay và cách nhìn.
Thành:
  TỪ DẤU XƯA ĐẾN HƠI THỞ HÔM NAY
  Qua nhiều giai đoạn, sơn mài đã đi từ những vật dụng quen thuộc trong đời sống đến một ngôn ngữ nghệ thuật giàu bản sắc, liên tục được gìn giữ, tiếp nối và làm mới.
"""

import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def update_html(fpath):
    if not os.path.exists(fpath):
        return
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Thay thế tiêu đề wide
    content = content.replace(
        'MỖI THỜI KỲ<br/>LẠI THÊM MỘT LỚP',
        'TỪ DẤU XƯA<br/>ĐẾN HƠI THỞ HÔM NAY'
    )
    content = content.replace(
        'MỖI THỜI KỲ<br>LẠI THÊM MỘT LỚP',
        'TỪ DẤU XƯA<br>ĐẾN HƠI THỞ HÔM NAY'
    )

    # Thay thế tiêu đề narrow
    content = content.replace(
        'MỖI THỜI KỲ<br/>LẠI THÊM<br/>MỘT LỚP',
        'TỪ DẤU XƯA<br/>ĐẾN HƠI THỞ<br/>HÔM NAY'
    )
    content = content.replace(
        'MỖI THỜI KỲ<br>LẠI THÊM<br>MỘT LỚP',
        'TỪ DẤU XƯA<br>ĐẾN HƠI THỞ<br>HÔM NAY'
    )

    # Thay thế đoạn mô tả
    content = content.replace(
        'Từ vật dụng đời sống đến thực hành đương đại, một chất liệu đi qua nhiều bàn tay và cách nhìn.',
        'Qua nhiều giai đoạn, sơn mài đã đi từ những vật dụng quen thuộc trong đời sống đến một ngôn ngữ nghệ thuật giàu bản sắc, liên tục được gìn giữ, tiếp nối và làm mới.'
    )

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated HTML: {fpath}")

def update_js_chunk(fpath):
    if not os.path.exists(fpath):
        return
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Thay thế tiêu đề wide trong JS chunk
    old_wide = '["MỖI THỜI KỲ",(0,i.jsx)("br",{}),"LẠI TH\\xcaM MỘT LỚP"]'
    new_wide = '["TỪ DẤU XƯA",(0,i.jsx)("br",{}),"ĐẾN HƠI THỞ HÔM NAY"]'
    content = content.replace(old_wide, new_wide)

    # Thay thế tiêu đề narrow trong JS chunk
    old_narrow = '["MỖI THỜI KỲ",(0,i.jsx)("br",{}),"LẠI TH\\xcaM",(0,i.jsx)("br",{}),"MỘT LỚP"]'
    new_narrow = '["TỪ DẤU XƯA",(0,i.jsx)("br",{}),"ĐẾN HƠI THỞ",(0,i.jsx)("br",{}),"HÔM NAY"]'
    content = content.replace(old_narrow, new_narrow)

    # Thay thế đoạn mô tả trong JS chunk
    old_desc = '"Từ vật dụng đời sống đến thực h\\xe0nh đương đại, một chất liệu đi qua nhiều b\\xe0n tay v\\xe0 c\\xe1ch nh\\xecn."'
    new_desc = '"Qua nhiều giai đoạn, sơn mài đã đi từ những vật dụng quen thuộc trong đời sống đến một ngôn ngữ nghệ thuật giàu bản sắc, liên tục được gìn giữ, tiếp nối và làm mới."'
    content = content.replace(old_desc, new_desc)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated JS: {fpath}")

if __name__ == '__main__':
    update_html(os.path.join(BASE_DIR, 'cau-chuyen-son-mai/index.html'))
    update_html(os.path.join(BASE_DIR, 'trang_html_goc/06_cau_chuyen_son_mai.html'))
    update_js_chunk(os.path.join(BASE_DIR, '_next/static/chunks/app/cau-chuyen-son-mai/page-18999a17f9a00aec.js'))
    update_js_chunk(os.path.join(BASE_DIR, 'ma_nguon_css_js/js/app_cau-chuyen-son-mai_page-18999a17f9a00aec.js'))
    print("DONE! Title and description updated successfully.")
