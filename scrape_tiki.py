import requests
import pandas as pd
import time
import random
import os
import re # Thư viện Biểu thức chính quy để bóc tách ID từ Link

def extract_tiki_id(url):
    """
    Hàm tự động trích xuất product_id và spid từ đường link Tiki.
    Ví dụ: https://tiki.vn/sach-xyz-p12345.html?spid=67890
    -> product_id = 12345, spid = 67890
    """
    product_id, spid = None, None
    
    # Tìm product_id (chuỗi số sau chữ -p và trước .html)
    p_match = re.search(r'-p(\d+)\.html', url)
    if p_match:
        product_id = p_match.group(1)
        
    # Tìm spid (chuỗi số sau chữ spid=)
    s_match = re.search(r'spid=(\d+)', url)
    if s_match:
        spid = s_match.group(1)
        
    return product_id, spid

def scrape_tiki_reviews_by_url(url, max_pages=15):
    """
    Hàm thu thập đánh giá thông qua đường link URL.
    """
    # Tự động bóc tách ID từ link
    product_id, spid = extract_tiki_id(url)
    
    if not product_id:
        print(f"  [Lỗi] Không tìm thấy product_id trong Link: {url}")
        return []
        
    danh_sach_binh_luan = []
    
    # Headers giả lập trình duyệt
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
        'Referer': url # Báo cho Tiki biết ta đang đứng từ đúng trang sản phẩm đó
    }

    # Tiki phân trang bắt đầu từ page=1
    for page in range(1, max_pages + 1):
        print(f"  [+] Đang quét Trang {page}...")
        
        # ĐƯỜNG LINK API
        # Giảm limit xuống 20, thêm đầy đủ các tham số include và sort bắt buộc
        api_url = f"https://tiki.vn/api/v2/reviews?limit=20&include=comments,contribute_info,attribute_vote_summary&sort=score|desc,id|desc,stars|all&page={page}&product_id={product_id}"
        if spid:
            api_url += f"&spid={spid}"
            
        try:
            response = requests.get(api_url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                reviews_data = data.get('data', [])
                
                # Nếu mảng rỗng nghĩa là đã hết bình luận ở các trang sau, dừng lại sớm
                if not reviews_data:
                    print("  [!] Đã hết bình luận cho sản phẩm này.")
                    break
                    
                for review in reviews_data:
                    content = review.get('content', '')
                    rating = review.get('rating', 0)
                    
                    # Chỉ lấy những đánh giá có viết chữ (bỏ qua những người chỉ chấm sao)
                    if content and str(content).strip():
                        # Xóa các ký tự xuống dòng để dữ liệu trên 1 dòng gọn gàng
                        clean_content = str(content).replace('\n', ' ').replace('\r', ' ').strip()
                        
                        danh_sach_binh_luan.append({
                            'Review': clean_content,
                            'Rating': rating
                        })
                
                # Nghỉ ngơi ngẫu nhiên 1-2 giây để tránh làm quá tải máy chủ Tiki (Polite Scraping)
                time.sleep(random.uniform(1.0, 2.0))
                
            else:
                print(f"  [Lỗi] Máy chủ phản hồi mã: {response.status_code}. Thử nghiệm trang tiếp theo...")
                # Nếu trang này lỗi (có thể do limit), vẫn cố gắng đi tiếp
                time.sleep(2)
                continue
                
        except Exception as e:
            print(f"  [Lỗi Hệ Thống] Mất kết nối: {e}")
            break
            
    return danh_sach_binh_luan

if __name__ == "__main__":
    print("="*60)
    print("HỆ THỐNG THU THẬP DỮ LIỆU ĐÁNH GIÁ TỰ ĐỘNG TỪ TIKI")
    print("="*60)
    
    # ĐƯỜNG LINK SẢN PHẨM TRÊN TRÌNH DUYỆT
    DANH_SACH_URL = [
        "https://tiki.vn/combo-5-doi-tat-nam-vo-nam-co-ngan-cao-cap-mrm-fashion-cung-mau-p34159013.html?itm_campaign=CTP_YPD_TKA_PLA_UNK_ALL_UNK_UNK_UNK_UNK_X.295949_Y.1878269_Z.3965267_CN.11%2F7---TCN---Auto---2k&itm_medium=CPC&itm_source=tiki-ads&spid=34159015",
        "https://tiki.vn/ta-doi-ta-tay-chon-luc-nang-cua-ta-20kg-30kg-40kg-tuy-chon-ta-p-tay-day-ket-hop-ta-nam-nu-tap-gym-tap-thon-tay-gia-tot-hang-chuan-hang-nhap-khau-p257845274.html?itm_campaign=CTP_YPD_TKA_PLA_UNK_ALL_UNK_UNK_UNK_UNK_X.248167_Y.1830487_Z.3752619_CN.Product-Ads-30%2F05%2F2023-ta&itm_medium=CPC&itm_source=tiki-ads&spid=57984817",
        "https://tiki.vn/combo-3-qua-n-lo-t-nam-so-i-cotton-organic-me-m-mi-n-thoa-ng-ma-t-co-gia-n-4-chie-u-mrm-manlywear-tang-doi-tat-nam-cao-cap-mau-ngau-nhien-p52189164.html?itm_campaign=CTP_YPD_TKA_PLA_UNK_ALL_UNK_UNK_UNK_UNK_X.299617_Y.1881937_Z.3985445_CN.07%2F9---QTG---Auto---3.5k&itm_medium=CPC&itm_source=tiki-ads&spid=52189166",
        "https://tiki.vn/bo-10-quan-lot-nu-modal-miley-lingerie-giao-mau-ngau-nhien-p1752845.html?itm_campaign=CTP_YPD_TKA_PLA_UNK_ALL_UNK_UNK_UNK_UNK_X.194452_Y.1776779_Z.3497193_CN.Combo-Quan-Lot-Nu-28%2F03&itm_medium=CPC&itm_source=tiki-ads&spid=4720785",
        "https://tiki.vn/dung-dich-tay-keo-nhua-duong-3m-08987-443ml-p892527.html?itm_campaign=CTP_YPD_TKA_PLA_UNK_ALL_UNK_UNK_UNK_UNK_X.149247_Y.1588182_Z.2636744_CN.Dung-Dich-Tay-Keo%2C-Nhua-%C4%90uong-3M-08987-%28425-g%29&itm_medium=CPC&itm_source=tiki-ads&spid=7378225",
        "https://tiki.vn/tinh-chat-chong-nang-nang-tong-skin-aqua-tone-up-lavender-cho-da-toi-mau-da-vang-sunplay-skin-aqua-tone-up-uv-essence-lavender-spf-50-pa-50g-p8959289.html?itm_campaign=CTP_YPD_TKA_PLA_UNK_ALL_UNK_UNK_UNK_UNK_X.306443_Y.1888763_Z.4017914_CN.Sunplay%2C-Skin-Aqua-l-Kem-Chong-Nang&itm_medium=CPC&itm_source=tiki-ads&spid=10863050",
        "https://tiki.vn/tai-nghe-bluetooth-cao-cap-hoco-eq2-5-3-pin-7h-am-thanh-song-dong-bass-cang-hang-chinh-hang-p272030678.html?itm_campaign=CTP_YPD_TKA_PLA_UNK_ALL_UNK_UNK_UNK_UNK_X.274009_Y.1856329_Z.3861499_CN.Tai-nghe-bluetooth-eq2&itm_medium=CPC&itm_source=tiki-ads&spid=272030680",
        "https://tiki.vn/noi-ap-suat-elmich-pce-1805-dung-tich-2-5l-hang-chinh-hang-p275515112.html?itm_campaign=CTP_YPD_TKA_PLA_UNK_ALL_UNK_UNK_UNK_UNK_X.304551_Y.1886871_Z.4008596_CN.SA---Key-SKUs-l-Noi-Ap-Suat-%C4%90ien&itm_medium=CPC&itm_source=tiki-ads&spid=193570412",
        "https://tiki.vn/kem-chong-nang-sunplay-cuc-manh-dang-sua-sunplay-super-block-spf-50-pa-30g-p1313871.html?itm_campaign=CTP_YPD_TKA_PLA_UNK_ALL_UNK_UNK_UNK_UNK_X.306622_Y.1888942_Z.4018713_CN.Sunplay%2C-Skin-Aqua---Key-SKUs-l-Kem-Chong-Nang&itm_medium=CPC&itm_source=tiki-ads&spid=10862283",
        "https://tiki.vn/bang-keo-cuong-luc-sieu-di-nh-3m-4229p-10-10mm-x-10m-p2045625.html?itm_campaign=CTP_YPD_TKA_PLA_UNK_ALL_UNK_UNK_UNK_UNK_X.149247_Y.1588182_Z.3857522_CN.Dung-Dich-Tay-Keo%2C-Nhua-%C4%90uong-3M-08987-%28425-g%29&itm_medium=CPC&itm_source=tiki-ads&spid=32052351",
        "https://tiki.vn/qua-n-du-i-short-gio-nam-the-thao-basic-tre-trung-nang-do-ng-thoa-ng-ma-t-co-gia-n-4-chie-u-mrm-manlywear-p99958075.html?itm_campaign=CTP_YPD_TKA_PLA_UNK_ALL_UNK_UNK_UNK_UNK_X.299618_Y.1881938_Z.3985450_CN.07%2F9---Q%C4%90N---Auto&itm_medium=CPC&itm_source=tiki-ads&spid=99958305",
        "https://tiki.vn/combo-3-qua-n-lo-t-nam-boxer-so-i-cotton-organic-me-m-mi-n-thoa-ng-ma-t-co-gia-n-4-chie-u-mrm-manlywear-tang-doi-tat-nam-cao-cap-giao-ngau-nhien-p52184516.html?itm_campaign=CTP_YPD_TKA_PLA_UNK_ALL_UNK_UNK_UNK_UNK_X.300134_Y.1882454_Z.3987584_CN.13%2F9---QBX---TTL---4k&itm_medium=CPC&itm_source=tiki-ads&spid=52184522",
    ] 
    
    # Vì limit đã giảm xuống 20, tăng số trang lên để cào được nhiều hơn
    SO_TRANG_MOI_SP = 30     # Quét tối đa 30 trang (x20 = 600 bình luận) cho mỗi sản phẩm
    MUC_TIEU_TONG = 3000     # Dừng hệ thống khi gom đủ 3000 câu
    
    tong_data_thu_thap = []

    for url in DANH_SACH_URL:
        print(f"\n---> Chuyển sang sản phẩm mới:")
        data_sp = scrape_tiki_reviews_by_url(url=url, max_pages=SO_TRANG_MOI_SP)
        tong_data_thu_thap.extend(data_sp)
        
        print(f"[*] Tiến độ hiện tại: Đã gom được {len(tong_data_thu_thap)} / {MUC_TIEU_TONG} bình luận.")
        
        # Kiểm tra nếu đã đạt mục tiêu thì ngắt vòng lặp lớn
        if len(tong_data_thu_thap) >= MUC_TIEU_TONG:
            print(f"\n[OK] TUYỆT VỜI! Đã đạt (hoặc vượt) mục tiêu {MUC_TIEU_TONG} bình luận.")
            break
            
        time.sleep(2) # Nghỉ một chút trước khi sang sản phẩm mới

    print("\n" + "="*60)
    if len(tong_data_thu_thap) > 0:
        # Chuyển đổi list dictionary thành bảng Pandas DataFrame
        df_raw = pd.DataFrame(tong_data_thu_thap)
        
        # Nếu cào lố mục tiêu (ví dụ 3025 câu), có thể cắt đúng 3000 câu cho đẹp
        if len(df_raw) > MUC_TIEU_TONG:
            df_raw = df_raw.head(MUC_TIEU_TONG)
        
        # Tạo thư mục data nếu chưa có
        thu_muc_luu = "data"
        if not os.path.exists(thu_muc_luu):
            os.makedirs(thu_muc_luu)
            
        # Lưu file raw_data.csv (Đầu ra của Bước 1.1)
        file_luu = os.path.join(thu_muc_luu, "raw_data.csv")
        df_raw.to_csv(file_luu, index=False, encoding='utf-8')
        
        print(f"[+] Tiến trình hoàn tất!")
        print(f"[+] Đã lưu thành công {len(df_raw)} tập dữ liệu gốc tại: {file_luu}")
        print("\n--- XEM TRƯỚC 5 MẪU DỮ LIỆU ---")
        print(df_raw.head())
    else:
        print("\n[!] Không thu thập được dữ liệu nào. Vui lòng kiểm tra lại danh sách ID sản phẩm.")