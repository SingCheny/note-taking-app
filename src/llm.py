# import libraries
import os
from openai import OpenAI
from dotenv import load_dotenv  


load_dotenv()  # Loads environment variables from .env 
token = os.environ["GITHUB_TOKEN"] 
endpoint = "https://models.github.ai/inference" 
model = "openai/gpt-4.1-mini" 

# A function to call an LLM model and return the response 

def call_llm_model(model, messages, temperature=1.0, top_p=1.0):
	client = OpenAI(base_url=endpoint,api_key=token) 
	response = client.chat.completions.create( 
		messages=messages, 
		temperature=temperature, top_p=top_p, model=model) 
	return response.choices[0].message.content 


def translate_to_language(text, target_language):
    # Use a deterministic, instruction-focused prompt to avoid clarification questions
    prompt = (
        f"You are a professional translator. Translate the following text into {target_language}.\n"
        "Return only the translated text and nothing else (no explanations, no questions, no extra markup).\n"
        "If the input is empty, return an empty string.\n\n"
        f"Text:\n{text}"
    )
    messages = [{"role": "user", "content": prompt}]
    # Use low temperature for deterministic translations and reduce chance of clarifying questions
    return call_llm_model(model, messages, temperature=0.2, top_p=1.0)

if __name__ == "__main__":
    sample_text = "Hello, how are you?"
    target_language = "janpanese"
    translated_text = translate_to_language(sample_text, target_language)
    print(f"Original Text: {sample_text}")
    print(f"Translated Text: {translated_text}")