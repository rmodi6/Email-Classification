import os
import knn
import extract as ex
import matplotlib.pyplot as plt

def main(dataset_name, testset_name, new_emails = False):
	'''Runs the knn classifier for a training set dataset_name and test set testset_name'''
	current_path = os.path.dirname(os.path.abspath(__file__)) + "\\"
	trainingset_path = current_path + dataset_name + "\\"
	testset_path = current_path + testset_name + "\\"
	results_path = testset_path + "results\\"

	if not os.path.exists(results_path):
		os.mkdir(results_path)

	folder_names = next(os.walk(testset_path + "."))[1]
	if 'results' in folder_names:
		folder_names.remove('results')
	if new_emails:
		folder_names = [""]
	
	workfilename = 'mergedworkfile.csv'
	wordfilename = 'wordfile.csv'
	# klist = [1, 3, 7, 15, 24, 33, 42, 50]
	klist = [1, 3]
	acc = []
	ks = []
	trainingSet=[]

	print("Loading Training Set...")
	wordsd, subd, digramsd, trigramsd = ex.loadTrainingset(trainingset_path, workfilename, wordfilename, trainingSet)
	print("Training Set loaded.")

	print('Collecting ' + 'New'*new_emails + 'Test'*(not new_emails) + ' Emails...')
	testSet, all_files = ex.loadTestset(testset_path, folder_names, wordsd, subd, digramsd, trigramsd)
	print('New'*new_emails + 'Test'*(not new_emails) + ' Emails Collected.')

	assert(len(trainingSet[0]) == len(testSet[0]))

	list_of_predictions = knn.classify(klist, trainingSet, testSet, results_path)

	if not new_emails:
		#Finds the predictions and accuracy for new test mails given the predictions for these mails
		for i in range(len(klist)):
			predictions = []
			for x in range(len(testSet)):	
				predictions.append(list_of_predictions[x][i])
			accuracy = knn.getAccuracy(testSet, predictions)
			acc.append(accuracy)
			ks.append(klist[i])
			print('K: ' + repr(klist[i]))
			print('Accuracy: ' + repr(accuracy) + '%')
			
		print('Overall Accuracy: '+ str(sum(acc)/len(acc)) + "%")
		plt.plot(ks, acc)
		plt.xlabel('K')
		plt.ylabel('Accuracy')
		plt.show()
	
	print('Find the results at: ' + results_path)

if __name__ == '__main__':
	main("dataset", "testset")
