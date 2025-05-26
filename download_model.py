import os
from huggingface_hub import snapshot_download

# Path to the specific cached snapshot of the Kocdigital LLM
MODEL_CACHE_PATH = r"D:\Mira\Smart_Process_Mapper\hf_cache\hub\models--KOCDIGITAL--Kocdigital-LLM-8b-v0.1\snapshots\85952962ddb7baf03f6550e36ca3188b6fc4c9f4"

if os.path.exists(MODEL_CACHE_PATH):
    print("\u2705 Model zaten indirilmis. Indirme atlaniyor.")
else:
    print("\u2B07\uFE0F Model indiriliyor...")
    snapshot_download(
        repo_id="KOCDIGITAL/Kocdigital-LLM-8b-v0.1",
        cache_dir=r"D:\Mira\Smart_Process_Mapper\hf_cache",
        resume_download=True,
        local_files_only=False,
    )
