import mysql.connector
import os
import re
from groq_api_debug import get_score

def extract_score(response_text):
    match = re.search(r"Score:\s*([0-1](?:\.\d+)?)", response_text)
    return float(match.group(1)) if match else None

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user=os.getenv('sql_username'),
        password=os.getenv('sql_password'),
        database="neuro_tutor_db"
    )

def get_next_question(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT concept
        FROM user_retention
        WHERE user_id = %s
        ORDER BY retention_score ASC
        LIMIT 1;
    ''', (user_id,))
    concept_row = cursor.fetchone()
    if not concept_row:
        cursor.close()
        conn.close()
        return None, None, "No concepts found for user."
    concept = concept_row[0]
    cursor.execute('''
        SELECT question_text, question_id FROM questions
        WHERE concept = %s AND question_id NOT IN (
            SELECT question_id FROM user_attempts WHERE user_id = %s
        )
        LIMIT 1;
    ''', (concept, user_id))
    question_row = cursor.fetchone()
    cursor.close()
    conn.close()

    if not question_row:
        return None, None, f"No more unattempted questions for concept: {concept}"
    question_text, question_id = question_row
    return question_id, question_text, concept

def submit_answer(user_id, question_id, question_text, concept, code):
    conn = get_connection()
    cursor = conn.cursor()
    response = get_score(question_text,code)
    score = extract_score(response)
    if score is None:
        print("Could not extract score. Try again.")
        cursor.close()
        conn.close()
        return None
    cursor.execute('''
        UPDATE user_retention
        SET retention_score =  (0.7 * retention_score) + (0.3 * %s),
            last_attempt = NOW()
        WHERE user_id = %s AND concept = %s;
    ''', (score, user_id, concept))
    conn.commit()

    cursor.execute('''
        INSERT INTO user_attempts (user_id, question_id, code_submitted, understanding_score, attempt_time)
        VALUES (%s, %s, %s, %s, NOW());
    ''', (user_id, question_id, code, score))
    conn.commit()
    cursor.close()
    conn.close()
    return score,response