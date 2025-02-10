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

modelVars = {
    'promptV':"v2o1",
    'gptModel':"gpt-4o",
    'p1Cols':['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'mrn', 'note_id', 'input_tokens', 'output_tokens'],
    'p2Cols':['Gene', 'Variant', 'Status', 'mrn', 'note_id', 'input_tokens', 'output_tokens']
}

## Prompt Pt1 specific processing function
def getDataFrame_fromResponse_pt1(myMRN,myResponse,myNoteID):
    
    wjdata = json.loads(myResponse)
    mystring=wjdata['choices'][0]['message']['content']
    
    ## Table response
    # Turn tab deliminated string into a pandas df
    sio = StringIO(mystring)
    resDF = pd.read_csv(sio, sep='\t',names=["F1", "F2", "F3", "F4", "F5", "F6"], index_col=None)

    # Add MRN
    resDF=resDF.assign(mrn=myMRN, note_id=myNoteID)
    
    # Add tokens
    resDF['input_tokens']=wjdata['usage']['prompt_tokens']
    resDF['response_tokens']=wjdata['usage']['completion_tokens']
    
    resDF.replace(np.nan, pd.NA, inplace=True)

    if not resDF['F1'].isin(['yes', 'no']).all():
        resDF="Format Error"
    if not resDF['F6'].isin(['yes', 'no', pd.NA]).all():
        resDF="Format Error"
    
    return(resDF)

# Prompt response processing pt2
def getDataFrame_fromResponse_pt2(myResponse,myMRN,myNoteID):
    
    wjdata = json.loads(myResponse)
    mystring=wjdata['choices'][0]['message']['content']
    
    ## Table response
    # Turn table string into a pandas df
    sio = StringIO(mystring)
    resDF = pd.read_csv(sio, sep='|').dropna(how='all', axis=1).iloc[1:]
    resDF.columns = ["Gene","Variant", "Variant_status"]
    
    # Add MRN + note ID
    resDF=resDF.assign(mrn=myMRN, note_id=myNoteID)
    
    # Add tokens
    resDF['input_tokens']=wjdata['usage']['prompt_tokens']
    resDF['response_tokens']=wjdata['usage']['completion_tokens']

    return(resDF)

## Prompts + Instructions 
instructions="You are a genetics counselor knowledgeable in genetics testing for several cancer types. You are reading {} that may contain results and other information about a patient's history of genetics testing. When asked about genetics testing history, you will provide responses in as few words as possible without any additional details or summary text. Your answers will be precise, and responses will not be assumed from context."

question_p1="For the genetics note pasted below, print one line of tab-delimited text with the following fields:\n\n - F1: Answer the question, 'Was genetic testing ordered in this patient?' Only answer 'yes' or 'no'.\n - F2: List the laboratory (e.g. 'Invitae', 'Ambry', 'Myriad', 'Foundation') that the testing was ordered from. Answer 'NA' if no testing was ordered \n - F3: List the name of the genetics panel performed by the laboratory in F2. (e.g. 'CancerNext Expanded', 'Multi-gene cancer risk panel', 'Multi-gene breast/ovarian cancer risk panel'). If no testing panel name was provided or genetics testing was not ordered, answer 'N/A'.\n - F4: If explicitly given, include a comma separated list of all gene names that were tested for in the testing laboratories gene panel, regardless of results or pathogenic variant discovery. Answer 'NA', if a full list of genes was not given\n - F5: List the date that genetic testing was performed or results were returned. Only include a single date, in the format mm/yyyy or mm/dd/yyyy. Answer 'NA' if no results were returned or the date is unknown\n - F6: Answer the question, 'Was a pathogenic variant, likely pathogenic variant, moderate risk variant, or variant of unknown or uncertain significance found in this patient?' Only answer 'yes', 'no', or 'NA' if results were not available.\n{}"

question_p2="The the following patient's genetics note contains results from the {} genetics test. Within the note are detected genetic variants that are reported to be pathogenic, likely pathogenic, of moderate risk, or of uncertain or unknown significance. List these detected variants given in the note in a 3 column data table where the column headers are 'Gene_name', 'Variant_id', and 'Variant_type'. Each row of the table is a single reported variant from the patient's genetic testing results. Include 1 row for each reported variant. Do not include multiple variants in each row.\n - Column1 - Gene_name: The gene name for detected variant.\n - Column1 - Variant_id: The variant ID with reported results from the genetic testing panel\n - Column2- Variant_type: The status of the gene or variant from column1. Only use the terms 'pathogenic' , 'likely pathogenic', 'moderate risk', 'Uncertain significance' or 'Unknown significance' in your response.\n\nBelow are two examples of what these tables might look like:\nExample 1:\n| Gene_name |  Variant_id | Variant_type |\n|-------|-------|-------|\n| PALB2 | c.2167_2168del | pathogenic|\n|CHEK2 | c.190G>A (p.E64K) |likely pathogenic|\n| DIS3L2 | p.Leu63Phe | Uncertain significance|\n\nExample2:\n| Gene_name |  Variant_id | Variant_type |\n|-------|-------|-------|\n| ATM | c.7919C>T | Unknown significance|\n| RET | c.2370G>C | pathogenic|\n| APC | c.3308G>A (p.Arg1103Lys)| Uncertain significance|\n\n{}"