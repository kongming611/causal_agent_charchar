from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# 创建数据库引擎（本地 SQLite 文件）
engine = create_engine('sqlite:///cil_history.db', echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 定义聊天记录模型
class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String(20))          # user 或 assistant
    content = Column(Text)             # 文本内容
    image_path = Column(String(255))   # 图片路径（如果有）
    timestamp = Column(DateTime, default=datetime.utcnow)

# 初始化数据库
def init_db():
    Base.metadata.create_all(bind=engine)

# 保存消息的工具函数
def save_message(role, content, image_path=None):
    db = SessionLocal()
    try:
        new_msg = ChatMessage(role=role, content=content, image_path=image_path)
        db.add(new_msg)
        db.commit()
    finally:
        db.close()

# 加载所有历史记录
def get_all_history():
    db = SessionLocal()
    try:
        return db.query(ChatMessage).order_by(ChatMessage.timestamp.asc()).all()
    finally:
        db.close()