import glob
from collections import OrderedDict

outfilename = 'FeatureStore.txt'
cleanedfilename = 'FinalFeatures.txt'

filenames = glob.glob('JSReference/*.txt')
print "Hello!"

JSDict = OrderedDict()
dupDict = OrderedDict()

#A dictionary of mismatching duplicates, with final labels set manually
dict_manual = {
"item":"R",
"id":"R",
"error":"E",
"type":"R",
"target":"R",
"clear":"W",
"accessKey":"R",
"value":"R",
"height":"R",
"width":"R",
"select":"E",
"toggle":"W",
"open":"N",
"returnValue":"R",
"hidden":"R",
"translate":"W",
"validationMessage":"R",
"validity":"R",
"willValidate":"R",
"checkValidity":"E",
"reportValidity":"E",
"files":"R",
"sizes":"R",
"ended":"E",
"readyState":"E",
"seeking":"R",
"start":"E",
"label":"R",
"length":"R",
"htmlFor":"R",
"rows":"R",
"content":"R",
"kind":"R",
"close":"N",
"data":"R",
"search":"E",
"replace":"W",
"message":"R",
"name":"R",
"version":"R",
"selectedIndex":"R",
"event":"E",
"location":"R",
"moveTo":"W",
"prompt":"R",
"restore":"E",
}

key = 0

#Merge all in one file
with open(outfilename, 'w') as outfile:
    for fname in filenames:
        with open(fname, 'r') as readfile:
            infile = readfile.read()
            for char in infile:
                #print "Writing....."
                #print char
                outfile.write(char)


#Remove redundancy, and write the final set of featues to JSDict
with open(outfilename, 'r') as readoutfile:
	countMatch = 0
	countMis = 0
	countdis = 0
	for line in readoutfile:
		if '|' in line:
			content = line.split('|')[0]
			label = line.strip().split('|')[1]
			if content not in JSDict:
				#print "Not found"
				JSDict[content] = label
			else:
				#print "Found!  " + content + " labeled as: " + JSDict[content]
				#print "new label is " + label
				
				if JSDict[content] != label:
					print "Label Mismatch!  " + content + " is labeled as: " + JSDict[content]
					print "new label is " + label
					countMis = countMis + 1

					if content not in dupDict:
						dupDict[content] = label
						countdis = countdis + 1

	    			#Make decisions on mismatched duplicate labels, based on dict_manual
					if content in dict_manual:
						label = dict_manual[content]
						print "Final label is set as: " + label
						JSDict[content] = label

				else:
					countMatch = countMatch + 1

    			
#Writing final features
with open(cleanedfilename, 'w') as cleanedfile:
	for feature in JSDict:
		aline = feature + "|" + JSDict[feature] + "\n"
		cleanedfile.write(aline)


print JSDict
print "\n\n\n\n\n\n\n\n"

print "This is a list of mimatching distinct duplicates:"
for item in dupDict:
	print item

print "Matching cases = " + str(countMatch)
print "Mismatching cases = " + str(countMis)
print "The total number of distinct mismatched duplicates is: " + str(countdis)
