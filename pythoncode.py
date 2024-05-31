from flask import Flask, render_template, request, jsonify
import smtplib
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

def send_scheduled_email(recipient, subject, body):
    try:
        sender_email = "xyz@gmail.com"
        sender_password = ""
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, sender_password)
        message = f"Subject: {subject}\n\n{body}"
        server.sendmail(sender_email, recipient, message)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(str(e))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    data = request.get_json()
    recipient = data['recipient']
    subject = data['subject']
    body = data['body']
    send_time = data.get('sendTime')

    if send_time:
        scheduler = BackgroundScheduler()
        scheduler.add_job(send_scheduled_email, 'date', run_date=send_time, args=[recipient, subject, body])
        scheduler.start()
        return jsonify({'status': 'success', 'message': 'Email scheduled successfully!'})
    else:
        try:
            sender_email = "xyz@gmail.com"
            sender_password = ""
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(sender_email, sender_password)
            message = f"Subject: {subject}\n\n{body}"
            server.sendmail(sender_email, recipient, message)
            server.quit()
            return jsonify({'status': 'success', 'message': 'Email sent successfully!'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
