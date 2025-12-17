"""
測試花小軟系統
"""

import sys
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print("=" * 60)
print("花小軟語氣靈咒語系統測試")
print("=" * 60)
print()

# 測試導入
try:
    import sys
    sys.path.insert(0, '.')
    from modules.soft_ling import (
        process_with_soft_ling, 
        detect_soft_ling_invocation, 
        get_soft_ling_opening,
        SOFT_LING_TONE_SPELL
    )
    print("✅ 模組導入成功")
    print()
    
    # 測試召喚咒語
    invocation = SOFT_LING_TONE_SPELL["activation_phrase"]
    print(f"召喚咒語：{invocation}")
    is_invocation = detect_soft_ling_invocation(invocation)
    print(f"是否為召喚：{is_invocation}")
    print()
    
    # 測試處理
    result = process_with_soft_ling("你好")
    print(f"輸入：你好")
    print(f"標籤：{result['tags']}")
    print(f"代理名稱：{result['agent_name']}")
    print(f"聲音設定強度：{result['voice_settings'].get('intensity', 0.5):.2f}")
    print()
    
    # 測試開靈語
    opening = get_soft_ling_opening()
    print(f"開靈語：{opening}")
    print()
    
    print("=" * 60)
    print("✅ 所有測試完成")
    print("=" * 60)
    
except Exception as e:
    print(f"❌ 錯誤：{e}")
    import traceback
    traceback.print_exc()


