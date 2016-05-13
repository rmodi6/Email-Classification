import os
import mnb
import shutil
import extract as ex

def main(dataset_name, testset_name, new_emails = False):
	'''Runs the mnb classifier for a training set dataset_name and test set testset_name'''
	current_path = os.path.dirname(os.path.abspath(__file__)) + "\\"
	trainingset_path = current_path + dataset_name + "\\"
	testset_path = current_path + testset_name + "\\"
	results_path = testset_path + "results\\"

	if not os.path.exists(results_path):
		os.mkdir(results_path)

	folder_names = next(os.walk(testset_path + "."))[1]
	if 'results' in folder_names:
		folder_names.remove('results')
	# folder_names = ["calendar"]
	if new_emails:
		folder_names = [""]

	workfilename = 'mergedworkfile.csv'
	wordfilename = 'wordfile.csv'
	trainingSet = []
	predicted_folders = []
	
	print("Loading Training Set...")
	wordsd, subd, digramsd, trigramsd = ex.loadTrainingset(trainingset_path, workfilename, wordfilename, trainingSet)
	print("Training Set loaded.")

	print('Collecting ' + 'New'*new_emails + 'Test'*(not new_emails) + ' Emails...')
	testSet, all_files = ex.loadTestset(testset_path, folder_names, wordsd, subd, digramsd, trigramsd)
	print('New'*new_emails + 'Test'*(not new_emails) + ' Emails Collected.')

	assert(len(trainingSet[0]) == len(testSet[0]))

	# prepare model
	summaries, classpriorprobabilities = mnb.summarizeByClass(trainingSet)

	# test model
	predictions = mnb.getPredictions(summaries, classpriorprobabilities, testSet, results_path)
	
	folder_names = next(os.walk(trainingset_path + "."))[1]
	if 'results' in folder_names:
		folder_names.remove('results')
	for fname in folder_names:
		if not os.path.exists(results_path + fname):
			os.mkdir(results_path + fname)
	for i in range(len(predictions)):
		shutil.copy2(all_files[i], results_path + folder_names[predictions[i]])
		predicted_folders.append(folder_names[predictions[i]])
		
	if not new_emails:
				#Finds the accuracy for new test mails given the predictions for these mails
		accuracy = mnb.getAccuracy(testSet, predictions)
		print('Accuracy: {0}%'.format(accuracy))

	print('Find the results at: ' + results_path)
	return predicted_folders

if __name__ == '__main__':
	main("outlook mails", "outlook test", new_emails = False)
