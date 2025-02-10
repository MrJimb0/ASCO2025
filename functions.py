import requests
import re
import json
import io
import os
import pandas as pd
from io import StringIO
from openai import AzureOpenAI
from openai import OpenAI
import numpy as np
from time import sleep
import pyspark

### --- getPromptResultsfromAPI --- ###
# --------------------- #
def getPromptResultsfromAPI(myurl,ntries,model,myinstructions,myprompt,key):
    url=myurl
    for x in range(ntries):
        try:
            payload = json.dumps({
                "model": model,
                "messages": [
                    {
                        "role": "system",
                        "content": myinstructions
                    
                    },
                {
                    "role": "user",
                    "content": myprompt
                }]
            })
            headers = {
              'Ocp-Apim-Subscription-Key': key,
              'Content-Type': 'application/json'
            }

            response=requests.request("POST", myurl, headers=headers, data=payload)
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