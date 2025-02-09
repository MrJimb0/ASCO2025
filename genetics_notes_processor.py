"""
Genetics Notes Processor - Example Script

This script demonstrates how to process genetics notes using an LLM model.
It shows the prompts used, leaves the API key blank for security,
and demonstrates how data is processed.
"""

import requests
import json
import pandas as pd
from io import StringIO
import numpy as np
from time import sleep

# Constants
API_URL = "https://api.example.com/v1/chat/completions"  # Replace with actual API endpoint
MODEL_NAME = "gpt-4"
MAX_RETRIES = 3

# System instructions for the AI model
INSTRUCTIONS = """
You are a genetics counselor knowledgeable in genetics testing for several cancer types. 
You are reading a genetics note with a patient's history of genetics testing. 
When asked about genetics testing history, you will provide responses in as few words as possible 
without any additional details or summary text. Your answers will be precise, and responses 
will not be assumed from context.
"""

# Prompt templates
PROMPT_P1 = """
For the genetics note pasted below, print one line of tab-delimited text with the following fields:

- F1: Was genetic testing ordered? (yes/no)
- F2: Testing laboratory (e.g., 'Invitae', 'Ambry') or 'NA'
- F3: Name of genetics panel or 'N/A'
- F4: Comma-separated list of tested genes or 'NA'
- F5: Test date (mm/yyyy or mm/dd/yyyy) or 'NA'
- F6: Pathogenic variant found? (yes/no/NA)

Note: {}
"""

PROMPT_P2 = """
List detected genetic variants in a 3-column table with:
1. Gene_name
2. Variant_id
3. Variant_type (pathogenic, likely pathogenic, etc.)

Example:
| Gene_name | Variant_id | Variant_type |
|-----------|------------|--------------|
| PALB2     | c.2167_2168del | pathogenic |

Note: {}
"""

def get_prompt_results(api_url, model, instructions, prompt, api_key, max_retries=MAX_RETRIES):
    """
    Get results from the API using the provided prompt
    """
    for attempt in range(max_retries):
        try:
            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": instructions},
                    {"role": "user", "content": prompt}
                ]
            }
            
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }

            response = requests.post(api_url, headers=headers, json=payload)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Attempt {attempt + 1} failed. Retrying...")
                sleep(60)
                continue
            raise

def process_p1_response(response, mrn, note_id):
    """
    Process the response from Prompt 1 into a DataFrame
    """
    content = response['choices'][0]['message']['content']
    
    # Convert tab-delimited string to DataFrame
    sio = StringIO(content)
    df = pd.read_csv(sio, sep='\t', names=["F1", "F2", "F3", "F4", "F5", "F6"])
    
    # Add metadata
    df = df.assign(mrn=mrn, note_id=note_id)
    df['input_tokens'] = response['usage']['prompt_tokens']
    df['response_tokens'] = response['usage']['completion_tokens']
    
    # Validate response format
    if not df['F1'].isin(['yes', 'no']).all() or not df['F6'].isin(['yes', 'no', pd.NA]).all():
        raise ValueError("Invalid response format")
    
    return df

def process_p2_response(response, mrn, note_id):
    """
    Process the response from Prompt 2 into a DataFrame
    """
    content = response['choices'][0]['message']['content']
    
    # Convert table string to DataFrame
    sio = StringIO(content)
    df = pd.read_csv(sio, sep='|').dropna(how='all', axis=1).iloc[1:]
    df.columns = ["Gene", "Variant", "Variant_status"]
    
    # Add metadata
    df = df.assign(mrn=mrn, note_id=note_id)
    df['input_tokens'] = response['usage']['prompt_tokens']
    df['response_tokens'] = response['usage']['completion_tokens']
    
    return df

def main():
    # Example usage
    api_key = "YOUR_API_KEY"  # Replace with your actual API key
    example_note = "Patient underwent genetic testing through Invitae..."
    
    try:
        # Get and process Prompt 1 results
        p1_response = get_prompt_results(API_URL, MODEL_NAME, INSTRUCTIONS, 
                                       PROMPT_P1.format(example_note), api_key)
        p1_df = process_p1_response(p1_response, "12345", "note_001")
        print("Prompt 1 Results:")
        print(p1_df)
        
        # Get and process Prompt 2 results
        p2_response = get_prompt_results(API_URL, MODEL_NAME, INSTRUCTIONS,
                                       PROMPT_P2.format(example_note), api_key)
        p2_df = process_p2_response(p2_response, "12345", "note_001")
        print("\nPrompt 2 Results:")
        print(p2_df)
        
    except Exception as e:
        print(f"Error processing note: {str(e)}")

if __name__ == "__main__":
    main()
