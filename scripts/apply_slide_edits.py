import os

def update_file(filepath):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Chuyển từ VIẾT HOA sang chữ thường thanh lịch (Title / Sentence case) chuẩn phong cách web gốc
    replacements = [
        # Hero title
        (
            'ĐI QUA TỪNG ĐƯỜNG MÀI,<br/>KHÁM PHÁ GIÁ TRỊ VIỆT',
            'Đi qua từng đường mài,<br/>khám phá giá trị Việt'
        ),
        (
            'ĐI QUA TỪNG ĐƯỜNG MÀI,\\",[\\"$\\",\\"br\\",null,{}],\\"KHÁM PHÁ GIÁ TRỊ VIỆT',
            'Đi qua từng đường mài,\\",[\\"$\\",\\"br\\",null,{}],\\"khám phá giá trị Việt'
        ),
        (
            'ĐI QUA TỪNG ĐƯỜNG MÀI,",["$","br",null,{}],"KHÁM PHÁ GIÁ TRỊ VIỆT',
            'Đi qua từng đường mài,",["$","br",null,{}],"khám phá giá trị Việt'
        ),

        # Card 1 (Chuẩn chữ hoa đầu câu)
        (
            'Sơn Mài<br/>là gì ?',
            'Sơn mài<br/>là gì?'
        ),
        (
            'Sơn Mài\\",[\\"$\\",\\"br\\",null,{}],\\"là gì ?',
            'Sơn mài\\",[\\"$\\",\\"br\\",null,{}],\\"là gì?'
        ),
        (
            'Sơn Mài",["$","br",null,{}],"là gì ?',
            'Sơn mài",["$","br",null,{}],"là gì?'
        ),

        # Card 3 (Chuyển TỪ DẤU XƯA ĐẾN HƠI THỞ HÔM NAY sang chữ thường thanh nhã)
        (
            'TỪ DẤU XƯA<br/>ĐẾN HƠI THỞ HÔM NAY',
            'Từ dấu xưa<br/>đến hơi thở hôm nay'
        ),
        (
            'TỪ DẤU XƯA\\",[\\"$\\",\\"br\\",null,{}],\\"ĐẾN HƠI THỞ HÔM NAY',
            'Từ dấu xưa\\",[\\"$\\",\\"br\\",null,{}],\\"đến hơi thở hôm nay'
        ),
        (
            'TỪ DẤU XƯA",["$","br",null,{}],"ĐẾN HƠI THỞ HÔM NAY',
            'Từ dấu xưa",["$","br",null,{}],"đến hơi thở hôm nay'
        ),
    ]

    count = 0
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            count += 1
            print(f"[{os.path.basename(filepath)}] Replaced: {old[:30]}... -> {new[:30]}...")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Finished {filepath}, total replacements made: {count}\n")

update_file('index.html')
update_file('rsc_payloads/root.rsc')
update_file('kiem_tra_2026-10-12/ban_chup_goc/index.html')
