# logicInference
CSCI 404 Project 3  
(This file is saved as .txt to comply with the project requirements but is written in Markdown. It can be previewed with https://markdownlivepreview.com/ for an easier lecture)

## 1. Names and CWID
Leo Chely, 10818125  
David An, 10727498

## 2. Programming Language
Python 3

## 3. Code Structure
Our code is added to the end of logic_expression.py. We have created an `extract_symbols` function that extracts, and stores in a dict, the set of all symbols used in the wumpus rule, the knowledge base, and the statement. The dictionary contains no repetitions.
We then created an `entail` function that given the knowledge base (including the wumpus rules), the statement to be shown true or false, and a set of boolean assigments entails or does not entail the statement.
We made use of the ttable python library. This library provided us a basic truth table implementation that we used in our entailment function.
WARNING: due to that library's limitations, the truth table takes a very long time to get generated, despites our efforts to integrate the answer to homework 3. Even if we restrain the truth table to not expand symbol that we are sure about the actual value, the complexity is still very high.
If you want to test the functionality of our program, we suggest you to use the `test_wumpus_rules.txt` we provide you, which is essentially a lighter version of the `wumpus_rules.txt`. This will allow the truth table to be generated in a reasonable amount of time.
Sample statements that can be run with `test_wumpus_rules.txt` as the rules file and the corresponding statement file:
Definitely True: `(and (not P_1_2) (not P_2_1))` (file: inputDT.txt)
Definitely False: `(and M_3_3 M_3_4)` (file: inputDF.txt)
Both True and False: `M_3_3` (file: inputBTF.txt)
Possibly True, possibly False: `(if B_2_2 P_2_3)` (file: inputPTF.txt)

## 4. How to run
First, run `pip install -r requirements.txt`. This will install the dependencies for the truth table.
On the school computers or on Windows machine in general when using git bash, `python3` has to be replaced by `python`  
The program does not need to be compiled. Cd into the directory and run the following command:

`python3 main.py [rules] [additional_knowledge] [statement]`
