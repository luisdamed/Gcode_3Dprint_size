import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from gcode_get_size import get_max_size


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'gco', 'gcode'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('show_results', name=filename))
    return render_template("index.html")
    # return '''
    # <!doctype html>
    # <title>Upload new File</title>
    # <h1>Upload new File</h1>
    # <form method=post enctype=multipart/form-data>
    #   <input type=file name=file>
    #   <input type=submit value=Upload>
    # </form>
    # '''

from flask import send_from_directory

@app.route('/uploads/<name>')
def show_results(name):
    with open(os.path.join(app.config['UPLOAD_FOLDER'], name), 'r') as f:
            lines = f.readlines()  # List of strings, one for each line 
            text_string  = ''.join(lines) # Large string containing all the text
            x_max, y_max, z_max = get_max_size(text_string)
    return render_template("results.html", 
                           x_size = x_max, 
                           y_size = y_max, 
                           z_size = z_max )

# if __name__ == "__main__":
#     app.run()
    # app.run(host="127.0.0.1", port=8080, debug=False)


