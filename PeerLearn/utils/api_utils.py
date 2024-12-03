import json
from anthropic import Anthropic
import os
# from django.conf import settings

def generate_learning_materials(extracted_text):
    """
    Generate flashcards and test questions from OCR extracted text using Claude API
    """
    try:
        client = Anthropic(api_key=os.getenv('CLAUDE_API_KEY'))
        
        prompt = f"""
        You are receiving text that was extracted through OCR (Optical Character Recognition). 
        This means there might be:
        - Misspellings or character recognition errors
        - Incorrect word breaks
        - Missing punctuation
        - Mixed formatting
        
        First, try to understand and mentally correct any obvious OCR errors in the text.
        Then, create two JSON objects based on the corrected understanding:
        1. A flashcard set for learning the key concepts
        2. A multiple choice test to assess understanding
        
        Follow these exact JSON structures:
        
        Flashcard JSON:
        {{
            "lang": "en",
            "questions": [
                {{
                    "question": "Clear, focused question about a key concept",
                    "answer": "Concise, accurate answer",
                    "hint": "Helpful hint for remembering",
                    "explain": "Detailed explanation with context"
                }}
            ]
        }}
        
        Test JSON:
        {{
            "lang": "en",
            "questions": [
                {{
                    "question": "Clear multiple choice question",
                    "options": [
                        {{"option": "Correct option", "is_correct": true}},
                        {{"option": "Plausible wrong option", "is_correct": false}},
                        {{"option": "Plausible wrong option", "is_correct": false}}
                    ]
                }}
            ]
        }}
        
        Create 3-5 high-quality questions for each format based on this OCR-extracted text:
        {extracted_text}
        
        Return only the two JSON objects, with 'FLASHCARDS_JSON:' and 'TEST_JSON:' as separators.
        """
        
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = response.content[0].text
        
        parts = response_text.split('FLASHCARDS_JSON:')
        if len(parts) > 1:
            flashcards_text = parts[1].split('TEST_JSON:')[0].strip()
            test_text = parts[1].split('TEST_JSON:')[1].strip()
            
            return json.loads(flashcards_text), json.loads(test_text)
            
        return None, None
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return None, None

def validate_json_structure(json_obj, json_type):
    """
    Validate the structure of generated JSONs
    """
    try:
        if not isinstance(json_obj, dict):
            return False
            
        required_keys = {'lang', 'questions'}
        if not all(key in json_obj for key in required_keys):
            return False
            
        if not isinstance(json_obj['questions'], list):
            return False
            
        for question in json_obj['questions']:
            if json_type == 'flashcard':
                required_question_keys = {'question', 'answer', 'hint', 'explain'}
            else:  # test
                required_question_keys = {'question', 'options'}
                
            if not all(key in question for key in required_question_keys):
                return False
                
            if json_type == 'test':
                for option in question['options']:
                    if not {'option', 'is_correct'}.issubset(option.keys()):
                        return False
                        
        return True
        
    except Exception:
        return False

def process_extracted_text(extracted_text):
    """
    Process OCR-extracted text and generate validated learning materials
    """
    # Basic text preprocessing
    if extracted_text:
        extracted_text = ' '.join(extracted_text.split())
        extracted_text = extracted_text.replace('|', 'I')
        extracted_text = extracted_text.replace('0', 'O')
        
    flashcards_json, test_json = generate_learning_materials(extracted_text)
    
    if flashcards_json and test_json:
        if (validate_json_structure(flashcards_json, 'flashcard') and 
            validate_json_structure(test_json, 'test')):
            return flashcards_json, test_json
            
    return None, None