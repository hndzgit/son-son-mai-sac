#!/usr/bin/env python3
import os
import subprocess

FILES = [
    "_next/static/chunks/840-f19fdd306966b2e5.js",
    "ma_nguon_css_js/js/840-f19fdd306966b2e5.js"
]

def patch_file(filepath):
    print(f"\n--- Patching {filepath} ---")
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found!")
        return False
        
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update Section 1 title and cards:
    # From "1. PHỦ LỚP SƠN TRONG & Ủ KHÔ" to "1. PHỦ LỚP SƠN ĐEN (SƠN THEN) & Ủ KHÔ"
    replacements = [
        (
            '1. PHỦ LỚP SƠN TRONG & Ủ KHÔ',
            '1. PHỦ LỚP SƠN ĐEN (SƠN THEN) & Ủ KHÔ'
        ),
        (
            'children:"Phủ lớp sơn trong"',
            'children:"Phủ lớp sơn đen (sơn then)"'
        ),
        (
            '[Z," lượt đã phủ · có thể phủ nhiều lượt"]',
            '[Z," lượt đã phủ · Che kín toàn bộ bề mặt"]'
        ),
        (
            '[Z," lượt đ\\xe3 phủ \xb7 c\\xf3 thể phủ nhiều lượt"]',
            '[Z," lượt đ\\xe3 phủ \xb7 Che k\\xedn to\\xe0n bộ bề mặt"]'
        ),
        (
            'B("Đã phủ thêm một lượt sơn trong suốt lên bề mặt; sẵn sàng ủ khô.")',
            'B("Đã phủ lớp sơn đen (sơn then) che kín bề mặt; sẵn sàng ủ khô.")'
        ),
        (
            'B("Đ\\xe3 phủ th\\xeam một lượt sơn trong suốt l\\xean bề mặt; sẵn s\\xe0ng ủ kh\\xf4.")',
            'B("Đ\\xe3 phủ lớp sơn đen (sơn then) che k\\xedn bề mặt; sẵn s\\xe0ng ủ kh\\xf4.")'
        ),
        (
            'B("Lớp phủ đã ủ khô hoàn toàn. Sẵn sàng tiến hành mài nước.")',
            'B("Lớp sơn đen đã ủ khô hoàn toàn. Sẵn sàng tiến hành mài nước.")'
        ),
        (
            'B("Lớp phủ đ\\xe3 ủ kh\\xf4 ho\\xe0n to\\xe0n. Sẵn s\\xe0ng tiến h\\xe0nh m\\xe0i nước.")',
            'B("Lớp sơn đen đ\\xe3 ủ kh\\xf4 ho\\xe0n to\\xe0n. Sẵn s\\xe0ng tiến h\\xe0nh m\\xe0i nước.")'
        ),
        # 2. Sidebar and header description:
        (
            '["Phủ sơn & Mài nước","Phủ lớp sơn trong suốt, ủ khô, mài nước làm lộ họa tiết và đánh bóng hoàn thiện."]',
            '["Phủ then & Mài nước","Phủ lớp sơn đen (sơn then), ủ khô, mài nước làm lộ họa tiết và đánh bóng hoàn thiện."]'
        ),
        (
            '["Phủ sơn & M\\xe0i nước","Phủ lớp sơn trong suốt, ủ kh\\xf4, m\\xe0i nước l\\xe0m lộ họa tiết v\\xe0 đ\\xe1nh b\\xf3ng ho\\xe0n thiện."]',
            '["Phủ then & M\\xe0i nước","Phủ lớp sơn đen (sơn then), ủ kh\\xf4, m\\xe0i nước l\\xe0m lộ họa tiết v\\xe0 đ\\xe1nh b\\xf3ng ho\\xe0n thiện."]'
        ),
        (
            '"Phủ lớp sơn trong, tiến hành mài nước để làm lộ họa tiết và đánh bóng hoàn thiện."',
            '"Phủ lớp sơn đen (sơn then), tiến hành mài nước để làm lộ họa tiết và đánh bóng hoàn thiện."'
        ),
        (
            '"Phủ lớp sơn trong, tiến h\\xe0nh m\\xe0i nước để l\\xe0m lộ họa tiết v\\xe0 đ\\xe1nh b\\xf3ng ho\\xe0n thiện."',
            '"Phủ lớp sơn đen (sơn then), tiến h\\xe0nh m\\xe0i nước để l\\xe0m lộ họa tiết v\\xe0 đ\\xe1nh b\\xf3ng ho\\xe0n thiện."'
        ),
        (
            '"Công đoạn phủ sơn trong (sơn cánh gián/sơn quang) và mài nước là linh hồn của nghệ thuật sơn mài. Càng mài nước đều tay, từng lớp màu, vỏ trứng và vàng quỳ càng ánh lên chiều sâu huyền ảo."',
            '"Công đoạn phủ sơn đen (sơn then) và mài nước là linh hồn của nghệ thuật sơn mài. Càng mài nước đều tay, lớp sơn đen mỏng dần, từng lớp màu, vỏ trứng và vàng quỳ càng ánh lên chiều sâu huyền ảo."'
        ),
        (
            'c\\xf4ng đoạn phủ sơn trong (sơn c\\xe1nh gi\\xe1n/sơn quang) v\\xe0 m\\xe0i nước l\\xe0 linh hồn của nghệ thuật sơn m\\xe0i. C\\xe0ng m\\xe0i nước đều tay, từng lớp m\\xe0u, vỏ trứng v\\xe0 v\\xe0ng quỳ c\\xe0ng \\xe1nh l\\xean chiều s\\xe2u huyền ảo.',
            'c\\xf4ng đoạn phủ sơn đen (sơn then) v\\xe0 m\\xe0i nước l\\xe0 linh hồn của nghệ thuật sơn m\\xe0i. C\\xe0ng m\\xe0i nước đều tay, lớp sơn đen mỏng dần, từng lớp m\\xe0u, vỏ trứng v\\xe0 v\\xe0ng quỳ c\\xe0ng \\xe1nh l\\xean chiều s\\xe2u huyền ảo.'
        ),
        # 3. Advance to stage 4 click: start at 0% coverage (pure black) instead of 20%:
        (
            'z("sand");O(20);var sRef=es.current;if(sRef&&sRef.setCoverage)sRef.setCoverage(20);B("Chuyển sang c\\xf4ng đoạn Phủ sơn & M\\xe0i nước.',
            'z("sand");O(0);var sRef=es.current;if(sRef&&sRef.setCoverage)sRef.setCoverage(0);B("Chuyển sang c\\xf4ng đoạn Phủ then & M\\xe0i nước. Lớp sơn đen đ\\xe3 phủ k\\xedn bề mặt, tiến h\\xe0nh m\\xe0i nước để l\\xe0m lộ hoa văn.'
        ),
        # 4. BLACK LACQUER OVERLAY (Sơn then đen) in preview:
        (
            'radial-gradient(ellipse at 50% 50%, rgba(55,20,8,"+Math.max(0,.94-q/100*1.05)+") 0%, rgba(20,6,2,"+Math.max(0,.98-q/100*1.05)+") 100%)',
            'radial-gradient(ellipse at 50% 50%, rgba(12,10,10,"+Math.max(0,(100-q)/100*0.99)+") 0%, rgba(4,3,3,"+Math.max(0,(100-q)/100*1.0)+") 100%)'
        ),
        # 5. Wet abrasion sheen:
        (
            'radial-gradient(circle at 50% 50%, transparent 35%, rgba(255,255,255,"+(q>8&&q<96?.14:.03)+") 65%, transparent 85%)',
            'radial-gradient(circle at 50% 50%, rgba(255,255,255,"+(q>0&&q<100?.12:.01)+") 0%, transparent 75%)'
        ),
        # 6. Status pill text in preview wrap:
        (
            'q<=15?"Lớp sơn phủ k\\xedn \xb7 Họa tiết chìm b\\xean dưới":q>=85?["M\\xe0i ho\\xe0n tất (",q,"%) \xb7 Hoa văn lộ r\\xf5 n\\xe9t"]:["Đang m\\xe0i nước (",q,"%): Họa tiết & sắc nền dần hiện"]',
            'q<=15?"Lớp sơn đen phủ k\\xedn \xb7 Bề mặt đen tuyền, hoa văn ẩn":q>=85?["M\\xe0i lộ ho\\xe0n tất (",q,"%) \xb7 T\\xe1c phẩm lộ r\\xf5 tr\\xean nền sơn m\\xe0i"]:["Đang m\\xe0i nước (",q,"%): M\\xe0i mỏng lớp sơn đen \xb7 Hoa văn dần lộ diện"]'
        ),
        (
            'q<=15?"Lớp sơn phủ kín · Họa tiết chìm bên dưới":q>=85?["Mài hoàn tất (",q,"%) · Hoa văn lộ rõ nét"]:["Đang mài nước (",q,"%): Họa tiết & sắc nền dần hiện"]',
            'q<=15?"Lớp sơn đen phủ kín · Bề mặt đen tuyền, hoa văn ẩn":q>=85?["Mài lộ hoàn tất (",q,"%) · Tác phẩm lộ rõ trên nền sơn mài"]:["Đang mài nước (",q,"%): Mài mỏng lớp sơn đen · Hoa văn dần lộ diện"]'
        ),
        # 7. Button subtitle:
        (
            '[et," lượt m\\xe0i \xb7 Đang lộ ",q,"% hoa văn"]',
            '[et," lượt m\\xe0i \xb7 ",q===0?"Lớp sơn đen đang phủ k\\xedn (0%)":"Đang lộ "+q+"% hoa văn"]'
        ),
        (
            '[et," lượt mài · Đang lộ ",q,"% hoa văn"]',
            '[et," lượt mài · ",q===0?"Lớp sơn đen đang phủ kín (0%)":"Đang lộ "+q+"% hoa văn"]'
        ),
        # 8. Button click nextQ logic:
        (
            'let nextQ=Math.min(100,Math.max(25,q<18?32:q+14));',
            'let nextQ=Math.min(100,q<10?28:q+18);'
        ),
        # 9. Messages array on click:
        (
            'let msgs=["Đang m\\xe0i nước ("+nextQ+"%): Lớp sơn trong mờ dần, c\\xe1c mảng vỏ trứng v\\xe0 bụi v\\xe0ng quỳ bắt đầu \\xe1nh l\\xean.","Đang m\\xe0i nước ("+nextQ+"%): Bề mặt phẳng mịn, c\\xe1c đường n\\xe9t hoa văn v\\xe0 sắc nền hiện r\\xf5 độ s\\xe2u.","Nước m\\xe0i ho\\xe0n thiện ("+nextQ+"%): Bề mặt đ\\xe3 lộ đều c\\xe1c lớp họa tiết v\\xe0 sắc nền, sẵn s\\xe0ng đ\\xe1nh b\\xf3ng."];',
            'let msgs=["Đang m\\xe0i nước ("+nextQ+"%): M\\xe0i mỏng lớp sơn đen, c\\xe1c mảng vỏ trứng v\\xe0 bụi v\\xe0ng quỳ bắt đầu \\xe1nh l\\xean từ nền đen.","Đang m\\xe0i nước ("+nextQ+"%): Bề mặt phẳng mịn, c\\xe1c đường n\\xe9t hoa văn v\\xe0 sắc đỏ son ph\\xe1t lộ r\\xf5 rệt.","Nước m\\xe0i ho\\xe0n thiện ("+nextQ+"%): Lớp sơn đen đ\\xe3 được m\\xe0i lộ đều, họa tiết hiện r\\xf5 sắc n\\xe9t, sẵn s\\xe0ng đ\\xe1nh b\\xf3ng."];'
        ),
        # 10. Description paragraph below button:
        (
            'children:"D\\xf9ng nước kết hợp giấy r\\xe1p/than củi m\\xe0i phẳng bề mặt. Mỗi lượt m\\xe0i l\\xe0m mỏng lớp sơn phủ, gi\\xfap họa tiết v\\xe0 sắc nền b\\xean dưới dần hiện r\\xf5 với chiều s\\xe2u sơn m\\xe0i."',
            'children:"D\\xf9ng nước kết hợp giấy r\\xe1p m\\xe0i mỏng dần lớp sơn đen (sơn then) đ\\xe3 ủ kh\\xf4. Mỗi lượt m\\xe0i l\\xe0m mỏng lớp sơn đen, gi\\xfap c\\xe1c mảng vỏ trứng, v\\xe0ng quỳ v\\xe0 họa tiết ẩn b\\xean dưới ph\\xe1t lộ với chiều s\\xe2u độc bản."'
        ),
        # 11. Section 3: Polish step subtitle (showing clear amber coat & high gloss):
        (
            'children:"B\\xf3ng"===ei?"Đ\\xe3 đ\\xe1nh b\\xf3ng s\\xe1ng gương":"L\\xe0m mịn & s\\xe1ng b\\xf3ng bề mặt"',
            'children:"B\\xf3ng"===ei?"Đ\\xe3 phủ sơn trong & đ\\xe1nh b\\xf3ng s\\xe1ng gương":"Lớp phủ trong (sơn c\\xe1nh gi\\xe1n) & đ\\xe1nh b\\xf3ng s\\xe1ng gương"'
        ),
        (
            'B("Đ\\xe3 đ\\xe1nh b\\xf3ng bề mặt; \\xe1nh phản xạ được l\\xe0m mịn v\\xe0 s\\xe1ng gương.")',
            'B("Đ\\xe3 phủ lớp sơn trong v\\xe0 đ\\xe1nh b\\xf3ng ho\\xe0n thiện; \\xe1nh phản xạ s\\xe1ng b\\xf3ng như gương.")'
        )
    ]

    count = 0
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            print(f"Patched: {old[:45]}... -> {new[:45]}...")
            count += 1
        else:
            print(f"Skipped (not found): {old[:45]}...")

    print(f"Total replacements in {filepath}: {count}")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    res = subprocess.run(["node", "-c", filepath], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Node syntax error in {filepath}:\n{res.stderr}")
        return False
    else:
        print(f"Node syntax OK for {filepath}")
        return True

if __name__ == "__main__":
    ok = True
    for f in FILES:
        if not patch_file(f):
            ok = False
    print("\nResult:", "SUCCESS" if ok else "FAILED")
