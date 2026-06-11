import json
import os
import shutil

# Path to the JSON files
AI_DATA_PATH = "data/specialties_cleaned.json"
MICROSERVICE_DATA_PATH = "../medicalink-microservice/data/specialties_cleaned.json"

ENRICHMENT_DATA = {
    "Nội tổng quát": {
        "keywords": ["khám tổng quát", "kiểm tra sức khỏe", "mệt mỏi", "suy nhược", "sốt", "đau nhức", "khám định kỳ", "chóng mặt", "sụt cân không rõ nguyên nhân", "khám sức khỏe xin việc", "tầm soát bệnh"],
        "common_conditions": ["sốt virus", "nhiễm trùng", "suy nhược cơ thể", "mệt mỏi mãn tính"]
    },
    "Da liễu": {
        "keywords": ["mụn", "ngứa", "vảy nến", "dị ứng da", "phát ban", "viêm da cơ địa", "nám", "tàn nhang", "rụng tóc", "mề đay", "hắc lào", "lang ben", "ghẻ", "chàm", "viêm nang lông", "nổi cục", "mụn trứng cá", "mụn nhọt"],
        "common_conditions": ["viêm da", "vảy nến", "mề đay", "chàm (eczema)", "dị ứng", "nấm da", "mụn trứng cá"]
    },
    "Nội tiết": {
        "keywords": ["tiểu đường", "tuyến giáp", "cường giáp", "suy giáp", "rối loạn hoóc môn", "đái tháo đường", "bướu cổ", "béo phì", "tăng cân bất thường", "khát nước nhiều", "tiểu nhiều", "rối loạn chuyển hóa", "đổ mồ hôi nhiều"],
        "common_conditions": ["đái tháo đường (tiểu đường)", "cường giáp", "suy giáp", "rối loạn chuyển hóa lipit", "bướu tuyến giáp", "rối loạn nội tiết"]
    },
    "Hô hấp": {
        "keywords": ["ho kéo dài", "khó thở", "hen suyễn", "viêm phế quản", "phổi", "ngạt thở", "viêm phổi", "thở khò khè", "lao phổi", "viêm đường hô hấp", "ho khan", "ho có đờm", "thở hụt hơi", "tức ngực khi thở"],
        "common_conditions": ["viêm phổi", "hen phế quản (suyễn)", "Bệnh phổi tắc nghẽn mạn tính (COPD)", "viêm phế quản", "lao phổi", "tràn dịch màng phổi"]
    },
    "Tiêu hóa": {
        "keywords": ["đau dạ dày", "tiêu chảy", "táo bón", "viêm loét", "trào ngược", "ợ chua", "đầy hơi", "viêm đại tràng", "nội soi", "gan nhiễm mỡ", "viêm gan", "đau bụng", "buồn nôn", "nôn mửa", "đi cầu ra máu", "khó tiêu", "đau bao tử"],
        "common_conditions": ["viêm loét dạ dày tá tràng", "trào ngược dạ dày thực quản (GERD)", "viêm đại tràng", "hội chứng ruột kích thích", "viêm gan", "xơ gan", "trĩ", "nhiễm HP"]
    },
    "Tim mạch": {
        "keywords": ["huyết áp cao", "đau thắt ngực", "nhồi máu", "hồi hộp", "rối loạn nhịp tim", "suy tim", "cao huyết áp", "mỡ máu", "nhịp tim nhanh", "nhịp tim chậm", "đánh trống ngực", "tức ngực trái", "thiếu máu cơ tim"],
        "common_conditions": ["tăng huyết áp", "suy tim", "bệnh mạch vành", "rối loạn nhịp tim", "hở van tim", "nhồi máu cơ tim", "rối loạn mỡ máu"]
    },
    "Nhi khoa": {
        "keywords": ["trẻ em", "trẻ sơ sinh", "con nít", "sốt ở trẻ", "biếng ăn", "tiêm chủng", "khám bệnh cho bé", "khám dinh dưỡng cho trẻ", "trẻ quấy khóc", "trẻ ho", "trẻ nôn trớ", "sốt phát ban ở trẻ", "tay chân miệng"],
        "common_conditions": ["viêm họng ở trẻ", "viêm tai giữa ở trẻ", "sốt xuất huyết", "tay chân miệng", "suy dinh dưỡng", "viêm phế quản trẻ em"]
    },
    "Sản phụ khoa": {
        "keywords": ["khám thai", "phụ khoa", "kinh nguyệt", "viêm nhiễm phụ khoa", "tầm soát ung thư cổ tử cung", "siêu âm thai", "kế hoạch hóa gia đình", "đau bụng kinh", "rong kinh", "khí hư bất thường", "hiếm muộn", "sảy thai", "mãn kinh"],
        "common_conditions": ["viêm âm đạo", "u xơ tử cung", "nang buồng trứng", "rối loạn kinh nguyệt", "thai kỳ", "vô sinh - hiếm muộn", "viêm lộ tuyến"]
    },
    "Thần kinh": {
        "keywords": ["đau đầu", "đau nửa đầu", "chóng mặt", "mất ngủ", "động kinh", "đột quỵ", "tê bì chân tay", "rối loạn tiền đình", "trầm cảm", "suy giảm trí nhớ", "tai biến", "co giật", "Parkinson", "Alzheimer", "căng thẳng"],
        "common_conditions": ["đau nửa đầu (Migraine)", "rối loạn tiền đình", "đột quỵ (tai biến mạch máu não)", "động kinh", "mất ngủ mãn tính", "viêm dây thần kinh"]
    },
    "Tai Mũi Họng": {
        "keywords": ["viêm họng", "viêm amidan", "viêm xoang", "ù tai", "chảy máu cam", "ngạt mũi", "khàn tiếng", "đau họng", "điếc", "đau tai", "sổ mũi", "viêm tai giữa", "hắt hơi liên tục", "mất khứu giác"],
        "common_conditions": ["viêm amidan", "viêm xoang", "viêm họng hạt", "viêm tai giữa", "viêm mũi dị ứng", "hạt dây thanh", "polyp mũi"]
    },
    "Mắt (Nhãn khoa)": {
        "keywords": ["cận thị", "viêm kết mạc", "đau mắt đỏ", "đục thủy tinh thể", "khô mắt", "mờ mắt", "cườm nước", "tăng nhãn áp", "loạn thị", "viễn thị", "chảy nước mắt sống", "nhức mắt", "cườm khô"],
        "common_conditions": ["tật khúc xạ (cận, viễn, loạn)", "viêm kết mạc", "đục thủy tinh thể", "glocom (cườm nước)", "khô mắt", "viêm giác mạc"]
    },
    "Răng Hàm Mặt": {
        "keywords": ["nhổ răng", "trám răng", "sâu răng", "niềng răng", "viêm nướu", "chảy máu chân răng", "hôi miệng", "đau răng", "răng khôn", "nha chu", "tẩy trắng răng", "bọc răng sứ", "trồng răng implant", "tủy răng"],
        "common_conditions": ["sâu răng", "viêm tủy răng", "viêm nha chu", "viêm nướu", "răng khôn mọc lệch", "mất răng"]
    },
    "Cơ xương khớp": {
        "keywords": ["đau nhức xương khớp", "viêm khớp", "thoái hóa cột sống", "đau lưng", "thoát vị đĩa đệm", "loãng xương", "bệnh gút", "gout", "đau vai gáy", "đau thần kinh tọa", "trật khớp", "bong gân", "đau đầu gối", "cứng khớp"],
        "common_conditions": ["thoái hóa khớp", "thoát vị đĩa đệm", "viêm khớp dạng thấp", "gout (gút)", "loãng xương", "đau thần kinh tọa", "viêm cột sống dính khớp"]
    },
    "Nam khoa": {
        "keywords": ["yếu sinh lý", "xuất tinh sớm", "liệt dương", "vô sinh nam", "rối loạn cương dương", "cắt bao quy đầu", "viêm niệu đạo", "tiểu buốt", "tiểu rắt", "bệnh xã hội", "giang mai", "lậu"],
        "common_conditions": ["viêm tuyến tiền liệt", "phì đại tuyến tiền liệt", "rối loạn cương dương", "vô sinh nam", "viêm niệu đạo", "hẹp bao quy đầu"]
    },
    "Ung bướu": {
        "keywords": ["ung thư", "khối u", "hạch", "tầm soát ung thư", "xạ trị", "hóa trị", "sinh thiết", "u lành tính", "u ác tính", "ung thư vú", "ung thư gan", "ung thư phổi", "sụt cân", "ho ra máu"],
        "common_conditions": ["ung thư vú", "ung thư phổi", "ung thư gan", "ung thư đại trực tràng", "ung thư dạ dày", "u tuyến giáp", "u xơ tử cung"]
    }
}

def enrich_specialties():
    if not os.path.exists(AI_DATA_PATH):
        print(f"File not found: {AI_DATA_PATH}")
        return

    with open(AI_DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    specialties = data.get("specialties", data) if isinstance(data, dict) else data
    
    enriched_count = 0
    for spec in specialties:
        name = spec.get("name")
        if name in ENRICHMENT_DATA:
            enrichment = ENRICHMENT_DATA[name]
            
            # Enrich keywords
            existing_keywords = set(spec.get("keywords", []))
            new_keywords = [k for k in enrichment["keywords"] if k not in existing_keywords]
            spec["keywords"] = list(existing_keywords) + new_keywords
            
            # Enrich common conditions
            existing_conditions = set(spec.get("common_conditions", []))
            new_conditions = [c for c in enrichment["common_conditions"] if c not in existing_conditions]
            spec["common_conditions"] = list(existing_conditions) + new_conditions
            
            enriched_count += 1
            print(f"Enriched '{name}': Added {len(new_keywords)} keywords and {len(new_conditions)} conditions.")
    
    # Save back to AI service
    with open(AI_DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(data if isinstance(data, list) else {"specialties": specialties}, f, ensure_ascii=False, indent=2)
    
    print(f"\nSuccessfully enriched {enriched_count} specialties.")

    # Sync to Microservice project
    if os.path.exists(os.path.dirname(MICROSERVICE_DATA_PATH)):
        shutil.copy2(AI_DATA_PATH, MICROSERVICE_DATA_PATH)
        print(f"Synced enriched file to {MICROSERVICE_DATA_PATH}")
    else:
        print(f"Directory not found: {os.path.dirname(MICROSERVICE_DATA_PATH)}")

if __name__ == "__main__":
    enrich_specialties()
