# Project Constants
## DIRECTORIES ##
# Main - directory
project_dir=# Your project directory
# Sub-main
subdirs = {
    'datRaw':project_dir + "data-raw\\", # Raw unchanged data from source
    'datFinal':project_dir + "data-final\\", # Modified/intermediate data/output from analysis
    'results':project_dir + "results\\", # Final project results
    'tmpOutDir': # Local directory for prompt output
}

# Note file IDs
noteIDs=['GSv1','ID00', 'ID01','ID02','ID03', 'ID04','ID05', 'ID06','ID07', 'ID08','ID09']

# Raw Notes - Column IDs -- keep these IDs in Raw Note file when adding new notes
rawNotes_cols=['mrn','department_name','effective_time','prov_name','department_name','note_type','note_type_desc','note', 'note_length', 'note_id']

## must assign patientID, note_id, note_date, and note columns in the raw input notes file
noteFileConstants={
    'patientID':'mrn',
    'note_id':'note_id',
    'note_date':'effective_time',
    'note':'note'
}

### Consistant Wording Dictionary ###

## Testing company dictionary
testCompanyDict= {'invitae' : 'InVitae Laboratories',
                   'ambry' : 'Ambry Genetics',
                   'myriad' : 'Myriad Labs',
                   'foundation' : 'Foundation',
                   'genedx' : 'GeneDx Laboratories',
                   'guardant' : 'Guardant',
                   'counsyl':  'Counsyl',
                   'blueprint': 'Blueprint',
                   'prevention': 'Prevention Genetics',
                   'quest': 'Quest Diagnostics',
                   'color': 'Color Genetics'}

