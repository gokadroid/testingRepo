import sys
import operator
import time
import re
import codecs


#check if user gave the .txt file or not
if len(sys.argv) != 2:
	print ("Usage: PDF_Text.py <CSV File>")
	exit()

#marksFile is the handle in which file name will be loaded	
marksFile = ""

marksFile = open(sys.argv[1])
#Open marks file

#REGEX of interesting lines
# student first line 
#"xxxxxxxxxxx"|"xxxxx(x)"|"xxxxx(x)"|"xxxxx(x)"|"xxxxx(x)"|"xxxxx(x)"|"xxxxx(x)"|"xxxxx(x)"|"xxxxx(x)"|"xxxxx(x)"|"xx"|
#firstLineRegEx = '\"\d{11}\"(\|\"\d{5}\(\d+\)\"){9}\|\"\d+\"\|'
firstLineRegEx = '\"\d{11}\"\|\"\d{5}\(\d+\)\"\|\"\d{5}\(\d+\)\"\|\"\d{5}\(\d+\)\"\|\"\d{5}\(\d+\)\"\|\"\d{5}\(\d+\)\"\|\"\d{5}\(\d+\)\"\|\"\d{5}\(\d+\)\"\|\"\d{5}\(\d+\)\"\|\"\d{5}\(\d+\)\"\|\"\d+\"\|'
rollNoRegEx = '\"\d{11}\"'
subjectRegEx = '\"\d{5}\(\d+\)\"'

#List to hold data from above regexes
firstLine = []
rollNoList = []
subjectList = []

# student second line 
#"xxxxx xxxxxx"|
nameRegEx = '\"[^\"]+\"'
nameList = []

# student third line 
#"SID: 1xxxxxxxxxx"|"xx"|"xx"|"xx"|"xx"|"xx"|"xx"|"xx"|"xx"|"xx"|"xx"|"xx"|"xx"|"xx"|"xx"|"xx"|"xx"|"- xx"|
#allMarksRegEx = '\"SID:\s\d{12}\"\|(\"(\d|-|\s)+\"\|)+'
#allMarksRegEx = '\"SID:\s\d{12}\"\|(\"(\d|-|\s)+\"\|)+'
marksRegEx = '\|(\"[^\"]+\")'
sidRegEx = '\"SID:\s(\d{12})\"\|'

marksList = []
sidList = []

#student fourth line 
#"SchemeID: xxxxxxxxxxxxxx"|
schemeRegEx = '\"SchemeID:\s(\d{12})\"\|'

schemeList = []


#student fifth line
#xx|"xx(x+)"|"xx(x+)"|"xx(x+)"|"xx(x+)"|"xx(x+)"|"xx(x+)"|"xx(x+)"|"xx(x+)"|"xx(x+)"|
#allGradeRegEx = '\d+\|(\"[^\"]+\"\|){9}'
#allGradeRegEx = '\d+\|\"[^\"]+\"\|\"[^\"]+\"\|\"[^\"]+\"\|\"[^\"]+\"\|\"[^\"]+\"\|\"[^\"]+\"\|\"[^\"]+\"\|\"[^\"]+\"\|\"[^\"]+\"\|'
gradeRegEx = '\|(\"[^\"]+\")'

gradeList = []

# this list will check if first line for a student record has reached or not

#this test line will contain any intermediate results worked upon by firstLine or other lists
testLine = ""
# count is to count when to switch the user record after reading 5 lines per student
count = 0
#performance list has the preformance per subject for each student
performanceList = []

#each student record for the student
universityList = []


#start reading the csv file
for line in marksFile:
	#since some lines has en-dash, remove them
	line = re.sub(u"\u2013", "-", line)
	#print (line)
	firstLine = re.findall(firstLineRegEx , line)
	#print (firstLine)
	#print (str(line))
	#check if the first line for a student has arrived or not, if not, keep reading the file
	if( not firstLine and count == 0 ):
		continue
	#print (line)
	#since the regex matched before this it means first student record is found
	if(count == 0):
		#testline= firstLine[0]
		#print ("Hi", count, testline)
		#rollNoList = re.findall(rollNoRegEx , testline)
		#subjectList = re.findall(subjectRegEx , testline)
		#find the rollNo and subjects from the first line of record
		rollNoList = re.findall(rollNoRegEx , line)
		subjectList = re.findall(subjectRegEx , line)
		#increment this counter as to track that now second line of student record will be interpreted in next loop \
		# it is to make this if( not firstLine and count == 0 ): to fail as line will not match the regex and will continue\
		#otherwise
		count = count +1
	elif (count == 1):
		#print ("Hi", count, line)
		nameList = re.findall(nameRegEx, line)
		count = count + 1
	elif (count == 2):
		#testline = str(re.findall(allMarksRegEx, line))
		#print ("Hi    ----- ", count,  line)
		marksList = re.findall(marksRegEx, line)
		sidList = re.findall(sidRegEx, line)
		count = count+1
	elif (count == 3):
		#print ("Hi    ----- ", count,  line)
		schemeList = re.findall(schemeRegEx, line)
		count = count + 1
	else:
		#now all lines are extracted and only final line of grades is needed. At the end set count=0 to find new student
		##print ("Hi    ----- ", count,  line)
		#testline = str(re.findall(allGradeRegEx, line))
		##print ("Hi", testline)
		gradeList = re.findall(gradeRegEx, line)
		temp= []
		marksInternal = ""
		marksExternal = ""
		#build the marksList once more correctly as there are marks with " - 60"
		for x in range(0, len(marksList)):
			if str(marksList[x])[1].isdigit() and "-" in marksList[x]:
				temp.append(str(marksList[x]).replace("-", "").replace(" ", ""))
				temp.append("\"0\"")
			elif "-" in marksList[x]:
				temp.append("\"0\"")
				temp.append(str(marksList[x]).replace("-", "").replace(" ", ""))
			else:
				temp.append(marksList[x])
		
		marksList = temp
		performanceList = []
		#once the marks list is correctly made now we can filter the subject, internal, external and grading into a list\
		# for each student.
		for x in range(0, len(subjectList)):
			marksInternal = marksList[(2*x)]
			marksExternal = marksList[((2*x)+1)]
			#print ("internal - ", marksInternal)
			performanceList.append([subjectList[x], marksInternal, marksExternal, gradeList[x] ])
		#Now add all the data of student in university list
		universityList.append([rollNoList, nameList, sidList, schemeList, performanceList])	
		count = 0
for x in universityList:
	print("")
	print (x)
#print (universityList)
	
