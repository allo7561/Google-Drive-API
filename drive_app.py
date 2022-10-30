from flask import Flask, render_template, request, flash, redirect, url_for
import os
import requests 
import driveFolder as df
import uploader as upld
from utils import upload_basic
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/')
def home():
    # returns index
    return render_template('index.html')        

@app.route('/link_search', methods = ["POST", "GET"])
def link_search():
    # checks if the user submitted a folder id
    if request.method == "POST":
        # if they did submit, the folder id is pulled from the form
        user_folder_id = request.form['user_folder_id']
        # a new drive folder object is made, utilizing the inputted folder id
        new_object = df.Drive_folder(user_folder_id)
        # lists all the files from the object
        files = new_object.file_names
        # returns the results page, passing in the files and the folder id
        return render_template('results.html', files = files, user_folder_id = user_folder_id)
    # returns the link search page
    return render_template('link_search.html')

# declares the path to the current directory into a variable
dir_path = os.path.dirname(os.path.realpath(__file__))
# assigns the upload folder from within the directory
UPLOAD_FOLDER = f'{dir_path}/UPLOAD_FOLDER'
# allowed extensions for upload
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mov', 'mp4'}
# this is boiler plate flask code, not entirely sure what it does, but seems very important
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# boiler plate flask code for checking that the file is an allowed extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    #checks if the user uploaded anything
    if request.method == 'POST':
        # check if the post request has the file part (boiler plate flask code)
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an empty file without a filename (boiler plate flask code)
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        # if a file exists and the file extension is valid
        if file and allowed_file(file.filename):
            # ensure the file name is secure
            filename = secure_filename(file.filename)
            # save the uploaded file to the upload folder
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # create a variable that holds the path and the file name
            file_to_upload = f'{UPLOAD_FOLDER}/{filename}'
            # create a new instance of the Uploader class
            uploader_object = upld.Uploader()
            # create a new google drive folder using the folder_maker method
            new_folder = uploader_object.folder_maker()
            # upload the file, passing the filename, the path to the file, and the id of the newly create drive folder
            upload_basic(filename, file_to_upload, new_folder)
            # create a new folder object, like in the link search route, but using the newly created folder id, instead of a provided id
            new_folder_object = df.Drive_folder(new_folder)
            # list the files from the new folder object
            files = new_folder_object.file_names
            # feed the files and folder id into the results page
            return render_template('results.html', files = files, new_folder = new_folder)
    # renders the upload page    
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0', port=3000)