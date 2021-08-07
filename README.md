

# Write up: Sử dụng Google API

## I. Mở đầu
Trong context của bài sẽ hướng dẫn cách sử dụng Google API cho web application cụ thể là tạp một app nhỏ để send mail thông qua **[Gmail API](https://developers.google.com/gmail/api)**.
Đồng thời tác giả sẽ chia sẻ một số lỗi dế mắc phải trong quá trình thiết lập kết nối, xác thực Oauth với **[Google Cloud Flatform](https://console.cloud.google.com/)**.


![](https://i.imgur.com/MmTDEt0.png)


## II. Google Gmail API
### 1. Giới thiệu
API Gmail là một API RESTful có thể được sử dụng để truy cập hộp thư Gmail và gửi thư. Đối với hầu hết các ứng dụng web, API Gmail là lựa chọn tốt nhất để truy cập được phép vào dữ liệu Gmail của người dùng và phù hợp với các ứng dụng khác nhau, chẳng hạn như:

 - Trích xuất, lập chỉ mục và sao lưu thư (read-only)
 - Gửi mail tự động hoặc có điều khiển
 - Di chuyển tài khoản email
 - Tổ chức email bao gồm lọc và sắp xếp mail
 - Tiêu chuẩn hóa chữ ký email trong tổ chức

![](https://i.imgur.com/qHau2JE.png)


## 2. Triển khai gửi mail qua Gmail API với Python
### 2.1. Tạo Google Cloud Platform (GCP) project
Trước tiên truy cập vào  **[Cloud google console](https://console.cloud.google.com/)**

![](https://i.imgur.com/4X0tymY.jpeg)

Lần đầu tiên truy cập cần chọn **Country**(vietnam) và chọn **Agree and Continue**.
Chọn mục Create Project phía bên phải giao diện.

![](https://i.imgur.com/uMLteT0.jpeg)

Đặt tên cho Project và chọn **Create** 

> vd: Demo

![](https://i.imgur.com/s2PEpmB.jpeg)


Sau khi giao diện **Dashboard** hiện ra chọn vào mục **APIs & Service**  ở thanh công cụ bên trái. Tại cửa sổ option chọn tuy chọn **Library** để thêm loại APIs mà Google cung cấp cụ thể ở đây là **Gmail API**.

![](https://i.imgur.com/mkOfl7M.jpeg)

Tại **API Library** tìm kiếm Gmail API và **Enable** API.

![](https://i.imgur.com/IK6WEGv.jpeg)

Sau khi kích hoạt API, tiếp theo cần thực hiện hai viêc bao gồm Tạo **Credential Oauth ** và cấu hình **Consent Screen** cho Web của chúng ta.

Consent Screen chính là cái hiện lên hỏi mỗi lần chúng ta sử dụng Oauth.

![](https://i.imgur.com/PemM2F5.jpeg)

Chọn vào mục **CONFIGURE CONSENT SCREEN** và điền các thông tin như sau.

![](https://i.imgur.com/r7EEYXZ.png)

![](https://i.imgur.com/k0SJtna.jpeg)

Điền đầy đủ thông tin bao gồm Tên ứng dụng, email user support và có thể chon consent image hoặc không.

![](https://i.imgur.com/KTpBRmq.jpeg)


![](https://i.imgur.com/RjC13m8.jpeg)

Chọn tạm thời một domain để điền vào mục yêu cầu link homepage ...

![](https://i.imgur.com/4g7Dckp.jpeg)

Đê mặc định không thêm các Sensitive scope.

![](https://i.imgur.com/nk5kvMB.jpeg)


Trong bài hướng dẫn này sẽ public luôn API chứ không đưa vào mode Test nên không cần thêm Test User.

