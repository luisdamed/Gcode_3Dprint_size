import os
import re
from flask import Flask, redirect, send_file, url_for, render_template, request
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField
from werkzeug.utils import secure_filename
from gcode_get_size import get_max_size

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"txt", "gco", "gcode"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 15 * 1000 * 1000
app.config["SECRET_KEY"] = os.urandom(24)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


class UploadFileForm(FlaskForm):
    file = FileField(
        "File",
        validators=[
            FileRequired(),
            FileAllowed(["txt", "gco", "gcode"], "Gcode only!"),
        ],
    )
    submit = SubmitField("Get model dimensions")
    submit2 = SubmitField("Remove extrusions")


@app.route("/", methods=["GET", "POST"])
def upload_file():
    form = UploadFileForm()
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        form.file.data.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        if request.form.get("action") == "Get model dimensions":
            return redirect(url_for("show_results", name=filename))
        if request.form.get("action") == "Remove extrusions":
            return redirect(url_for("edit_file", name=filename))
    return render_template("index.html", form=form)


from flask import send_from_directory


@app.route("/uploads/<name>")
def show_results(name):
    with open(os.path.join(app.config["UPLOAD_FOLDER"], name), "r") as f:
        lines = f.readlines()  # List of strings, one for each line
        text_string = "".join(lines)  # Large string containing all the text
        x_max, y_max, z_max = get_max_size(text_string)
    return render_template("results.html", x_size=x_max, y_size=y_max, z_size=z_max)


@app.route("/removed/<name>")
def edit_file(name):
    pattern = r"(?<=E)-?\d*(\.\d+)"
    replace = r"0.000001"
    with open(os.path.join(app.config["UPLOAD_FOLDER"], name), "r") as f:
        lines = f.readlines()  # List of strings, one for each line
        text_string = "".join(lines)  # Large string containing all the text
    len1 = len(text_string)
    str_output = re.sub(pattern, replace, text_string)
    len2 = len(str_output)

    path = os.path.join(app.config["UPLOAD_FOLDER"], f"edited_{name}")

    with open(path, "w") as edit_file:
        edit_file.write(str_output)

    return send_file(path, as_attachment=True)


if __name__ == "__main__":
    # app.run()
    app.run(host="127.0.0.1", port=8080, debug=False)
