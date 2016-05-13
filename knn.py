import os
import csv
import random
import math
import operator
import matplotlib.pyplot as plt

def loadDataset(current_path, filename, split, trainingSet=[] , testSet=[]):
	'''Loads the dataset from the current_path and filename and splits it according to the split ratio into trainingSet and testSet'''
	with open(current_path + filename, 'r') as csvfile:
		lines = csv.reader(csvfile)
		dataset = list(lines)
		#Splits the dataset into training set and test set
		for x in range(len(dataset)):
			for y in range(len(dataset[x])):
				dataset[x][y] = float(dataset[x][y])	
			if random.random() < split:
				trainingSet.append(dataset[x])
			else:
				testSet.append(dataset[x])

def hammingDistance(instance1, instance2, length):
	'''Calculates the distance using Hamming Distance metric between instance1 email and instance2 email for a total of length features'''
	distance = 0
	for x in range(length):
		val=int(pow(instance1[x],instance2[x]))
		dist=0
		while(val!=0):
			dist+=1
			val&=val-1
		distance += dist
	return distance

def manhattanDistance(instance1, instance2, length):
	'''Calculates the distance using Manhattan Distance metric between instance1 email and instance2 email for a total of length features'''
	distance = 0
	for x in range(length):
		distance += abs(instance1[x] - instance2[x])
	return distance

def euclideanDistance(instance1, instance2, length):
	'''Calculates the distance using Euclidean Distance metric between instance1 email and instance2 email for a total of length features'''
	distance = 0
	for x in range(length):
		distance += pow((instance1[x] - instance2[x]), 2)
	return math.sqrt(distance)

def getNeighbors(trainingSet, testInstance, maxk):
	'''Finds the list of maxk nearest neighbors for the testInstance email in the trainingSet of all emails'''
	distances = []
	length = len(testInstance)-1
	for x in range(len(trainingSet)):
				#Distance can be calculated using euclideanDistance(), manhattanDistance() and hammingDistance() metrics
		dist = euclideanDistance(testInstance, trainingSet[x], length)
		distances.append((trainingSet[x][-1], dist))
	#Sorts the distances and appends the k neighbors having least distances to the neighbors list	
	distances.sort(key=operator.itemgetter(1))
	neighbors = []
	for x in range(maxk):
		neighbors.append(distances[x][0])
	return neighbors

def getResponse(neighbors, k):
	'''Gives the class vote for a set of neighbors for a given value of k'''
	classVotes = {}
	for x in range(k):
		response = neighbors[x]
		if response in classVotes:
			classVotes[response] += 1
		else:
			classVotes[response] = 1
	sortedVotes = sorted(classVotes.items(), key=operator.itemgetter(1), reverse=True)
	return sortedVotes[0][0]

def getAccuracy(testSet, predictions):
	'''Calculates the accuracy of classifying emails in testSet given the predictions of these emails'''
	correct = 0
	for x in range(len(testSet)):
		if testSet[x][-1] == predictions[x]:
			correct += 1
	return (correct/float(len(testSet))) * 100.0

def classify(klist, trainingSet, testSet, path):
	'''Classifies the testSet using the trainingSet for klist and stores the predicted results at path'''
	list_of_predictions = []
	print('Completed 0.00%', end = '\r')
	#Find the k nearest neighbors for each test mail and predict the class of each test mail using these neighbors
	for x in range(len(testSet)):
		predictions = []
		neighbors = getNeighbors(trainingSet, testSet[x], klist[-1])
		for k in klist:
			result = getResponse(neighbors, k)
			predictions.append(result)
		list_of_predictions.append(predictions)
		completed = (x+1)*100/len(testSet)
		print('Completed {0:.2f}%'.format(completed), end = '\r')
	print('Completed 100.00%')
	for i in range(len(klist)):
				# Opens file for appending
		outfile = open(path + "predicted_class_"+str(klist[i])+".csv",'w') 
		for x in range(len(testSet)):	
			outfile.write(str(list_of_predictions[x][i])+"\n")
	return list_of_predictions
	
def main(dataset_name):
	klist = [1, 3, 7, 15, 24, 33, 42, 50]
	acc = []
	ks = []
	trainingSet = []
	testSet=[]
	split = 0.67
	current_path = os.path.dirname(os.path.abspath(__file__)) + "\\"
	dataset_path = current_path + dataset_name + "\\"
	results_path = dataset_path + "results\\"

	if not os.path.exists(results_path):
		os.mkdir(results_path)

	print("Loading Dataset...")
	loadDataset(dataset_path, 'mergedworkfile.csv', split, trainingSet, testSet)
	print ('Train set length: ' + repr(len(trainingSet)))
	print ('Test set length: ' + repr(len(testSet)))
	
	list_of_predictions = classify(klist, trainingSet, testSet, results_path)
		
	for i in range(len(klist)):
		predictions = []
		for x in range(len(testSet)):	
			predictions.append(list_of_predictions[x][i])
		accuracy = getAccuracy(testSet, predictions)
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
	main("dataset")
