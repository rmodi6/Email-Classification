import extract as ex
import knn
import mnb
import knn_classify

if __name__ == '__main__':
	choice = 0
	while choice != 4:
		print('\nMenu:')
		print('1 -> Create Dataset.\n2 -> Classify using kNN.\n3 -> Classify using MNB.\n4 -> Exit.')
		choice = int(input('Enter your choice: '))
		
		if choice == 1:
			# Create Dataset
			dataset_name = input('Enter the name of dataset folder: ')
			ex.main(dataset_name)

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
					new_emails_name = input('Enter the name of new emails folder: ')
					knn_classify.main(dataset_name, new_emails_name, new_emails = True)

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
					new_emails_name = input('Enter the name of new emails folder: ')
					mnb_classify.main(dataset_name, new_emails_name, new_emails = True)

				elif choice2 == 4:
					break

				else:
					print('Invalid choice.')
		
		elif choice == 4:
			# Exit
			exit(0)
		else:
			print('Invalid Choice.')