import streamlit as st
import unicodedata
import re

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Hinova - Tra cứu hệ số vùng NĐ293", page_icon="💰", layout="centered")

# --- THANH CÔNG CỤ BÊN TRÁI (SIDEBAR) ---
with st.sidebar:
    st.title("⚙️ Cài đặt")
    st.write("Tùy chỉnh giao diện:")
    
    # Nút chọn giao diện
    theme_choice = st.radio(
        "Chế độ hiển thị:",
        ("🌙 Tối (Neon Mode)", "☀️ Sáng (Light Mode)"),
        index=0 
    )
    
    st.divider()
    st.info("ℹ️ Dữ liệu được tham chiếu tại Nghị định 293/2025/NĐ-CP quy định mức lương tối thiểu đối với người lao động làm việc theo hợp đồng lao động  .")

# --- XỬ LÝ CSS  THEO GIAO DIỆN ---
if theme_choice == "🌙 Tối (Neon Mode)":
    # CSS DARK MODE (NEON)
    css_style = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700;900&display=swap');
    
    /* Nền tối */
    .stApp { background-color: #0E1117; color: white; }
    
    /* Tiêu đề Neon */
    .main-title {
        text-align: center;
        background: -webkit-linear-gradient(45deg, #00C6FF, #0072FF);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 3em; font-weight: 900; margin-top: 10px; text-transform: uppercase;
    }
    .sub-title { text-align: center; color: #b0bec5; margin-bottom: 30px; }
    
    /* Input Fields Dark */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] > div {
        background-color: #262730 !important; color: white !important; border: 1px solid #4A4A4A !important;
    }
    
    /* Nút bấm Neon */
    .stButton>button {
        width: 100%; border-radius: 12px; height: 3.5em;
        background: linear-gradient(90deg, #0072FF 0%, #00C6FF 100%);
        color: white; font-size: 1.2em; font-weight: bold; border: none;
        box-shadow: 0 0 15px rgba(0, 198, 255, 0.5); transition: all 0.3s ease;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 25px rgba(0, 198, 255, 0.8); }
    
    /* Kết quả Neon */
    .result-box {
        margin-top: 30px; padding: 30px; border-radius: 16px;
        background: rgba(255, 255, 255, 0.05); border: 1px solid #00C6FF;
        text-align: center; animation: slideUp 0.5s ease-out;
    }
    .result-value { font-size: 3.5em; color: #00E5FF; font-weight: 900; text-shadow: 0 0 20px rgba(0, 229, 255, 0.6); margin: 0; }
    .result-location { font-size: 1.1em; color: #eceff1; margin-bottom: 10px; }
    
    .warning-note { color: #FFD700; border-top: 1px dashed rgba(255, 215, 0, 0.5); font-style: italic; margin-top: 15px; padding-top: 15px;}
    .footer { color: #546e7a; background: rgba(14, 17, 23, 0.9); border-top: 1px solid #37474f; }
    </style>
    """
else:
    # CSS LIGHT MODE (FIX LỖI CHỮ TRẮNG)
    css_style = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700;900&display=swap');
    
    /* Nền Sáng */
    .stApp { background-color: #ffffff; color: #31333F; }
    
    /* Tiêu đề Xanh Dương */
    .main-title {
        text-align: center; color: #0d6efd;
        font-size: 3em; font-weight: 900; margin-top: 10px; text-transform: uppercase;
    }
    .sub-title { text-align: center; color: #6c757d; margin-bottom: 30px; font-weight: 500; }
    
    /* Ép màu chữ đen cho Label (Tên tỉnh, tên phường) */
    .stTextInput label, .stSelectbox label {
        color: #31333F !important;
        font-weight: bold;
    }
    
    /* Ép màu chữ đen cho ô nhập liệu và dropdown */
    .stTextInput input {
        color: #31333F !important;
        background-color: #f0f2f6 !important;
        border: 1px solid #ced4da;
    }
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #f0f2f6 !important;
        color: #31333F !important;
        border: 1px solid #ced4da;
    }
    /* Chữ bên trong dropdown khi đã chọn */
    .stSelectbox div[data-baseweb="select"] span {
        color: #31333F !important;
    }
    
    /* Nút bấm */
    .stButton>button {
        width: 100%; border-radius: 12px; height: 3.5em;
        background: linear-gradient(90deg, #0d6efd 0%, #0a58ca 100%);
        color: white; font-size: 1.2em; font-weight: bold; border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 6px 10px rgba(0,0,0,0.15); }
    
    /* Hộp kết quả Sáng */
    .result-box {
        margin-top: 30px; padding: 30px; border-radius: 16px;
        background: #f8f9fa; border: 2px solid #0d6efd;
        text-align: center; box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        animation: slideUp 0.5s ease-out;
    }
    .result-value { font-size: 3.5em; color: #198754; font-weight: 900; margin: 0; }
    .result-location { font-size: 1.1em; color: #212529; margin-bottom: 10px; }
    
    .warning-note { 
        margin-top: 15px; padding-top: 15px; border-top: 1px dashed #ffc107;
        color: #d63384; font-size: 0.9em; font-style: italic; font-weight: bold;
    }
    
    .footer { color: #adb5bd; background: #ffffff; border-top: 1px solid #dee2e6; }
    </style>
    """

# Inject CSS
st.markdown(css_style + """
    <style>
    @keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; padding: 10px; font-size: 0.8em; }
    </style>
""", unsafe_allow_html=True)


# --- DỮ LIỆU CHUẨN---
raw_data = """
1. Thành phố Hà Nội
- Vùng I, gồm các phường Hoàn
Kiếm, Cửa Nam, Ba Đình, Ngọc Hà, Giảng Võ, Hai Bà Trưng, Vĩnh Tuy, Bạch Mai, Đống
Đa, Kim Liên, Văn Miếu - Quốc Tử Giám, Láng, Ô Chợ Dừa, Hồng Hà, Lĩnh Nam,
Hoàng Mai, Vĩnh Hưng, Tương Mai, Định Công, Hoàng Liệt, Yên Sở, Thanh Xuân,
Khương Đình, Phương Liệt, Cầu Giấy, Nghĩa Đô, Yên Hoà, Tây Hồ, Phú Thượng, Tây
Tựu, Phú Diễn, Xuân Đỉnh, Đông Ngạc, Thượng Cát, Từ Liêm, Xuân Phương, Tây Mỗ,
Đại Mỗ, Long Biên, Bồ Đề, Việt Hưng, Phúc Lợi, Hà Đông, Dương Nội, Yên Nghĩa,
Phú Lương, Kiến Hưng, Thanh Liệt, Chương Mỹ, Sơn Tây, Tùng Thiện và các xã
Thanh Trì, Đại Thanh, Nam Phù, Ngọc Hồi, Thượng Phúc, Thường Tín, Chương Dương,
Hồng Vân, Phú Xuyên, Thanh Oai, Bình Minh, Tam Hưng, Dân Hòa, Phú Nghĩa, Xuân
Mai, Trần Phú, Hoà Phú, Quảng Bị, Yên Bài, Đoài Phương, Thạch Thất, Hạ Bằng,
Tây Phương, Hoà Lạc, Yên Xuân, Quốc Oai, Hưng Đạo, Kiều Phú, Phú Cát, Hoài Đức,
Dương Hoà, Sơn Đồng, An Khánh, Gia Lâm, Thuận An, Bát Tràng, Phù Đổng, Thư Lâm,
Đông Anh, Phúc Thịnh, Thiên Lộc, Vĩnh Thanh, Mê Linh, Yên Lãng, Tiến Thắng,
Quang Minh, Sóc Sơn, Đa Phúc, Nội Bài, Trung Giã, Kim Anh, Ô Diên, Liên Minh.
- Vùng II, gồm các xã, phường
còn lại.
2. Tỉnh Cao Bằng
- Vùng III, gồm các phường Thục
Phán, Nùng Trí Cao, Tân Giang.
- Vùng IV, gồm các xã, phường
còn lại.
3. Tỉnh Tuyên Quang
- Vùng III, gồm các phường Mỹ
Lâm, Minh Xuân, Nông Tiến, An Tường, Bình Thuận, Hà Giang 1, Hà Giang 2 và xã
Ngọc Đường.
- Vùng IV, gồm các xã, phường
còn lại.
4. Tỉnh Điện Biên
- Vùng III, gồm các phường Điện
Biên Phủ, Mường Thanh và xã Mường Phăng, Nà Tấu.
- Vùng IV, gồm các xã, phường
còn lại.
5. Tỉnh Lai Châu
- Vùng III, gồm các phường Tân
Phong, Đoàn Kết.
- Vùng IV, gồm các xã, phường
còn lại.
6. Tỉnh Sơn La
- Vùng III, gồm các phường Tô
Hiệu, Chiềng An, Chiềng Cơi, Chiềng Sinh.
- Vùng IV, gồm các xã, phường
còn lại.
7. Tỉnh Lào Cai
- Vùng II, gồm các phường Cam
Đường, Lào Cai và các xã Cốc San, Hợp Thành, Gia Phú.
- Vùng III, gồm các phường Văn
Phú, Yên Bái, Nam Cường, Âu Lâu, Sa Pa và các xã Phong Hải, Xuân Quang, Bảo Thắng,
Tằng Loỏng, Mường Bo, Bản Hồ, Tả Phìn, Tả Van, Ngũ Chỉ Sơn.
- Vùng IV, gồm các xã, phường
còn lại.
8. Tỉnh Thái Nguyên
- Vùng II, gồm các phường Phan
Đình Phùng, Linh Sơn, Tích Lương, Gia Sàng, Quyết Thắng, Quan Triều, Phổ Yên, Vạn
Xuân, Trung Thành, Phúc Thuận, Sông Công, Bá Xuyên, Bách Quang và các xã Tân
Cương, Đại Phúc, Thành Công.
- Vùng III, gồm các phường Đức
Xuân, Bắc Kạn và các xã Đại Từ, Đức Lương, Phú Thịnh, La Bằng, Phú Lạc, An
Khánh, Quân Chu, Vạn Phú, Phú Xuyên, Phú Bình, Tân Thành, Điềm Thụy, Kha Sơn,
Tân Khánh, Đồng Hỷ, Quang Sơn, Trại Cau, Nam Hòa, Văn Hán, Văn Lăng, Phú Lương,
Vô Tranh, Yên Trạch, Hợp Thành, Phong Quang.
- Vùng IV, gồm các xã, phường
còn lại.
9. Tỉnh Lạng Sơn
- Vùng III, gồm các phường Tam
Thanh, Lương Văn Tri, Kỳ Lừa, Đông Kinh.
- Vùng IV, gồm các xã, phường
còn lại.
10. Tỉnh Quảng Ninh
- Vùng I, gồm các phường An
Sinh, Đông Triều, Bình Khê, Mạo Khê, Hoàng Quế, Yên Tử, Vàng Danh, Uông Bí,
Đông Mai, Hiệp Hoà, Quảng Yên, Hà An, Phong Cốc, Liên Hoà, Tuần Châu, Việt
Hưng, Bãi Cháy, Hà Tu, Hà Lầm, Cao Xanh, Hồng Gai, Hạ Long, Hoành Bồ, Móng Cái
1, Móng Cái 2, Móng Cái 3 và các xã Quảng La, Thống Nhất, Hải Sơn, Hải Ninh,
Vĩnh Thực.
- Vùng II, gồm các phường Mông
Dương, Quang Hanh, Cẩm Phả, Cửa Ông và xã Hải Hòa.
- Vùng III, gồm các xã Tiên
Yên, Điền Xá, Đông Ngũ, Hải Lạng, Quảng Tân, Đầm Hà, Quảng Hà, Đường Hoa, Quảng
Đức, Cái Chiên và đặc khu Vân Đồn.
- Vùng IV, gồm các xã, phường
và đặc khu còn lại.
11. Tỉnh Bắc Ninh
- Vùng II, gồm các phường Kinh
Bắc, Võ Cường, Vũ Ninh, Hạp Lĩnh, Nam Sơn, Từ Sơn, Tam Sơn, Đồng Nguyên, Phù
Khê, Thuận Thành, Mão Điền, Trạm Lộ, Trí Quả, Song Liễu, Ninh Xá, Quế Võ,
Phương Liễu, Nhân Hoà, Đào Viên, Bồng Lai, Tự Lan, Việt Yên, Nếnh, Vân Hà, Bắc
Giang, Đa Mai, Tiền Phong, Tân An, Yên Dũng, Tân Tiến, Cảnh Thuỵ và các xã Chi
Lăng, Phù Lãng, Yên Phong, Văn Môn, Tam Giang, Yên Trung, Tam Đa, Tiên Du, Liên
Bão, Tân Chi, Đại Đồng, Phật Tích, Gia Bình, Nhân Thắng, Đại Lai, Cao Đức, Đông
Cứu, Lương Tài, Lâm Thao, Trung Chính, Trung Kênh, Đồng Việt.
- Vùng III, gồm các xã Lạng
Giang, Mỹ Thái, Kép, Tân Dĩnh, Tiên Lục, Tân Yên, Ngọc Thiện, Nhã Nam, Phúc
Hòa, Quang Trung, Hợp Thịnh, Hiệp Hòa, Hoàng Vân, Xuân Cẩm.
- Vùng IV, gồm các xã, phường
còn lại.
12. Tỉnh Phú Thọ
- Vùng II, gồm các phường Việt
Trì, Nông Trang, Thanh Miếu, Vân Phú, Vĩnh Phúc, Vĩnh Yên, Phúc Yên, Xuân Hòa,
Hòa Bình, Kỳ Sơn, Tân Hòa, Thống Nhất và các xã Hy Cương, Yên Lạc, Tề Lỗ, Liên
Châu, Tam Hồng, Nguyệt Đức, Bình Nguyên, Xuân Lãng, Bình Xuyên, Bình Tuyền,
Lương Sơn, Cao Dương, Liên Sơn, Thịnh Minh.
- Vùng III, gồm các phường
Phong Châu, Phú Thọ, Âu Cơ và các xã Lâm Thao, Xuân Lũng, Phùng Nguyên, Bản
Nguyên, Phù Ninh, Dân Chủ, Phú Mỹ, Trạm Thản, Bình Phú, Thanh Ba, Quảng Yên,
Hoàng Cương, Đông Thành, Chí Tiên, Liên Minh, Tam Nông, Thọ Văn, Vạn Xuân, Hiền
Quan, Tam Sơn, Sông Lô, Hải Lựu, Yên Lãng, Lập Thạch, Tiên Lữ, Thái Hòa, Liên
Hòa, Hợp Lý, Sơn Đông, Tam Đảo, Đại Đình, Đạo Trù, Tam Dương, Hội Thịnh, Hoàng
An, Tam Dương Bắc, Vĩnh Tường, Thổ Tang, Vĩnh Hưng, Vĩnh An, Vĩnh Phú, Vĩnh
Thành.
- Vùng IV, gồm các xã, phường
còn lại.
13. Thành phố Hải Phòng
- Vùng I, gồm các phường Thuỷ
Nguyên, Thiên Hương, Hoà Bình, Nam Triệu, Bạch Đằng, Lưu Kiếm, Lê Ích Mộc, Hồng
Bàng, Hồng An, Ngô Quyền, Gia Viên, Lê Chân, An Biên, Hải An, Đông Hải, Kiến
An, Phù Liễn, Nam Đồ Sơn, Đồ Sơn, Hưng Đạo, Dương Kinh, An Dương, An Hải, An
Phong, Hải Dương, Lê Thanh Nghị, Việt Hoà, Thành Đông, Nam Đồng, Tân Hưng, Thạch
Khôi, Tứ Minh, Ái Quốc, Chu Văn An, Chí Linh, Trần Hưng Đạo, Nguyễn Trãi, Trần
Nhân Tông, Lê Đại Hành, Kinh Môn, Nguyễn Đại Năng, Trần Liễu, Bắc An Phụ, Phạm
Sư Mạnh, Nhị Chiểu; các xã An Hưng, An Khánh, An Quang, An Trường, An Lão, Kiến
Thuỵ, Kiến Minh, Kiến Hải, Kiến Hưng, Nghi Dương, Quyết Thắng, Tiên Lãng, Tân
Minh, Tiên Minh, Chấn Hưng, Hùng Thắng, Vĩnh Bảo, Nguyễn Bỉnh Khiêm, Vĩnh Am,
Vĩnh Hải, Vĩnh Hoà, Vĩnh Thuận, Vĩnh Thịnh, Việt Khê, Nam An Phụ, Nam Sách,
Thái Tân, Hợp Tiến, Trần Phú, An Phú, Cẩm Giang, Cẩm Giàng, Tuệ Tĩnh, Mao Điền,
Kẻ Sặt, Bình Giang, Đường An, Thượng Hồng, Gia Lộc, Yết Kiêu, Gia Phúc, Trường
Tân, Tứ Kỳ, Tân Kỳ, Đại Sơn, Chí Minh, Lạc Phượng, Nguyên Giáp, Nguyễn Lương Bằng,
Phú Thái, Lai Khê, An Thành, Kim Thành và đặc khu Cát Hải.
- Vùng II, gồm các xã Thanh Hà,
Hà Tây, Hà Bắc, Hà Nam, Hà Đông, Ninh Giang, Vĩnh Lại, Khúc Thừa Dụ, Tân An, Hồng
Châu, Thanh Miện, Bắc Thanh Miện, Nam Thanh Miện, Hải Hưng và đặc khu Bạch Long
Vĩ.
- Vùng III, gồm các xã, phường
còn lại.
14. Tỉnh Hưng Yên
- Vùng II, gồm các phường Phố
Hiến, Sơn Nam, Hồng Châu, Mỹ Hào, Đường Hào, Thượng Hồng, Thái Bình, Trần Lãm,
Trần Hưng Đạo, Trà Lý, Vũ Phúc và các xã Tân Hưng, Yên Mỹ, Việt Yên, Hoàn Long,
Nguyễn Văn Linh, Như Quỳnh, Lạc Đạo, Đại Đồng, Nghĩa Trụ, Phụng Công, Văn
Giang, Mễ Sở.
- Vùng III, gồm các xã Hoàng
Hoa Thám, Tiên Lữ, Tiên Hoa, Quang Hưng, Đoàn Đào, Tiên Tiến, Tống Trân, Lương
Bằng, Nghĩa Dân, Hiệp Cường, Đức Hợp, Ân Thi, Xuân Trúc, Phạm Ngũ Lão, Nguyễn
Trãi, Hồng Quang, Khoái Châu, Triệu Việt Vương, Việt Tiến, Chí Minh, Châu Ninh,
Thái Thụy, Đông Thụy Anh, Bắc Thụy Anh, Thụy Anh, Nam Thụy Anh, Bắc Thái Ninh,
Thái Ninh, Đông Thái Ninh, Nam Thái Ninh, Tây Thái Ninh, Tây Thụy Anh, Tiền Hải,
Tây Tiền Hải, Ái Quốc, Đồng Châu, Đông Tiền Hải, Nam Cường, Hưng Phú, Nam Tiền
Hải.
- Vùng IV, gồm các xã, phường
còn lại.
15. Tỉnh Ninh Bình
- Vùng II, gồm các phường Tây
Hoa Lư, Hoa Lư, Nam Hoa Lư, Đông Hoa Lư, Nam Định, Thiên Trường, Đông A, Vị
Khê, Thành Nam, Trường Thi, Hồng Quang, Mỹ Lộc.
- Vùng III, gồm các phường Tam
Điệp, Yên Sơn, Trung Sơn, Yên Thắng, Hà Nam, Phủ Lý, Phù Vân, Châu Sơn, Liêm
Tuyền, Duy Tiên, Duy Tân, Đồng Văn, Duy Hà, Tiên Sơn, Lê Hồ, Nguyễn Úy, Lý Thường
Kiệt, Kim Thanh, Tam Chúc, Kim Bảng và các xã Gia Viễn, Đại Hoàng, Gia Hưng,
Gia Phong, Gia Vân, Gia Trấn, Yên Khánh, Khánh Nhạc, Khánh Thiện, Khánh Hội,
Khánh Trung, Nam Trực, Nam Minh, Nam Đồng, Nam Ninh, Nam Hồng, Minh Tân, Hiển
Khánh, Vụ Bản, Liên Minh, Ý Yên, Yên Đồng, Yên Cường, Vạn Thắng, Vũ Dương, Tân
Minh, Phong Doanh, Cổ Lễ, Ninh Giang, Cát Thành, Trực Ninh, Quang Hưng, Minh Thái,
Ninh Cường, Xuân Trường, Xuân Hưng, Xuân Giang, Xuân Hồng, Hải Hậu, Hải Anh, Hải
Tiến, Hải Hưng, Hải An, Hải Quang, Hải Xuân, Hải Thịnh, Giao Minh, Giao Hòa,
Giao Thủy, Giao Phúc, Giao Hưng, Giao Bình, Giao Ninh, Đồng Thịnh, Nghĩa Hưng,
Nghĩa Sơn, Hồng Phong, Quỹ Nhất, Nghĩa Lâm, Rạng Đông.
- Vùng IV, gồm các xã, phường
còn lại.
16. Tỉnh Thanh Hóa
- Vùng II, gồm các phường Hạc
Thành, Quảng Phú, Đông Quang, Đông Sơn, Đông Tiến, Hàm Rồng, Nguyệt Viên, Sầm
Sơn, Nam Sầm Sơn, Bỉm Sơn, Quang Trung, Ngọc Sơn, Tân Dân, Hải Lĩnh, Tĩnh Gia,
Đào Duy Từ, Hải Bình, Trúc Lâm, Nghi Sơn và các xã Trường Lâm, Các Sơn.
- Vùng III, gồm các xã Hà
Trung, Tống Sơn, Hà Long, Hoạt Giang, Lĩnh Toại, Triệu Lộc, Đông Thành, Hậu Lộc,
Hoa Lộc, Vạn Lộc, Nga Sơn, Nga Thắng, Hồ Vương, Tân Tiến, Nga An, Ba Đình, Hoằng
Hóa, Hoằng Tiến, Hoằng Thanh, Hoằng Lộc, Hoằng Châu, Hoằng Sơn, Hoằng Phú, Hoằng
Giang, Lưu Vệ, Quảng Yên, Quảng Ngọc, Quảng Ninh, Quảng Bình, Tiên Trang, Quảng
Chính, Nông Cống, Thắng Lợi, Trung Chính, Trường Văn, Thăng Bình, Tượng Lĩnh,
Công Chính, Thiệu Hóa, Thiệu Quang, Thiệu Tiến, Thiệu Toán, Thiệu Trung, Yên Định,
Yên Trường, Yên Phú, Quý Lộc, Yên Ninh, Định Tân, Định Hòa, Thọ Xuân, Thọ Long,
Xuân Hòa, Sao Vàng, Lam Sơn, Thọ Lập, Xuân Tín, Xuân Lập, Vĩnh Lộc, Tây Đô, Biện
Thượng, Triệu Sơn, Thọ Bình, Thọ Ngọc, Thọ Phú, Hợp Tiến, An Nông, Tân Ninh, Đồng
Tiến.
- Vùng IV, gồm các xã, phường
còn lại.
17. Tỉnh Nghệ An
- Vùng II, gồm các phường Hoàng
Mai, Tân Mai, Trường Vinh, Thành Vinh, Vinh Hưng, Vinh Phú, Vinh Lộc, Cửa Lò và
các xã Hưng Nguyên, Yên Trung, Hưng Nguyên Nam, Lam Thành, Nghi Lộc, Phúc Lộc,
Đông Lộc, Trung Lộc, Thần Lĩnh, Hải Lộc, Văn Kiều.
- Vùng III, gồm các phường Quỳnh
Mai, Thái Hòa, Tây Hiếu và các xã Diễn Châu, Đức Châu, Quảng Châu, Hải Châu,
Tân Châu, An Châu, Minh Châu, Hùng Châu, Đô Lương, Bạch Ngọc, Văn Hiến, Bạch
Hà, Thuần Trung, Lương Sơn, Vạn An, Nam Đàn, Đại Huệ, Thiên Nhẫn, Kim Liên,
Nghĩa Đàn, Nghĩa Thọ, Nghĩa Lâm, Nghĩa Mai, Nghĩa Hưng, Nghĩa Khánh, Nghĩa Lộc,
Quỳnh Lưu, Quỳnh Văn, Quỳnh Anh, Quỳnh Tam, Quỳnh Phú, Quỳnh Sơn, Quỳnh Thắng,
Đông Hiếu, Yên Thành, Quan Thành, Hợp Minh, Vân Tụ, Vân Du, Quang Đồng, Giai Lạc,
Bình Minh, Đông Thành.
- Vùng IV, gồm các xã, phường
còn lại.
18. Tỉnh Hà Tĩnh
- Vùng III, gồm các phường Sông
Trí, Hải Ninh, Hoành Sơn, Vũng Áng, Thành Sen, Trần Phú, Hà Huy Tập và các xã
Thạch Lạc, Đồng Tiến, Thạch Khê, Cẩm Bình, Kỳ Hoa.
- Vùng IV, gồm các xã, phường
còn lại.
19. Tỉnh Quảng Trị
- Vùng II, gồm các phường Đồng
Hới, Đồng Thuận, Đồng Sơn, Đông Hà, Nam Đông Hà.
- Vùng III, gồm các phường Quảng
Trị, Ba Đồn, Bắc Gianh và các xã Nam Gianh, Nam Ba Đồn, Tân Gianh, Trung Thuần,
Quảng Trạch, Hòa Trạch, Phú Trạch, Phong Nha, Bắc Trạch, Đông Trạch, Hoàn Lão,
Bố Trạch, Nam Trạch, Quảng Ninh, Ninh Châu, Trường Ninh, Lệ Thủy, Cam Hồng, Sen
Ngư, Tân Mỹ, Trường Phú, Lệ Ninh, Đồng Lê, Vĩnh Linh, Cửa Tùng, Bến Quan, Cửa
Việt, Gio Linh, Cam Lộ, Khe Sanh, Lao Bảo, Triệu Phong, Hướng Hiệp, Diên Sanh.
- Vùng IV, gồm các xã, phường
và đặc khu còn lại.
20. Thành phố Huế
- Vùng II, gồm các phường Thuận
An, Hóa Châu, Mỹ Thượng, Vỹ Dạ, Thuận Hóa, An Cựu, Thủy Xuân, Kim Long, Hương
An, Phú Xuân, Dương Nỗ.
- Vùng III, gồm các phường
Phong Điền, Phong Thái, Phong Dinh, Phong Phú, Phong Quảng, Hương Trà, Kim Trà,
Hương Thuỷ, Phú Bài, Thanh Thủy và các xã Đan Điền, Quảng Điền, Bình Điền, Phú
Vinh, Phú Hồ, Phú Vang, Vinh Lộc, Hưng Lộc, Lộc An, Phú Lộc, Chân Mây - Lăng
Cô, Long Quảng, Nam Đông, Khe Tre.
- Vùng IV, gồm các xã, phường
còn lại.
21. Thành phố Đà Nẵng
- Vùng II, gồm các phường Hải
Châu, Hòa Cường, Thanh Khê, An Khê, An Hải, Sơn Trà, Ngũ Hành Sơn, Hòa Khánh, Hải
Vân, Liên Chiểu, Cẩm Lệ, Hòa Xuân, Tam Kỳ, Quảng Phú, Hương Trà, Bàn Thạch, Hội
An, Hội An Đông, Hội An Tây và các xã Hòa Vang, Hòa Tiến, Bà Nà, Tân Hiệp và đặc
khu Hoàng Sa.
- Vùng III, gồm các phường Điện
Bàn, Điện Bàn Đông, An Thắng, Điện Bàn Bắc và các xã Núi Thành, Tam Mỹ, Tam
Anh, Đức Phú, Tam Xuân, Tam Hải, Tây Hồ, Chiên Đàn, Phú Ninh, Thăng Bình, Thăng
An, Thăng Trường, Thăng Điền, Thăng Phú, Đồng Dương, Quế Sơn Trung, Quế Sơn,
Xuân Phú, Nông Sơn, Quế Phước, Duy Nghĩa, Nam Phước, Duy Xuyên, Thu Bồn, Điện
Bàn Tây, Gò Nổi, Đại Lộc, Hà Nha, Thượng Đức, Vu Gia, Phú Thuận.
- Vùng IV, gồm các xã, phường
còn lại.
22. Tỉnh Quảng Ngãi
- Vùng III, gồm các phường
Trương Quang Trọng, Cẩm Thành, Nghĩa Lộ, Kon Tum, Đăk Cấm, Đăk Bla và các xã Tịnh
Khê, An Phú, Bình Minh, Bình Chương, Bình Sơn, Vạn Tường, Đông Sơn, Trường
Giang, Ba Gia, Sơn Tịnh, Thọ Phong, Ngọk Bay, Ia Chim, Đăk Rơ Wa, Đăk Pxi, Đăk
Mar, Đăk Ui, Đăk Hà, Ngọk Réo.
- Vùng IV, gồm các xã, phường
và đặc khu còn lại.
23. Tỉnh Gia Lai
- Vùng III, gồm các phường Quy
Nhơn, Quy Nhơn Đông, Quy Nhơn Tây, Quy Nhơn Nam, Quy Nhơn Bắc, Pleiku, Hội Phú,
Thống Nhất, Diên Hồng, An Phú và các xã Biển Hồ, Gào.
- Vùng IV, gồm các xã, phường
còn lại.
24. Tỉnh Khánh Hòa
- Vùng II, gồm các phường Nha
Trang, Bắc Nha Trang, Tây Nha Trang, Nam Nha Trang, Bắc Cam Ranh, Cam Ranh, Cam
Linh, Ba Ngòi, Ninh Hòa, Đông Ninh Hòa, Hòa Thắng, Phan Rang, Đông Hải, Ninh Chử,
Bảo An, Đô Vinh và các xã Nam Cam Ranh, Bắc Ninh Hòa, Tân Định, Nam Ninh Hòa,
Tây Ninh Hòa, Hòa Trí, Thuận Bắc, Công Hải.
- Vùng III, gồm các xã Đại
Lãnh, Tu Bông, Vạn Thắng, Vạn Ninh, Vạn Hưng, Diên Khánh, Diên Lạc, Diên Điền,
Suối Hiệp, Diên Thọ, Diên Lâm, Cam Lâm, Suối Dầu, Cam Hiệp, Cam An, Ninh Phước,
Phước Hữu, Phước Hậu, Phước Dinh, Ninh Hải, Xuân Hải, Vĩnh Hải, Ninh Sơn, Lâm
Sơn, Anh Dũng, Mỹ Sơn, Thuận Nam, Cà Ná, Phước Hà.
- Vùng IV, gồm các xã, phường
và đặc khu còn lại.
25. Tỉnh Đắk Lắk
- Vùng III, gồm các phường Buôn
Ma Thuột, Tân An, Tân Lập, Xuân Đài, Sông Cầu, Thành Nhất, Ea Kao, Tuy Hòa, Phú
Yên, Bình Kiến, Đông Hòa, Hòa Hiệp và các xã Hòa Phú, Xuân Thọ, Xuân Cảnh, Xuân
Lộc, Hòa Xuân.
- Vùng IV, gồm các xã, phường
còn lại.
26. Tỉnh Lâm Đồng
- Vùng II, gồm các phường Xuân
Hương - Đà Lạt, Cam Ly - Đà Lạt, Lâm Viên - Đà Lạt, Xuân Trường - Đà Lạt, Lang
Biang - Đà Lạt, 1 Bảo Lộc, 2 Bảo Lộc, 3 Bảo Lộc, B' Lao, Hàm Thắng, Bình Thuận,
Mũi Né, Phú Thủy, Phan Thiết, Tiến Thành và xã Tuyên Quang.
- Vùng III, gồm các phường La
Gi, Phước Hội, Bắc Gia Nghĩa, Nam Gia Nghĩa, Đông Gia Nghĩa và các xã Hiệp Thạnh,
Đức Trọng, Tân Hội, Tà Hine, Tà Năng, Đinh Văn Lâm Hà, Di Linh, Hòa Ninh, Hòa Bắc,
Đinh Trang Thượng, Bảo Thuận, Sơn Điền, Gia Hiệp, Tân Hải, Đông Giang, La Dạ,
Hàm Thuận Bắc, Hàm Thuận, Hồng Sơn, Hàm Liêm, Hàm Thạnh, Hàm Kiệm, Tân Thành,
Hàm Thuận Nam, Tân Lập, Ninh Gia.
- Vùng IV, gồm các xã, phường
và đặc khu còn lại.
27. Tỉnh Đồng Nai
- Vùng I, gồm các phường Biên
Hòa, Trấn Biên, Tam Hiệp, Long Bình, Trảng Dài, Hố Nai, Long Hưng, Bình Lộc, Bảo
Vinh, Xuân Lập, Long Khánh, Hàng Gòn, Tân Triều, Phước Tân, Tam Phước và các xã
Đại Phước, Nhơn Trạch, Phước An, Phước Thái, Long Phước, Bình An, Long Thành,
An Phước, An Viễn, Bình Minh, Trảng Bom, Bàu Hàm, Hưng Thịnh, Dầu Giây, Gia Kiệm,
Thống Nhất, Xuân Đường, Xuân Đông, Xuân Định, Xuân Phú, Xuân Lộc, Xuân Hòa,
Xuân Thành, Xuân Bắc, Trị An, Tân An, Phú Lý.
- Vùng II, gồm các phường Minh
Hưng, Chơn Thành, Đồng Xoài, Bình Phước và các xã Xuân Quế, Cẩm Mỹ, Sông Ray,
La Ngà, Định Quán, Phú Vinh, Phú Hòa, Tà Lài, Nam Cát Tiên, Tân Phú, Phú Lâm,
Nha Bích, Tân Quan, Thuận Lợi, Đồng Tâm, Tân Lợi, Đồng Phú, Đak Lua, Thanh Sơn.
- Vùng III, gồm các phường Bình
Long, An Lộc, Phước Bình, Phước Long và các xã Tân Hưng, Tân Khai, Minh Đức, Lộc
Thành, Lộc Ninh, Lộc Hưng, Lộc Tấn, Lộc Thạnh, Lộc Quang, Tân Tiến, Bình Tân,
Long Hà, Phú Riềng, Phú Trung.
- Vùng IV, gồm các xã, phường
còn lại.
28. Thành phố Hồ Chí Minh
- Vùng I, gồm các phường Sài
Gòn, Tân Định, Bến Thành, Cầu Ông Lãnh, Bàn Cờ, Xuân Hoà, Nhiêu Lộc, Xóm Chiếu,
Khánh Hội, Vĩnh Hội, Chợ Quán, An Đông, Chợ Lớn, Bình Tây, Bình Phú, Bình Tiên,
Phú Lâm, Tân Thuận, Phú Thuận, Tân Mỹ, Tân Hưng, Chánh Hưng, Phú Định, Bình
Đông, Diên Hồng, Vườn Lài, Hoà Hưng, Minh Phụng, Bình Thới, Hoà Bình, Phú Thọ,
Đông Hưng Thuận, Trung Mỹ Tây, Tân Thới Hiệp, Thới An, An Phú Đông, An Lạc, Tân
Tạo, Bình Tân, Bình Trị Đông, Bình Hưng Hoà, Gia Định, Bình Thạnh, Bình Lợi
Trung, Thạnh Mỹ Tây, Bình Quới, Hạnh Thông, An Nhơn, Gò Vấp, An Hội Đông, Thông
Tây Hội, An Hội Tây, Đức Nhuận, Cầu Kiệu, Phú Nhuận, Tân Sơn Hoà, Tân Sơn Nhất,
Tân Hoà, Bảy Hiền, Tân Bình, Tân Sơn, Tân Thạnh, Tân Sơn Nhì, Phú Thọ Hoà, Tân
Phú, Phú Thạnh, Hiệp Bình, Thủ Đức, Tam Bình, Linh Xuân, Tăng Nhơn Phú, Long
Bình, Long Phước, Long Trường, Cát Lái, Bình Trưng, Phước Long, An Khánh, Đông
Hoà, Dĩ An, Tân Đông Hiệp, An Phú, Bình Hoà, Lái Thiêu, Thuận An, Thuận Giao,
Thủ Dầu Một, Phú Lợi, Chánh Hiệp, Bình Dương, Hoà Lợi, Thới Hoà, Phú An, Tây
Nam, Long Nguyên, Bến Cát, Chánh Phú Hoà, Vĩnh Tân, Bình Cơ, Tân Uyên, Tân Hiệp,
Tân Khánh, Vũng Tàu, Tam Thắng, Rạch Dừa, Phước Thắng, Tân Hải, Tân Phước, Phú
Mỹ, Tân Thành và các xã Vĩnh Lộc, Tân Vĩnh Lộc, Bình Lợi, Tân Nhựt Bình Chánh,
Hưng Long, Bình Hưng, Củ Chi, Tân An Hội, Thái Mỹ, An Nhơn Tây, Nhuận Đức, Phú
Hoà Đông, Bình Mỹ, Đông Thạnh, Hóc Môn, Xuân Thới Sơn, Bà Điểm, Nhà Bè, Hiệp
Phước, Thường Tân, Bắc Tân Uyên, Phú Giáo, Phước Hoà, Phước Thành, An Long, Trừ
Văn Thố, Bàu Bàng, Long Hoà, Thanh An, Dầu Tiếng, Minh Thạnh, Long Sơn, Châu
Pha.
- Vùng II, gồm các phường Bà Rịa,
Long Hương, Tam Long và các xã Bình Khánh, An Thới Đông, Cần Giờ, Thạnh An; các
xã Kim Long, Châu Đức, Ngãi Giao, Nghĩa Thành, Long Hải, Long Điền và đặc khu
Côn Đảo.
- Vùng III, gồm các xã, phường
và đặc khu còn lại.
29. Tỉnh Tây Ninh
- Vùng I, gồm các phường Long
An, Tân An, Khánh Hậu và các xã An Ninh, Hiệp Hòa, Hậu Nghĩa, Hòa Khánh, Đức Lập,
Mỹ Hạnh, Đức Hòa, Thạnh Lợi, Bình Đức, Lương Hòa, Bến Lức, Mỹ Yên, Phước Lý, Mỹ
Lộc, Cần Giuộc, Phước Vĩnh Tây, Tân Tập.
- Vùng II, gồm các phường Kiến
Tường, Tân Ninh, Bình Minh, Ninh Thạnh, Long Hoa, Hòa Thành, Thanh Điền, Trảng
Bàng, An Tịnh, Gò Dầu, Gia Lộc và các xã Tuyên Thạnh, Bình Hiệp, Thủ Thừa, Mỹ
An, Mỹ Thạnh, Tân Long, Long Cang, Rạch Kiến, Mỹ Lệ, Tân Lân, Cần Đước, Long Hựu,
Hưng Thuận, Phước Chỉ, Thạnh Đức, Phước Thạnh, Truông Mít, Nhựt Tảo.
- Vùng III, gồm các xã Bình
Thành, Thạnh Phước, Thạnh Hoá, Tân Tây, Mỹ Quý, Đông Thành, Đức Huệ, Vàm Cỏ,
Tân Trụ, Thuận Mỹ, An Lục Long, Tầm Vu, Vĩnh Công, Lộc Ninh, Cầu Khởi, Dương
Minh Châu, Tân Đông, Tân Châu, Tân Phú, Tân Hội, Tân Thành, Tân Hoà, Tân Lập,
Tân Biên, Thạnh Bình, Trà Vong, Phước Vinh, Hoà Hội, Ninh Điền, Châu Thành, Hảo
Đước, Long Chữ, Long Thuận, Bến Cầu.
- Vùng IV, gồm các xã, phường
còn lại.
30. Tỉnh Đồng Tháp
- Vùng II, gồm các phường Mỹ
Tho, Đạo Thạnh, Mỹ Phong, Thới Sơn, Trung An và các xã Tân Hương, Châu Thành,
Long Hưng, Long Định, Vĩnh Kim, Kim Sơn, Bình Trưng.
- Vùng III, gồm các phường Gò
Công, Long Thuận, Sơn Qui, Bình Xuân, Mỹ Phước Tây, Thanh Hòa, Cai Lậy, Nhị
Quý, An Bình, Hồng Ngự, Thường Lạc, Cao Lãnh, Mỹ Ngãi, Mỹ Trà, Sa Đéc và các xã
Tân Phú, Tân Phước 1, Tân Phước 2, Tân Phước 3, Hưng Thạnh, Mỹ Tịnh An, Lương
Hòa Lạc, Tân Thuận Bình, Chợ Gạo, An Thạnh Thủy, Bình Ninh, Tân Dương.
- Vùng IV, gồm các xã, phường
còn lại.
31. Tỉnh Vĩnh Long
- Vùng II, gồm các phường Thanh
Đức, Long Châu, Phước Hậu, Tân Hạnh, Tân Ngãi, Bình Minh, Cái Vồn, Đông Thành,
An Hội, Phú Khương, Bến Tre, Sơn Đông, Phú Tân, Long Đức, Trà Vinh, Nguyệt Hóa,
Hòa Thuận và các xã Phú Túc, Giao Long, Tiên Thủy, Tân Phú.
- Vùng III, gồm các phường
Duyên Hải, Trường Long Hòa và các xã Cái Nhum, Tân Long Hội, Nhơn Phú, Bình Phước,
An Bình, Long Hồ, Phú Quới, Đồng Khởi, Mỏ Cày, Thành Thới, An Định, Hương Mỹ,
Tân Thủy, Bảo Thạnh, Ba Tri, Tân Xuân, Mỹ Chánh Hòa, An Ngãi Trung, An Hiệp, Thới
Thuận, Thạnh Phước, Bình Đại, Thạnh Trị, Lộc Thuận, Châu Hưng, Phú Thuận, Long
Hữu, Hưng Nhượng.
- Vùng IV, gồm các xã, phường
còn lại.
32. Tỉnh An Giang
- Vùng II, gồm các phường Long
Xuyên, Bình Đức, Mỹ Thới, Châu Đốc, Vĩnh Tế, Vĩnh Thông, Rạch Giá, Hà Tiên, Tô
Châu; các xã Mỹ Hòa Hưng, Tiên Hải và các đặc khu Phú Quốc, Thổ Châu.
- Vùng III, gồm các phường Tân
Châu, Long Phú; các xã Tân An, Châu Phong, Vĩnh Xương, Châu Phú, Mỹ Đức, Vĩnh
Thạnh Trung, Bình Mỹ, Thạnh Mỹ Tây, An Châu, Bình Hòa, Cần Đăng, Vĩnh Hanh,
Vĩnh An, Thoại Sơn, Óc Eo, Định Mỹ, Phú Hòa, Vĩnh Trạch, Tây Phú, Thạnh Lộc,
Châu Thành, Bình An, Hòa Điền, Kiên Lương, Sơn Hải, Hòn Nghệ và đặc khu Kiên Hải.
- Vùng IV, gồm các xã, phường
còn lại.
33. Thành phố Cần Thơ
- Vùng II, gồm các phường Phú Lợi,
Mỹ Xuyên, Ninh Kiều, Cái Khế, Tân An, An Bình, Thới An Đông, Bình Thủy, Long
Tuyền, Cái Răng, Hưng Phú, Ô Môn, Thới Long, Phước Thới, Trung Nhứt, Thốt Nốt,
Thuận Hưng, Tân Lộc, Sóc Trăng.
- Vùng III, gồm các phường Vị
Thanh, Vị Tân, Đại Thành, Ngã Bảy, Vĩnh Phước, Vĩnh Châu, Khánh Hòa, Ngã Năm, Mỹ
Quới và các xã Tân Long, Phong Điền, Nhơn Ái, Trường Long, Thới Lai, Đông Thuận,
Trường Xuân, Trường Thành, Cờ Đỏ, Đông Hiệp, Thạnh Phú, Thới Hưng, Trung Hưng,
Vĩnh Thạnh, Vĩnh Trinh, Thạnh An, Thạnh Quới, Hỏa Lựu, Thạnh Xuân, Tân Hòa, Trường
Long Tây, Châu Thành, Đông Phước, Phú Hữu, Vĩnh Hải, Lai Hòa.
- Vùng IV, gồm các xã, phường
còn lại.
34. Tỉnh Cà Mau
- Vùng II, gồm các phường An
Xuyên, Lý Văn Lâm, Tân Thành, Hòa Thành, Bạc Liêu, Vĩnh Trạch, Hiệp Thành.
- Vùng III, gồm các phường Giá
Rai, Láng Tròn và các xã U Minh, Nguyễn Phích, Khánh Lâm, Khánh An, Khánh Bình,
Đá Bạc, Khánh Hưng, Sông Đốc, Trần Văn Thời, Đất Mới, Năm Căn, Tam Giang, Lương
Thế Trân, Hưng Mỹ, Cái Nước, Tân Hưng, Phú Mỹ, Phong Thạnh, Hòa Bình, Vĩnh Mỹ,
Vĩnh Hậu.
- Vùng IV, gồm các xã, phường
còn lại.
"""

# --- LOGIC XỬ LÝ DỮ LIỆU ---
def normalize_text(text):
    if not isinstance(text, str): return ""
    text = unicodedata.normalize('NFC', text.lower())
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

@st.cache_data(show_spinner=False)
def get_database():
    db = {}
    display_names = {}
    
    # Regex tách các tỉnh (Thêm \n vào đầu để bắt được dòng 1)
    full_text = '\n' + raw_data.strip()
    entries = re.split(r'\n\d+\.\s+', full_text)
    province_titles = re.findall(r'\n\d+\.\s+(.*)', full_text)
    
    for i in range(len(province_titles)):
        display_name = province_titles[i].strip()
        content = entries[i+1] # entry[0] là rỗng
        
        province_key = normalize_text(display_name)
        display_names[province_key] = display_name

        province_data = {"default": "Vùng IV"} 
        
        zones = re.findall(r'-\s*Vùng\s+([I|V]+)[^,]*,\s*gồm\s*(.*?)(?=\n-\s*Vùng|\n\d+\.|$)', content, re.DOTALL)
        
        for zone_id, places in zones:
            zone_key = zone_id.strip()
            
            # XỬ LÝ DẤU CHẤM PHẨY (;) và CHẤM (.)
            cleaned = places.replace('\n', ' ') \
                            .replace(";", ",") \
                            .replace(".", ",") 
                            
            # Lọc từ khóa rác
            cleaned = cleaned.replace("các xã", "") \
                            .replace("các phường", "") \
                            .replace("các đặc khu", "") \
                            .replace("đặc khu", "") \
                            .replace(" và ", ", ")
            
            if "còn lại" in cleaned:
                province_data["default"] = f"Vùng {zone_key}"
            else:
                p_list = []
                for p in cleaned.split(','):
                    p_norm = normalize_text(p)
                    # Fix lỗi Lâm Đồng (Xuân Hương - Đà Lạt)
                    if "-" in p_norm: p_norm = p_norm.split("-")[0].strip()
                    
                    if p_norm and len(p_norm) > 1:
                        p_list.append(p_norm)
                province_data[zone_key] = p_list
        
        db[province_key] = province_data
        
    return db, display_names

database, display_names_map = get_database()

# --- GIAO DIỆN NGƯỜI DÙNG ---
st.markdown("""
    <h1 class="main-title">💰 TRA CỨU HỆ SỐ VÙNG 2026</h1>
    <p class="sub-title">PDA-HINOVA 2026</p>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    province_options = list(display_names_map.values())
    selected_province = st.selectbox("📍 Chọn Tỉnh / Thành phố:", province_options, index=None, placeholder="Chọn hoặc gõ để tìm...")
    
with col2:
    xa_input = st.text_input("🏠 Phường / Xã / Đặc Khu:", placeholder="Nhập tên địa phương...", key="xa")

st.markdown('<br>', unsafe_allow_html=True)
search_btn = st.button("🔍 TRA CỨU NGAY")

if search_btn:
    if selected_province and xa_input:
        t_norm = normalize_text(selected_province)
        x_norm = normalize_text(xa_input)
        
        info = database.get(t_norm)
        
        if info:
            res_vung = None
            is_default = False 
            
            # Ưu tiên tìm trong danh sách liệt kê
            for z in ["I", "II", "III", "IV"]:
                if z in info and any(p in x_norm for p in info[z]):
                    res_vung = f"VÙNG {z}"
                    break
            
            # Nếu không tìm thấy tên -> Vùng mặc định -> BẬT CỜ CẢNH BÁO
            if not res_vung:
                res_vung = info['default']
                is_default = True
            
            # Chỉ hiện cảnh báo khi rơi vào trường hợp mặc định
            note_content = ""
            if is_default:
                note_content = """
                <div class="warning-note">
                    ⚠️ Địa phương thuộc trường hợp loại trừ (vùng còn lại) căn cứ Nghị định 293/2025/NĐ-CP.
                    <br>Vui lòng kiểm tra lại chính tả nếu kết quả chưa chính xác.
                </div>
                """
            
            st.markdown(f"""
                <div class="result-box">
                    <p class="result-location">Địa bàn: <b>{xa_input.title()}</b> - <b>{selected_province}</b></p>
                    <p class="result-value">{res_vung}</p>
                    {note_content}
                </div>
            """, unsafe_allow_html=True)
        else:
             st.error("Lỗi dữ liệu hệ thống.")
    else:
        st.warning("⚠️ Vui lòng chọn Tỉnh và nhập tên Phường/Xã để tra cứu.")

st.markdown('<div class="footer">Copyright © Hinova 2026. All rights reserved.</div>', unsafe_allow_html=True)


