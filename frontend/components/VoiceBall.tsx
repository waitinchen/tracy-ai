import React, { useMemo } from "react";

type VoiceBallProps = {
  tags: string[];
  isActive: boolean;
};

type Palette = {
  keywords: string[];
  gradient: string;
  glow: string;
};

const palettes: Palette[] = [
  {
    keywords: ["happy", "excited", "playful", "laugh"],
    gradient: "radial-gradient(circle, rgba(255,178,102,0.9) 0%, rgba(255,94,156,0.6) 55%, rgba(123,67,255,0.3) 100%)",
    glow: "0 0 40px rgba(255,153,102,0.45)",
  },
  {
    keywords: ["soft", "whisper", "calm", "gentle"],
    gradient: "radial-gradient(circle, rgba(119,191,255,0.85) 0%, rgba(185,210,255,0.45) 55%, rgba(120,159,255,0.25) 100%)",
    glow: "0 0 50px rgba(119,191,255,0.35)",
  },
  {
    keywords: ["curious", "wonder", "question"],
    gradient: "radial-gradient(circle, rgba(120,255,214,0.85) 0%, rgba(96,186,255,0.5) 55%, rgba(71,115,255,0.28) 100%)",
    glow: "0 0 45px rgba(120,255,214,0.35)",
  },
  {
    keywords: ["angry", "furious", "intense", "power"],
    gradient: "radial-gradient(circle, rgba(255,138,128,0.85) 0%, rgba(255,71,87,0.55) 55%, rgba(130,36,52,0.35) 100%)",
    glow: "0 0 60px rgba(255,71,87,0.45)",
  },
  {
    keywords: ["sad", "cry", "tear", "melancholy"],
    gradient: "radial-gradient(circle, rgba(135,167,255,0.8) 0%, rgba(86,105,180,0.45) 55%, rgba(41,48,95,0.3) 100%)",
    glow: "0 0 35px rgba(135,167,255,0.35)",
  },
];

const defaultPalette: Palette = {
  keywords: [],
  gradient: "radial-gradient(circle, rgba(202,202,255,0.8) 0%, rgba(120,120,255,0.4) 55%, rgba(70,70,120,0.25) 100%)",
  glow: "0 0 30px rgba(150,150,255,0.25)",
};

const VoiceBall: React.FC<VoiceBallProps> = ({ tags, isActive }) => {
  const palette = useMemo(() => {
    if (!tags || tags.length === 0) {
      return defaultPalette;
    }

    const tagLower = tags.map((tag) => tag.toLowerCase());
    const match = palettes.find((item) => item.keywords.some((keyword) => tagLower.some((tag) => tag.includes(keyword))));
    return match ?? defaultPalette;
  }, [tags]);

  const scale = isActive ? 1.1 : 1.0;
  const animationClass = isActive ? "voiceball-active" : "voiceball-idle";

  return (
    <div className={`voiceball-wrapper ${animationClass}`} style={{ filter: `drop-shadow(${palette.glow})` }}>
      <div
        className="voiceball-core"
        style={{ background: palette.gradient, transform: `scale(${scale})` }}
      />
      <div className="voiceball-halo" style={{ background: palette.gradient }} />
    </div>
  );
};

export default VoiceBall;

