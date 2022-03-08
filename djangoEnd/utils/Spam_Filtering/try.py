import easyimap

host = 'imap.gmail.com'
user = 'satishadhikari.075@kathford.edu.np'
password = 'hahahehehoHO71!'
mailbox = 'INBOX.subfolder'
imapper = easyimap.connect(host, user, password, mailbox)

email_quantity = 10
emails_from_your_mailbox = imapper.listids(limit=email_quantity)
print(emails_from_your_mailbox)
imapper.quit()
