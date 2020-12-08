import os
import knn
import mnb
import knn_classify
import mnb_classify
import extract as ex
from mail import Mail
from pprint import pprint
from getpass import getpass

if __name__ == '__main__':
	current_path = os.path.dirname(os.path.abspath(__file__))
	choice = 0
	while choice != 5:
		print('\nMenu:')
		print('1 -> Create Dataset.\n2 -> Classify using kNN.\n3 -> Classify using MNB.\n4 -> Exit.')
		choice = int(input('Enter your choice: '))
		
		if choice == 1:
			# Create Dataset
			reply = input('Do you want to get emails from your email account? (y/n): ')[0].lower()
			if reply == 'n':
				dataset_name = input('Enter the name of existing dataset folder: ')
				ex.main(dataset_name)
			elif reply == 'y':
				usr = input('Email: ')
				pwd = getpass('Password: ')
				e = Mail()
				success = e.login(usr, pwd)
				if success:
					dataset_name = input('Enter a name for your dataset: ')
					dataset_path = os.path.join(current_path, dataset_name)
					if not os.path.exists(dataset_path):
						os.mkdir(dataset_path)

					print('Your Folders:')
					pprint(e.list())
					folder_names = []
					print('Enter folder names you want in your dataset: (New line when done)')
					while True:
						name = input()
						if name == '':
							if len(folder_names) < 2:
								print('Enter atleast two Folders!')
								continue
							else:
								break
						success = e.select(name)
						if success:
							folder_names.append(name)

					for label in folder_names:
						print('Fetching mails from ' + label + '...')
						e.fetch_mailbox(dataset_path, label)

					e.logout()
					ex.main(dataset_name)

			else:
				print('Invalid Input.')

		elif choice == 2:
			# Classify using kNN
			choice2 = 0
			while choice2 != 4:
				print('\nkNN Classification:')
				print('1 -> Classify Dataset. (Splits Dataset into training and test set)')
				print('2 -> Classify Testset. (Test kNN accuracy using Dataset as training set)')
				print('3 -> Classify New Emails.\n4 -> Back.')
				choice2 = int(input('Enter your choice: '))

				if choice2 == 1:
					# Classify Dataset
					dataset_name = input('Enter the name of dataset folder to be classified: ')
					knn.main(dataset_name)

				elif choice2 == 2:
					# Classify Testset
					dataset_name = input('Enter the name of dataset folder to be used as training set: ')
					testset_name = input('Enter the name of test set folder: ')
					knn_classify.main(dataset_name, testset_name)

				elif choice2 == 3:
					# Classify New Emails
					dataset_name = input('Enter the name of dataset folder to be used as training set: ')
					reply = input('Do you want get new unread emails from your email account? (y/n): ')[0].lower()
					
					if reply == 'y':
						usr = input('Email: ')
						pwd = getpass('Password: ')
						e = Mail()
						success = e.login(usr, pwd)
						if success:
							new_emails_name = input('Enter a folder name to store new emails: ')
							new_emails_path = current_path + new_emails_name + "\\"
							if not os.path.exists(new_emails_path):
								os.mkdir(new_emails_path)
							msg_uids = e.fetch_unread(new_emails_path)
							knn_classify.main(dataset_name, new_emails_name, new_emails = True)

					elif reply == 'n':
						new_emails_name = input('Enter the name of new emails folder: ')
						knn_classify.main(dataset_name, new_emails_name, new_emails = True)
					else:
						print('Invalid Input.')

				elif choice2 == 4:
					break

				else:
					print('Invalid choice.')
		
		elif choice == 3:
			# Classify using MNB
			choice2 = 0
			while choice2 != 4:
				print('\nMNB Classification:')
				print('1 -> Classify Dataset. (Splits Dataset into training and test set)')
				print('2 -> Classify Testset. (Test MNB accuracy using Dataset as training set)')
				print('3 -> Classify New Emails.\n4 -> Back.')
				choice2 = int(input('Enter your choice: '))

				if choice2 == 1:
					# Classify Dataset
					dataset_name = input('Enter the name of dataset folder to be classified: ')
					mnb.main(dataset_name)

				elif choice2 == 2:
					# Classify Testset
					dataset_name = input('Enter the name of dataset folder to be used as training set: ')
					testset_name = input('Enter the name of test set folder: ')
					mnb_classify.main(dataset_name, testset_name)

				elif choice2 == 3:
					# Classify New Emails
					dataset_name = input('Enter the name of dataset folder to be used as training set: ')
					reply = input('Do you want get new unread emails from your email account? (y/n): ')[0].lower()
					
					if reply == 'y':
						usr = input('Email: ')
						pwd = getpass('Password: ')
						e = Mail()
						success = e.login(usr, pwd)
						if success:
							new_emails_name = input('Enter a folder name to store new emails: ')
							new_emails_path = current_path + new_emails_name + "\\"
							if not os.path.exists(new_emails_path):
								os.mkdir(new_emails_path)
							msg_uids = e.fetch_unread(new_emails_path)
							predictions = mnb_classify.main(dataset_name, new_emails_name, new_emails = True)
							e.assign_label(msg_uids, predictions)

					elif reply == 'n':
						new_emails_name = input('Enter the name of new emails folder: ')
						mnb_classify.main(dataset_name, new_emails_name, new_emails = True)
					else:
						print('Invalid Input.')

				elif choice2 == 4:
					break

				else:
					print('Invalid choice.')

		elif choice == 4:
			# Exit
			exit(0)

		else:
			print('Invalid Choice.')