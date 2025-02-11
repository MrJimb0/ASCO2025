## Prompt v2o1
import requests
import re
import json
import io
import os
import pandas as pd
import numpy as np
from time import sleep
import pyspark
from io import StringIO

## Model Variables
promptV="v2o1"
gptModel="gpt-4o"
gpturl= # your URL to GPT API / Model Version

# Fields from prompt response
p1_fields=["F1", "F2", "F3", "F4", "F5", "F6"]
p2_fields=['Gene', 'Variant', 'Status']
# Full column names in output
p1Cols=['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'mrn', 'note_id', 'input_tokens', 'output_tokens'] 
p2Cols=['Gene', 'Variant', 'Status', 'mrn', 'note_id', 'input_tokens', 'output_tokens']


## Prompt Pt1 specific processing function
def getDataFrame_fromResponse_pt1(response,indID,noteID):
    """
    Reads in the json formatted response, parses response and input/ouput tokens. Creates a single line DF with response, IDs, token counts. Does a brief formatting check to make sure response is following guidelines, will resubmit if parameters not met (ie incorrect seperators, phrasing outside of requested response).

    Parameters:
        response (str): json response str from getPromptResultsfromAPI()
        indID (str): unique individual ID
        noteID (str): unique note ID

    Returns:
    str: Returns a results DF, for part 1 prompt, note will have 1 row per response 
    """
    
    wjdata = json.loads(response)
    mystring=wjdata['choices'][0]['message']['content']
    
    ## Table response
    # Turns tab deliminated string into a pandas df
    sio = StringIO(mystring)
    resDF = pd.read_csv(sio, sep='\t',names=p1_fields, index_col=None)

    # Add MRN
    resDF=resDF.assign(mrn=indID, note_id=noteID)
    
    # Add tokens
    resDF['input_tokens']=wjdata['usage']['prompt_tokens']
    resDF['response_tokens']=wjdata['usage']['completion_tokens']
    
    resDF.replace(np.nan, pd.NA, inplace=True)

    # Prompt specific formatting checks, if not met, rerun
    if not resDF['F1'].isin(['yes', 'no']).all():
        resDF="Format Error"
    if not resDF['F6'].isin(['yes', 'no', pd.NA]).all():
        resDF="Format Error"
    
    return(resDF)

# Prompt response processing pt2
def getDataFrame_fromResponse_pt2(response,indID,noteID):
        """
    Reads in the json formatted response, parses response and input/ouput tokens. Creates a single line DF with response, IDs, token counts. Does a brief formatting check to make sure response is following guidelines, will resubmit if parameters not met (ie incorrect seperators, phrasing outside of requested response).

    Parameters:
        response (str): json response str from getPromptResultsfromAPI()
        indID (str): unique individual ID
        noteID (str): unique note ID

    Returns:
    str: Returns a results DF, for part 2 prompt, note could have several row per response 
    """
    
    wjdata = json.loads(response)
    mystring=wjdata['choices'][0]['message']['content']
    
    ## Table response
    # Turns table to string into a pandas df, expects tables to be built with '|'
    sio = StringIO(mystring)
    resDF = pd.read_csv(sio, sep='|').dropna(how='all', axis=1).iloc[1:]
    resDF.columns = p2_fields
    
    # Add MRN + note ID
    resDF=resDF.assign(mrn=indID, note_id=noteID)
    
    # Add tokens
    resDF['input_tokens']=wjdata['usage']['prompt_tokens']
    resDF['response_tokens']=wjdata['usage']['completion_tokens']

    return(resDF)