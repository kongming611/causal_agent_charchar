import os
import subprocess
import sys


def start_cil_agent():
    print("🚀 正在初始化 CIL 智能体运行环境...")

    # 【工业级防御】写死专属环境的路径，彻底杜绝环境漂移
    env_python_dir = r"D:\miniconda3\envs\causal_agent"

    # 找到专属环境下的 streamlit 执行程序
    streamlit_exe = os.path.join(env_python_dir, "Scripts", "streamlit.exe")

    if not os.path.exists(streamlit_exe):
        print(f"❌ 严重错误：未找到隔离环境的 Streamlit！请检查路径：{streamlit_exe}")
        sys.exit(1)

    # 获取前端代码的绝对路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(current_dir, "final_frontend.py")

    print(f"✅ 环境锁定成功！正在拉起前端 UI...")
    print(f"📂 目标文件: {app_path}")
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
        print("\n🛑 服务已手动关闭。")
    except Exception as e:
        print(f"\n❌ 启动失败: {str(e)}")


if __name__ == "__main__":
    start_cil_agent()