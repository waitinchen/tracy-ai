"""
🧪 測試環境變數配置
"""

import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("🔍 環境變數配置檢查")
print("=" * 60)
print()

# 檢查 ElevenLabs 配置
print("📡 ElevenLabs API:")
print(f"  ELEVEN_API_KEY: {'✅ 已設定' if os.getenv('ELEVEN_API_KEY') else '❌ 未設定'}")
print(f"  ELEVEN_HUANGRONG_ID: {os.getenv('ELEVEN_HUANGRONG_ID', '❌ 未設定')}")
print()

# 檢查 LLM 配置
print("🧠 LLM API:")
print(f"  OPENAI_API_KEY: {'✅ 已設定' if os.getenv('OPENAI_API_KEY') else '❌ 未設定'}")
print(f"  OPENAI_MODEL: {os.getenv('OPENAI_MODEL', 'gpt-4o-mini')}")
print(f"  ANTHROPIC_API_KEY: {'✅ 已設定' if os.getenv('ANTHROPIC_API_KEY') else '❌ 未設定'}")
print()

# 檢查 API URL
print("🌐 API 設定:")
print(f"  BASE_URL: {os.getenv('BASE_URL', 'http://localhost:8000')}")
print()

print("=" * 60)
print("✅ 配置檢查完成！")
print("=" * 60)


