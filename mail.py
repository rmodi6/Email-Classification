import re
import os
import sys
import imaplib
import email

class Mail():

	GMAIL_IMAP_HOST = 'imap.gmail.com'
	OUTLOOK_IMAP_HOST = 'imap-mail.outlook.com'

	def __init__(self):
		self.username = None
		self.password = None
		self.imap = None
		self.pattern_uid = re.compile('\d+ \(UID (?P<uid>\d+)\)')
		self.pattern_email = re.compile(r"(@[a-zA-Z0-9-]+\.)")

	def parse_uid(self, data):
		match = self.pattern_uid.match(data)
		return match.group('uid')

	def parse_emailaddr(self, data):
		match = self.pattern_email.search(data)
		return match.group()[1:-1]
	
	def login(self, username, password):
		self.username = username
		self.password = password
		email_server = self.parse_emailaddr(username)

		if email_server == 'gmail':
			self.imap = imaplib.IMAP4_SSL(self.GMAIL_IMAP_HOST)
		elif email_server == 'outlook' or email_server == 'live' or email_server == 'hotmail':
			self.imap = imaplib.IMAP4_SSL(self.OUTLOOK_IMAP_HOST)
			


		print('Trying to login...')
		try:
			response, data = self.imap.login(self.username, self.password)
			if response == 'OK':
				print('Login Successful.')
				return True
		except imaplib.IMAP4.error:
			print("Authentication Error!")
			return False

	def logout(self):
		return self.imap.logout()

	def list(self):
		response, results = self.imap.list()
		if response == 'OK':
			return results

	def select(self, mailbox_name):
		response, data = self.imap.select(mailbox_name)
		if response == 'OK':
			return True
		else:
			print(mailbox_name + ' folder not found.')
			return False

	def fetch_mailbox(self, path, mailbox_name):
		folder_path = path + mailbox_name + "\\"
		if not os.path.exists(folder_path):
			os.mkdir(folder_path)

		response, data = self.imap.select(mailbox_name)
		response, data = self.imap.search(None, "ALL")
		if response != 'OK':
			print('No messages found in the folder ' + mailbox_name)
			return

		count, total = 1, len(data[0].split())

		for id in data[0].split():
			response, data = self.imap.fetch(id, '(RFC822)')
			if response != 'OK':
				print ("ERROR getting message", id)
				return

			msg = email.message_from_string(data[0][1].decode("utf-8"))
			
			outfile = open(folder_path + str(count) + ".txt", 'w') # open file for appending
			outfile.write("Subject: " + msg['Subject'] + "\n")
			# print ('Message %s: %s' % (id, msg['Subject']))

			for part in msg.walk():
				if part.get_content_type() == 'text/plain':
					outfile.write("Content-Type: text/plain; charset=utf-8"+"\nx-filename: "+str(count)+"\n\n"+part.get_payload())
					# print (part.get_payload()) 
					# body.append(part.get_payload())
			count += 1

	def fetch_unread(self, path):
		response, data = self.imap.select("Inbox", readonly = False)
		response, data = self.imap.search(None, "UNSEEN")
		if response != 'OK':
			print('No new messages found.')
			return

		count, msg_uids = 1, []

		for id in data[0].split():
			resp, items = self.imap.fetch(id, '(UID)')
			msg_uids.append(self.parse_uid(items[0].decode('UTF-8')))

			response, data = self.imap.fetch(id, '(RFC822)')
			if response != 'OK':
				print ("ERROR getting message", id)
				return

			msg = email.message_from_string(data[0][1].decode("utf-8"))
			
			outfile = open(path + str(count) + ".txt", 'w') # open file for appending
			outfile.write("Subject: " + msg['Subject'] + "\n")
			# print ('Message %s: %s' % (id, msg['Subject']))

			for part in msg.walk():
				if part.get_content_type() == 'text/plain':
					outfile.write("Content-Type: text/plain; charset=utf-8"+"\nx-filename: "+str(count)+"\n\n"+part.get_payload())
					# print (part.get_payload()) 
					# body.append(part.get_payload())
			count += 1

		return msg_uids

	def assign_label(self, msg_uids, predictions):

		for i in range(len(predictions)):
			mov, data = self.imap.uid('STORE', msg_uids[i] , '-FLAGS', '(\SEEN)')
			result = self.imap.uid('COPY', msg_uids[i], predictions[i])
			if result[0] == 'OK':
				mov, data = self.imap.uid('STORE', msg_uids[i] , '+FLAGS', '(\Deleted)')
				self.imap.expunge()

if __name__ == '__main__':
	e = Mail()
	usr = ''
	pwd = ''
	e.login(usr, pwd)