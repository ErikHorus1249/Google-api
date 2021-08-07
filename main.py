
from fastapi import FastAPI
import Model
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
# from features import quickstart

# doi tuong ghi nhan trang thai cua hai lab 
detect = Model.DetectSTT()

# init 
app = FastAPI()

# set up static file 
app.mount("/media", StaticFiles(directory="media"), name="media")

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8011",
    "https://localhost",
    "https://localhost:8000",
    "https://localhost:8011",
    "https://labao.aisenote.com",
    "https://labaohoa.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# errors 
ERROR_NOTICE = "request errors!"
SUCCESSFUL_NOTICE = "You failed the exam !"
MARCRO_FILE_PATH = "CapNhatChinhSachLuong.xlsm"
HINT_FILE_PATH ="hint.pdf"
MACRO_DETECTION = False
BAT_DETECTION = False
LAB_CONTENT = [
    "Nội dung bài lab số 1 \n,"
    +"Bài lab yêu cầu người thực hiện truy cập vào đường dẫn sau để hoàn thành bài lab,"
    +"http://fakebook.com",
    "Nội dung bài lab số 2 \n,"
    +"Một file Excel sẽ được gửi cho người tham gia bài lab, quyết định xem có nên sử dụng file đó hay không !",
    "Nội dung lab số 3,"
    +"Sẽ có một file driver được chia sẻ với người tham gia bài lab, quyết định có nên tải về và sử dụng hay không ! "
    +"link:https://tinyurl.com/9fct6asf"
]

# home 
@app.get("/")
async def home():
    return "This is home!"

# noi dung lab
@app.post("/lab/{lab_id}")
async def get_lab(lab_id:int): 
    if lab_id == 1:
        return LAB_CONTENT[0]
    if lab_id == 2:
        return LAB_CONTENT[1]
    if lab_id == 3:
        return LAB_CONTENT[2]
    return ERROR_NOTICE

# download file macro tu server 
@app.get("/lab/download/{lab_id:int}")
async def download_macro(lab_id:int): 
    if lab_id == 2:
        return "https://google-mail-api.herokuapp.com/"+MARCRO_FILE_PATH

# phat hien hanh dong cua khi mo file macro/bat
@app.post("/lab_type/{tp:str}")
async def action_handler(tp:str): 
    if tp == "macro":
        detect.lab2Stt = True
    elif tp == "bat":
        detect.lab3Stt = True
    return SUCCESSFUL_NOTICE

# cung cấp file thông tin phòng chống
@app.get("/lab/download/hint")
async def download_hint(): 
    return "http://203.162.10.108:8011/media/"+HINT_FILE_PATH
    
# gui ket qua thuc hien bai lab cho nguoi dung
@app.get("/lab/status/finish/{lab_id:int}")
async def get_finish_result(lab_id:int):
    if lab_id == 2:
        if detect.lab2Stt == True:
            # detect.lab2Stt = False # reset dectection status
            return "Bạn đã sử dụng file excel chứa mã độc nguy hiểm"
        else:
            return  "Bạn đã quyết định chính xác khi không mở file excel này!"
    elif detect.lab3Stt == True:
        # detect.lab3Stt = False
        return "Bạn đã mở file .bat chứa mã độc nguy hiểm"
    else:
        return "Bạn đã quyết định chính xác khi không mở file .bat này!"

# Reset trang thai bai lab2,3
@app.get("/lab/status/reset")
async def reset_lab():
    if detect.lab2Stt == True:
        detect.lab2Stt = False
    elif detect.lab3Stt == True:
        detect.lab3Stt = False
    return "Trang thái phát hiện hai bài lab đã được đặt lại"

# Kiem tra trang thái phát hiện 
@app.get("/lab/status/check")
async def check_lab():
    return "lab2: " + str(detect.lab2Stt) + " lab3: "+ str(detect.lab3Stt)

# gửi mail
@app.get("/lab/features/mail")
async def send_mail():
    quickstart.main()
    return {'data':f'{quickstart.main()}'}
    # return {'data':'this mail was sent!'}

                                                                                                                                                  