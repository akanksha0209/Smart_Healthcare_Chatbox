import smtplib

my_email = "akankshaapai0209@gmail.com"
my_password = "0203202001"
connection = smtplib.SMTP("smtp.gmail.com")
connection.starttls()
connection.login(user=my_email, password=my_password)
connection.sendmail(from_addr=my_email, to_addrs="nisargav.is20@rvce.edu.in ", msg="Hi its me...ur aku!!!!")
connection.close()
import os
# from twilio.rest import Client
#
# TWILIO_AUTH_TOKEN='06ad7e4678c4a070583f8eac8bb621bf'
# TWILIO_ACCOUNT_SID='AC4baa963cf82e183f476146c38b7c949a'
# # Find your Account SID and Auth Token at twilio.com/console
# # and set the environment variables. See http://twil.io/secure
# account_sid = TWILIO_ACCOUNT_SID
# auth_token = TWILIO_AUTH_TOKEN
# client = Client(account_sid, auth_token)
#
# message = client.messages \
#     .create(
#          media_url=['https://images.unsplash.com/photo-1545093149-618ce3bcf49d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=668&q=80'],
#          from_='whatsapp:+918105138859',
#          to='whatsapp:+918277795385'
#      )
#
# print(message.sid)
#!/usr/bin/python

# import smtplib
# from smtplib import SMTPException
#
# sender = 'from@fromdomain.com'
# receivers = ['to@todomain.com']
#
# message = """From: From Person <from@fromdomain.com>
# To: To Person <to@todomain.com>
# Subject: SMTP e-mail test
#
# This is a test e-mail message.
# """
#
# try:
#    smtpObj = smtplib.SMTP('localhost')
#    smtpObj.sendmail(sender, receivers, message)
#    print( "Successfully sent email")
# except SMTPException:
#    print ("Error: unable to send email")