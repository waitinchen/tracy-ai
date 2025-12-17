# 📦 Module: voice_cache_engine.py
# 🎯 Purpose: Handle audio file caching and re-use to reduce ElevenLabs API calls
# 🧠 Context: Part of Voice Agent v2.0 upgrade under OpenSpec task: audio-cache

import hashlib
import os
import time
from pathlib import Path
from typing import Iterable


AUDIO_CACHE_DIR = Path("public/audio")
CACHE_TTL_SECONDS = int(os.getenv("AUDIO_CACHE_TTL", 60 * 60 * 6))  # default 6 hours


def ensure_cache_dir() -> None:
    AUDIO_CACHE_DIR.mkdir(parents=True, exist_ok=True)


def generate_audio_key(text: str, voice_id: str, tags: Iterable[str]) -> str:
    """Generate a deterministic hash key for caching audio requests."""
    tags_part = "-".join(sorted(tags)) if tags else ""
    base = f"{voice_id}|{tags_part}|{text.strip()}"
    return hashlib.md5(base.encode("utf-8")).hexdigest()


def get_cached_audio_path(audio_key: str) -> Path:
    """Return full path to cached audio file."""
    return AUDIO_CACHE_DIR / f"{audio_key}.mp3"


def is_cache_valid(path: Path) -> bool:
    """Check if cached file exists and is still within TTL."""
    if not path.exists():
        return False
    age = time.time() - path.stat().st_mtime
    return age < CACHE_TTL_SECONDS


def clean_expired_cache(now: float | None = None) -> None:
    """Delete expired audio cache files from disk."""
    ensure_cache_dir()
    current = now or time.time()
    for file in AUDIO_CACHE_DIR.glob("*.mp3"):
        age = current - file.stat().st_mtime
        if age > CACHE_TTL_SECONDS:
            try:
                file.unlink()
            except Exception as exc:
                print(f"Failed to delete expired cache: {file} => {exc}")


# ✅ Usage Example
if __name__ == "__main__":
    ensure_cache_dir()
    clean_expired_cache()
    key = generate_audio_key("你好我是小軟～", "huangrong-v3-output", ["excited", "playful"])
    path = get_cached_audio_path(key)
    print("🔑 Key:", key)
    print("📁 Path:", path)
    print("✅ Valid cache:", is_cache_valid(path))

