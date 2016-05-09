# Example of Naive Bayes implemented from Scratch in Python
import os
import csv
import random
import math
import matplotlib.pyplot as plt

def loadCsv(filename):
	lines = csv.reader(open(filename, "r"))
	dataset = list(lines)
	for i in range(len(dataset)):
		dataset[i] = [float(x) for x in dataset[i]]
	return dataset

def splitDataset(dataset, splitRatio):
	trainSize = int(len(dataset) * splitRatio)
	trainSet = []
	copy = list(dataset)
	while len(trainSet) < trainSize:
		index = random.randrange(len(copy))
		trainSet.append(copy.pop(index))
	return [trainSet, copy]

def separateByClass(dataset):
	separated = {}
	for i in range(len(dataset)):
		vector = dataset[i]
		if (vector[-1] not in separated):
			separated[vector[-1]] = []
		separated[vector[-1]].append(vector)
	return separated

def summarize(dataset,noofClasses):
	summaries = {}
	
	for k in range(noofClasses):
		wordnumerators=[]
		total=0
		for i in range(len(dataset)):
			dataset[i] = [float(x) for x in dataset[i]]
			for j in range(len(dataset[i])-1):
				if dataset[i][-1]==k:
					if len(wordnumerators)==j:
						wordnumerators.append(dataset[i][j])
					else:
						wordnumerators[j]=wordnumerators[j]+dataset[i][j]
					total+=dataset[i][j]
		
		if (k not in summaries):
			summaries[k] = []
		for i in range(len(wordnumerators)):
			summaries[k].append((wordnumerators[i]+1)/(total+len(wordnumerators)))
	
	return summaries

def summarizeByClass(dataset):
	separated = separateByClass(dataset)
	classproirprobabilities=[]
	summaries = {}
	total=len(separated)
	for classValue, instances in separated.items():
		classproirprobabilities.append(len(instances)/total)
		
	summaries = summarize(dataset,len(classproirprobabilities))
	return [summaries,classproirprobabilities]

def calculateClassProbabilities(summaries,classproirprobabilities, inputVector):
	probabilities = {}
	for classValue, classSummaries in summaries.items():
		probabilities[classValue] = 1*classproirprobabilities[classValue]
		#print(len(classSummaries))
		for i in range(len(classSummaries)):
			likelihood = classSummaries[i]
			x = inputVector[i]
			probabilities[classValue] *= math.pow(likelihood,x)
			
	return probabilities
			
def predict(summaries, classproirprobabilities,inputVector):
	probabilities = calculateClassProbabilities(summaries,classproirprobabilities, inputVector)
	bestLabel, bestProb = None, -1
	for classValue, probability in probabilities.items():
		if bestLabel is None or probability > bestProb:
			bestProb = probability
			bestLabel = classValue
	return bestLabel

def getPredictions(summaries, classproirprobabilities, testSet, path):
	predictions = []
	outfile = open(path + "predicted_class.csv",'w') # open file for appending

	print('Completed 0.00%', end = '\r')
	for i in range(len(testSet)):
		result = predict(summaries, classproirprobabilities,testSet[i])
		outfile.write(str(result)+"\n")
		predictions.append(result)
		completed = (i+1)*100/len(testSet)
		print('Completed {0:.2f}%'.format(completed), end = '\r')	
	print('Completed 100.00%')

	return predictions

def getAccuracy(testSet, predictions):
	correct = 0
	for i in range(len(testSet)):
		if testSet[i][-1] == predictions[i]:
			correct += 1
	return (correct/float(len(testSet))) * 100.0

def main(dataset_name):
	current_path = os.path.dirname(os.path.abspath(__file__)) + "\\"
	dataset_path = current_path + dataset_name + "\\"
	results_path = dataset_path + "results\\"

	if not os.path.exists(results_path):
		os.mkdir(results_path)

	splitRatio = [0.5, 0.6, 0.7, 0.8]
	accuracylist=[]
	dataset = loadCsv(dataset_path + "mergedworkfile.csv")
	for i in range(len(splitRatio)):
		trainingSet, testSet = splitDataset(dataset, splitRatio[i])
		print('Split ratio: {0}% \nSplit {1} rows into train={2} and test={3} rows'.format(splitRatio[i]*100, len(dataset), len(trainingSet), len(testSet)))
		# prepare model
		summaries,classproirprobabilities = summarizeByClass(trainingSet)
		# test model
		predictions = getPredictions(summaries, classproirprobabilities, testSet, results_path)
		accuracy = getAccuracy(testSet, predictions)
		accuracylist.append(accuracy)
		print('Accuracy: {0}%'.format(accuracy))

	plt.plot(splitRatio, accuracylist)
	plt.xlabel('Split Ratio %')
	plt.ylabel('Accuracy %')
	plt.show()

	print('Find the results at: ' + results_path)

if __name__ == '__main__':
	main("dataset")