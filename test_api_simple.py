"""
簡化版 API 測試腳本（Windows 兼容）
"""

import requests
import json
import sys

# 設置 UTF-8 編碼
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

API_BASE_URL = "http://localhost:8000"

def test_health():
    """測試健康檢查"""
    print("=" * 60)
    print("測試 1: API 健康檢查")
    print("=" * 60)
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"[OK] 健康檢查通過")
            print(f"    狀態: {data.get('status')}")
            print(f"    API Key 設定: {data.get('api_key_set')}")
            print(f"    Voice ID 設定: {data.get('voice_id_set')}")
            return True
        else:
            print(f"[FAIL] 健康檢查失敗: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"[FAIL] 無法連接到 API（請確認 API 是否運行中）")
        return False
    except Exception as e:
        print(f"[FAIL] 錯誤: {str(e)}")
        return False

def test_voice_api():
    """測試語音產生 API"""
    print("\n" + "=" * 60)
    print("測試 2: 語音產生 API")
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
    
    passed = 0
    for i, case in enumerate(test_cases, 1):
        print(f"\n測試用例 {i}: {case['text']}")
        
        try:
            response = requests.post(
                f"{API_BASE_URL}/api/voice/huangrong",
                json=case,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"  [OK] 成功")
                print(f"      狀態: {data.get('status')}")
                print(f"      原文: {data.get('text')}")
                print(f"      標籤後: {data.get('tagged_text')}")
                print(f"      音訊 URL: {data.get('audio_url')}")
                passed += 1
            else:
                print(f"  [FAIL] 失敗: {response.status_code}")
                print(f"      錯誤: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print(f"  [FAIL] 無法連接到 API")
            break
        except Exception as e:
            print(f"  [FAIL] 錯誤: {str(e)}")
    
    print(f"\n結果: {passed}/{len(test_cases)} 通過")
    return passed == len(test_cases)

def test_voice_stream():
    """測試語音流 API"""
    print("\n" + "=" * 60)
    print("測試 3: 語音流 API")
    print("=" * 60)
    
    test_text = "你好，我是黃蓉！"
    print(f"測試文字: {test_text}")
    
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
            content_type = response.headers.get('Content-Type', '')
            if 'audio' in content_type:
                print(f"  [OK] 成功")
                print(f"      Content-Type: {content_type}")
                print(f"      資料大小: {len(response.content)} bytes")
                
                filename = "test_stream_output.mp3"
                with open(filename, "wb") as f:
                    f.write(response.content)
                print(f"      已儲存為: {filename}")
                return True
            else:
                print(f"  [WARN] 回應類型不正確: {content_type}")
                return False
        else:
            print(f"  [FAIL] 失敗: {response.status_code}")
            print(f"      錯誤: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"  [FAIL] 無法連接到 API")
        return False
    except Exception as e:
        print(f"  [FAIL] 錯誤: {str(e)}")
        return False

def main():
    """主測試函數"""
    print("=" * 60)
    print("黃蓉語音系統 - API 測試")
    print("=" * 60)
    print("\n請確保 API 服務正在運行 (py start_api.py)")
    print()
    
    results = []
    results.append(("健康檢查", test_health()))
    
    if results[0][1]:  # 如果健康檢查通過
        results.append(("語音產生 API", test_voice_api()))
        results.append(("語音流 API", test_voice_stream()))
    
    # 總結
    print("\n" + "=" * 60)
    print("測試結果總結")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"  {name}: {status}")
    
    print(f"\n總計: {passed}/{total} 項測試通過")
    
    if passed == total:
        print("\n[SUCCESS] 所有 API 測試通過！")
        return 0
    else:
        print(f"\n[WARN] 有 {total - passed} 項測試未通過。")
        return 1

if __name__ == "__main__":
    sys.exit(main())


