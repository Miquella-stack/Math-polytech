import os
import smtplib
import mimetypes

from flask import Flask, render_template, redirect, request
from dotenv import load_dotenv

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders


app = Flask(__name__)
load_dotenv()
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

 
@app.route("/s")
def a():

    return 'ususus'


@app.route("/", methods=['GET', 'POST'])
def creator():

    if request.method == 'POST':

        dict_ = request.form.to_dict()
        user_file = request.files['fileFF']
        file_url = f'vs/static/img/{user_file.filename}'
        with open(file_url, 'wb') as new_file:
            new_file.write(user_file.read())

        send_email(dict_['contactFF'], dict_['nameFF'], dict_['messageFF'], file_url)

        return redirect('/')
    
    return render_template("index.html")


def attach_file(message: MIMEMultipart, f):

    attach_types = {
        'text': MIMEText,
        'image': MIMEAudio,
        'audio': MIMEImage
    }

    filename = os.path.basename(f)
    ctype, encoding = mimetypes.guess_type(f)

    if (ctype is None) or (encoding is not None):
        ctype = 'application/octet-stream'

    maintype, subtype = ctype.split('/', 1)

    with open(f, mode='rb' if maintype != 'text' else 'r') as fp:
        if maintype in attach_types:
            file = attach_types[maintype](fp.read(), _subtype=subtype)
        else:
            file = MIMEBase(maintype, subtype)
            file.set_payload(fp.read())
            encoders.encode_base64(file)

    file.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(file)
            




def send_email(to_mail, subject, text, file):

    from_mail = os.getenv("FROM")
    password = os.getenv("PASSWORD")

    message = MIMEMultipart()
    message["From"] = from_mail
    message["To"] = to_mail
    message["Subject"] = subject


    # recipient_mail = os.getenv("TO_EMAIL")
    # text += f'Отправлено пользователем {subject}'

    message.attach(MIMEText(text, "plain"))
    attach_file(message, file)
    
    server = smtplib.SMTP_SSL(os.getenv("HOST"), os.getenv("PORT"))
    server.login(from_mail, password)
    server.send_message(message)
    server.quit()


if __name__ == '__main__':
    app.run(port=3000, host='127.0.0.1')