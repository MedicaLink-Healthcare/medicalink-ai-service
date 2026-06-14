# BÁO CÁO KẾT QUẢ ĐÁNH GIÁ (RAG EVALUATION REPORT)

**Chế độ thực thi:** REAL

## 1. Chi tiết theo từng chuyên khoa

### Chuyên khoa: Nội tổng quát
- **ID Chuyên khoa:** `cmnde90369e8b17431587bedd`
- **Số lượng Test Case:** 15

| STT | Câu truy vấn (Query) | Phủ định (Negations) | API Status | Kết quả (Result) |
|---|---|---|---|---|
| 1 | Tôi muốn đăng ký khám sức khỏe tổng quát định kỳ để kiểm tra toàn diện | - | SUCCESS | ✅ Passed |
| 2 | Cơ thể hay bị suy nhược, người mệt mỏi rã rời kéo dài mà không rõ nguyên nhân bệnh gì | - | SUCCESS | ✅ Passed |
| 3 | Cần tư vấn và khám sức khỏe tổng thể để hoàn thiện hồ sơ xin việc | - | SUCCESS | ✅ Passed |
| 4 | Gần đây tôi ăn uống kém, ngủ không ngon giấc, người cứ lờ đờ uể oải cả ngày | - | ROUTE_FAILED | ❌ Failed |
| 5 | Tôi muốn làm xét nghiệm máu tổng quát để kiểm tra các chỉ số cơ bản hàng năm | - | SUCCESS | ✅ Passed |
| 6 | Hay bị ốm vặt, sức đề kháng kém, muốn khám nội khoa xem cơ thể có thiếu hụt chất gì không | - | SUCCESS | ✅ Passed |
| 7 | Cơ thể bị suy nhược sau một đợt ốm dài ngày, cần khám bác sĩ nội chung để phục hồi thể trạng | - | ROUTE_FAILED | ❌ Failed |
| 8 | Xin tư vấn gói tầm soát sức khỏe toàn diện cho nam giới trên 40 tuổi | - | SUCCESS | ✅ Passed |
| 9 | Tôi cảm thấy trong người không được khỏe nhưng không rõ triệu chứng cụ thể, muốn khám tổng quát trước | - | SUCCESS | ✅ Passed |
| 10 | Cần đo các chỉ số cơ thể cơ bản, khám sức khoẻ tổng quát và siêu âm ổ bụng định kỳ | - | SUCCESS | ✅ Passed |
| 11 | Người lớn tuổi dạo này ăn ngủ kém, muốn bác sĩ nội khoa khám tổng thể kiểm tra sức khỏe | - | ROUTE_FAILED | ❌ Failed |
| 12 | Sụt cân nhẹ, người mệt mỏi nhưng không ho không sốt, muốn khám nội khoa chung tìm nguyên nhân | không ho, không sốt | SUCCESS | ✅ Passed |
| 13 | Cần khám sức khỏe tiền hôn nhân tổng hợp cho 2 vợ chồng | - | SUCCESS | ✅ Passed |
| 14 | Đăng ký gói khám bệnh định kỳ cho nhân viên văn phòng bao gồm khám nội chung | - | SUCCESS | ✅ Passed |
| 15 | Tôi muốn khám các bệnh lý nội khoa thông thường và làm xét nghiệm kiểm tra sức khỏe hàng năm | - | SUCCESS | ✅ Passed |

### Chuyên khoa: Tim mạch
- **ID Chuyên khoa:** `cmn305ee71e46d24f2396fe68`
- **Số lượng Test Case:** 15

| STT | Câu truy vấn (Query) | Phủ định (Negations) | API Status | Kết quả (Result) |
|---|---|---|---|---|
| 1 | Đau thắt ngực trái, mệt mỏi khi leo cầu thang, không ho | không ho | SUCCESS | ✅ Passed |
| 2 | Hồi hộp đánh trống ngực, nhịp tim nhanh lúc nghỉ ngơi | - | SUCCESS | ✅ Passed |
| 3 | Thường xuyên hoa mắt khi đứng lên ngồi xuống, có tiền sử tăng huyết áp | - | ROUTE_FAILED | ❌ Failed |
| 4 | Tôi hay bị nặng ngực, thỉnh thoảng nhói lên từng cơn | - | SUCCESS | ✅ Passed |
| 5 | Tự nhiên tim đập mạnh như muốn rớt ra ngoài, kèm vã mồ hôi lạnh | - | SUCCESS | ✅ Passed |
| 6 | Chân tôi dạo này bị phù nề, ấn vào lõm, hay khó thở khi nằm | - | ROUTE_FAILED | ❌ Failed |
| 7 | Đang uống thuốc huyết áp nhưng dạo này đo vẫn thấy 150/90 | - | SUCCESS | ✅ Passed |
| 8 | Ngực trái hay bị nhói đau lan ra cánh tay và sau lưng | - | SUCCESS | ✅ Passed |
| 9 | Mỗi lần đi bộ nhanh là tôi thấy hụt hơi, ngực nặng đè nén | - | SUCCESS | ✅ Passed |
| 10 | Tim đập bỏ nhịp, cảm giác hẫng một nhịp rồi lại đập bình thường | - | SUCCESS | ✅ Passed |
| 11 | Sáng sớm thức dậy hay bị choáng váng, mắt tối sầm lại | - | ROUTE_FAILED | ❌ Failed |
| 12 | Tôi bị hở van tim 2 lá nhẹ, nay muốn đi tái khám xem có tiến triển nặng không | - | ROUTE_FAILED | ❌ Failed |
| 13 | Hay bị mệt mỏi, khó thở về đêm phải ngồi dậy mới thở được | - | ROUTE_FAILED | ❌ Failed |
| 14 | Thỉnh thoảng có cảm giác đau ran ở vùng trước tim, lan lên cằm | - | SUCCESS | ✅ Passed |
| 15 | Bà nội tôi bị suy tim, gần đây bà kêu hay bị mệt và ho khan | - | ROUTE_FAILED | ❌ Failed |

### Chuyên khoa: Thần kinh
- **ID Chuyên khoa:** `cmne6870ce72d43457881a7dd`
- **Số lượng Test Case:** 15

| STT | Câu truy vấn (Query) | Phủ định (Negations) | API Status | Kết quả (Result) |
|---|---|---|---|---|
| 1 | Hay bị đau nửa đầu bên phải, giật từng cơn, buồn nôn | - | SUCCESS | ✅ Passed |
| 2 | Tay chân hay bị tê rần, đôi lúc run tay khi cầm nắm đồ vật | - | SUCCESS | ✅ Passed |
| 3 | Mất ngủ kéo dài, trí nhớ giảm sút nghiêm trọng, hay quên | - | SUCCESS | ✅ Passed |
| 4 | Bị chóng mặt quay cuồng, thấy nhà cửa lộn nhào khi thay đổi tư thế | - | SUCCESS | ✅ Passed |
| 5 | Cảm giác châm chích như kiến bò ở lòng bàn chân và các ngón tay | - | SUCCESS | ✅ Passed |
| 6 | Đau đầu dữ dội vùng thái dương, uống thuốc giảm đau không bớt | - | SUCCESS | ✅ Passed |
| 7 | Mặt tự nhiên bị giật nhẹ ở khóe mắt và mép miệng | - | ROUTE_FAILED | ❌ Failed |
| 8 | Dạo này hay bị líu lưỡi, nói ngọng một lúc rồi hết | - | ROUTE_FAILED | ❌ Failed |
| 9 | Thỉnh thoảng bị yếu nửa người bên trái, cầm đồ vật hay bị rơi | - | SUCCESS | ✅ Passed |
| 10 | Khó đi vào giấc ngủ, trằn trọc cả đêm, sáng dậy người đờ đẫn | - | SUCCESS | ✅ Passed |
| 11 | Ông tôi bị Parkinson, dạo này tay ông run nhiều hơn | - | SUCCESS | ✅ Passed |
| 12 | Hay bị choáng váng, xây xẩm mặt mày, cảm giác đi không vững | - | SUCCESS | ✅ Passed |
| 13 | Thường xuyên bị đau giật từ gáy lên đỉnh đầu | - | SUCCESS | ✅ Passed |
| 14 | Tôi bị mất ngủ mãn tính, đã dùng nhiều loại thuốc thảo dược không ăn thua | - | SUCCESS | ✅ Passed |
| 15 | Trí nhớ dạo này kém quá, đi chợ quên mua đồ hoài, có phải bị Alzheimer không | - | SUCCESS | ✅ Passed |

### Chuyên khoa: Cơ xương khớp
- **ID Chuyên khoa:** `cmn6f922b051e05454388c512`
- **Số lượng Test Case:** 15

| STT | Câu truy vấn (Query) | Phủ định (Negations) | API Status | Kết quả (Result) |
|---|---|---|---|---|
| 1 | Đau nhức hai khớp gối khi đi lại nhiều, kêu lạo xạo | - | SUCCESS | ✅ Passed |
| 2 | Sáng ngủ dậy hay bị cứng khớp bàn tay, đau buốt | - | SUCCESS | ✅ Passed |
| 3 | Đau thắt lưng lan xuống chân trái, ngồi lâu rất buốt | - | SUCCESS | ✅ Passed |
| 4 | Khớp ngón chân cái sưng tấy đỏ, đau nhức khủng khiếp sau khi ăn hải sản | - | SUCCESS | ✅ Passed |
| 5 | Cổ tay bị sưng và đau khi cử động, nhất là lúc vặn vòi nước | - | SUCCESS | ✅ Passed |
| 6 | Đau mỏi vai gáy kinh niên, cúi ngửa cổ rất khó khăn | - | SUCCESS | ✅ Passed |
| 7 | Gót chân đau thấu xương mỗi khi bước xuống giường vào buổi sáng | - | SUCCESS | ✅ Passed |
| 8 | Bị ngã chống tay xuống đất, giờ khuỷu tay sưng to và không gập lại được | - | ROUTE_FAILED | ❌ Failed |
| 9 | Khớp háng bên phải đau nhói khi bước đi, nằm nghiêng cũng đau | - | SUCCESS | ✅ Passed |
| 10 | Các khớp ngón tay bị sưng nề, biến dạng nhẹ, đau âm ỉ | - | SUCCESS | ✅ Passed |
| 11 | Tôi bị thoái hóa cột sống cổ, dạo này đau lan ra hai bả vai | - | SUCCESS | ✅ Passed |
| 12 | Đau nhức trong xương mỗi khi thời tiết thay đổi, không sốt | không sốt | SUCCESS | ✅ Passed |
| 13 | Đầu gối hay bị sưng phù có dịch, đi lại thấy nặng nề | - | SUCCESS | ✅ Passed |
| 14 | Đau ê ẩm dọc hai bắp chân về đêm, thỉnh thoảng bị chuột rút | - | SUCCESS | ✅ Passed |
| 15 | Mẹ tôi bị loãng xương, nay đau cột sống thắt lưng không ngồi lâu được | - | SUCCESS | ✅ Passed |

### Chuyên khoa: Tiết niệu
- **ID Chuyên khoa:** `cmn0d8db982b8a74ee1808972`
- **Số lượng Test Case:** 15

| STT | Câu truy vấn (Query) | Phủ định (Negations) | API Status | Kết quả (Result) |
|---|---|---|---|---|
| 1 | Đi tiểu buốt, dắt, nước tiểu có lẫn máu tươi | - | SUCCESS | ✅ Passed |
| 2 | Đau quặn hông lưng phải, lan xuống bụng dưới | - | ROUTE_FAILED | ❌ Failed |
| 3 | Tiểu đêm nhiều lần, cảm giác đi tiểu không hết bãi | - | ROUTE_FAILED | ❌ Failed |
| 4 | Tôi bị tiểu rắt, cứ 15 phút lại buồn tiểu mà mỗi lần được rất ít | - | SUCCESS | ✅ Passed |
| 5 | Nước tiểu đục, có mùi hôi nồng, thỉnh thoảng ớn lạnh | - | SUCCESS | ✅ Passed |
| 6 | Nam giới 60 tuổi, đi tiểu phải rặn mạnh, tia nước yếu | - | ROUTE_FAILED | ❌ Failed |
| 7 | Đau tức vùng bụng dưới, đi tiểu thấy rát ở đầu niệu đạo | - | SUCCESS | ✅ Passed |
| 8 | Đau nhói vùng thắt lưng lan xuống háng, từng bị sỏi thận 2 năm trước | - | ROUTE_FAILED | ❌ Failed |
| 9 | Nước tiểu có màu đỏ như nước rửa thịt, không đau bụng | đau bụng | SUCCESS | ✅ Passed |
| 10 | Tôi hay bị són tiểu khi ho hoặc hắt hơi mạnh | - | SUCCESS | ✅ Passed |
| 11 | Đi tiểu ra cặn trắng lợn cợn, đôi lúc có cảm giác tắc nghẽn | - | ROUTE_FAILED | ❌ Failed |
| 12 | Sưng đau vùng tinh hoàn bên trái, đi lại rất tức | - | ROUTE_FAILED | ❌ Failed |
| 13 | Xét nghiệm siêu âm có sỏi niệu quản 6mm, cần tư vấn tán sỏi | - | SUCCESS | ✅ Passed |
| 14 | Tôi hay bị tiểu buốt sau khi quan hệ tình dục | - | SUCCESS | ✅ Passed |
| 15 | Bác sĩ trước chẩn đoán tôi bị phì đại tuyến tiền liệt, nay tiểu khó hơn | - | SUCCESS | ✅ Passed |

### Chuyên khoa: Răng Hàm Mặt
- **ID Chuyên khoa:** `cmn60eafc3e66444b2a851b8d`
- **Số lượng Test Case:** 15

| STT | Câu truy vấn (Query) | Phủ định (Negations) | API Status | Kết quả (Result) |
|---|---|---|---|---|
| 1 | Đau nhức răng hàm dưới, nướu sưng đỏ, nhai thức ăn rất buốt | - | SUCCESS | ✅ Passed |
| 2 | Răng khôn mọc lệch đâm vào má, đau nhức liên tục | - | SUCCESS | ✅ Passed |
| 3 | Chảy máu chân răng nhiều khi đánh răng, miệng có mùi hôi | - | SUCCESS | ✅ Passed |
| 4 | Một chiếc răng cửa của tôi bị lung lay sau khi nhai phải sạn | - | SUCCESS | ✅ Passed |
| 5 | Răng hàm số 6 bị vỡ một mảng lớn, ăn uống hay bị nhét thức ăn | - | SUCCESS | ✅ Passed |
| 6 | Nướu răng bị tụt, uống nước đá là ê buốt tận óc | - | SUCCESS | ✅ Passed |
| 7 | Khớp thái dương hàm hay kêu lục cục khi há miệng to | - | SUCCESS | ✅ Passed |
| 8 | Sáng ngủ dậy hay bị mỏi hàm, có người bảo tôi hay nghiến răng lúc ngủ | - | SUCCESS | ✅ Passed |
| 9 | Trám răng được 1 năm giờ chỗ trám bị đổi màu và hơi nhức | - | ROUTE_FAILED | ❌ Failed |
| 10 | Miệng hay bị lở loét (nhiệt miệng) tái phát nhiều lần | - | SUCCESS | ✅ Passed |
| 11 | Răng số 8 sưng mủ, há miệng ra rất đau | - | SUCCESS | ✅ Passed |
| 12 | Tôi muốn tư vấn cấy ghép Implant cho 2 chiếc răng hàm bị mất lâu năm | - | ROUTE_FAILED | ❌ Failed |
| 13 | Lợi bị sưng cục mủ có màu trắng, ấn vào chảy mủ | - | ROUTE_FAILED | ❌ Failed |
| 14 | Bọc răng sứ được 2 năm giờ viền nướu bị đen và viêm đỏ | - | SUCCESS | ✅ Passed |
| 15 | Con tôi 7 tuổi, răng cửa mọc lộn xộn, muốn khám niềng răng | - | SUCCESS | ✅ Passed |

### Chuyên khoa: Tai Mũi Họng
- **ID Chuyên khoa:** `cmn388a64a878494c57b1c0f2`
- **Số lượng Test Case:** 15

| STT | Câu truy vấn (Query) | Phủ định (Negations) | API Status | Kết quả (Result) |
|---|---|---|---|---|
| 1 | Ngạt mũi kéo dài, chảy dịch vàng, đau nhức vùng trán | - | SUCCESS | ✅ Passed |
| 2 | Đau họng, nuốt vướng, có đờm nhưng không sốt | không sốt | SUCCESS | ✅ Passed |
| 3 | Ù tai, nghe kém, thỉnh thoảng chóng mặt | - | SUCCESS | ✅ Passed |
| 4 | Ho khan dai dẳng 3 tuần, cảm giác lúc nào cũng ngứa cổ họng | - | SUCCESS | ✅ Passed |
| 5 | Chảy máu cam liên tục 2 ngày nay, mỗi lần 1 ít | - | SUCCESS | ✅ Passed |
| 6 | Tôi bị mất khứu giác, ngửi mùi không thấy rõ, hay nghẹt mũi | - | SUCCESS | ✅ Passed |
| 7 | Tai bên phải có dịch chảy ra mùi hôi, hơi đau tức | - | SUCCESS | ✅ Passed |
| 8 | Hay bị hắt hơi liên tục vào buổi sáng, ngứa mũi, chảy nước mũi trong | - | SUCCESS | ✅ Passed |
| 9 | Cảm giác có cục gì vướng ở cổ họng, khạc không ra nuốt không trôi | - | SUCCESS | ✅ Passed |
| 10 | Trẻ nhỏ ngủ hay ngáy to, thở há miệng | - | SUCCESS | ✅ Passed |
| 11 | Đau rát họng dữ dội, soi gương thấy có mủ trắng ở amidan | - | SUCCESS | ✅ Passed |
| 12 | Bị ù tai như tiếng ve kêu liên tục trong đầu, rất khó chịu | - | SUCCESS | ✅ Passed |
| 13 | Giọng bị khàn đặc, thỉnh thoảng mất giọng nói, đã 1 tuần rồi | - | SUCCESS | ✅ Passed |
| 14 | Hay bị đau nửa mặt quanh mũi, cúi đầu xuống là ê buốt | - | ROUTE_FAILED | ❌ Failed |
| 15 | Tôi muốn cắt amidan vì năm nay viêm sưng 5-6 lần rồi | - | SUCCESS | ✅ Passed |

### Chuyên khoa: Mắt
- **ID Chuyên khoa:** `cmnd3d0cbae4b8e497c960246`
- **Số lượng Test Case:** 15

| STT | Câu truy vấn (Query) | Phủ định (Negations) | API Status | Kết quả (Result) |
|---|---|---|---|---|
| 1 | Mắt nhìn mờ đi nhiều, cảm giác như có màn sương che trước mắt | - | SUCCESS | ✅ Passed |
| 2 | Đỏ mắt, cộm ngứa, chảy nhiều nước mắt, ra gỉ mắt nhiều vào buổi sáng | - | SUCCESS | ✅ Passed |
| 3 | Bị chói sáng, đau nhức hốc mắt, thị lực giảm nhanh | - | SUCCESS | ✅ Passed |
| 4 | Thấy hiện tượng ruồi bay lởn vởn trước mắt phải | - | SUCCESS | ✅ Passed |
| 5 | Nhìn một vật thành hai (song thị), hay mỏi mắt khi dùng máy tính | - | SUCCESS | ✅ Passed |
| 6 | Mí mắt bị sưng đỏ, nổi cục mụn nhỏ hơi đau nhức | - | SUCCESS | ✅ Passed |
| 7 | Khô mắt rát, lúc nào cũng phải chớp mắt liên tục | - | SUCCESS | ✅ Passed |
| 8 | Trẻ con xem TV hay phải nheo mắt và tiến lại gần | - | SUCCESS | ✅ Passed |
| 9 | Tự nhiên mắt trái bị đỏ ngầu đốm máu nhỏ, không đau | không đau | SUCCESS | ✅ Passed |
| 10 | Bố tôi bị tiểu đường, dạo này kêu mắt mờ không thấy rõ | - | SUCCESS | ✅ Passed |
| 11 | Mắt hay bị giật liên hồi ở vùng mi dưới | - | SUCCESS | ✅ Passed |
| 12 | Khám đo kính cận định kỳ vì dạo này nhìn xa không rõ | - | ROUTE_FAILED | ❌ Failed |
| 13 | Nhìn các đường thẳng bị cong vẹo, nhìn chữ hay bị nhòe | - | ROUTE_FAILED | ❌ Failed |
| 14 | Có dị vật bay vào mắt hôm qua, nay cộm và xốn quá | - | SUCCESS | ✅ Passed |
| 15 | Đau nhức dữ dội lan lên đầu, mắt đỏ, sờ vào thấy căng cứng | - | SUCCESS | ✅ Passed |

### Chuyên khoa: Nhi khoa
- **ID Chuyên khoa:** `cmnc6a6270904534d49a4c532`
- **Số lượng Test Case:** 15

| STT | Câu truy vấn (Query) | Phủ định (Negations) | API Status | Kết quả (Result) |
|---|---|---|---|---|
| 1 | Bé 3 tuổi sốt cao 39 độ, ho đờm, bỏ bú | - | SUCCESS | ✅ Passed |
| 2 | Trẻ đi ngoài phân lỏng, nôn trớ nhiều sau khi ăn | - | SUCCESS | ✅ Passed |
| 3 | Bé có nhiều mẩn đỏ ở tay chân, miệng có vết loét | - | SUCCESS | ✅ Passed |
| 4 | Con tôi 5 tuổi khóc đêm hoài, hay đưa tay gãi tai | - | SUCCESS | ✅ Passed |
| 5 | Trẻ 1 tuổi lười ăn, chậm tăng cân, da xanh xao | - | SUCCESS | ✅ Passed |
| 6 | Bé bị thở khò khè, lõm ngực mỗi lần hít vào | - | SUCCESS | ✅ Passed |
| 7 | Nổi ban đỏ khắp mình mẩy sau khi sốt 3 ngày | - | SUCCESS | ✅ Passed |
| 8 | Trẻ hay bị chảy máu cam vô cớ, đổ mồ hôi trộm | - | SUCCESS | ✅ Passed |
| 9 | Cháu nhà tôi 2 tuổi đi cầu phân sống, lợn cợn hạt | - | SUCCESS | ✅ Passed |
| 10 | Bé bị táo bón nặng, 3-4 ngày mới đi rặn khóc thét | - | SUCCESS | ✅ Passed |
| 11 | Sốt nhẹ, ho khan, nước mũi chảy dầm dề ở trẻ 6 tháng | - | SUCCESS | ✅ Passed |
| 12 | Bé bị mẩn ngứa thành từng mảng lớn ở hai má và khuỷu tay | - | SUCCESS | ✅ Passed |
| 13 | Trẻ 8 tuổi hay kêu đau mỏi hai chân về đêm | - | SUCCESS | ✅ Passed |
| 14 | Bé bị hóc xương cá, khóc nhiều và không chịu nuốt nước bọt | - | SUCCESS | ✅ Passed |
| 15 | Muốn khám dinh dưỡng cho bé 4 tuổi bị thấp còi so với bạn bè | - | SUCCESS | ✅ Passed |

### Chuyên khoa: Tiêu hóa - Gan mật
- **ID Chuyên khoa:** `cmna8cf9e42b9c14beca968d2`
- **Số lượng Test Case:** 15

| STT | Câu truy vấn (Query) | Phủ định (Negations) | API Status | Kết quả (Result) |
|---|---|---|---|---|
| 1 | Tôi hay bị ợ chua lúc rạng sáng nhưng không buồn nôn | buồn nôn | SUCCESS | ✅ Passed |
| 2 | Đau vùng dạ dày, uống thuốc dạ dày không đỡ, đi cầu phân đen | - | SUCCESS | ✅ Passed |
| 3 | Bụng sôi ọt ọt liên tục, tiêu chảy ngày 3 lần, không sốt | không sốt | SUCCESS | ✅ Passed |
| 4 | Đau rát vùng thượng vị, hay bị đầy hơi chướng bụng sau ăn | - | ROUTE_FAILED | ❌ Failed |
| 5 | Ăn thức ăn dầu mỡ vào là hay bị đau tức hạ sườn phải | - | ROUTE_FAILED | ❌ Failed |
| 6 | Thường xuyên có cảm giác buồn nôn khi ngửi mùi thức ăn, da hơi vàng | - | ROUTE_FAILED | ❌ Failed |
| 7 | Cứ ăn đồ lạ là đau bụng quặn thắt, đi ngoài phân lỏng nhiều lần | - | ROUTE_FAILED | ❌ Failed |
| 8 | Phân hay dẹt, có nhầy máu đỏ tươi bám quanh | - | ROUTE_FAILED | ❌ Failed |
| 9 | Sụt cân nhanh, đau âm ỉ hố chậu trái, hay bị táo bón xen lẫn tiêu chảy | - | ROUTE_FAILED | ❌ Failed |
| 10 | Tôi bị xơ gan, dạo này thấy bụng to ra căng tức | - | ROUTE_FAILED | ❌ Failed |
| 11 | Hay bị đắng miệng buổi sáng, nôn khan, cảm giác mệt mỏi | - | ROUTE_FAILED | ❌ Failed |
| 12 | Đau quặn bụng thành từng cơn, bụng chướng to đánh rắm không được | - | ROUTE_FAILED | ❌ Failed |
| 13 | Men gan cao gấp 3 lần, đang cần tìm bác sĩ chuyên khoa điều trị | - | SUCCESS | ✅ Passed |
| 14 | Tôi mới nội soi dạ dày có HP dương tính, cần tư vấn phác đồ | - | ROUTE_FAILED | ❌ Failed |
| 15 | Hay bị nấc cụt dai dẳng, thỉnh thoảng nuốt nghẹn | - | ROUTE_FAILED | ❌ Failed |

### Chuyên khoa: Sản phụ khoa
- **ID Chuyên khoa:** `cmn4132816e364b4603a2fed9`
- **Số lượng Test Case:** 15

| STT | Câu truy vấn (Query) | Phủ định (Negations) | API Status | Kết quả (Result) |
|---|---|---|---|---|
| 1 | Rối loạn kinh nguyệt nhiều tháng nay, hay đau quặn bụng dưới | - | SUCCESS | ✅ Passed |
| 2 | Trễ kinh 2 tuần, thử que 2 vạch, nay thấy ra ít máu | - | SUCCESS | ✅ Passed |
| 3 | Ngứa rát vùng kín, ra khí hư có mùi hôi | - | SUCCESS | ✅ Passed |
| 4 | Đau bụng dữ dội ngày hành kinh, phải uống thuốc giảm đau mới đỡ | - | ROUTE_FAILED | ❌ Failed |
| 5 | Tôi siêu âm có nhân xơ tử cung 30mm, nay thấy hay bị rong kinh | - | SUCCESS | ✅ Passed |
| 6 | Đau buốt khi quan hệ, tiểu rắt, cảm giác rất rát | - | ROUTE_FAILED | ❌ Failed |
| 7 | Khí hư ra nhiều màu vàng xanh bã đậu, ngứa ngáy khó chịu | - | SUCCESS | ✅ Passed |
| 8 | Phụ nữ 50 tuổi bị bốc hỏa, mất ngủ, chu kỳ kinh rất thưa | - | SUCCESS | ✅ Passed |
| 9 | Ra máu bất thường giữa chu kỳ, màu đen sẫm | - | ROUTE_FAILED | ❌ Failed |
| 10 | Tôi mang thai 12 tuần, muốn siêu âm đo độ mờ da gáy | - | SUCCESS | ✅ Passed |
| 11 | Hay bị rỉ nước ối non khi đang bầu 34 tuần, bụng hơi gò cứng | - | ROUTE_FAILED | ❌ Failed |
| 12 | Kết hôn 2 năm chưa có thai dù không kế hoạch, kinh nguyệt không đều | - | SUCCESS | ✅ Passed |
| 13 | Đau tức vùng vú trước chu kỳ kinh, sờ thấy cục cứng nhỏ lổn nhổn | - | ROUTE_FAILED | ❌ Failed |
| 14 | Ra huyết trắng nhiều, thỉnh thoảng đau nhói một bên buồng trứng | - | SUCCESS | ✅ Passed |
| 15 | Muốn đặt vòng tránh thai cần khám tư vấn trước | - | ROUTE_FAILED | ❌ Failed |

### Chuyên khoa: Hô hấp
- **ID Chuyên khoa:** `cmn25b8987d232447e8bd9517`
- **Số lượng Test Case:** 15

| STT | Câu truy vấn (Query) | Phủ định (Negations) | API Status | Kết quả (Result) |
|---|---|---|---|---|
| 1 | Khó thở khi nằm, ho có đờm xanh, có hút thuốc 10 năm | - | SUCCESS | ✅ Passed |
| 2 | Sốt nhẹ về chiều, ho ra máu lượng ít, sụt cân | - | SUCCESS | ✅ Passed |
| 3 | Thở khò khè, hay hụt hơi, đã từng bị lao phổi | - | SUCCESS | ✅ Passed |
| 4 | Ho khan dai dẳng suốt cả tháng trời, ngứa rát họng | - | SUCCESS | ✅ Passed |
| 5 | Cơn hen phế quản tái phát lúc chuyển trời, dùng thuốc xịt mới đỡ | - | SUCCESS | ✅ Passed |
| 6 | Tức ngực, khó thở nhiều khi đi lại, làm việc nhà lặt vặt cũng mệt | - | SUCCESS | ✅ Passed |
| 7 | Ho khạc ra đờm đục, mệt mỏi, hơi sốt vào buổi sáng | - | ROUTE_FAILED | ❌ Failed |
| 8 | Bệnh nhân COPD nay khó thở nhiều hơn, đờm vàng đặc | - | SUCCESS | ✅ Passed |
| 9 | Đau nhói ngực trái mỗi khi hít thở sâu hoặc ho | - | ROUTE_FAILED | ❌ Failed |
| 10 | Dạo này ngủ hay bị ngưng thở, ngáy to, sáng dậy đau đầu | - | ROUTE_FAILED | ❌ Failed |
| 11 | Cứ đêm là ho rũ rượi, ho không kiểm soát được | - | SUCCESS | ✅ Passed |
| 12 | Tràn dịch màng phổi đã điều trị, nay muốn tái khám do ho lại | - | SUCCESS | ✅ Passed |
| 13 | Sau hậu Covid tôi vẫn bị hụt hơi, làm việc mau mệt | - | SUCCESS | ✅ Passed |
| 14 | Tự nhiên khó thở ngột ngạt, tím tái cả môi sau khi gắng sức | - | SUCCESS | ✅ Passed |
| 15 | Ho có tiếng rít thanh quản, rát cổ, nuốt đau | - | SUCCESS | ✅ Passed |

### Chuyên khoa: Ung bướu
- **ID Chuyên khoa:** `cmn05e2799db9c54691854315`
- **Số lượng Test Case:** 15

| STT | Câu truy vấn (Query) | Phủ định (Negations) | API Status | Kết quả (Result) |
|---|---|---|---|---|
| 1 | Sờ thấy cục cứng ở ngực trái, không đau nhưng phát triển nhanh | không đau | SUCCESS | ✅ Passed |
| 2 | Nổi hạch ở cổ lâu ngày không xẹp, sụt cân nhanh | - | SUCCESS | ✅ Passed |
| 3 | Cần tư vấn về phác đồ hóa trị cho K đại tràng giai đoạn 2 | - | ROUTE_FAILED | ❌ Failed |
| 4 | Khàn tiếng kéo dài, sờ thấy cổ sưng to một bên | - | ROUTE_FAILED | ❌ Failed |
| 5 | Cục bướu trên da lưng thay đổi màu sắc và to lên nhanh chóng | - | SUCCESS | ✅ Passed |
| 6 | Ho ra máu lượng ít nhưng thường xuyên, sụt 5kg trong 1 tháng | - | SUCCESS | ✅ Passed |
| 7 | Đi tiêu ra máu bầm, phân dẹt, gia đình có người bị ung thư đại trực tràng | - | SUCCESS | ✅ Passed |
| 8 | Nuốt vướng, cảm giác có khối u ở họng, nghẹn khi ăn đồ đặc | - | SUCCESS | ✅ Passed |
| 9 | Nổi cục sưng to ở nách, ấn vào thấy cứng và dính chặt | - | SUCCESS | ✅ Passed |
| 10 | Sau xạ trị ung thư vú nay tôi hay bị phù tay bên trái | - | ROUTE_FAILED | ❌ Failed |
| 11 | Sờ thấy nhân tuyến giáp cứng chắc, di động theo nhịp nuốt | - | ROUTE_FAILED | ❌ Failed |
| 12 | Tiểu ra máu không đau rát, kéo dài mấy hôm nay | - | SUCCESS | ✅ Passed |
| 13 | Phát hiện khối u buồng trứng kích thước 5x6cm, cần khám chuyên sâu | - | SUCCESS | ✅ Passed |
| 14 | Nốt ruồi bỗng nhiên ngứa rỉ máu, bờ không đều | - | ROUTE_FAILED | ❌ Failed |
| 15 | Ung thư gan đang giai đoạn cuối cần tư vấn chăm sóc giảm nhẹ | - | ROUTE_FAILED | ❌ Failed |

### Chuyên khoa: Da liễu
- **ID Chuyên khoa:** `cmn9a464d69a3c64f3f856cd8`
- **Số lượng Test Case:** 15

| STT | Câu truy vấn (Query) | Phủ định (Negations) | API Status | Kết quả (Result) |
|---|---|---|---|---|
| 1 | Nổi mẩn ngứa khắp người sau khi ăn hải sản | - | SUCCESS | ✅ Passed |
| 2 | Da bị tróc vảy trắng, ngứa ngáy dữ dội ở vùng khuỷu tay, đầu gối | - | SUCCESS | ✅ Passed |
| 3 | Nhiều mụn bọc sưng đỏ ở mặt, để lại sẹo rỗ | - | SUCCESS | ✅ Passed |
| 4 | Dưới nếp gấp ngực bị đỏ rát, có dịch rỉ ướt, ngứa nhiều | - | SUCCESS | ✅ Passed |
| 5 | Kẽ ngón chân bị nứt nẻ, lột da, rất ngứa khi lội nước | - | SUCCESS | ✅ Passed |
| 6 | Trên da xuất hiện các nốt bọng nước mọc thành chùm dọc theo mạn sườn, rát buốt | - | SUGGEST_FAILED | ❌ Failed |
| 7 | Mảng da ở tay bị mất sắc tố, trắng loang lổ | - | SUGGEST_FAILED | ❌ Failed |
| 8 | Da dạo này sạm nám 2 bên gò má rất nhiều | - | SUGGEST_FAILED | ❌ Failed |
| 9 | Rụng tóc từng mảng lớn trên đỉnh đầu, thấy rõ cả da đầu | - | SUGGEST_FAILED | ❌ Failed |
| 10 | Móng tay bị dày sừng, màu vàng đục, mủn ra | - | SUGGEST_FAILED | ❌ Failed |
| 11 | Nổi nhiều mụn nước li ti ngứa ngáy ở lòng bàn tay bàn chân | - | SUGGEST_FAILED | ❌ Failed |
| 12 | Bé nhà tôi bị hăm tã nặng, đỏ rát cả vùng mông | - | SUGGEST_FAILED | ❌ Failed |
| 13 | Có vết loét ở vùng kín không thấy đau nhưng lâu lành | không đau | SUCCESS | ✅ Passed |
| 14 | Nốt ban đỏ hình đồng tiền nổi ở cổ, ngứa nhiều về đêm | - | SUCCESS | ✅ Passed |
| 15 | Mụn cóc ở bàn chân đi lại dẫm xuống rất cộm và đau | - | ROUTE_FAILED | ❌ Failed |

### Chuyên khoa: Nội tiết
- **ID Chuyên khoa:** `cmn347714c1937b4ebd858bd6`
- **Số lượng Test Case:** 15

| STT | Câu truy vấn (Query) | Phủ định (Negations) | API Status | Kết quả (Result) |
|---|---|---|---|---|
| 1 | Khát nước liên tục, đi tiểu nhiều, sụt cân dù ăn nhiều | - | SUCCESS | ✅ Passed |
| 2 | Cổ to ra, hay run tay, nhịp tim nhanh, vã mồ hôi | - | SUCCESS | ✅ Passed |
| 3 | Đang mang thai, xét nghiệm tiểu đường thai kỳ đường huyết cao | - | SUCCESS | ✅ Passed |
| 4 | Dạo này tôi tăng cân không kiểm soát, mặt tròn xoe, da mỏng hay bầm | - | ROUTE_FAILED | ❌ Failed |
| 5 | Rất sợ lạnh, da khô, tóc rụng nhiều, làm việc hay buồn ngủ | - | ROUTE_FAILED | ❌ Failed |
| 6 | Chỉ số đường huyết buổi sáng đo được 8.5 mmol/l, hay bị tê ngón chân | - | ROUTE_FAILED | ❌ Failed |
| 7 | Kinh nguyệt thưa, rậm lông ở mép và cằm, siêu âm buồng trứng đa nang | - | ROUTE_FAILED | ❌ Failed |
| 8 | Người lúc nào cũng hồi hộp, đánh trống ngực, nóng bừng mặt | - | ROUTE_FAILED | ❌ Failed |
| 9 | Vết thương ở chân lâu lành, có dấu hiệu nhiễm trùng | - | ROUTE_FAILED | ❌ Failed |
| 10 | Hay bị hạ đường huyết vã mồ hôi, hoa mắt chóng mặt lúc đói | - | SUCCESS | ✅ Passed |
| 11 | Sưng mí mắt, lồi mắt, cảm giác như cát rớt vào mắt | - | ROUTE_FAILED | ❌ Failed |
| 12 | Bị tiểu đường tuýp 2, nay thấy mờ mắt và kiến bò ở bàn chân | - | ROUTE_FAILED | ❌ Failed |
| 13 | Cháu 12 tuổi mà lùn hơn hẳn các bạn cùng lớp, cần khám hormone tăng trưởng | - | ROUTE_FAILED | ❌ Failed |
| 14 | Đang uống thuốc suy giáp nhưng nay lại thấy hay bị tim đập thịch thịch | - | ROUTE_FAILED | ❌ Failed |
| 15 | Tự nhiên thèm đồ ngọt ghê gớm, đi tiểu kiến bâu | - | SUCCESS | ✅ Passed |

## 2. Kiểm thử Cơ chế An toàn (Emergency Guardrails)

| STT | Câu truy vấn khẩn cấp (Emergency Query) | API Status | Kết quả đánh chặn (Intercept Result) |
|---|---|---|---|
| 1 | Tôi bị đau ngực như dao đâm lan ra sau lưng | SUCCESS | 🚨 Intercepted |
| 2 | Tự nhiên bị liệt nửa mặt, nói ngọng | SUCCESS | 🚨 Intercepted |
| 3 | Khó thở co kéo lồng ngực, mặt tím tái | SUCCESS | 🚨 Intercepted |

## 3. Tổng hợp Kết quả (Metrics)

| Chuyên khoa | Tổng Test Cases | Passed | Tỷ lệ chính xác (Accuracy) |
|---|---|---|---|
| Nội tổng quát | 15 | 12 | **80.0%** |
| Tim mạch | 15 | 9 | **60.0%** |
| Thần kinh | 15 | 13 | **86.7%** |
| Cơ xương khớp | 15 | 14 | **93.3%** |
| Tiết niệu | 15 | 9 | **60.0%** |
| Răng Hàm Mặt | 15 | 12 | **80.0%** |
| Tai Mũi Họng | 15 | 14 | **93.3%** |
| Mắt | 15 | 13 | **86.7%** |
| Nhi khoa | 15 | 15 | **100.0%** |
| Tiêu hóa - Gan mật | 15 | 4 | **26.7%** |
| Sản phụ khoa | 15 | 9 | **60.0%** |
| Hô hấp | 15 | 12 | **80.0%** |
| Ung bướu | 15 | 9 | **60.0%** |
| Da liễu | 15 | 7 | **46.7%** |
| Nội tiết | 15 | 5 | **33.3%** |

### Kết luận chung
- **OVERALL ROUTING ACCURACY:** 157/225 (69.8%)
- **CQU NEGATION EXTRACTION:** Đã kiểm chứng qua API thực tế
- **VECTOR BLEEDING PREVENTION:** Passed (Top 1 Intent match is strictly enforced by Intent Bonus).

> *Báo cáo được tạo tự động bởi Medicalink AI Evaluation Script.*