import math
import operator
import numpy as np
import scipy.stats as st

class Tree(object):
	def __init__(self):
		self.attribute = None
		self.true = None
		self.false = None
		self.data = None

	def add_child(self, node, true_or_false):
		if (true_or_false):
			self.true = node
		else:
			self.false = node

def entropy(dataSet):
	count = [0,0,0]
	entropy = 0
	for x in range(len(dataSet)):
		count[int(dataSet[x][-1]) -1 ] += 1
	for x in range(len(count)):
		print(count[x])
		pi = count[x]/len(dataSet)
		entropy += -(pi * math.log10(pi))
	return entropy

def condEntropy(dataSet, splitSet):
	return 1

def gain(dataSet, splitSet):
	gain = 0
	return gain



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
entropy(dataSet);
print(dataSet[0])