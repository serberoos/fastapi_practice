# 각 환경에 따른 설정

from dataclasses import dataclass, asdict
from os import path, environ

base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
# base_dir은 config.py파일을 기준으로 notification-api 폴더를 가리키고 있다.
# 참조할 때 쉽게 경로 가져오기 위해

@dataclass # 객체를 언패킹 할 수 있도록 하기 위해서 dataclass 어노테이션과 asdict함수를 사용해 딕셔너리로 바꾼다.
class Config: # 기본 Configuration
    BASE_DIR = base_dir

    DB_POOL_RECYCLE: int = 900
    DB_ECHO:bool = True

#Config를 그대로 상속 받는다.
@dataclass
class LocalConfig(Config):
    PROJ_RELOAD:bool=True
    DB_URL: str = "mysql+pymysql://root@localhost/fastapi_db?charset=utf8mb4"

@dataclass
class ProdConfig(Config):
    PROJ_RELOAD:bool=False

def conf(): # 환경 불러오기
    config = dict(prod=ProdConfig(), local=LocalConfig())
    return config.get(environ.get("API_ENV","local"))
# API_ENV라는 환경변수를 찾고 그런 환경 변수가 없다면 local을 써라