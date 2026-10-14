import os

js_files = [
    '_next/static/chunks/app/kham-pha/page-b0c7a974225638c7.js',
    'ma_nguon_css_js/js/app_kham-pha_page-b0c7a974225638c7.js'
]

start_marker = 'let N=[{title:"'
end_marker = 'function w(){'

new_n = (
    'let N=['
    '{title:"CHUẨN BỊ CỐT",short:"Tạo dáng và làm phẳng bề mặt cốt gỗ, xử lý kỹ để bảo đảm độ ổn định cho toàn bộ sản phẩm.",detail:"Cốt là phần vật liệu tạo hình và nâng đỡ tác phẩm. Gỗ, tre, gốm hay vật liệu khác cần cách chuẩn bị phù hợp; đây là chặng mở đầu, không phải lớp phủ bề mặt.",alt:"Khối cốt gỗ hình hộp trước khi hoàn thiện, ảnh minh họa"},'
    '{title:"LÀM VÓC",short:"Bó hom, phủ sơn lót và mài nhiều lớp để hình thành bề mặt nền mịn, chắc và đồng đều.",detail:"Cốt được hom, bồi các lớp sơn-vải phù hợp, ủ cho đạt trạng thái rồi mài phẳng. Các lượt xử lý có thể lặp lại; độ ẩm, vật liệu và yêu cầu của tác phẩm ảnh hưởng đến cách làm.",alt:"Cận cảnh cốt gỗ đang được xử lý, ảnh minh họa"},'
    '{title:"SƠN NỀN",short:"Phủ các lớp sơn nền nhằm tạo chiều sâu màu sắc và chuẩn bị nền bám tốt cho các công đoạn trang trí tiếp theo.",detail:"Sau khi làm vóc, người thợ phủ lớp sơn nền để tạo sắc độ nâng đỡ hình ảnh. Với sơn ta, lớp sơn được ủ trong môi trường phù hợp để đóng rắn; cách làm tiếp theo tùy vào chất liệu và yêu cầu của từng tác phẩm.",alt:"Mặt sơn mài đỏ đang được tạo lớp, ảnh minh họa"},'
    '{title:"TẠO HÌNH VÀ TRANG TRÍ",short:"Đặt màu, gắn chất liệu như vỏ trứng, vàng quỳ hoặc họa tiết thủ công để xây dựng bố cục thẩm mỹ.",detail:"Vỏ trứng, vỏ trai, vàng, bạc và sắc màu được đặt vào bố cục theo ý đồ. Các vật liệu có thể nằm dưới nhiều lớp sơn; người làm tiếp tục ủ, phủ và mài chỉnh theo từng tác phẩm.",alt:"Nghệ nhân đang thực hiện công đoạn trên tác phẩm sơn mài, ảnh minh họa"},'
    '{title:"PHỦ, MÀI VÀ HOÀN THIỆN",short:"Phủ lớp sơn cuối, mài nhẵn và đánh bóng để hoàn thiện bề mặt, làm nổi bật độ sâu và vẻ tinh xảo của tác phẩm.",detail:"Mài nước lấy đi có kiểm soát các lớp phía trên để sắc màu và vật liệu bên dưới hiện ra. Người làm có thể quay lại phủ và mài nhiều lượt; khi bố cục đạt yêu cầu mới đánh bóng hoàn thiện.",alt:"Cận cảnh bề mặt sơn mài đã hoàn thiện, ảnh minh họa"}'
    '];'
)

for js_p in js_files:
    if not os.path.exists(js_p):
        continue
    with open(js_p, 'r', encoding='utf-8') as f:
        c = f.read()
    idx1 = c.find(start_marker)
    if idx1 != -1:
        idx2 = c.find(end_marker, idx1)
        if idx2 != -1:
            old_block = c[idx1:idx2]
            print(f"Found block in {js_p}, length {len(old_block)}")
            new_c = c[:idx1] + new_n + c[idx2:]
            with open(js_p, 'w', encoding='utf-8') as f:
                f.write(new_c)
            print(f"Successfully updated array N in {js_p}")
        else:
            print(f"Could not find end marker in {js_p}")
    else:
        print(f"Could not find start marker in {js_p}")
