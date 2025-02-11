import requests
import re
import json
import io
import os
from io import StringIO
from openai import AzureOpenAI
from openai import OpenAI
import numpy as np
from time import sleep
import pyspark

### --- getPromptResultsfromAPI --- ###
# --------------------- #
def getPromptResultsfromAPI(ntries,model,instructions,prompt,key,url):
    """
    Submits the instructions followed by the prompt to the API in json format. API returns the response in json format. If the prompt returns a max token limit reached output, the script sleeps for 1 minute while tokens reset and then resubmits. A single prompt will be submitted ntries times, before the function moves on to the next prompt. 

    Parameters:
        ntries (int): Number of times function will retry prompt submission.
        model (str): GPT model being used (in your prompt_version.py)
        instructions (str): Instructions part of prompt (in your prompt_version.py)
        prompt (str): Prompt question, note pasted at end
        key (str): your API key parsed from text file
        url (str): URL to API / model version

    Returns:
    str: Prompt response from API in json format 
    """

    for x in range(ntries):
        try:
            payload = json.dumps({
                "model": model,
                "messages": [
                    {
                        "role": "system",
                        "content": instructions
                    
                    },
                {
                    "role": "user",
                    "content": prompt
                }]
            })
            headers = {
              'Ocp-Apim-Subscription-Key': key,
              'Content-Type': 'application/json'
            }

            response=requests.request("POST", url, headers=headers, data=payload)
            myAnswer=response.text

            if "Token limit is exceeded. Try again" in myAnswer:
                raise ValueError
    
        except:
            if x < ntries - 1:
                print("Token limit exceeded, waiting 60 seconds ...")
                sleep(60)
                continue
            else:
                raise

        break  
    return(myAnswer)

##