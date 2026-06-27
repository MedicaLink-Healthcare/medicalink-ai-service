7.3. Kiểm thử AI worker
7.3.1 Tổng quan và Môi trường Kiểm thử
	Không giống như các API CRUD truyền thống, hệ thống định tuyến phân luồng lâm sàng (Semantic Routing) dựa trên AI không mang tính tất định tuyệt đối. Việc đánh giá đòi hỏi một bộ công cụ kiểm thử đa giai đoạn (Multi-stage Evaluation), bao gồm đánh giá từng thành phần của hệ thống và đánh giá toàn bộ quy trình xử lý đầu cuối (End-to-End).
	Để thực hiện kiểm thử, một tập các script Python được xây dựng nhằm giao tiếp trực tiếp với các API Production của hệ thống MedicaLink, bao gồm:
-	/api/ai/suggest-specialties: API định tuyến chuyên khoa. 
-	/api/ai/recommend-doctor: API gợi ý bác sĩ. 
Các bài kiểm thử được thực hiện trên môi trường thực tế sử dụng RabbitMQ làm hệ thống hàng đợi thông điệp, PostgreSQL làm cơ sở dữ liệu nghiệp vụ và Qdrant Cloud làm cơ sở dữ liệu vector phục vụ Hybrid RAG.

7.3.2. Tập Dữ liệu Kiểm thử (Test Dataset)
	Bộ dữ liệu kiểm thử bao gồm 225 kịch bản (Test cases) được thiết kế kỹ lưỡng bởi sinh viên có tham khảo các ca bệnh thực tế. Bộ dữ liệu được chia đều cho 15 chuyên khoa lâm sàng (mỗi chuyên khoa 15 kịch bản). Đặc điểm của các kịch bản trải dài từ:
-	Câu hỏi có triệu chứng rõ ràng (Ví dụ: “Trẻ 5 tuổi khóc đêm, hay gãi tai” -> Nhi khoa / Tai Mũi Họng).
-	Câu hỏi mơ hồ, chồng lấn đa khoa (Ví dụ: “Đau tức ngực kèm ho đờm” -> Tim mạch / Hô hấp).
-	Câu hỏi chứa yếu tố phủ định CQU (Ví dụ: “Đau đầu dữ dội nhưng không bị sốt”).
-	Các câu hỏi giả lập cấp cứu (Ví dụ: “Tôi bị ép tim dữ dội, khó thở thành cơn”, “Liệt nửa người đột ngột”).
-	Các truy vấn ngoài phạm vi y tế (Out-of-Domain) nhằm kiểm thử cơ chế Intent Classification của hệ thống (Ví dụ: “Cách nấu cơm ngon?”, “Thời tiết hôm nay thế nào?”, “Giá vàng hiện tại là bao nhiêu?”).
 
Hình 7.4 Minh hoạ bộ dữ liệu triệu chứng của chuyên khoa tim mạch

7.3.3. Các Kịch bản và Tiêu chí Đánh giá
	Script thực thi sẽ đánh giá hệ thống qua 3 tiêu chí cốt lõi:
-	Kiểm thử Bóc tách Ngữ nghĩa (CQU Extraction): Xác nhận LLM trích xuất thành công mảng negated_symptoms (ví dụ: “không ho”) để làm cơ sở trừ điểm Reranking.
-	Độ chính xác Định tuyến (Routing Accuracy): Hệ thống được xem là “Passed” nếu specialty_id kỳ vọng của Test case xuất hiện thành công trong danh sách Top chuyên khoa được trả về từ Giai đoạn 2 và bảo toàn được kết quả sau Giai đoạn Reranking.
-	Kiểm thử Lưới an toàn Cấp cứu (Emergency Guardrails): Cố tình tiêm các truy vấn mang tín hiệu đe dọa tính mạng để kiểm tra xem phân hệ AI có ngắt luồng RAG và từ chối gợi ý bác sĩ hay không.
-	Kiểm thử Truy vấn Ngoài Phạm vi (Out-of-Domain Detection): Đưa vào các truy vấn không thuộc lĩnh vực y tế nhằm đánh giá khả năng nhận diện và từ chối xử lý của hệ thống. Hệ thống được xem là đạt yêu cầu nếu không thực hiện truy xuất chuyên khoa hoặc gợi ý bác sĩ đối với các truy vấn này.
 
7.3.4. Đánh giá chiến lược Truy xuất Hybrid RAG:
	Để chứng minh tính hiệu quả của kiến trúc Hybrid RAG, tầng Retrieval được đánh giá độc lập thông qua script benchmark_retrieval.py.
	Khác với bài kiểm thử End-to-End, bài kiểm thử này cô lập riêng tầng truy xuất bằng cách truy vấn trực tiếp Qdrant và đo lường khả năng tìm đúng chuyên khoa mong muốn.
	Chỉ số sử dụng bao gồm Hit Rate@5 và Mean Reciprocal Rank (MRR):
-	Hit Rate@5: Đánh giá xem chuyên khoa kỳ vọng có lọt vào top 5 kết quả trả về hay không.
-	MRR (Mean Reciprocal Rank): Đánh giá chất lượng xếp hạng, cho biết chuyên khoa đúng được xếp ở vị trí cao đến mức nào.
 
Hình 7.5 Kết quả benchmark tầng Retrieval trên 225 kịch bản lâm sàng
	Kết quả cho thấy Hybrid RAG đạt hiệu quả cao nhất với Hit Rate@5 bằng 80.0% (180/225 kịch bản) và chỉ số MRR đạt 0.632, vượt trội hoàn toàn so với mô hình Dense Vector đơn thuần (Hit Rate@5: 61.3%, MRR: 0.525). Mặc dù mức cải thiện Hit Rate so với Sparse Retrieval (Hit Rate@5: 76.9%, MRR: 0.636) không chênh lệch quá lớn, việc kết hợp Dense Vector (bắt ngữ nghĩa) và Sparse Vector (khớp từ khóa chính xác) cùng thuật toán RRF giúp hệ thống xử lý ổn định hơn các truy vấn chứa đồng thời ngôn ngữ đời thường của bệnh nhân và thuật ngữ chuyên môn y khoa, đẩy kết quả đúng lên các vị trí đầu tiên.
 
7.3.5. Kết quả Kiểm thử End to end 
Hình 7.6 Kết quả kiểm thử trên môi trường production
	Kết quả kiểm thử trên môi trường thực tế cho thấy hệ thống đạt hiệu năng vô cùng khả quan với kiến trúc Hybrid RAG:
-	Tỷ lệ đánh chặn Cơ chế An toàn (Guardrail Intercept Rate): Đạt tỷ lệ 100%. Hệ thống đánh chặn thành công toàn bộ 10 truy vấn khẩn cấp (trả về khuyến nghị gọi 115) và 10 truy vấn rác ngoài phạm vi y tế (Out-of-Domain).
-	Độ chính xác Định tuyến Tổng quát (Overall Routing Accuracy): Đạt mức 65.3% (147/225 cases passed).
	Phân tích theo chuyên khoa:
-	Nhóm chuyên khoa có triệu chứng đặc trưng (Nhi khoa, Tai Mũi Họng, Tim mạch, Mắt) đạt độ chính xác đột phá từ 86% đến 100%.
-	Nhóm chuyên khoa có triệu chứng hay bị chồng lấn (overlap) như Tiêu hóa, Nội tiết duy trì tỷ lệ nhận diện thấp hơn (26% - 40%), phản ánh đúng tính chất mơ hồ trong chẩn đoán sơ bộ lâm sàng thực tế, khi một bác sĩ Nội tổng quát (GP Fallback) sẽ là lựa chọn an toàn hơn.
-	Cơ chế tái xếp hạng (Multi-Factor Reranking): Chứng minh được sự hiệu quả nhờ cộng điểm “Intent Bonus”, ép các bác sĩ thuộc chuyên khoa đích (Top 1) vượt lên trên các bác sĩ chuyên khoa khác bị lẫn vào do chồng chéo từ vựng.

7.3.6. Đánh giá Chất lượng Sinh phản hồi bằng RAGAS
	Phương pháp đánh giá sử dụng mô hình ngôn ngữ lớn (LLM-as-a-Judge) để chấm điểm các phản hồi được sinh ra từ API Production dựa trên framework đánh giá RAGAS [9]. Trong đánh giá này, mô hình GPT-4o-mini được sử dụng làm giám khảo. Các chỉ số được sử dụng bao gồm: Faithfulness (Tính trung thực) và Answer Relevancy (Độ bám sát truy vấn).
 
Hình 7.7 Kết quả đánh giá chất lượng sinh văn bản (RAGAS) 
	Kết quả thực nghiệm cho thấy hệ thống đạt hiệu năng xuất sắc với định hướng là một hệ thống Khuyến nghị Bác sĩ (Doctor Recommendation System):
-	Tính trung thực với ngữ cảnh (Faithfulness): Đạt 88.5%. Hệ thống lấy trọn điểm nhờ vào cơ chế không "ảo giác" (hallucinate) hay tự bịa đặt thông tin chẩn đoán y khoa, chỉ bám sát vào lý do và hồ sơ bác sĩ đã được truy xuất.
-	Độ bám sát truy vấn (Answer Relevancy): Đạt 84.4%. Câu trả lời giải quyết trực diện nhu cầu tìm bác sĩ của người dùng bằng cách đưa ra lý do khuyến nghị ngắn gọn, an toàn và hoàn toàn không vi phạm ranh giới chẩn đoán.
	Sự khác biệt lớn nhất so với một QA Chatbot thông thường là hệ thống MedicaLink không sinh ra các phân tích bệnh lý dài dòng, mà tập trung định tuyến an toàn. Các chỉ số RAGAS sau khi được chuẩn hóa đã phản ánh chính xác năng lực cốt lõi này của hệ thống.
