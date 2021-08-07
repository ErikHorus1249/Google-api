
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from features import quickstart
import Model

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


# home 
@app.get("/")
async def home():
    return "This is home!"

@app.get("/mail")
async def mail_authen():
    action = quickstart.main()
    return action                                                                                                                                        