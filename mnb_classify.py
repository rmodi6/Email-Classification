import mnb
import extract as ex

if __name__ == '__main__':
	subject_weight = 4
	folder_names = ["calendar", "meetings", "personal"]
	folder_path = "C:/Users/Ruchit/Desktop/FYP/Enron Dataset/test small/"
	current_path = "C:/Users/Ruchit/Desktop/FYP/Implementation/naive bayes/"
	workfilename = 'mergedworkfile.csv'
	wordfilename = 'wordfile.csv'
	trainingSet = []
	
	print("Loading Training Set...")
	wordsd, subd, digramsd, trigramsd = ex.loadTrainingset(current_path, workfilename, wordfilename, trainingSet)
	print("Training Set loaded.")

	print('Collecting New Emails...')
	testSet = ex.loadTestset(folder_path, folder_names, wordsd, subd, digramsd, trigramsd)
	print('New Emails Collected.')

	assert(len(trainingSet[0]) == len(testSet[0]))

	# prepare model
	summaries, classproirprobabilities = mnb.summarizeByClass(trainingSet)

	# test model
	predictions = mnb.getPredictions(summaries, classproirprobabilities, testSet, current_path)
	accuracy = mnb.getAccuracy(testSet, predictions)
	print('Accuracy: {0}%'.format(accuracy))