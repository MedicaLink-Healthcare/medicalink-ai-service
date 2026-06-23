# Báo cáo Đánh giá Chất lượng Sinh văn bản (RAGAS)
    
- **Tổng số Test Cases**: 41 (Stratified Sampling: 3 cases/chuyên khoa, gồm Rõ ràng, Chồng lấn, Khó)
- **Faithfulness**: 88.5%
- **Answer Relevancy & Correctness**: 84.4%

> *Đánh giá được thực hiện thông qua kỹ thuật LLM-as-a-Judge sử dụng gpt-4o-mini (OpenAI).*

## Chi tiết các Test Case

### Case 2
**Query:** Sụt cân nhẹ, người mệt mỏi nhưng không ho không sốt, muốn khám nội khoa chung tìm nguyên nhân

**API Answer:** TS.BS HỒ HOÀNG PHƯƠNG chuyên về nội tổng quát, có thể giúp tìm nguyên nhân sụt cân và mệt mỏi.

- **Faithfulness:** 1.0
- **Answer Relevancy:** 1.0
- **Reason:** Câu trả lời phản ánh đúng ngữ cảnh và chuyên khoa đề xuất khớp với hướng giải quyết trong đáp án tiêu chuẩn.

### Case 4
**Query:** Hồi hộp đánh trống ngực, nhịp tim nhanh lúc nghỉ ngơi

**API Answer:** Bác sĩ Châu Thị Ngọc Ánh chuyên về Tim mạch, có thể giúp đánh giá tình trạng hồi hộp và nhịp tim nhanh.

- **Faithfulness:** 1.0
- **Answer Relevancy:** 1.0
- **Reason:** Câu trả lời phản ánh đúng ngữ cảnh và đề xuất bác sĩ chuyên khoa Tim mạch phù hợp với triệu chứng đã được trích xuất.

### Case 5
**Query:** Ngực trái hay bị nhói đau lan ra cánh tay và sau lưng

**API Answer:** Bác sĩ chuyên về Tim mạch, có thể giúp đánh giá tình trạng đau ngực và triệu chứng liên quan.

- **Faithfulness:** 1.0
- **Answer Relevancy:** 1.0
- **Reason:** Câu trả lời phản ánh đúng ngữ cảnh và đề xuất bác sĩ chuyên khoa Tim mạch phù hợp với triệu chứng đau ngực trái, đau cánh tay và đau sau lưng.

### Case 6
**Query:** Chân tôi dạo này bị phù nề, ấn vào lõm, hay khó thở khi nằm

**API Answer:** TS.BS VŨ HỮU KHIÊM chuyên về hô hấp, có thể giúp kiểm tra tình trạng khó thở của bạn.

- **Faithfulness:** 0.5
- **Answer Relevancy:** 0.0
- **Reason:** Câu trả lời không phản ánh đúng ngữ cảnh và không đề xuất đúng chuyên khoa liên quan đến triệu chứng phù nề chân và khó thở khi nằm, mà lại chỉ định bác sĩ chuyên về hô hấp, trong khi triệu chứng này thường liên quan đến tim mạch.

### Case 7
**Query:** Mất ngủ kéo dài, trí nhớ giảm sút nghiêm trọng, hay quên

**API Answer:** Bác sĩ Nguyễn Chính Nghĩa chuyên về thần kinh, có thể giúp bạn với triệu chứng mất ngủ và trí nhớ giảm sút.

- **Faithfulness:** 1.0
- **Answer Relevancy:** 1.0
- **Reason:** Câu trả lời phản ánh đúng ngữ cảnh và đề xuất bác sĩ chuyên khoa thần kinh phù hợp với triệu chứng được nêu trong câu hỏi của người bệnh.

### Case 8
**Query:** Tay chân hay bị tê rần, đôi lúc run tay khi cầm nắm đồ vật

**API Answer:** Bác sĩ chuyên về thần kinh, có thể giúp đánh giá tình trạng tê rần và run tay của bạn.

- **Faithfulness:** 1.0
- **Answer Relevancy:** 1.0
- **Reason:** Câu trả lời phản ánh đúng ngữ cảnh và lý do đề xuất bác sĩ phù hợp với triệu chứng đã được trích xuất, không có thông tin sai lệch hay chẩn đoán không có thật.

### Case 10
**Query:** Đau nhức hai khớp gối khi đi lại nhiều, kêu lạo xạo

**API Answer:** Bác sĩ Chế Đình Nghĩa chuyên về cơ xương khớp, có thể giúp bạn với triệu chứng đau khớp gối.

- **Faithfulness:** 1.0
- **Answer Relevancy:** 1.0
- **Reason:** Câu trả lời phản ánh đúng ngữ cảnh và triệu chứng, đồng thời đề xuất đúng chuyên khoa cơ xương khớp phù hợp với triệu chứng đau khớp gối.

### Case 11
**Query:** Đau thắt lưng lan xuống chân trái, ngồi lâu rất buốt

**API Answer:** Bác sĩ Lê Văn Tuấn chuyên về cơ xương khớp, có thể giúp chẩn đoán và điều trị các vấn đề liên quan đến đau lưng và chân.

- **Faithfulness:** 1.0
- **Answer Relevancy:** 1.0
- **Reason:** Câu trả lời phản ánh đúng ngữ cảnh và đề xuất bác sĩ chuyên về cơ xương khớp, phù hợp với triệu chứng đau thắt lưng và buốt chân trái.

### Case 12
**Query:** Khớp ngón chân cái sưng tấy đỏ, đau nhức khủng khiếp sau khi ăn hải sản

**API Answer:** Bác sĩ chuyên về cơ xương khớp, có thể giúp chẩn đoán và điều trị các vấn đề liên quan đến khớp.

- **Faithfulness:** 1.0
- **Answer Relevancy:** 1.0
- **Reason:** Câu trả lời phản ánh đúng ngữ cảnh và đề xuất bác sĩ chuyên về cơ xương khớp, phù hợp với triệu chứng đã được mô tả.

### Case 13
**Query:** Đi tiểu buốt, dắt, nước tiểu có lẫn máu tươi

**API Answer:** Bác sĩ Từ Thành Trí Dũng chuyên về Tiết niệu, có thể giúp chẩn đoán và điều trị các vấn đề liên quan đến đường tiết niệu.

- **Faithfulness:** 1.0
- **Answer Relevancy:** 1.0
- **Reason:** Câu trả lời phản ánh đúng ngữ cảnh và đề xuất bác sĩ chuyên khoa Tiết niệu phù hợp với triệu chứng đã được trích xuất.

### Case 14
**Query:** Đau quặn hông lưng phải, lan xuống bụng dưới

**API Answer:** Bác sĩ Trần Quang Hiển chuyên về cơ xương khớp, có thể giúp chẩn đoán và điều trị các vấn đề liên quan đến đau lưng.

- **Faithfulness:** 0.0
- **Answer Relevancy:** 0.0
- **Reason:** Câu trả lời không phản ánh đúng ngữ cảnh và không đề xuất đúng chuyên khoa cần thiết cho triệu chứng đã nêu. Đau quặn hông lưng phải lan xuống bụng dưới liên quan đến sỏi niệu quản, trong khi bác sĩ được đề xuất lại chuyên về cơ xương khớp, không phù hợp với tình trạng bệnh lý này.

### Case 15
**Query:** Nam giới 60 tuổi, đi tiểu phải rặn mạnh, tia nước yếu

**API Answer:** Bác sĩ Từ Thành Trí Dũng chuyên về tiết niệu, rất phù hợp với triệu chứng đi tiểu khó khăn.

- **Faithfulness:** 1.0
- **Answer Relevancy:** 1.0
- **Reason:** Câu trả lời phản ánh đúng ngữ cảnh và triệu chứng, đồng thời đề xuất bác sĩ chuyên khoa phù hợp mà không bịa đặt thêm thông tin y khoa không có thật.

### Case 16
**Query:** Đau nhức răng hàm dưới, nướu sưng đỏ, nhai thức ăn rất buốt

**API Answer:** Bác sĩ chuyên về Răng Hàm Mặt, có thể giúp bạn với triệu chứng đau nhức răng và nướu sưng đỏ.

- **Faithfulness:** 1.0
- **Answer Relevancy:** 1.0
- **Reason:** Câu trả lời phản ánh đúng ngữ cảnh và triệu chứng đã được trích xuất, đồng thời hướng người dùng đến đúng chuyên khoa Răng Hàm Mặt mà không tự bịa đặt thêm thông tin y khoa không có thật.

### Case 17
**Query:** Răng khôn mọc lệch đâm vào má, đau nhức liên tục

**API Answer:** TS.BS LÊ PHÚC LIÊN chuyên về Răng Hàm Mặt, có thể giúp bạn xử lý tình trạng răng khôn mọc lệch.

- **Faithfulness:** 1.0
- **Answer Relevancy:** 1.0
- **Reason:** Câu trả lời phản ánh đúng ngữ cảnh và đề xuất bác sĩ chuyên khoa phù hợp với triệu chứng đã được trích xuất.

### Case 18
**Query:** Khớp thái dương hàm hay kêu lục cục khi há miệng to

**API Answer:** Bác sĩ chuyên về cơ xương khớp, có thể giúp đánh giá tình trạng khớp thái dương hàm của bạn.

- **Faithfulness:** 0.8
- **Answer Relevancy:** 0.6
- **Reason:** Câu trả lời không hoàn toàn phản ánh đúng ngữ cảnh vì bác sĩ chuyên về cơ xương khớp không phải là lựa chọn chính xác cho triệu chứng liên quan đến khớp thái dương hàm, mà nên là bác sĩ Răng Hàm Mặt.

### Case 19
**Query:** Ngạt mũi kéo dài, chảy dịch vàng, đau nhức vùng trán

**API Answer:** Bác sĩ Nguyễn Văn Dương chuyên về Tai Mũi Họng, rất phù hợp với triệu chứng ngạt mũi và đau nhức vùng trán.

- **Faithfulness:** 1.0
- **Answer Relevancy:** 1.0
- **Reason:** Câu trả lời phản ánh đúng ngữ cảnh và triệu chứng đã được trích xuất, đồng thời đề xuất đúng chuyên khoa Tai Mũi Họng phù hợp với triệu chứng của người bệnh.

### Case 20
**Query:** Ù tai, nghe kém, thỉnh choáng chóng mặt

**API Answer:** Bác sĩ chuyên về Tai Mũi Họng, có thể giúp chẩn đoán và điều trị các vấn đề liên quan đến ù tai và nghe kém.

- **Faithfulness:** 1.0
- **Answer Relevancy:** 1.0
- **Reason:** Câu trả lời phản ánh đúng ngữ cảnh và đề xuất bác sĩ Tai Mũi Họng phù hợp với triệu chứng ù tai và nghe kém, không bịa đặt thêm thông tin y khoa không có thật.

### Case 21
**Query:** Cảm giác có cục gì vướng ở cổ họng, khạc không ra nuốt không trôi

**API Answer:** Bác sĩ Trần Minh Giang chuyên về Tai Mũi Họng, có thể giúp bạn với triệu chứng vướng ở cổ họng.

- **Faithfulness:** 1.0
- **Answer Relevancy:** 1.0
- **Reason:** Câu trả lời phản ánh đúng ngữ cảnh và đề xuất bác sĩ chuyên khoa Tai Mũi Họng phù hợp với triệu chứng vướng ở cổ họng.

### Case 22
**Query:** Mắt nhìn mờ đi nhiều, cảm giác như có màn sương che trước mắt

**API Answer:** Bác sĩ chuyên về Mắt, có thể giúp chẩn đoán và điều trị các vấn đề về thị lực.

- **Faithfulness:** 1.0
- **Answer Relevancy:** 1.0
- **Reason:** Câu trả lời phản ánh đúng ngữ cảnh và đề xuất bác sĩ chuyên về Mắt phù hợp với triệu chứng nhìn mờ và cảm giác màn sương, không bịa đặt thêm thông tin y khoa.

### Case 23
**Query:** Đỏ mắt, cộm ngứa, chảy nhiều nước mắt, ra gỉ mắt nhiều vào buổi sáng

**API Answer:** Bác sĩ Nguyễn Định Quân chuyên về Mắt, có thể giúp bạn với triệu chứng đỏ mắt và ngứa.

- **Faithfulness:** 1.0
- **Answer Relevancy:** 1.0
- **Reason:** Câu trả lời phản ánh đúng ngữ cảnh và triệu chứng đã được trích xuất, đồng thời đề xuất đúng chuyên khoa Mắt phù hợp với tình trạng của người bệnh.

### Case 24
**Query:** Bố tôi bị tiểu đường, dạo này kêu mắt mờ không thấy rõ

**API Answer:** Bác sĩ chuyên về Mắt, có thể giúp kiểm tra tình trạng mắt của bố bạn.

- **Faithfulness:** 1.0
- **Answer Relevancy:** 1.0
- **Reason:** Câu trả lời phản ánh đúng ngữ cảnh và đề xuất bác sĩ chuyên khoa Mắt phù hợp với triệu chứng mắt mờ, không thấy rõ của bệnh nhân tiểu đường.

### Case 25
**Query:** Bé 3 tuổi sốt cao 39 độ, ho đờm, bỏ bú

**API Answer:** Bác sĩ chuyên về Nhi khoa, có thể giúp chẩn đoán và điều trị các triệu chứng ở trẻ nhỏ.

- **Faithfulness:** 1.0
- **Answer Relevancy:** 1.0
- **Reason:** Câu trả lời phản ánh đúng ngữ cảnh và đề xuất bác sĩ chuyên khoa phù hợp với triệu chứng đã được trích xuất.

### Case 26
**Query:** Trẻ đi ngoài phân lỏng, nôn trớ nhiều sau khi ăn

**API Answer:** Bác sĩ chuyên về Nhi khoa, có thể giúp chẩn đoán và điều trị các vấn đề tiêu hóa ở trẻ em.

- **Faithfulness:** 1.0
- **Answer Relevancy:** 1.0
- **Reason:** Câu trả lời phản ánh đúng ngữ cảnh và đề xuất chuyên khoa Nhi khoa phù hợp với triệu chứng đi ngoài phân lỏng và nôn trớ của trẻ.

### Case 27
**Query:** Bé bị mẩn ngứa thành từng mảng lớn ở hai má và khuỷu tay

**API Answer:** Bác sĩ chuyên về Da liễu, có thể giúp chẩn đoán và điều trị các vấn đề về da như mẩn ngứa.

- **Faithfulness:** 1.0
- **Answer Relevancy:** 1.0
- **Reason:** Câu trả lời thực tế phản ánh đúng ngữ cảnh và đề xuất bác sĩ chuyên về Da liễu, phù hợp với triệu chứng mẩn ngứa đã được nêu.

### Case 28
**Query:** Đau rát vùng thượng vị, hay bị đầy hơi chướng bụng sau ăn

**API Answer:** Bác sĩ chuyên về cơ xương khớp có thể giúp đánh giá các triệu chứng liên quan đến đau và khó chịu vùng bụng.

- **Faithfulness:** 0.0
- **Answer Relevancy:** 0.0
- **Reason:** Câu trả lời không phản ánh đúng ngữ cảnh và không đề xuất đúng chuyên khoa phù hợp với triệu chứng đã được cung cấp.

### Case 29
**Query:** Thường xuyên có cảm giác buồn nôn khi ngửi mùi thức ăn, da hơi vàng

**API Answer:** Bác sĩ chuyên về da liễu, có thể giúp kiểm tra tình trạng da vàng của bạn.

- **Faithfulness:** 0.0
- **Answer Relevancy:** 0.0
- **Reason:** Câu trả lời không phản ánh đúng ngữ cảnh và không đề xuất đúng chuyên khoa liên quan đến triệu chứng buồn nôn và da vàng. Bác sĩ chuyên về da liễu không phải là lựa chọn phù hợp cho tình trạng này.

### Case 30
**Query:** Sụt cân nhanh, đau âm ỉ hố chậu trái, hay bị táo bón xen lẫn tiêu chảy

**API Answer:** Bác sĩ Châu Thị Ngọc Ánh chuyên về Tiêu hóa - Gan mật, có thể giúp chẩn đoán và điều trị các vấn đề tiêu hóa liên quan đến triệu chứng của bạn.

- **Faithfulness:** 1.0
- **Answer Relevancy:** 1.0
- **Reason:** Câu trả lời phản ánh đúng ngữ cảnh và triệu chứng đã được trích xuất, đồng thời đề xuất bác sĩ chuyên khoa Tiêu hóa phù hợp với tình trạng của người bệnh.

### Case 31
**Query:** Rối loạn kinh nguyệt nhiều tháng nay, hay đau quặn bụng dưới

**API Answer:** Bác sĩ Phùng Huy Tuân chuyên về sản phụ khoa, có thể giúp bạn với rối loạn kinh nguyệt và đau bụng dưới.

- **Faithfulness:** 1.0
- **Answer Relevancy:** 1.0
- **Reason:** Câu trả lời phản ánh đúng ngữ cảnh và đề xuất bác sĩ phù hợp với triệu chứng đã nêu, không có thông tin sai lệch hay chẩn đoán không có thật.

### Case 32
**Query:** Ngứa rát vùng kín, ra khí hư có mùi hôi

**API Answer:** ThS.BS Giang Huỳnh Như chuyên về Sản phụ khoa, có thể giúp bạn với triệu chứng ngứa rát và khí hư.

- **Faithfulness:** 1.0
- **Answer Relevancy:** 1.0
- **Reason:** Câu trả lời phản ánh đúng ngữ cảnh và đề xuất bác sĩ chuyên khoa phù hợp với triệu chứng đã nêu.

### Case 33
**Query:** Phụ nữ 50 tuổi bị bốc hỏa, mất ngủ, chu kỳ kinh rất thưa

**API Answer:** Bác sĩ Phùng Huy Tuân chuyên về Sản phụ khoa, có thể giúp tư vấn về các vấn đề liên quan đến chu kỳ kinh nguyệt và bốc hỏa.

- **Faithfulness:** 1.0
- **Answer Relevancy:** 1.0
- **Reason:** Câu trả lời phản ánh đúng ngữ cảnh và lý do đề xuất bác sĩ phù hợp với các triệu chứng đã được trích xuất, đồng thời hướng đến đúng chuyên khoa Sản phụ khoa như trong đáp án tiêu chuẩn.

### Case 34
**Query:** Ho khan dai dẳng suốt cả tháng trời, ngứa rát họng

**API Answer:** Bác sĩ Nguyễn Văn Dương chuyên về Tai Mũi Họng, rất phù hợp với triệu chứng ho khan và ngứa rát họng của bạn.

- **Faithfulness:** 1.0
- **Answer Relevancy:** 0.0
- **Reason:** Mặc dù lý do đề xuất bác sĩ phù hợp với triệu chứng ho khan và ngứa rát họng, nhưng không hướng đến chuyên khoa Hô hấp như trong đáp án tiêu chuẩn, mà lại đề xuất bác sĩ chuyên về Tai Mũi Họng, điều này không hoàn toàn chính xác trong ngữ cảnh cần loại trừ nguyên nhân từ phổi hoặc phế quản.

### Case 35
**Query:** Khó thở khi nằm, ho có đờm xanh, có hút thuốc 10 năm

**API Answer:** Bác sĩ Nguyễn Đại Nam chuyên về hô hấp, có thể giúp bạn với triệu chứng khó thở và ho có đờm.

- **Faithfulness:** 1.0
- **Answer Relevancy:** 1.0
- **Reason:** Câu trả lời phản ánh đúng ngữ cảnh và đề xuất bác sĩ chuyên khoa hô hấp phù hợp với triệu chứng đã nêu.

### Case 36
**Query:** Cơn hen phế quản tái phát lúc chuyển trời, dùng thuốc xịt mới đỡ

**API Answer:** Bác sĩ Ngô Thị Tính chuyên về hô hấp, có thể giúp bạn quản lý cơn hen phế quản hiệu quả.

- **Faithfulness:** 1.0
- **Answer Relevancy:** 1.0
- **Reason:** Câu trả lời phản ánh đúng ngữ cảnh và đề xuất bác sĩ chuyên khoa Hô hấp phù hợp với triệu chứng cơn hen phế quản, không bịa đặt thêm thông tin y khoa.

### Case 37
**Query:** Sờ thấy cục cứng ở ngực trái, không đau nhưng phát triển nhanh

**API Answer:** Bác sĩ chuyên về ung bướu, có thể giúp đánh giá tình trạng cục cứng ở ngực.

- **Faithfulness:** 1.0
- **Answer Relevancy:** 1.0
- **Reason:** Câu trả lời phản ánh đúng ngữ cảnh và đề xuất bác sĩ chuyên khoa phù hợp với triệu chứng đã được trích xuất.

### Case 38
**Query:** Ho ra máu lượng ít nhưng thường xuyên, sụt 5kg trong 1 tháng

**API Answer:** Bác sĩ Phạm Xuân Dũng chuyên về ung bướu, có thể giúp đánh giá tình trạng ho ra máu và sụt cân.

- **Faithfulness:** 1.0
- **Answer Relevancy:** 1.0
- **Reason:** Câu trả lời phản ánh đúng ngữ cảnh và đề xuất bác sĩ chuyên về ung bướu, phù hợp với triệu chứng ho ra máu và sụt cân, không bịa đặt thêm thông tin y khoa.

### Case 39
**Query:** Nốt ruồi bỗng nhiên ngứa rỉ máu, bờ không đều

**API Answer:** Bác sĩ chuyên về ung bướu, có thể giúp đánh giá tình trạng nốt ruồi bất thường.

- **Faithfulness:** 1.0
- **Answer Relevancy:** 1.0
- **Reason:** Câu trả lời phản ánh đúng ngữ cảnh và không bịa đặt thêm thông tin, đồng thời hướng người dùng đến đúng chuyên khoa ung bướu như trong đáp án tiêu chuẩn.

### Case 40
**Query:** Nổi mẩn ngứa khắp người sau khi ăn hải sản

**API Answer:** Bác sĩ Huỳnh Khiêm Huy chuyên về da liễu, có thể giúp bạn với các vấn đề về da như nổi mẩn ngứa.

- **Faithfulness:** 1.0
- **Answer Relevancy:** 1.0
- **Reason:** Câu trả lời phản ánh đúng ngữ cảnh và đề xuất bác sĩ chuyên khoa phù hợp với triệu chứng nổi mẩn ngứa.

### Case 41
**Query:** Da bị tróc vảy trắng, ngứa ngáy dữ dội ở vùng khuỷu tay, đầu gối

**API Answer:** Bác sĩ chuyên về Da liễu, có thể giúp bạn với triệu chứng ngứa và tróc vảy trên da.

- **Faithfulness:** 1.0
- **Answer Relevancy:** 1.0
- **Reason:** Câu trả lời phản ánh đúng ngữ cảnh và đề xuất bác sĩ Da liễu phù hợp với triệu chứng được mô tả.

### Case 42
**Query:** Rụng tóc từng mảng lớn trên đỉnh đầu, thấy rõ cả da đầu

**API Answer:** Bác sĩ Trần Văn Đồng chuyên về da liễu, có thể giúp bạn với tình trạng rụng tóc.

- **Faithfulness:** 1.0
- **Answer Relevancy:** 1.0
- **Reason:** Câu trả lời phản ánh đúng ngữ cảnh và đề xuất bác sĩ chuyên khoa phù hợp với triệu chứng rụng tóc từng mảng lớn.

### Case 43
**Query:** Khát nước liên tục, đi tiểu nhiều, sụt cân dù ăn nhiều

**API Answer:** Bác sĩ chuyên về nội tiết, có thể giúp đánh giá các triệu chứng liên quan đến hormone và chuyển hóa.

- **Faithfulness:** 1.0
- **Answer Relevancy:** 1.0
- **Reason:** Câu trả lời phản ánh đúng ngữ cảnh và đề xuất bác sĩ chuyên về nội tiết phù hợp với triệu chứng đã nêu, không bịa đặt thêm thông tin y khoa.

### Case 44
**Query:** Cổ to ra, hay run tay, nhịp tim nhanh, vã mồ hôi

**API Answer:** Bác sĩ có chuyên môn về Tim mạch và Hô hấp, phù hợp với triệu chứng nhịp tim nhanh và vã mồ hôi.

- **Faithfulness:** 0.0
- **Answer Relevancy:** 0.0
- **Reason:** Câu trả lời không phản ánh đúng ngữ cảnh và không đề xuất đúng chuyên khoa phù hợp với triệu chứng đã được nêu trong Reference Answer.


