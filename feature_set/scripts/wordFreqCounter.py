import re
import string
frequency = {}
document_text = open('test.txt','r')


#Change all to lower case
text_string = document_text.read().lower()

#define a pattern
#return words with number of characters in the range [3-15]
#\b is related to word boundary

match_pattern = re.findall(r'\b[a-z]{3,15}\b', text_string)

for word in match_pattern:
	count = frequency.get(word,0)
	frequency[word] = count + 1

frequency_list = frequency.keys()

for words in frequency_list:
	print words, frequency[words]



