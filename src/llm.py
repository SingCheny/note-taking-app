# import libraries
import os
from openai import OpenAI
from dotenv import load_dotenv
  


load_dotenv()  # Loads environment variables from .env 

# Safely retrieve GITHUB_TOKEN with clear error message if missing
token = os.environ.get("GITHUB_TOKEN")
if not token:
    raise ValueError(
        "GITHUB_TOKEN environment variable is required but not set. "
        "Please add it to your .env file (local) or Vercel Environment Variables (production)."
    )

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

system_prompt = '''
Extract the user's notes into the following structured fields: 
1. Title: A concise title of the notes less than 5 words 
2. Notes: The notes based on user input written in full sentences. 
3. Tags (A list): At most 3 Keywords or tags that categorize the content of the notes. 
4. Date: Extract or calculate the date in YYYY-MM-DD format. Handle these cases:
   - Relative dates: "tmr"/"tomorrow" = next day, "后天"/"day after tomorrow" = day after next, "下周一"/"next monday" = calculate next monday
   - Short dates: "11.2" or "11/2" = "2025-11-02" (current year), "3.15" = "2025-03-15" 
   - Full dates: "2025-12-25" = keep as is
   - Today's date is 2025-10-24. If no date mentioned, return null.
5. Time: Extract the time in HH:MM format (24-hour) if mentioned. Convert "5pm"="17:00", "上午9点"="09:00". If no time mentioned, return null.
Output in JSON format without ```json. Output title and notes in the language: {lang}. 
Examples: 
Input: "Badminton tmr 5pm @polyu" → Date: "2025-10-25", Time: "17:00"
Input: "会议 11.2 下午3点" → Date: "2025-11-02", Time: "15:00"  
Input: "后天上午开会" → Date: "2025-10-26", Time: null
Output format: {{ 
	"Title": "Meeting Title",
 	"Notes": "Full sentence description.", 
	"Tags": ["tag1", "tag2"],
	"Date": "2025-10-25",
	"Time": "17:00"
 }}
'''

# a funtion to extract structured notes using llm

def extract_structured_notes(text, lang ="English"):
    prompt = f"extract the user's notes into structured fields in {lang}.\n" 
    messages = [{"role": "system", "content": system_prompt.format(lang=lang)},
                {"role": "user", "content": text}
                ]
    response = call_llm_model(model, messages)
    return response



if __name__ == "__main__":
    sample_text = "badminton tmr 5pm @polyu"
    print("structured_notes:")
    print(extract_structured_notes(sample_text, lang="English"))

