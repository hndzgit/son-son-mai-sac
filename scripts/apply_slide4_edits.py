import os
import re

# New data definitions
NEW_MATERIALS = [
    {
        "name": "Sơn then",
        "description": "Sơn then mang sắc đen sâu, thường được sử dụng để tạo nền, tạo tương phản và làm nổi bật những lớp màu, hình ảnh hay vật liệu khác trên bề mặt."
    },
    {
        "name": "Sơn son",
        "old_name": "Sơn / màu",
        "description": "Sắc son mang gam đỏ ấm và sâu, là một trong những màu sắc quen thuộc của sơn mài truyền thống, góp phần tạo nên vẻ rực rỡ và giàu sức biểu cảm."
    },
    {
        "name": "Vỏ trứng",
        "description": "Vỏ trứng được ghép thành từng mảnh trên bề mặt, tạo nên sắc trắng cùng những đường nứt tự nhiên, mang lại hiệu ứng thị giác rất riêng cho tác phẩm."
    },
    {
        "name": "Vàng",
        "description": "Vàng được thếp hoặc sử dụng trong trang trí để tạo những điểm sáng ấm, bắt ánh sáng và làm tăng chiều sâu thị giác cho bề mặt sơn mài."
    },
    {
        "name": "Bạc",
        "description": "Bạc tạo hiệu ứng ánh kim lạnh. Khi nằm dưới hoặc kết hợp với các lớp sơn, sắc bạc có thể biến đổi, tạo nên những hiệu ứng màu sắc và chiều sâu khác nhau."
    },
    {
        "name": "Xà cừ",
        "description": "Vỏ trai, vỏ ốc được xử lý và khảm lên bề mặt, tạo hiệu ứng óng ánh với nhiều sắc độ thay đổi theo ánh sáng và góc nhìn."
    }
]

P1_TEXT = "Vẻ đẹp của sơn mài được tạo nên từ sự kết hợp giữa sơn, màu và nhiều chất liệu trang trí đặc trưng. Mỗi yếu tố mang một sắc độ, hiệu ứng và cảm giác bề mặt riêng."
P2_TEXT = "Từ đen then, đỏ son đến ánh sáng của vàng, bạc, những đường nứt của vỏ trứng hay sắc óng của xà cừ, tất cả cùng góp phần tạo nên chiều sâu và vẻ đẹp khó trộn lẫn của sơn mài."

# 1. Update JS files
JS_FILES = [
    "/Users/hoainam/Documents/Sơn son mài sắc/_next/static/chunks/369-2063549c42145b16.js",
    "/Users/hoainam/Documents/Sơn son mài sắc/ma_nguon_css_js/js/369-2063549c42145b16.js",
    "/Users/hoainam/Documents/Sơn son mài sắc/kiem_tra_2026-10-12/ban_chup_goc/_next/static/chunks/369-2063549c42145b16.js"
]

old_d = 'let d=[{name:"Sơn then",description:"Nền sơn đen tạo chiều sâu, làm nổi màu và ánh kim của những vật liệu đặt trên bề mặt.",sample:"/story-assets/materials-macro-atlas-v1.webp",tile:0},{name:"Sơn / màu",description:"Màu được phối cùng sơn để xây dựng sắc độ, từ những mảng nền đến nét vẽ và chi tiết.",sample:"/story-assets/materials-macro-atlas-v1.webp",tile:1},{name:"Vỏ trứng",description:"Mảnh vỏ trứng tạo vùng sáng, đường rạn và một kết cấu rất riêng trên nền sơn.",sample:"/story-assets/materials-macro-atlas-v1.webp",tile:2},{name:"Vàng",description:"Vàng thếp tạo điểm sáng ấm; ánh kim biến đổi theo ánh sáng và góc nhìn.",sample:"/story-assets/materials-macro-atlas-v1.webp",tile:3},{name:"Bạc",description:"Bạc thếp mở ra những vùng ánh kim lạnh, cân bằng sắc son và nền tối.",sample:"/story-assets/materials-macro-atlas-v1.webp",tile:4},{name:"Xà cừ",description:"Vỏ trai, ốc mang ánh sắc óng, từ trắng ngà đến xanh và hồng khi đổi góc nhìn.",sample:"/story-assets/materials-macro-atlas-v1.webp",tile:5}];'

new_d = (
    'let d=['
    + '{name:"Sơn then",description:"Sơn then mang sắc đen sâu, thường được sử dụng để tạo nền, tạo tương phản và làm nổi bật những lớp màu, hình ảnh hay vật liệu khác trên bề mặt.",sample:"/story-assets/materials-macro-atlas-v1.webp",tile:0},'
    + '{name:"Sơn son",description:"Sắc son mang gam đỏ ấm và sâu, là một trong những màu sắc quen thuộc của sơn mài truyền thống, góp phần tạo nên vẻ rực rỡ và giàu sức biểu cảm.",sample:"/story-assets/materials-macro-atlas-v1.webp",tile:1},'
    + '{name:"Vỏ trứng",description:"Vỏ trứng được ghép thành từng mảnh trên bề mặt, tạo nên sắc trắng cùng những đường nứt tự nhiên, mang lại hiệu ứng thị giác rất riêng cho tác phẩm.",sample:"/story-assets/materials-macro-atlas-v1.webp",tile:2},'
    + '{name:"Vàng",description:"Vàng được thếp hoặc sử dụng trong trang trí để tạo những điểm sáng ấm, bắt ánh sáng và làm tăng chiều sâu thị giác cho bề mặt sơn mài.",sample:"/story-assets/materials-macro-atlas-v1.webp",tile:3},'
    + '{name:"Bạc",description:"Bạc tạo hiệu ứng ánh kim lạnh. Khi nằm dưới hoặc kết hợp với các lớp sơn, sắc bạc có thể biến đổi, tạo nên những hiệu ứng màu sắc và chiều sâu khác nhau.",sample:"/story-assets/materials-macro-atlas-v1.webp",tile:4},'
    + '{name:"Xà cừ",description:"Vỏ trai, vỏ ốc được xử lý và khảm lên bề mặt, tạo hiệu ứng óng ánh với nhiều sắc độ thay đổi theo ánh sáng và góc nhìn.",sample:"/story-assets/materials-macro-atlas-v1.webp",tile:5}'
    + '];'
)

old_header_js = '(0,r.jsxs)("header",{className:s().layersLead,"data-reveal":!0,children:[(0,r.jsx)("p",{className:s().kicker,children:"VẬT LIỆU · BÊN TRONG MỘT TÁC PHẨM"}),(0,r.jsxs)("h2",{id:"layers-title",children:["NHIỀU LỚP.",(0,r.jsx)("br",{}),"MỘT BỀ MẶT."]}),(0,r.jsx)("p",{children:"Điều ta nhìn thấy ở một tác phẩm hoàn thiện chỉ là bề mặt cuối cùng của cả một quá trình."}),(0,r.jsx)("p",{className:s().layerSequence,children:"Làm vóc → Cẩn & tạo hình → Phủ & ủ → Mài nước → Đánh bóng"}),(0,r.jsx)("p",{children:"Mỗi công đoạn để lại một lớp, một dấu vết hoặc một thay đổi trên bề mặt. Và để hiểu sơn mài, cách trực quan nhất là đi qua chính những lớp ấy."})]})'

new_header_js = (
    '(0,r.jsxs)("header",{className:s().layersLead,"data-reveal":!0,children:['
    + '(0,r.jsxs)("h2",{id:"layers-title",children:["NHỮNG ĐẶC TRƯNG",(0,r.jsx)("br",{}),"LÀM NÊN SƠN MÀI"]}),'
    + '(0,r.jsx)("p",{children:"' + P1_TEXT + '"}),'
    + '(0,r.jsx)("p",{children:"' + P2_TEXT + '"})'
    + ']})'
)

for js_path in JS_FILES:
    if os.path.exists(js_path):
        with open(js_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        if old_d in content:
            content = content.replace(old_d, new_d)
            print(f"Updated array d in {js_path}")
        else:
            print(f"WARNING: old_d not found in {js_path}")
            
        if old_header_js in content:
            content = content.replace(old_header_js, new_header_js)
            print(f"Updated header in {js_path}")
        else:
            print(f"WARNING: old_header_js not found in {js_path}")

        # Also update slide title if present
        content = content.replace('"data-slide-title":"Nhiều lớp, một bề mặt"', '"data-slide-title":"Những đặc trưng làm nên sơn mài"')

        with open(js_path, "w", encoding="utf-8") as f:
            f.write(content)

# 2. Update HTML files
HTML_FILES = [
    "/Users/hoainam/Documents/Sơn son mài sắc/index.html",
    "/Users/hoainam/Documents/Sơn son mài sắc/trai-nghiem/index.html",
    "/Users/hoainam/Documents/Sơn son mài sắc/kiem_tra_2026-10-12/ban_chup_goc/index.html",
    "/Users/hoainam/Documents/Sơn son mài sắc/kiem_tra_2026-10-12/ban_chup_goc/trai-nghiem/index.html"
]

old_html_header = '<header class="coreIntroduction_layersLead__acYPE" data-reveal="true"><p class="coreIntroduction_kicker__BC_x7">VẬT LIỆU · BÊN TRONG MỘT TÁC PHẨM</p><h2 id="layers-title">NHIỀU LỚP.<br/>MỘT BỀ MẶT.</h2><p>Điều ta nhìn thấy ở một tác phẩm hoàn thiện chỉ là bề mặt cuối cùng của cả một quá trình.</p><p class="coreIntroduction_layerSequence__Mizc0">Làm vóc → Cẩn &amp; tạo hình → Phủ &amp; ủ → Mài nước → Đánh bóng</p><p>Mỗi công đoạn để lại một lớp, một dấu vết hoặc một thay đổi trên bề mặt. Và để hiểu sơn mài, cách trực quan nhất là đi qua chính những lớp ấy.</p></header>'

new_html_header = f'<header class="coreIntroduction_layersLead__acYPE" data-reveal="true"><h2 id="layers-title">NHỮNG ĐẶC TRƯNG<br/>LÀM NÊN SƠN MÀI</h2><p>{P1_TEXT}</p><p>{P2_TEXT}</p></header>'

for html_path in HTML_FILES:
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read()

        if old_html_header in content:
            content = content.replace(old_html_header, new_html_header)
            print(f"Updated header in {html_path}")
        else:
            print(f"WARNING: old_html_header not found in {html_path}")

        # Update card contents in HTML
        # Card 1
        content = content.replace(
            '<strong>Sơn then</strong><span>Nền sơn đen tạo chiều sâu, làm nổi màu và ánh kim của những vật liệu đặt trên bề mặt.</span>',
            f'<strong>Sơn then</strong><span>{NEW_MATERIALS[0]["description"]}</span>'
        )
        # Card 2
        content = content.replace(
            'aria-label="Khám phá Sơn / màu"',
            'aria-label="Khám phá Sơn son"'
        )
        content = content.replace(
            '<strong>Sơn / màu</strong><span>Màu được phối cùng sơn để xây dựng sắc độ, từ những mảng nền đến nét vẽ và chi tiết.</span>',
            f'<strong>Sơn son</strong><span>{NEW_MATERIALS[1]["description"]}</span>'
        )
        # Card 3
        content = content.replace(
            '<strong>Vỏ trứng</strong><span>Mảnh vỏ trứng tạo vùng sáng, đường rạn và một kết cấu rất riêng trên nền sơn.</span>',
            f'<strong>Vỏ trứng</strong><span>{NEW_MATERIALS[2]["description"]}</span>'
        )
        # Card 4
        content = content.replace(
            '<strong>Vàng</strong><span>Vàng thếp tạo điểm sáng ấm; ánh kim biến đổi theo ánh sáng và góc nhìn.</span>',
            f'<strong>Vàng</strong><span>{NEW_MATERIALS[3]["description"]}</span>'
        )
        # Card 5
        content = content.replace(
            '<strong>Bạc</strong><span>Bạc thếp mở ra những vùng ánh kim lạnh, cân bằng sắc son và nền tối.</span>',
            f'<strong>Bạc</strong><span>{NEW_MATERIALS[4]["description"]}</span>'
        )
        # Card 6
        content = content.replace(
            '<strong>Xà cừ</strong><span>Vỏ trai, ốc mang ánh sắc óng, từ trắng ngà đến xanh và hồng khi đổi góc nhìn.</span>',
            f'<strong>Xà cừ</strong><span>{NEW_MATERIALS[5]["description"]}</span>'
        )

        content = content.replace('data-slide-title="Nhiều lớp, một bề mặt"', 'data-slide-title="Những đặc trưng làm nên sơn mài"')

        # Cache buster bump to ?v=4
        content = content.replace('3d939b8161363d36.css?v=3', '3d939b8161363d36.css?v=4')
        content = content.replace('369-2063549c42145b16.js?v=3', '369-2063549c42145b16.js?v=4')

        with open(html_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated HTML file: {html_path}")

print("Done updating Slide 4 content!")
