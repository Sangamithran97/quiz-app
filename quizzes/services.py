import random

def generate_questions(topic, difficulty, count):
    questions=[]

    for i in range(count):
        questions.append({
            "question_text": f"{topic} question {i+1} ({difficulty})",
            "options": ["A","B","C","D"],
            "correct_answer": random.choice(["A","B","C","D"])
        })
    
    return questions