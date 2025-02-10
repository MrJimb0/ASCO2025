# Jupyter workflow to use an LLM to extract structured genetics results from EMRs
Current method makes use of Stanford's Secure GPT to process patient EMRs from genetics providors to 

## Prompt Development

### Our Data Set:
We started with a large set of EMR records from several thousand patients. The best results for detailed genetic testing data were expected to come from Progress notes and RTF letters written by genetics providers, however to get a complete view of all patient results, our EMR query was expanded to include telephone visits and some non-genetics providors.

### Our Query:
Find patients with genetics testing, gathering the following information:
1) Was genetics testing performed in the patient? Y/N
2) What lab performed the testing
3) What panel was ordered
4) What genes were listed on the panel
5) What date was testing returned
6) Were there any variants reported
7) What were the gene IDs, variant names, and consequences for the detected variants


### Data Set / Query Limitations:
The following variables influenced the formatting and workflow steps required to refine the prompt/analysis to get the best results. 

- **EMR Format Variability** - Progress notes and RTF letters are highly detailed, and if present provide all answers to the questions in good detail. Other types of EMR records like telephone calls, patient instructions, etc, may also contain relevant results, but there is often a low level of detail and the formatting between these note types is inconsistant.
- **Multi-Formatted responses** - questions 1-6 can be answered once per note, but question 7 may have multiple responses or none at all. Variability in response formatting, can lead to more inconsistant results. To avoid formatting errors, the prompt here was divided. First notes are passed througha prompt to assess if they contain any relevant genetics results (questions 1-6), any notes with relevant results are passed to prompt 2.


## Recommended Steps:
**1) Patient note filtering, prioritization, and reduction**


**2) Prompt validation** - Run through workflow with goldstandard set alone, benchmark against set
    
    Repeating the following steps until the prompt achieves goal in goldstandard:
    a) Generating a gold standard set (note + patient level)
    b) LLM query + response analysis
    c) Benchmark against goldstandard

**3) Execution**
Run through LLM query + clean up to generate results
