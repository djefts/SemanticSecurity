Machine:
	contains all code pertaining to the reading and manipulation of text/messages from scraped srcs or local
directories and returns a file with "good questions." Currently incomplete as the questions are not completely tested
for proof of qulity. The reason for this is that more data needs to be collected and possilbe answers need to be
developed as tests cases. Other than that the program runs the current data against the questions and "made-up" answers.
	These answers can be changed and data manipulated further to prove the program does work. This can be done
as follows. 
-First, make question and answer that suit case study.
-Second, make data that has "keyword" that matches keyword in question.
-Finally, run program and check file to see that question is left out (since its answer was found).

	*Example Case:
Question: What is the name of your school?
Message: ... my brother was in the same school i got to right now. Hogwarts.
Answer: Hogwarts
* program will scan through this message because it has the keyword school.
* It will match Hogwarts in message and in answer and consider it True in the dictionary of answers
* It will leave this question out of the final questions. You can also verify this by uncommenting 
	"print(resulting)" under predict.

Converter:
	makes the graph file a readable file type.

 