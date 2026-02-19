import os
import sys
import subprocess

def start_cil_agent():
    scripts_dir = os.path.dirname(sys.executable)
    streamlit_exe = os.path.join(scripts_dir, "streamlit.exe")
    if not os.path.exists(streamlit_exe):
        streamlit_exe = os.path.join(scripts_dir, "streamlit")

    # 锁定前端代码的绝对路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(current_dir, "final_frontend.py")

    # 安全检查
    if not os.path.exists(streamlit_exe):
        print(f"启动失败，请确保执行过: pip install -r requirements.txt")
        return

    # 执行启动指令
    try:
        run_args = [
            streamlit_exe,
            "run",
            app_path,
            "--server.headless=false",        
            "--browser.gatherUsageStats=false" 
        ]
        subprocess.run(run_args)
    except KeyboardInterrupt:
        print("\n 服务已由用户手动关闭。")
    except Exception as e:
        print(f"\n 系统运行崩溃: {str(e)}")

if __name__ == "__main__":
    start_cil_agent()
