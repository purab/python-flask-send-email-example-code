from flask import Flask, render_template, request
from flask_mail import Mail, Message
import os
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
# initialize the log handler
logHandler = RotatingFileHandler('info.log', maxBytes=1000, backupCount=1)

# set the log handler level
logHandler.setLevel(logging.INFO)

# set the app logger level
app.logger.setLevel(logging.INFO)

app.logger.addHandler(logHandler) 

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['PORT'] = 465
app.config['MAIL_USERNAME'] = 'your_username'
app.config['MAIL_PASSWORD'] = 'your_pass'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

@app.route("/home",methods=["GET","POST"])
@app.route("/",methods=["GET","POST"])
def home():
    if request.method =='POST':
        msg = Message("subject",sender="noreply@gmail.com",recipients="test@test.com",body="this is body")
        retcode = 0
        try:
            mail.send(msg)
        except mail.exceptions.SMTPResponseException as e:
            retcode = 2
        except mail.exceptions.SMTPServerDisconnected as e:
            retcode = 3
        except mail.exceptions.SMTPException as e:
            retcode = 1
        app.logger.error('mail send error: '+retcode)
        return "send email"
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)    
