import queue
import threading
from database import save_message, SessionLocal, ChatMessage

# 1. 创建任务队列
db_queue = queue.Queue()


# 2. 定义异步工人
def db_worker():
    while True:
        task = db_queue.get()
        if task is None: break

        role, content, image_path = task
        print(f"核心：正在异步写入数据库... 来自 {role}")
        save_message(role, content, image_path)

        db_queue.task_done()


# 3. 启动后台线程
worker_thread = threading.Thread(target=db_worker, daemon=True)
worker_thread.start()


# 4. 提供给前端调用的函数：它只负责往队列丢任务，瞬间完成
def async_save_to_db(role, content, image_path=None):
    db_queue.put((role, content, image_path))


def clear_history():
    db = SessionLocal()
    try:
        db.query(ChatMessage).delete()
        db.commit()
        print("核心：数据库历史已清空")
    finally:
        db.close()