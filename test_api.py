"""
🚀 API 測試腳本

用於測試 FastAPI 後端的各個端點
"""

import requests
import json
import sys

API_BASE_URL = "http://localhost:8000"


def test_health_check():
    """測試健康檢查端點"""
    print("=" * 60)
    print("🏥 測試健康檢查端點")
    print("=" * 60)
    
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ 健康檢查通過")
            print(f"     狀態：{data.get('status')}")
            print(f"     API Key 設定：{data.get('api_key_set')}")
            print(f"     Voice ID 設定：{data.get('voice_id_set')}")
            return True
        else:
            print(f"  ❌ 健康檢查失敗：{response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"  ❌ 無法連接到 API（請確認 API 是否運行中）")
        print(f"     提示：執行 python start_api.py")
        return False
    except Exception as e:
        print(f"  ❌ 錯誤：{str(e)}")
        return False


def test_voice_api():
    """測試語音產生 API"""
    print("\n" + "=" * 60)
    print("🎤 測試語音產生 API")
    print("=" * 60)
    
    test_cases = [
        {
            "text": "你好，我是黃蓉！",
            "provider": "openai",
            "emotion_auto": True
        },
        {
            "text": "你知道嗎？我真的好感動。",
            "provider": "openai",
            "emotion_auto": True
        },
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n  測試用例 {i}: {case['text']}")
        
        try:
            response = requests.post(
                f"{API_BASE_URL}/api/voice/huangrong",
                json=case,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"    ✅ 成功")
                print(f"       狀態：{data.get('status')}")
                print(f"       原文：{data.get('text')}")
                print(f"       標籤後：{data.get('tagged_text')}")
                print(f"       音訊 URL：{data.get('audio_url')}")
            else:
                print(f"    ❌ 失敗：{response.status_code}")
                print(f"       錯誤：{response.text}")
                
        except requests.exceptions.ConnectionError:
            print(f"    ❌ 無法連接到 API")
            return False
        except Exception as e:
            print(f"    ❌ 錯誤：{str(e)}")
    
    return True


def test_voice_stream_api():
    """測試語音流 API"""
    print("\n" + "=" * 60)
    print("🌊 測試語音流 API")
    print("=" * 60)
    
    test_text = "你好，我是黃蓉！"
    print(f"  測試文字：{test_text}")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/voice/huangrong/stream",
            json={
                "text": test_text,
                "provider": "openai",
                "emotion_auto": True
            },
            stream=True,
            timeout=30
        )
        
        if response.status_code == 200:
            # 檢查 Content-Type
            content_type = response.headers.get('Content-Type', '')
            if 'audio' in content_type:
                print(f"    ✅ 成功")
                print(f"       Content-Type: {content_type}")
                print(f"       資料大小: {len(response.content)} bytes")
                
                # 儲存測試檔案
                filename = "test_stream_output.mp3"
                with open(filename, "wb") as f:
                    f.write(response.content)
                print(f"       已儲存為：{filename}")
                return True
            else:
                print(f"    ⚠️  回應類型不正確：{content_type}")
                return False
        else:
            print(f"    ❌ 失敗：{response.status_code}")
            print(f"       錯誤：{response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"    ❌ 無法連接到 API")
        return False
    except Exception as e:
        print(f"    ❌ 錯誤：{str(e)}")
        return False


def main():
    """主測試函數"""
    print("=" * 60)
    print("🚀 黃蓉語音系統 - API 測試")
    print("=" * 60)
    print("\n⚠️  請確保 API 服務正在運行（python start_api.py）")
    print()
    
    results = []
    
    # 執行測試
    results.append(("健康檢查", test_health_check()))
    
    if results[0][1]:  # 如果健康檢查通過，繼續其他測試
        results.append(("語音產生 API", test_voice_api()))
        results.append(("語音流 API", test_voice_stream_api()))
    
    # 總結
    print("\n" + "=" * 60)
    print("📊 測試結果總結")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"  {name}: {status}")
    
    print(f"\n總計：{passed}/{total} 項測試通過")
    
    if passed == total:
        print("\n🎉 所有 API 測試通過！")
        return 0
    else:
        print(f"\n⚠️  有 {total - passed} 項測試未通過。")
        return 1


if __name__ == "__main__":
    sys.exit(main())


