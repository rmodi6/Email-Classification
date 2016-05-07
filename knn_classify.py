import knn
import extract as ex
import matplotlib.pyplot as plt

if __name__ == '__main__':
	folder_names = ["calendar", "meetings", "personal"]
	folder_path = "C:/Users/Ruchit/Desktop/FYP/Enron Dataset/test small/"
	current_path = "C:/Users/Ruchit/Desktop/FYP/Implementation/knn/"
	workfilename = 'mergedworkfile.csv'
	wordfilename = 'wordfile.csv'
	klist = [1, 3, 7, 15, 24, 33, 42, 50]
	acc = []
	ks = []
	trainingSet=[]

	print("Loading Training Set...")
	wordsd, subd, digramsd, trigramsd = ex.loadTrainingset(current_path, workfilename, wordfilename, trainingSet)
	print("Training Set loaded.")

	print('Collecting New Emails...')
	testSet = ex.loadTestset(folder_path, folder_names, wordsd, subd, digramsd, trigramsd)
	print('New Emails Collected.')

	assert(len(trainingSet[0]) == len(testSet[0]))

	list_of_predictions = knn.classify(klist, trainingSet, testSet, current_path)
		
	for i in range(len(klist)):
		predictions = []
		for x in range(len(testSet)):	
			predictions.append(list_of_predictions[x][i])
		accuracy = knn.getAccuracy(testSet, predictions)
		acc.append(accuracy)
		ks.append(klist[i])
		print('K: ' + repr(klist[i]))
		print('Accuracy: ' + repr(accuracy) + '%')
		
	print('Overall Accuracy: '+str(sum(acc)/len(acc))+"%")
	plt.plot(ks, acc)
	plt.xlabel('K')
	plt.ylabel('Accuracy')
	plt.show()