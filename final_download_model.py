import os
from huggingface_hub import snapshot_download


try:
    model_path = snapshot_download(
        repo_id="moka-ai/m3e-base",
        resume_download=True,
        max_workers=4
    )
    print(f"模型已在本地缓存中：\n{model_path}")
except Exception as e:
    print(f"下载失败，具体报错: {str(e)}")