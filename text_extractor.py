from PyPDF2 import PdfFileReader

#Define path to PDF file
pdf_file_name = "C:/Users/vrajb/OneDrive/Desktop/Vrajeshkumar_resume.pdf"

#Open the file in binary mode for reading
with open(pdf_file_name, 'rb') as pdf_file:
    #Read the PDF file
    pdf_reader = PdfFileReader(pdf_file)
    #Get number of pages in the PDF file
    page_nums = pdf_reader.numPages
    #Iterate over each page number
    for page_num in range(page_nums):
        #Read the given PDF file page
        page = pdf_reader.getPage(page_num)
        #Extract text from the given PDF file page
        text = page.extractText()
        #Print text
        print(text)