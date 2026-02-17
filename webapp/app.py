from flask import Flask, render_template, request, send_file
import os
import time
from topsis.core import calculate_topsis
import smtplib
from email.message import EmailMessage

app = Flask(__name__,
            template_folder='.',
            static_folder='.',
            static_url_path='')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
RESULT_FOLDER = os.path.join(BASE_DIR, 'results')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

EMAIL = "mridulbatra2005@gmail.com"
PASSWORD = ""

def send_email(receiver_email, file_path):
    msg = EmailMessage()
    msg['Subject'] = 'TOPSIS Result'
    msg['From'] = EMAIL
    msg['To'] = receiver_email
    msg.set_content("Your TOPSIS result is attached.")

    with open(file_path, 'rb') as f:
        msg.add_attachment(
            f.read(),
            maintype='application',
            subtype='octet-stream',
            filename=os.path.basename(file_path)
        )

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL, PASSWORD)
        smtp.send_message(msg)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    try:
        file = request.files['file']
        weights = request.form['weights']
        impacts = request.form['impacts']
        email = request.form['email']

        unique_name = str(int(time.time())) + "_" + file.filename
        file_path = os.path.join(UPLOAD_FOLDER, unique_name)

        file.save(file_path)
        print("Saved file:", file_path)

        output_filename = unique_name.split('.')[0] + "_result.csv"
        output_file = os.path.join(RESULT_FOLDER, output_filename)

        calculate_topsis(file_path, weights, impacts, output_file)
        print("Saved result:", output_file)

        send_email(email, output_file)

        return send_file(output_file, as_attachment=True)

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
