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


