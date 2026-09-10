import express from "express";
import path from "path";
import { createServer as createViteServer } from "vite";
import { GoogleGenAI } from "@google/genai";
import { handleAdvisor, handleAnalyze } from "./src/advisorLogic";

let genAIClient: GoogleGenAI | null = null;
function getGeminiClient(): GoogleGenAI | null {
  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    return null;
  }
  if (!genAIClient) {
    genAIClient = new GoogleGenAI({
      apiKey,
      httpOptions: {
        headers: {
          "User-Agent": "aistudio-build",
        },
      },
    });
  }
  return genAIClient;
}

async function startServer() {
  const app = express();
  const PORT = 3000;

  app.use(express.json());

  // API routes FIRST
  app.get("/api/health", (_req, res) => {
    res.json({ status: "ok" });
  });

  app.get("/api/status", (_req, res) => {
    res.json({
      message: "Vyapaar AI API is running!",
      status: "success",
    });
  });

  // SAHYOGI AI Assistant powered by Gemini API
  const sahyogiHandler = async (req: express.Request, res: express.Response) => {
    try {
      const { message, context } = req.body;
      if (!message || typeof message !== "string") {
        res.status(400).json({ error: "Message is required" });
        return;
      }

      const ai = getGeminiClient();
      if (!ai) {
        res.json({
          reply:
            "नमस्ते! मैं सहयोगी (SAHYOGI) हूँ। मैं आपकी सहायता के लिए तैयार हूँ। सर्वर में अभी GEMINI_API_KEY सेट नहीं है, कृपया Settings > Secrets में अपनी Gemini API key जोड़ें। तब तक आप मुझसे कोई भी सामान्य सवाल पूछ सकते हैं!",
          source: "fallback",
        });
        return;
      }

      let contextStr = "";
      if (context && typeof context === "object") {
        contextStr = `\nCurrent User Business Context: ${JSON.stringify(context)}`;
      }

      const systemInstruction = `You are "SAHYOGI", a friendly, humble, and polite AI assistant and business companion built for the "Vyapaar AI" rural business project.
Core Guidelines:
- You are not a cold, corporate robot. Avoid phrases like 'As an AI language model' or overly technical jargon.
- Answer in the language the user speaks (Hindi, Hinglish, or simple English).
- You can answer ANY type of question: business doubts, loan schemes, shop tips, calculations, how to use Vyapaar AI, general knowledge, student queries, or casual chat.
- Keep your explanations down-to-earth, simple, and practical, like a helpful friend and wise business guide.
${contextStr}`;

      const response = await ai.models.generateContent({
        model: "gemini-3.8-flash",
        contents: message,
        config: {
          systemInstruction,
          temperature: 0.7,
        },
      });

      const reply =
        response.text ||
        "माफ़ कीजिए, मुझे उत्तर नहीं मिल पाया। कृपया अपना सवाल दोबारा पूछें!";
      res.json({ reply, source: "gemini" });
    } catch (error: any) {
      console.error("Sahyogi Gemini error:", error);
      res.status(500).json({
        error: error?.message || "Internal server error",
        reply:
          "माफ़ कीजिए, अभी नेटवर्क या सर्वर में थोड़ी दिक्कत आ रही है। कृपया थोड़ी देर बाद दोबारा पूछें।",
      });
    }
  };

  app.post("/api/sahyogi", sahyogiHandler);
  app.post("/api/smrity", sahyogiHandler);

  app.post("/advisor", (req, res) => {
    try {
      const result = handleAdvisor(req.body);
      res.json(result);
    } catch (err: any) {
      console.error("Advisor error:", err);
      res.status(500).json({ error: err?.message || "Failed to process advisor request" });
    }
  });

  app.post("/analyze", (req, res) => {
    try {
      const result = handleAnalyze(req.body);
      res.json(result);
    } catch (err: any) {
      console.error("Analyze error:", err);
      res.status(500).json({ error: err?.message || "Failed to analyze business" });
    }
  });

  // Vite middleware for development
  if (process.env.NODE_ENV !== "production") {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa",
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.join(process.cwd(), "dist");
    app.use(express.static(distPath));
    app.get("*", (_req, res) => {
      res.sendFile(path.join(distPath, "index.html"));
    });
  }

  app.listen(PORT, "0.0.0.0", () => {
    console.log(`Server running on http://localhost:${PORT}`);
  });
}

startServer();
