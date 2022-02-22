#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import smtplib

def main(user, pass):
    # SET EMAIL LOGIN REQUIREMENTS
    # gmail_user = 'satishadhikari71@gmail.com'
    # gmail_app_password = 'hahahehehoHO71!'
    gmail_user = user
    gmail_app_password = pass

    # SET THE INFO ABOUT THE SAID EMAIL
    sent_from = gmail_user
    # sent_to = ['THE-TO@gmail.com', 'THE-TO@gmail.com']
    sent_to = ['satishadhikari.075@kathford.edu.np']
    sent_subject = "Where are all my Robot Women at?"
    sent_body = ("Hey, what's up? friend!\n\n"
                 "I hope you have been well!\n"
                 "\n"
                 "Cheers,\n"
                 "Jay\n")

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(sent_to), sent_subject, sent_body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_app_password)
        server.sendmail(sent_from, sent_to, email_text)
        server.close()

        print('Email sent!')
    except Exception as exception:
        print("Error: %s!\n\n" % exception)
