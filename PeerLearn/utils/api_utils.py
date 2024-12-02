import openai
from django.conf import settings

# Set OpenAI API key
openai.api_key = settings.OPENAI_API_KEY

def generate_flashcards_and_test_from_text(extracted_text):
    """
    This function sends the extracted text (OCR data) to the OpenAI API and returns 
    the structured JSON for flashcards and a test.

    Parameters:
    - extracted_text: The OCR-extracted text that may contain errors and needs enhancement and conversion into a flashcard/test format.

    Returns:
    - A dictionary containing the JSON-formatted flashcards and test data, or an error message if the call fails.
    """
    print(f"\n*********** Inside api utils ***********\n")
    
    system_message = """
    You are a helpful assistant who converts extracted OCR text into flashcards and test questions. 
    The following text may contain OCR errors such as misinterpreted characters or missing information. 
    Please clean and enhance the text, correcting any obvious mistakes, and generate flashcards and a test based on the content. 
    Ensure the flashcards and test questions make sense and cover the key points of the text.
    """
    
    user_message = f"Extract the main ideas from the following text, which might contain OCR errors, and generate flashcards and a test: {extracted_text}"

    try:
        # Using the updated method openai.completions.create() for text-based completions (including chat-based models)
        response = openai.Completion.create(
            model="gpt-4",  # Use "gpt-4" or "gpt-3.5-turbo"
            prompt=f"{system_message}\n{user_message}",  # Combine system and user messages
            temperature=0.7,  # Adjust temperature as needed
            max_tokens=1500,  # Limit the output size
        )

        print(f"********* response ***********\n")
        print(f"original response: \n{response}")
        print("\n************ end of response **********")

        # Return the response text (you can use `json.loads()` to parse if needed)
        return response['choices'][0]['text']

    except Exception as e:
        # Log the actual error message for better diagnostics
        print(f"Error occurred: {str(e)}")  # This will be printed in the terminal
        return {"error": str(e)}
