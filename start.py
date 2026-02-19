import os
import subprocess
import sys


def start_cil_agent():
    # 找到专属环境下的 streamlit 执行程序
    streamlit_exe = os.path.join(env_python_dir, "Scripts", "streamlit.exe")

    if not os.path.exists(streamlit_exe):
        print(f"请检查路径：{streamlit_exe}")
        sys.exit(1)

    # 获取前端代码的绝对路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(current_dir, "final_frontend.py")

    print(f"正在拉起前端 UI...")
    print(f"目标文件: {app_path}")
    print("-" * 50)

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
        print("\n服务已手动关闭。")
    except Exception as e:
        print(f"\n启动失败: {str(e)}")


if __name__ == "__main__":
    start_cil_agent()