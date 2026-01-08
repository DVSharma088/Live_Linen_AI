"""
ai_clients.py
---------------------------------
Centralized AI client initialization for:
1) OpenAI (GPT-4o / GPT-4o-mini – vision + text)
2) Google Gemini (image editing / generation)

This file MUST be imported by other modules.
DO NOT initialize clients elsewhere.
"""

import os
from openai import OpenAI
import google.generativeai as genai

# =========================================================
# 🔹 ENVIRONMENT VARIABLES CHECK
# =========================================================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("❌ OPENAI_API_KEY is not set")

if not GEMINI_API_KEY:
    raise RuntimeError("❌ GEMINI_API_KEY is not set")

# =========================================================
# 🔹 OPENAI CLIENT (GPT-4o / GPT-4o-mini)
# =========================================================

openai_client = OpenAI(
    api_key=OPENAI_API_KEY
)

# =========================================================
# 🔹 GEMINI CLIENT (IMAGE MODEL)
# =========================================================

genai.configure(api_key=GEMINI_API_KEY)

# Image-capable Gemini model
GEMINI_IMAGE = genai.GenerativeModel(
    model_name="models/gemini-2.5-flash-image"
)

# =========================================================
# 🔹 OPTIONAL: SIMPLE HEALTH CHECK
# =========================================================

def health_check():
    """
    Quick sanity check to ensure clients are loaded.
    Call manually if needed.
    """
    return {
        "openai": "ready",
        "gemini": "ready"
    }
