import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key=os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def generate_questions(topic, difficulty, count):
    model= genai.GenerativeModel("gemini-3-flash-preview")

    prompt=f"""
    Generate {count} multiple-choice questions about {topic} at a {difficulty} level.
    Return the response ONLY as a JSON list of objects with these keys:
    "question_text", "options" (a list of 4 strings), and "correct_answer" (must be one of the options).
    Do not include markdown formatting like ```json.
    """

    try:
        response= model.generate_content(prompt)
        data=response.text.strip()
        if "```" in data:
            data = data.split("```")[1].replace("json", "").strip()
        data=json.loads(data)
        return data
    except Exception as e:
        print(f"AI Error: {e}")
        return []