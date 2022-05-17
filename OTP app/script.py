from flask import *
import smtplib
import random


app = Flask(__name__)

global OTP
OTP = random.randint(100000, 999999)
#print(OTP)

def OTPapi(email):
    TEXT = f"Dear Customer,\n\n{OTP} is your One Time Password (OTP). Please enter to proceed \n\nThank you,"
    SUBJECT = "LAN CHAT APP"
    msg = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("otpbot9094@gmail.com", "qqpbvnzvfveabtkr")
    emailid = email
    s.sendmail("&&", emailid, msg)

    return True


@app.route('/')
def home():
    return render_template('OTP.html')

@app.route('/getOTP' , methods=['POST'])
def enterotp():
    number = request.form['number']
    val = OTPapi(number)
    if val:
        return render_template('verify.html')
    else:
         return 'error occured'

@app.route('/verifyOTP',methods=['POST'])
def verifyOTP():
    otp = request.form['oneTP']
    c = int(otp)
    if c == OTP:
        return 'Verified!!!'
    else:
        return 'Please try again'



if __name__ == '__main__':
    app.run(debug=True)