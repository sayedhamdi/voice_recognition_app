from flask import Flask, render_template,request ,redirect,send_from_directory ,flash , url_for
from os.path import  join, dirname, realpath
from werkzeug.utils import secure_filename

import speech_recognition as sr 


app = Flask(__name__)

UPLOADS_FOLDER = join(dirname(realpath(__file__)), 'static/uploads')

ALLOWED_EXTENSIONS = {'wav','mp3'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOADS_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template("index.html")
    


@app.route('/uploads', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(join(app.config['UPLOAD_FOLDER'], filename))
            text = Recognize_to_text(filename)
            return render_template("result.html",text=text)
            


@app.route('/upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
 
def Recognize_to_text(filename):
     
    AUDIO_FILE = join(app.config['UPLOAD_FOLDER'], filename)
    
    # use the audio file as the audio source 
    
    r = sr.Recognizer() 
    
    with sr.AudioFile(AUDIO_FILE) as source: 
        #reads the audio file. Here we use record instead of 
        #listen 
        audio = r.record(source)   
    
    try: 
        text = r.recognize_google(audio)
        print("The audio file contains: " + r.recognize_google(audio)) 
    
    except sr.UnknownValueError: 
        print("Google Speech Recognition could not understand audio") 
    
    except sr.RequestError as e: 
        print("Could not request results from Google Speech  Recognition service; {0}".format(e)) 
    return text

