# from resume_parser import resumeparse

# data = resumeparse.read_file(r"C:\Users\vrajb\OneDrive\Desktop\Vrajeshkumar's Resume.pdf")

import pandas as pd
import spacy
from PyPDF2 import PdfFileReader

nlp = spacy.load('en_core_web_sm')

## Extracting text from PDF
def pdftotext(m):
    # pdf file object
    # you can find find the pdf file with complete code in below
    pdfFileObj = open(m, 'rb')

    # pdf reader object
    pdfFileReader = PdfFileReader(pdfFileObj)

    # number of pages in pdf
    num_pages = pdfFileReader.numPages

    currentPageNumber = 0
    text = ''

    # Loop in all the pdf pages.
    while(currentPageNumber < num_pages ):

        # Get the specified pdf page object.
        pdfPage = pdfFileReader.getPage(currentPageNumber)

        # Get pdf page text.
        text = text + pdfPage.extractText()

        # Process next page.
        currentPageNumber += 1
    return (text)

def extract_skills(resume_text):
    nlp_text = nlp(resume_text)

    # removing stop words and implementing word tokenization
    tokens = [token.text for token in nlp_text if not token.is_stop]
    colnames = ['skill']
    
    
    skills = ["machine learning",
             "deep learning",
             "nlp",
             "natural language processing",
             "mysql",
             "sql",
             "django",
             "computer vision",
              "tensorflow",
             "opencv",
             "mongodb",
             "artificial intelligence",
             "ai",
             "flask",
             "robotics",
             "data structures",
             "python",
             "c++",
             "matlab",
             "css",
             "html",
             "github",
             "php"]

             
    skills = pd.DataFrame(skills)
    skills.to_csv('skill.csv')
    # reading the csv file
    data = pd.read_csv('skill.csv', names=colnames) 
    
    # extract values
    skills = data.skill.tolist()
    # print(skills)
    skillset = []
    
    # check for one-grams (example: python)
    for token in tokens:
        if token.lower() in skills:
            skillset.append(token)
   
    for token in nlp_text.noun_chunks:
        token = token.text.lower().strip()
        if token in skills:
            skillset.append(token)
    return [i.capitalize() for i in set([i.lower() for i in skillset])]

resume_text = pdftotext(r"C:\Users\vrajb\OneDrive\Desktop\Vrajeshkumar's Resume.pdf")  

print ('Skills',extract_skills(resume_text))