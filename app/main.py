from dataclasses import asdict
from typing import Optional

import uvicorn
from fastapi import FastAPI
from app.database.conn import db
from app.common.config import conf
from app.routes import index


def create_app():
    # 앱 함수 실행

    c = conf()  # 환경에 따라 환경변수를 가져온다.
    app = FastAPI()
    conf_dict = asdict(c)
    db.init_app(app, **conf_dict)  # 데이터 베이스 이니셜라이즈

    # 레디스 이니셜라이즈

    # 미들웨어 정의

    # 라우터 정의
    app.include_router(index.router)
    return app


app = create_app()

if __name__ == "__main__":  # 실행되는 파일이 이 파일일 경우
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)  # conf().PROJ_RELOAD 환경에 따라 다른 PROJ_RELOAD를 쓴다.

# 후에 서버로 올릴 때는 도커로 빌드를 해서 올릴 것임.
