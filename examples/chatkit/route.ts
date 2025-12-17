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


