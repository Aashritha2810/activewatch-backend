import anthropic
import os
import json
from dotenv import load_dotenv
load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def classify_video(transcript, title):
    prompt = f"""
    Classify this YouTube video into exactly one category.
    
    Title: {title}
    Transcript (first 500 words): {transcript[:2000]}
    
    Rules:
    - LEARN: coding tutorials, programming, tech education
    - CAPTURE: podcasts, self improvement, productivity, business
    - GUARD: vlogs, lifestyle, comedy, entertainment
    
    Return ONLY one word: LEARN, CAPTURE, or GUARD
    Nothing else.
    """
    r = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=10,
        messages=[{"role": "user", "content": prompt}]
    )
    return r.content[0].text.strip()

def generate_tasks(transcript, title):
    prompt = f"""
    You are an expert educator. Analyze this YouTube video and create a structured learning experience.
    
    Video Title: {title}
    Transcript: {transcript[:4000]}
    
    Return ONLY valid JSON in this exact structure, nothing else:
    {{
        "chapters": [
            {{
                "id": 1,
                "title": "Chapter title here",
                "summary": "2-3 sentence summary of this section",
                "mcq": [
                    {{
                        "question": "Question based on this chapter?",
                        "options": ["Option A", "Option B", "Option C", "Option D"],
                        "correct": "Option A",
                        "explanation": "Why this is correct"
                    }},
                    {{
                        "question": "Second question?",
                        "options": ["Option A", "Option B", "Option C", "Option D"],
                        "correct": "Option B",
                        "explanation": "Why this is correct"
                    }}
                ],
                "coding_challenge": {{
                    "title": "Challenge title",
                    "description": "What to build or solve",
                    "starter_code": "def solution():\n    # your code here\n    pass",
                    "hint": "A helpful hint"
                }}
            }}
        ]
    }}
    
    Create 3-4 chapters. Make questions specific to THIS video content.
    """
    r = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}]
    )
    text = r.content[0].text.strip()
    # Clean any markdown
    text = text.replace("```json", "").replace("```", "").strip()
    return json.loads(text)

def verify_answer(question, user_answer, correct_answer):
    prompt = f"""
    A student is answering a quiz question. Evaluate their answer.
    
    Question: {question}
    Correct Answer: {correct_answer}
    Student's Answer: {user_answer}
    
    Return ONLY valid JSON:
    {{
        "correct": true or false,
        "feedback": "encouraging and educational feedback here",
        "hint": "helpful hint if wrong, empty string if correct",
        "explanation": "full explanation of the correct answer"
    }}
    """
    r = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )
    text = r.content[0].text.strip()
    text = text.replace("```json", "").replace("```", "").strip()
    return json.loads(text)

def generate_summary(transcript, title):
    prompt = f"""
    You are an expert at extracting actionable insights from content.
    
    Video/Podcast Title: {title}
    Transcript: {transcript[:4000]}
    
    Return ONLY valid JSON:
    {{
        "summary": "3-4 sentence overview of the entire content",
        "takeaways": [
            "Key insight 1",
            "Key insight 2", 
            "Key insight 3",
            "Key insight 4",
            "Key insight 5"
        ],
        "action_plan": [
            "Concrete step 1 to implement what was learned",
            "Concrete step 2",
            "Concrete step 3",
            "Concrete step 4"
        ],
        "quotes": [
            "Most impactful quote from the content"
        ]
    }}
    """
    r = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    text = r.content[0].text.strip()
    text = text.replace("```json", "").replace("```", "").strip()
    return json.loads(text)