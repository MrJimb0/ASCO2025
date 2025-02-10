# Jupyter workflow to use an LLM to extract structured genetics results from EMRs
Current method makes use of Stanford's Secure GPT to process patient EMRs from genetics providors to 

**Our Data Set:**
We started with a large set of EMR records from several thousand patients. The best results for detailed genetic testing data were expected to come from Progress notes and RTF letters written by genetics providers, however to get a complete view of all patient results, our EMR query was expanded to include telephone visits and some non-genetics providors.

**Our Query:**
Find patients with genetics testing, gathering the following information:
1) Was genetics testing performed in the patient? Y/N
2) What lab performed the testing
3) 


## Basic Recommended Steps:
**1) Patient note filtering, prioritization and reduction**

We started with a large set of EMR records from several thousand patients. 

**2) Prompt validation** - Run through workflow with goldstandard set alone, benchmark against set
    
    Repeating the following steps until the prompt achieves goal in goldstandard:
    a) Generating a gold standard set (note + patient level)
    b) LLM query + response analysis
    c) Benchmark against goldstandard

**3) Execution**
Run through LLM query + clean up to generate results
