import csv
import random
import math
import operator
import matplotlib.pyplot as plt

def loadDataset(current_path, filename, split, trainingSet=[] , testSet=[]):
	#labels = open('label.txt','r')
	#label = labels.readlines()
	#trainlabels = open('trainlabel','w')
	#testlabels = open('testlabel', 'w')
	with open(current_path + filename, 'r') as csvfile:
		lines = csv.reader(csvfile)
		dataset = list(lines)
		for x in range(len(dataset)):
			for y in range(len(dataset[x])):
				dataset[x][y] = float(dataset[x][y])
			if random.random() < split:
				trainingSet.append(dataset[x])
				#trainlabels.write(str(label[x]))
			else:
				testSet.append(dataset[x])
				#testlabels.write(str(label[x]))

def euclideanDistance(instance1, instance2, length):
	distance = 0
	for x in range(length):
		distance += pow((instance1[x] - instance2[x]), 2)
	return math.sqrt(distance)

def getNeighbors(trainingSet, testInstance, maxk):
	distances = []
	length = len(testInstance)-1
	for x in range(len(trainingSet)):
		dist = euclideanDistance(testInstance, trainingSet[x], length)
		distances.append((trainingSet[x][-1], dist))
	distances.sort(key=operator.itemgetter(1))
	neighbors = []
	for x in range(maxk):
		neighbors.append(distances[x][0])
	return neighbors

def getResponse(neighbors, k):
	classVotes = {}
	for x in range(k):
		response = neighbors[x]
		if response in classVotes:
			classVotes[response] += 1
		else:
			classVotes[response] = 1
	sortedVotes = sorted(classVotes.items(), key=operator.itemgetter(1), reverse=True)
	# print(sortedVotes)
	return sortedVotes[0][0]

def getAccuracy(testSet, predictions):
	correct = 0
	for x in range(len(testSet)):
		if testSet[x][-1] == predictions[x]:
			correct += 1
	return (correct/float(len(testSet))) * 100.0

def classify(klist, trainingSet, testSet, current_path):
	list_of_predictions = []
	# make output file for predicted state
	print('Completed 0.0%', end = '\r')
	for x in range(len(testSet)):
		predictions = []
		neighbors = getNeighbors(trainingSet, testSet[x], klist[-1])
		for k in klist:
			result = getResponse(neighbors, k)
			predictions.append(result)
		list_of_predictions.append(predictions)
		completed = (x+1)*100/len(testSet)
		print('Completed {0:.2f}%'.format(completed), end = '\r')
		#print('> predicted=' + repr(result) + ', actual=' + repr(testSet[x][-1]))
	print('Completed 100.0%')

	for i in range(len(klist)):
		outfile = open(current_path + "predicted_class_"+str(klist[i])+".csv",'w') # open file for appending
		for x in range(len(testSet)):	
			outfile.write(str(list_of_predictions[x][i])+"\n")

	return list_of_predictions
	
def main():
	# prepare data
	klist = [1, 3, 7, 15, 24, 33, 42, 50]
	acc = []
	ks = []
	trainingSet = []
	testSet=[]
	split = 0.67
	current_path = os.path.dirname(os.path.abspath(__file__)) + "\\"

	print("Loading DataSet...")
	loadDataset(current_path, 'mergedworkfile.csv', split, trainingSet, testSet)
	print ('Train set length: ' + repr(len(trainingSet)))
	print ('Test set length: ' + repr(len(testSet)))
	
	list_of_predictions = classify(klist, trainingSet, testSet, current_path)
		
	for i in range(len(klist)):
		predictions = []
		for x in range(len(testSet)):	
			predictions.append(list_of_predictions[x][i])
		accuracy = getAccuracy(testSet, predictions)
		acc.append(accuracy)
		ks.append(klist[i])
		print('K: ' + repr(klist[i]))
		print('Accuracy: ' + repr(accuracy) + '%')

	print('Overall Accuracy: '+str(sum(acc)/len(acc))+"%")
	plt.plot(ks, acc)
	plt.xlabel('K')
	plt.ylabel('Accuracy')
	plt.show()

if __name__ == '__main__':
	main()
