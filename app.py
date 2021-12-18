from PIL import Image
import pytesseract
from flask import Flask, render_template, request
from main import *


def ocr_core(filename):
    text = pytesseract.image_to_string(Image.open(
        filename))  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    return text


app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)


# function to check the file extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# route and function to handle the home page
@app.route('/', methods=['GET', 'POST'])
def homepage():
    return render_template('index.html')


@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        # check if there is a file in the request
        if 'file' not in request.files:
            return render_template('messages.html', msg='No file selected')
        file = request.files['file']
        # if no file is selected
        if file.filename == '':
            return render_template('messages.html', msg='No file selected')

        if file and allowed_file(file.filename):
            # call the OCR function on it
            extracted_text = ocr_core(file)

            # extract the text and display it
            return render_template('result.html',
                                   msg='Successfully processed',
                                   extracted_text=extracted_text)
    else:
        return render_template('messages.html')


@app.route('/prescription', methods=['POST'])
def prescription():
    if request.method == 'POST':
        return render_template('prescription.html')
    else:
        return render_template('messages.html')


@app.route('/interactions', methods=['POST'])
def interactions():
    if request.method == 'POST':
        # TODO python script to derive drugs interactions from medicines
        if 'medicines' not in request.form:
            return render_template('messages.html', msg='No file selected')
        text_detected = request.form['medicines']
        interactions_final, med_drugs_dict = get_interactions_from_med(text_detected, True)

        if type(interactions_final) == str:
            return render_template('messages.html', msg=interactions_final)
        try:
            # this line removes duplicates from the list of dicts on the basis of 'Desc' value
            interactions_final = list({v['Desc']: v for v in interactions_final}.values())
        except Exception as e:
            print('Empty')
        print('App.py: ', interactions_final)
        print('Type is: ', type(interactions_final))
        print('App.py: ', med_drugs_dict)
        print('Type is: ', type(med_drugs_dict))

        return render_template('interactions.html', msg='Text successfully recognized', result_text=text_detected,
                               all_interactions=interactions_final, med_drugs_dict=med_drugs_dict)


    else:
        return render_template('messages.html')


@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)
