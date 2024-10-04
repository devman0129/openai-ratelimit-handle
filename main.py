import openai  
import os  
import json  
from tenacity import retry, stop_after_attempt, wait_random_exponential  
from dotenv import load_dotenv  

load_dotenv()  

# Fetch the API key safely  
api_key = os.environ.get("OPENAI_API_KEY")  
if not api_key:  
    raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")  

# Initialize the OpenAI client  
client = openai.OpenAI(api_key=api_key)  

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))  
def completion_with_backoff(**kwargs):  
    response = client.chat.completions.create(**kwargs)  
    result = response.choices[0].message.content.strip()  
    print(result)

INPUT_FILE_DIR = ""
input_file_name = ""
try:  
    with open(os.path.join(INPUT_FILE_DIR, input_file_name), "r", encoding='utf-8') as file:  
        message_list = json.load(file)  
        
        for message in message_list:  
            content = f"""  
                Please review the message history of the guests regarding house rental. Analyze the message content to identify any complaints. If complaints are found, only provide a detailed explanation of the issues. If no complaints are present, must return N.  
                message content: {message}  
            """ 

            # Call OpenAI API with backoff  
            completion_with_backoff(model="gpt-4o", messages=[{"role": "user", "content": content}])  
except FileNotFoundError:  
    print(f"Input file {input_file_name} not found in directory: {INPUT_FILE_DIR}. Please check the file path.")