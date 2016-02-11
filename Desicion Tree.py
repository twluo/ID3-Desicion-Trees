import math
import operator

class Tree(object):
	def __init__(self):
		self.attribute = None
		self.left = None
		self.right = None
		self.data = None
		self.threshold = None
		self.label = None
		self.count = None
		self.level = None

	def printRule(self):
		if (self.attribute == 0):
			print("Petal width(" + str(self.attribute) + ") with threshold of " + str(self.threshold)  + " and count of " + str(self.count))
		elif (self.attribute == 1):
			print("Petal length(" + str(self.attribute) + ") with threshold of " + str(self.threshold)  + " and count of " + str(self.count))
		elif (self.attribute == 2):
			print("Sepal width(" + str(self.attribute) + ") with threshold of " + str(self.threshold)  + " and count of " + str(self.count))
		elif (self.attribute == 3):
			print("Sepal length(" + str(self.attribute) + ") with threshold of " + str(self.threshold)  + " and count of " + str(self.count))
	def printLabel(self):
		print("Label #" + str(self.label) + " with count of " + str(self.count))

	def printNode(self):
		for x in range(self.level):
			print(" ", end = '')
		if (self.left is None and self.right is None):
			print("I'm a leaf", end = ' ')
			self.printLabel()
		else:
			print("My rule is", end = ' ')
			self.printRule()
			self.left.printNode()
			self.right.printNode()


def getCount(dataSet):
	count = [0,0,0]
	for x in range(len(dataSet)):
		count[int(dataSet[x][-1]) -1 ] += 1
	return count

def isPure(dataSet):
	count = getCount(dataSet)
	flag = 0
	label = -1
	total = 0
	for x in range(len(count)):
		if (count[x] > 0):
			flag += 1
			label = x + 1
		total += count[x]
	if (flag == 1):
		return (label, total)
	else:
		return (-1, total)

def splitData(dataSet, attribute, threshold):
	leftSet = []
	rightSet = []
	for x in range(len(dataSet)):
		if (dataSet[x][attribute] <= threshold):
			leftSet.append(dataSet[x])
		else:
			rightSet.append(dataSet[x])
	return (leftSet, rightSet)

def entropy(dataSet):
	entropy = 0.0
	count = getCount(dataSet)
	for x in range(len(count)):
		pi = count[x]/len(dataSet)
		if (pi != 0):
			entropy += -(pi * math.log10(pi))
	return entropy

def condEntropy(dataSet, attribute, threshold):
	(leftSet, rightSet) = splitData(dataSet, attribute, threshold)
	totalEntropy = len(leftSet)/len(dataSet)*entropy(leftSet)
	totalEntropy += len(rightSet)/len(dataSet)*entropy(rightSet)
	return totalEntropy

def gain(dataSet, attribute, threshold):
	gain = entropy(dataSet) - condEntropy(dataSet, attribute, threshold)
	return gain

def maxGain(dataSet):
	maxGain = float('-inf')
	attribute = 0
	threshold = 0
	Set0 = sorted(dataSet, key = lambda attribute:attribute[0])
	Set1 = sorted(dataSet, key = lambda attribute:attribute[1])
	Set2 = sorted(dataSet, key = lambda attribute:attribute[2])
	Set3 = sorted(dataSet, key = lambda attribute:attribute[3])
	for x in range(len(dataSet) - 1):
		if (Set0[x][0] != Set0[x+1][0]):
			tempThreshold = (Set0[x][0] + Set0[x+1][0])/2
			tempGain = gain(Set0, 0, tempThreshold)
			if (tempGain > maxGain):
				maxGain = tempGain
				attribute = 0
				threshold = tempThreshold
	for x in range(len(dataSet) - 1):
		if (Set1[x][1] != Set1[x+1][1]):
			tempThreshold = (Set1[x][1] + Set1[x+1][1])/2
			tempGain = gain(Set1, 1, tempThreshold)
			if (tempGain > maxGain):
				maxGain = tempGain
				attribute = 1
				threshold = tempThreshold
	for x in range(len(dataSet) - 1):
		if (Set2[x][2] != Set2[x+1][2]):
			tempThreshold = (Set2[x][2] + Set2[x+1][2])/2
			tempGain = gain(Set2, 2, tempThreshold)
			if (tempGain > maxGain):
				maxGain = tempGain
				attribute = 2
				threshold = tempThreshold
	for x in range(len(dataSet) - 1):
		if (Set3[x][3] != Set3[x+1][3]):
			tempThreshold = (Set3[x][3] + Set3[x+1][3])/2
			tempGain = gain(Set3, 3, tempThreshold)
			if (tempGain > maxGain):
				maxGain = tempGain
				attribute = 3
				threshold = tempThreshold
	return (attribute, threshold)

def buildTree(dataSet, level):
	if (dataSet == []):
		return
	(label, count) = isPure(dataSet)
	if (label != -1):
		node = Tree()
		node.label = label
		node.count = count
		node.level = level
		return node
	else:
		(attribute, threshold) = maxGain(dataSet)
		node = Tree()
		node.attribute = attribute
		node.threshold = threshold
		node.count = count
		node.level = level
		(leftSet, rightSet) = splitData(dataSet, attribute, threshold)
		node.left = buildTree(leftSet, level + 1)
		node.right = buildTree(rightSet, level + 1)
		return node

def getLabel(root, test):
	if (root.left is None and root.right is None):
		return root.label
	else:
		if (test[root.attribute] < root.threshold):
			return getLabel(root.left, test)
		else:
			return getLabel(root.right, test)

# Setting up the dataset
def setUpDataSet(filename, dataSet):
	with open(filename,'r') as f:
		numLine = 0
		for line in f:
			lineList = line.split(" ")
			dataSet.append(lineList)
			del dataSet[numLine][-1]
			for y in range(len(dataSet[numLine])):
				dataSet[numLine][y] = float(dataSet[numLine][y])
			numLine += 1

dataSet = []
testSet = []
setUpDataSet('Training Data.txt', dataSet)
setUpDataSet('Test Data.txt', testSet)
root = buildTree(dataSet, 0)
root.printNode()
correct = 0
for x in range (len(dataSet)):
	label = getLabel(root, dataSet[x])
	if (label == dataSet[x][-1]):
		correct += 1
print ('Training data Acc = ' + str((correct/float(len(dataSet))) * 100.0) + '%')
correct = 0
for x in range (len(testSet)):
	label = getLabel(root, testSet[x])
	if (label == testSet[x][-1]):
		correct += 1
print ('Test data Acc = ' + str((correct/float(len(testSet))) * 100.0) + '%')