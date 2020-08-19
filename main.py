from flask import Flask, render_template, url_for, request
import smtplib, re, pymongo
from random import randint
from pymongo import MongoClient


my_client = MongoClient('mongodb+srv://saiteja:nani8466@cluster0.0xd31.mongodb.net/<dbname>?retryWrites=true&w=majority')
my_db = my_client.saiteja
tablename1 = my_db["emails"]


app = Flask(__name__)


# this will generate us the 4 digit otp
random_otp = randint(1000, 9999)
# storing random otp result into otp variable
otp = random_otp


@app.route('/')
def home():
    return render_template('homepage.html')


@app.route('/verification', methods = ['POST', 'GET'])
def result():
    global email, otp, msg
    if request.method == 'POST':
        verification = request.form
        email = request.form.get('email')
        # otp = request.form.get('otp')
        if email in [temp['email'] for temp in tablename1.find({}, {'_id':0, 'email':1})]:
            msg = 'Email as verified already'
            return render_template('status.html', result = email, message = msg)
        else:
            e = smtplib.SMTP('smtp.gmail.com', 587)
            e.starttls()
            e.login('tsaiteja7@gmail.com', 'Welcome_nani@8466')
            otp_message = 'Your OTP is ' + str(otp)
            e.sendmail('tsaiteja7@gmail.com', email, otp_message)
            print("email as sent")
            e.quit()
            return render_template('verification.html', result = verification)


@app.route('/status', methods = ['POST', 'GET'])
def status():
    if request.method == 'POST':
        sent_otp = int(request.form.get('otp'))
        sent_email = email
        if sent_otp == otp:
            tablename1.insert_one({'email': email})
            msg = 'Email is verified'
            return render_template('status.html', email = sent_email, message = msg)
        else:
            msg = "You have entered wrong otp, Please check and try again"
            return render_template('status.html', message = msg)


if __name__ == '__main__':
    app.run(debug=True)



