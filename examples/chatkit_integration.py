"""
💬 ChatKit 前端集成示例

示範如何在 ChatKit 中集成黃蓉語音系統。
"""

# React/Next.js 範例組件
CHATKIT_EXAMPLE_TSX = """
'use client';

import { useState } from 'react';
import { useChat } from '@ai-sdk/react';

export default function HuangrongChat() {
  const [isPlaying, setIsPlaying] = useState(false);
  const { messages, input, handleInputChange, handleSubmit } = useChat({
    api: '/api/chat', // 你的 Chat API
  });

  const playHuangrongVoice = async (text: string) => {
    try {
      setIsPlaying(true);
      
      // 呼叫黃蓉語音 API
      const response = await fetch('/api/voice/huangrong/stream', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: text,
          provider: 'openai',
          emotion_auto: true,
        }),
      });

      if (!response.ok) {
        throw new Error('語音產生失敗');
      }

      // 建立音訊並播放
      const blob = await response.blob();
      const audioUrl = URL.createObjectURL(blob);
      const audio = new Audio(audioUrl);
      
      audio.onended = () => {
        setIsPlaying(false);
        URL.revokeObjectURL(audioUrl);
      };
      
      audio.play();
    } catch (error) {
      console.error('播放錯誤:', error);
      setIsPlaying(false);
    }
  };

  return (
    <div className="flex flex-col h-screen">
      <div className="flex-1 overflow-y-auto p-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`mb-4 ${
              message.role === 'user' ? 'text-right' : 'text-left'
            }`}
          >
            <div
              className={`inline-block p-3 rounded-lg ${
                message.role === 'user'
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-200 text-gray-800'
              }`}
            >
              {message.content}
              {message.role === 'assistant' && (
                <button
                  onClick={() => playHuangrongVoice(message.content)}
                  disabled={isPlaying}
                  className="ml-2 text-blue-500 hover:text-blue-700 disabled:opacity-50"
                  title="播放黃蓉語音"
                >
                  🔊
                </button>
              )}
            </div>
          </div>
        ))}
      </div>

      <form onSubmit={handleSubmit} className="p-4 border-t">
        <input
          value={input}
          onChange={handleInputChange}
          placeholder="輸入訊息..."
          className="w-full p-2 border rounded"
        />
        <button
          type="submit"
          className="mt-2 w-full p-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          發送
        </button>
      </form>
    </div>
  );
}
"""

# Next.js API Route 範例
NEXTJS_API_ROUTE = """
// app/api/voice/huangrong/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const { text, provider = 'openai', emotion_auto = true } = await request.json();

    // 轉發到 FastAPI 後端
    const backendUrl = process.env.BACKEND_API_URL || 'http://localhost:8000';
    const response = await fetch(`${backendUrl}/api/voice/huangrong/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text,
        provider,
        emotion_auto,
      }),
    });

    if (!response.ok) {
      return NextResponse.json(
        { error: '語音產生失敗' },
        { status: response.status }
      );
    }

    // 返回音訊流
    return new NextResponse(response.body, {
      headers: {
        'Content-Type': 'audio/mpeg',
      },
    });
  } catch (error) {
    return NextResponse.json(
      { error: '伺服器錯誤' },
      { status: 500 }
    );
  }
}
"""

# JavaScript/TypeScript 工具函數
JS_UTILITY_FUNCTION = """
/**
 * 黃蓉語音播放工具函數
 */

export interface VoiceOptions {
  text: string;
  provider?: 'openai' | 'anthropic';
  emotion_auto?: boolean;
  voice_id?: string;
}

export async function playHuangrongVoice(
  options: VoiceOptions,
  apiBaseUrl: string = '/api/voice/huangrong'
): Promise<void> {
  try {
    const response = await fetch(`${apiBaseUrl}/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text: options.text,
        provider: options.provider || 'openai',
        emotion_auto: options.emotion_auto !== false,
        voice_id: options.voice_id,
      }),
    });

    if (!response.ok) {
      throw new Error(`API 錯誤: ${response.status}`);
    }

    // 建立並播放音訊
    const blob = await response.blob();
    const audioUrl = URL.createObjectURL(blob);
    const audio = new Audio(audioUrl);

    return new Promise((resolve, reject) => {
      audio.onended = () => {
        URL.revokeObjectURL(audioUrl);
        resolve();
      };
      audio.onerror = (error) => {
        URL.revokeObjectURL(audioUrl);
        reject(error);
      };
      audio.play();
    });
  } catch (error) {
    console.error('播放語音失敗:', error);
    throw error;
  }
}

// React Hook 範例
export function useHuangrongVoice() {
  const [isPlaying, setIsPlaying] = useState(false);

  const play = async (text: string, options?: Partial<VoiceOptions>) => {
    if (isPlaying) return;
    
    setIsPlaying(true);
    try {
      await playHuangrongVoice({ text, ...options });
    } finally {
      setIsPlaying(false);
    }
  };

  return { play, isPlaying };
}
"""

# 將範例寫入檔案
if __name__ == "__main__":
    import os
    from pathlib import Path
    
    examples_dir = Path("examples/chatkit")
    examples_dir.mkdir(parents=True, exist_ok=True)
    
    # 寫入 React 組件範例
    with open(examples_dir / "HuangrongChat.tsx", "w", encoding="utf-8") as f:
        f.write(CHATKIT_EXAMPLE_TSX)
    
    # 寫入 Next.js API Route
    with open(examples_dir / "route.ts", "w", encoding="utf-8") as f:
        f.write(NEXTJS_API_ROUTE)
    
    # 寫入工具函數
    with open(examples_dir / "voice-utils.ts", "w", encoding="utf-8") as f:
        f.write(JS_UTILITY_FUNCTION)
    
    print("✅ ChatKit 範例檔案已建立於 examples/chatkit/")


