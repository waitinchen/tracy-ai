import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App";
import "./styles/mic-recorder.css";
import "./styles/voice-ball.css";

const container = document.getElementById("root");

if (!container) {
  throw new Error("Root element #root not found. Please ensure index.html has a <div id='root'></div>.");
}

const root = createRoot(container);
root.render(<App />);

