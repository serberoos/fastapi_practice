from datetime import datetime, timedelta

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    func,
    Enum, Boolean,
)

from sqlalchemy.orm import Session
from app.database.conn import Base  # sql alchemy에 있는애


class BaseMixin:
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False, default=func.utc_timestamp())  # 생성 시간
    updated_at = Column(DateTime, nullable=False, default=func.utc_timestamp(), onupdate=func.utc_timestamp())  # 업데이트 시간

    def all_columns(self):
        return [c for c in self.__table__.columns if c.primary_key is False and c.name != "created_at"]

    def __hash__(self):
        return hash(self.id)

    def create(self, session: Session, auto_commit=False, **kwargs):
        # 테이블 데이터 객체 전용 함수
        #:param session
        #:param auto_commit: 자동 커밋 여부
        #:param kwargs: 적재 함 데이터
        # return :
        for col in self.all_columns():
            col_name = col.name
            if col_name in kwargs:
                setattr(self, col_name, kwargs.get(col_name))
        session.add(self)
        session.flush()
        if auto_commit:
            session.commit()
        return self


class Users(Base, BaseMixin):  # user 테이블 속성 정의
    __tablename__ = "users"
    status = Column(Enum("active", "deleted", "blocked"), default="active")  # Enum셋 중에 하나만 들어갈 수 있음
    email = Column(String(length=255), nullable=True)
    pw = Column(String(length=2000), nullable=True)
    name = Column(String(length=255), nullable=True)
    phone_number = Column(String(length=20), nullable=True)
    profile_img = Column(String(length=1000), nullable=True)
    sns_type = Column(Enum("FB", "G", "K"), nullable=True)
    marketing_agree = Column(Boolean, nullable=True, default=True)
