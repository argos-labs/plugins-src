

import PyPDF2
import textract
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


#Write a for-loop to open many files (leave a comment if you'd like to learn how).
filename = 'data01/[다원에셋] 경기 용인시 수지구 신봉동 946 신봉마을동부센트레빌6단지 605-602.pdf'
#open allows you to read the file.
pdfFileObj = open(filename,'rb')
#The pdfReader variable is a readable object that will be parsed.
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
#Discerning the number of pages will allow us to parse through all the pages.
num_pages = pdfReader.numPages
count = 0
text = ""
#The while loop will read each page.
while count < num_pages:
    pageObj = pdfReader.getPage(count)
    count +=1
    text += pageObj.extractText()
#This if statement exists to check if the above library returned words. It's done because PyPDF2 cannot read scanned files.
if text:
   text = text
#If the above returns as False, we run the OCR library textract to #convert scanned/image based PDF files into text.
else:
   text = textract.process(filename, method='tesseract', language='eng')
#Now we have a text variable that contains all the text derived from our PDF file. Type print(text) to see what it contains. It likely contains a lot of spaces, possibly junk such as '\n,' etc.
#Now, we will clean our text variable and return it as a list of keywords.

print(text)

#The word_tokenize() function will break our text phrases into individual words.
tokens = word_tokenize(text)
#We'll create a new list that contains punctuation we wish to clean.
punctuations = ['(',')',';',':','[',']',',']
#We initialize the stopwords variable, which is a list of words like "The," "I," "and," etc. that don't hold much value as keywords.
stop_words = stopwords.words('english')
#We create a list comprehension that only returns a list of words that are NOT IN stop_words and NOT IN punctuations.
keywords = [word for word in tokens if not word in stop_words and not word in punctuations]

