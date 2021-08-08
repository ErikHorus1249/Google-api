

# Write up: Sử dụng Google API

## I. Mở đầu
Trong context của bài sẽ hướng dẫn cách sử dụng Google API cho web application cụ thể là tạp một app nhỏ để gửi mail  qua **[Gmail API](https://developers.google.com/gmail/api)**.
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
**Truy cập vào  **[Cloud google console](https://console.cloud.google.com/)****

![](https://i.imgur.com/4X0tymY.jpeg)

Lần đầu truy cập cần chọn **Country**(vietnam) và chọn **Agree and Continue**.
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

**Tạo Credential Oauth** 

![](https://i.imgur.com/LirY0RR.jpeg)

Chọn **CREATE CREDENTIALS** > **OAuth client ID** 

![](https://i.imgur.com/LHr8DNJ.jpeg)

Chọn lại app -> **Web application** > Thêm tên hiển thị trên console > Thêm URIs
#### Chú ý: URI này dùng để gửi request OAUth cũng như nhận Response từ máy chủ cung cấp API, khi khởi tạo request sẽ chạy trên chính localhost nên xác định cổng cho dịch vụ này, trong thực nghiệm tác giả chọn cổng 8080.
![](https://i.imgur.com/gI1wpsU.jpeg)


Chọn **Create** và tải về file Credentials (JSON).

![](https://i.imgur.com/nmvXo7b.jpeg)


### 2.2. Coding

**Khởi tạo các file sau:**

    ├── client_secret.json
    ├── Google.py
    ├── main.py
    ├── requirements.txt
    └── venv

Thay đổi tên cho file JSON lại ngắn gọn hơn và **COPY** vào thư mục làm việc.

    vd: client_secret.json

**Chạy với Venv** 

> `$ python3 -m venv venv`
> 
> `$ source venv/bin/activate`

**Cài đặt các thư viện cần thiết:**

> `$ pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`


Tại [Google.py](h) sẽ bao gồm hàm khởi tạo service thông qua OAUth.
import  pickle

    import  os
    
    from google_auth_oauthlib.flow import Flow, InstalledAppFlow
    
    from googleapiclient.discovery import build
    
    from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
    
    from google.auth.transport.requests import Request
    
      
      
    
    def  Create_Service(client_secret_file, api_name, api_version, *scopes):
    
	    print(client_secret_file, api_name, api_version, scopes, sep='-')
	    
	    CLIENT_SECRET_FILE  =  client_secret_file
	    
	    API_SERVICE_NAME  =  api_name
	    
	    API_VERSION  =  api_version
	    
	    SCOPES  = [scope  for  scope  in  scopes[0]]
	    
	    print(SCOPES)
	    
	    cred  =  None
	    
	    working_dir  =  os.getcwd()
	    
	    token_dir  =  'token files'
	    
	    pickle_file  = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'
	    
	    # print(pickle_file)
	    
	    ### Check if token dir exists first, if not, create the folder
	    
	    if  not  os.path.exists(os.path.join(working_dir, token_dir)):
	    
		    os.mkdir(os.path.join(working_dir, token_dir))
	    
	    if  os.path.exists(os.path.join(working_dir, token_dir, pickle_file)):
	    
		    with  open(os.path.join(working_dir, token_dir, pickle_file), 'rb') as  token:
	    
			    cred  =  pickle.load(token)
	    
	    if  not  cred  or  not  cred.valid:
	    
		    if  cred  and  cred.expired and  cred.refresh_token:
	    
			    cred.refresh(Request())
		    
		    else:
		    
			    flow  = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
			    
			    cred  =  flow.run_local_server(port=8080)
			    
			      
			    
			    with  open(os.path.join(working_dir, token_dir, pickle_file), 'wb') as  token:
			    
			    pickle.dump(cred, token)
	    
	      
	    
	    try:
	    
		    service  = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
		    
		    print(API_SERVICE_NAME, 'service created successfully')
		    
		    return  service
	    
	    except  Exception  as  e:
	    
		    print(e)
		    
		    print(f'Failed to create service instance for {API_SERVICE_NAME}')
		    
		    os.remove(os.path.join(working_dir, token_dir, pickle_file))
		    
		    return  None

Tại [main.py](h) khởi tạo service và xác thực trước khi code phần gửi mail.

    from  email  import  message
    
    from  http  import  server
    
    from  Google  import  Create_Service
    
    
    CLIENT_SECRET_FILE  =  'client_secret.json' # chú ý vị trí lưu và tên file credentials 
    
    API_NAME  =  'gmail' # tên API
    
    API_VERSION  =  'v1' # phiên bản
    
    SCOPES  = ['https://mail.google.com/'] # Scope mà api có thể  tiếp cận
    
    # Khởi tạo service bắt đầu xác thực
    service  =  Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)


**Chạy file main.py** 

> `$ python main.py`

Trình duyệt sẽ mở tự động và Consent screen sẽ hiện ra yêu cầu chọn tài khoản thực hiện OAuth.

![](https://i.imgur.com/Aa9zRjG.jpeg)

Tuy nhiên nó sẽ dính lỗi sau:

![](https://i.imgur.com/7etCrAb.jpeg)

Lỗi này do bạn chưa Publish APP, nên vào lại mục **OAuth consent screen**  để Publish.

![](https://i.imgur.com/HKP845W.jpeg)

**Chạy lại main.py**


![](https://i.imgur.com/0u66IQ1.jpeg)

**Chọn đi tới App của bạn**

![](https://i.imgur.com/vs1NklY.jpeg)


**Chú ý tích mục quyền cũng như nhấn tiếp tục để hoàn tất OAuth**

Thông báo xác thực thành công:

    The authentication flow has completed. You may close this window.


**Hoàn thiện main.py để gửi mail.**

    from  email  import  message
    
    from  http  import  server
    
    from  Google  import  Create_Service
    
    from  email.mime.text  import  MIMEText
    
    from  email.mime.multipart  import  MIMEMultipart
    
    import  base64
    
      
    
    CLIENT_SECRET_FILE  =  'credentials/client_secret.json'
    
    API_NAME  =  'gmail'
    
    API_VERSION  =  'v1'
    
    SCOPES  = ['https://mail.google.com/']
    
      
    
    service  =  Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    
     
    emailmasg  =  "hello my friend" # nội dung 
    
    mineMessage  =  MIMEMultipart()
    
    mineMessage['to'] =  'tuananh1421999@gmail.com' # địa chỉ nhận
    
    mineMessage['subject'] =  'Hello' # subject
    
    mineMessage.attach(MIMEText(emailmasg, 'plain')) 
    
    raw_string  =  base64.urlsafe_b64encode(mineMessage.as_bytes()).decode()
    
      
    
    message  =  service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
    
    print(message)


#### Trên đây là toàn bộ nội dung hướng dẫn sử dụng Google Gmail API. Mọi thắc mắc liên hệ qua FB tại trang giới thiệu Github.

## References:
[Gmail for Deveoloper](https://developers.google.com/gmail/api/quickstart/python)

