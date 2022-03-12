NOTES:

- We did not have a record of which turn generated which RDF file. To do so we choose one csv file per scenario (
  randomly) and run the `map_rdf_files.py` to generate a JSON of turns and empty field for the name of the `.trig` file.
  The mapping was performed manually. 


- Piek scenario 2: Automatic metrics on Imme's CSV are corrupt. Copied columns manually 
- Jaap scenario 1: Piotr has a completely different conversation annotated. Removed that file.
- Lea scenario 1: conversation did not start on a fresh brain. Graph statistics may be biased. add ontology before?
- Lea scenario 2: missing RDF folder completely. Remove scenario completely.
- Tae scenario 1: Automatic metrics only available for Hyde. Copied columns manually to three others
- Tae scenario 2: missing 16 utterances for 3 annotators (only Hyde has them: 19-32). 
                    Automatic metrics only available for Hyde
                    Added them manually and assigned null human annotations 
