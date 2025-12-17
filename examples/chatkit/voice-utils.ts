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
import { useState } from 'react';

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


