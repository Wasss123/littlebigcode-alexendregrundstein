# Technical test LittleBigCode
## Part 1 - Python and Data engineering

The objective of test is to create a JSON file from several .csv files representing the link between drugs (contained in drugs.csv) and their mentions in articles in PubMed (pubmed.csv), in articles in clinical trials (clinical_trials.csv), and in several journals (pubmed.csv and clinical°_trials.csv)

### Start
---
Program name: test_technique_LittleBigCode.py  
Language: Python 3.8.8  
Needed packages: pandas, json  
Installation: the program can be install anywhere on any computer  
Modification: .csv files are stored on GitHub [here](https://github.com/alexandregrundstein/littlebigcode/tree/main/data). If the path of the .csv files is modified, then it should also be modify in the program

### Comments
---
I tried to take into account the constraints of the statement. So I tried to seperate my code in several distinct parts:  
- cleaning
- treatment of the drugs table
- link to pubmed table
- link to clinical_trials table
- creation of a journal table with link with drugs
- aggregation of those 3 tables
- creation of a dictionnary
- creation of the JSON file

When I coded, I kept in mind that it should works for a much bigger amount of data. I banished any loops.
I've made a lot of .apply (lambda x) that seems to me more efficient.
Maybe to be more efficient with a big amount of data, we should adapt the code with spark.

### Appendice
---
For the appendice part (find the name of the journal that mentions the most different drugs), I made another program (feature_LittleBigCode.py). It takes the JSON file obtained with the first program (and placed on the GitHub folder) and print the journal(s) with the max numbers of different drugs mentionned.

---
## Part 2 - SQL

I created a markdown document "Test 2 - SQL.md" present in this GitHub folder [here](https://github.com/alexandregrundstein/littlebigcode/blob/main/Test_2_SQL.md) to give the 2 SQL requests that were required.