import os
from pathlib import Path

from huggingface_hub import snapshot_download

MODEL_ID = "KOCDIGITAL/Kocdigital-LLM-8b-v0.1"
SNAPSHOT_ID = "85952962ddb7baf03f6550e36ca3188b6fc4c9f4"

# Determine HF_HOME or fall back to a local hf_cache directory
HF_HOME = os.environ.get("HF_HOME") or str(Path(__file__).resolve().parent / "hf_cache")

MODEL_CACHE_PATH = os.path.join(
    HF_HOME,
    "hub",
    "models--KOCDIGITAL--Kocdigital-LLM-8b-v0.1",
    "snapshots",
    SNAPSHOT_ID,
)


def main() -> None:
    """Download the model snapshot if not already cached."""
    if os.path.exists(MODEL_CACHE_PATH):
        print("\u2705 Model zaten indirilmis. Indirme atlaniyor.")
    else:
        print("\u2B07\uFE0F Model indiriliyor...")
        snapshot_download(
            repo_id=MODEL_ID,
            cache_dir=HF_HOME,
            resume_download=True,
            local_files_only=False,
        )


if __name__ == "__main__":
    main()
