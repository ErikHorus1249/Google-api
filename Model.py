from pydantic import BaseSettings


class DetectSTT(BaseSettings):
    lab2Stt: bool = False
    lab3Stt: bool = False