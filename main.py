import os
import glob
from flask import Flask, flash, request, redirect, url_for,render_template
from werkzeug.utils import secure_filename
from PyPDF2 import PdfFileReader
from prediction import predict_title

UPLOAD_FOLDER = 'upload_files'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['filename'] = ''
success_log = []
text = ''

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def text_extractor(pdf_file_name):  
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
        print(text)
        success_log.append('text extracted successfully')
        return render_template("index.html",success = success_log)

   # return text


@app.route('/')
def index():
   success_log.clear()
   return render_template("index.html")



@app.route('/upload_file', methods=['POST','GET'])
def upload_file():
   uploaded_file = request.files['file']

   if uploaded_file.filename != '':
      filename = secure_filename(uploaded_file.filename)
      app.config['filename'] = filename
      file_path = app.config['UPLOAD_FOLDER']+'/'+filename
      uploaded_file.save(file_path)
      print('-------------file uploaded-----------')
      # print(app.config['UPLOAD_FOLDER']+'/'+filename)
      # os.remove(file_path)
      success_log.append('File uploded')
      f_name = uploaded_file.filename
      print('filename',filename)
      return render_template("index.html",logs = success_log,name=filename)
   else:
      print('-----------unsuccessful------------') 

@app.route('/predict', methods=['POST','GET'])
def predict():
   # upload_file()
   print('file name',app.config['filename'])
   text = text_extractor(app.config['UPLOAD_FOLDER']+'/'+app.config['filename'])
   best_title,prob,titles = predict_title(text)
   print(best_title)
   success_log.append('Best title predicted')
   return render_template("index.html",logs = success_log,title=best_title[0])

if __name__ == '__main__':
   app.run(debug = True)