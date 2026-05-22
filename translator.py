import os
import asyncio
from openai import AsyncOpenAI

# OpenAI API Key Render के Environment Variables से ऑटोमैटिक लोड होगी
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def translate_text_block(text: str) -> str:
    """अंग्रेजी टेक्स्ट ब्लॉक को NEET हिंदी मीडियम के अनुसार ट्रांसलेट करता है"""
    if not text.strip() or text.isdigit():
        return text

    system_prompt = (
        "You are an expert NEET (Medical Entrance) exam paper and textbook translator. "
        "Translate English textbook text into Hindi tailored perfectly for Hindi-medium NEET aspirants.\n\n"
        "CRITICAL RULES FOR AUTO-DETECTING & TRANSLATING SCIENCE TERMS:\n"
        "1. AUTO-DETECT: Scan the text for any Physics, Chemistry, or Biology terms.\n"
        "2. NO COMPLEX HINDI: Do NOT use complex pure Hindi words (e.g., Do NOT write 'अपचयोपचय' for Redox).\n"
        "3. DEVANAGARI TRANSLITERATION: Write technical terms in Devanagari script (Hinglish).\n"
        "   Examples: Redox Reaction -> रेडॉक्स अभिक्रिया, Mitochondria -> माइटोकॉन्ड्रिया\n"
        "4. FORMULAS: Keep chemical formulas (e.g., H2SO4) and math symbols exactly in English characters.\n"
        "5. OUTPUT: Return ONLY the final translated Hindi text without any notes or explanations."
    )

    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            temperature=0.15
        )
        return response.choices.message.content.strip()
    except Exception as e:
        print(f"Translation Error: {e}")
        return text  # एरर आने पर ओरिजिनल टेक्स्ट वापस भेजें ताकि प्रोसेस न रुके
