"""Models"""
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship


class CustomBase:
    """https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/mixins.html"""

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_collate': 'utf8mb4_general_ci'
    }

    id = Column(Integer, primary_key=True, autoincrement=True)


BaseModel = declarative_base(cls=CustomBase)


class User(BaseModel):
    """User table"""
    name = Column(String(500), nullable=False, unique=True)
    password = Column(String(1024), nullable=False)
    create_time = Column(DateTime, default=datetime.now)

    articles = relationship(
        'Article',
        backref='user',
        # cascade='all, delete-orphan',   # 代码级别级联操作，适用于需要级联删除的关系，可以保证不出异常。
        passive_deletes=True  # 在删除父记录的时候检查子记录约束。如果 ON DELETE 为 RESTRICT 则抛出异常。
    )


class Article(BaseModel):
    """Article table"""
    title = Column(String(500))
    body = Column(Text(), nullable=True)
    create_time = Column(DateTime, default=datetime.now, nullable=False)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
