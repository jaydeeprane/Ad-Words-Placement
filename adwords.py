
import numpy as np
import pandas as pd 
import random
import sys
import math
random.seed(0)

if len(sys.argv)==1:
	print "Enter the name of the algorithm: (greedy/msvv/balance)"
	exit(1)

algorithm = sys.argv[1]

# Reading the Query File
queries = []
queries = [line.rstrip('\n') for line in open('queries.txt')]

# Dropping the NaN rows from the table to get budget for each Advertiser
bidder_dataset = pd.read_csv('bidder_dataset.csv')
bud = bidder_dataset[np.isfinite(bidder_dataset['Budget'])]

# Creating Dictionary (orignial and copy of original) mapping each advertiser to his/her budget
bud_dict = dict(zip(bud.Advertiser,bud.Budget))
bud_dict = {str(k):v for k,v in bud_dict.items()}
bud_dict_copy = bud_dict.copy()
bud_dict_copy = {str(k):v for k,v in bud_dict_copy.items()}

# Reading in data to create list of lists representation of the dataset, by omitting the header
bidder_dataset_wh = pd.read_csv('bidder_dataset.csv',header = None)
bidder_dataset_wh = pd.DataFrame(bidder_dataset_wh)
bidder_dataset_wh = bidder_dataset_wh.values.tolist()

def greedy(bud_dict,bidder_dataset_wh):
	revenue = 0.00

	for query in queries:
		bidders = []
		for bidder in bidder_dataset_wh[1:]:
			if bidder[1]==query:
				if ((bud_dict[(bidder[0])]))>=float(bidder[2]):
					bidders.append(bidder)
		max_bid = 0.00
		b = []
		for f in bidders:
			if float(f[2]) > max_bid:
				max_bid = float(f[2])
				b = f
		if len(b):
			t = float(b[2])
			bud_dict[(b[0])]-=t
			revenue+=t

	return revenue

def msvv(bud_dict,bidder_dataset_wh):
	revenue = 0.00

	for query in queries:
		bidders = []
		for bidder in bidder_dataset_wh[1:]:
			if bidder[1]==query:
				if bud_dict[(bidder[0])]>=float(bidder[2]) :
					bidders.append(bidder)
		max_bid = 0.00
		b = []
		for f in bidders:
			bi = 1 - math.exp((bud_dict_copy[(f[0])]-bud_dict[(f[0])])/bud_dict_copy[(f[0])]-1)
			if max_bid < (float(f[2]) * bi):
				b = f
				max_bid = float(f[2]) * bi
		if len(b):
			t = float(b[2])
			bud_dict[(b[0])]-=t
			revenue+=t

	return revenue

def balance(bud_dict,bidder_dataset_wh):
	revenue = 0.00

	for query in queries:
		bidders = []
		for bidder in bidder_dataset_wh[1:]:
			if bidder[1]==query:
				if bud_dict[(bidder[0])]>=float(bidder[2]):
					bidders.append(bidder)
		max_bud = 0.00
		b = []
		for f in bidders:
			if bud_dict[(f[0])] > max_bud:
				b = f
				max_bud = bud_dict[(f[0])]
		if len(b):
			t = float(b[2])
			bud_dict[(b[0])]-=t
			revenue+=t

	return revenue

sum_total = sum(bud_dict_copy.values())
average_revenue = 0.00

# Calculating the competitive ratio and revenue for each algorithm
if algorithm =='greedy':
	print 'Greedy Revenue'
	print 'Revenues = ',greedy(bud_dict,bidder_dataset_wh)
	for i in range(100):
		bud_dict = bud_dict_copy.copy()
		random.shuffle(queries)
		average_revenue+=greedy(bud_dict,bidder_dataset_wh)
		
	print "Competitive ratio = ",(average_revenue/100)/sum_total

if algorithm =='msvv':
	print 'MSVV Revenue'
	print 'Revenues = ',msvv(bud_dict,bidder_dataset_wh)
	for i in range(100):
		bud_dict = bud_dict_copy.copy()
		random.shuffle(queries)
		average_revenue+=msvv(bud_dict,bidder_dataset_wh)

	print "Competitive ratio = ",(average_revenue/100)/sum_total

if algorithm =='balance':
	print 'Balance Revenue'
	print 'Revenues = ',balance(bud_dict,bidder_dataset_wh)
	for i in range(100):
		bud_dict = bud_dict_copy.copy()
		random.shuffle(queries)
		average_revenue+=balance(bud_dict,bidder_dataset_wh)
	print "Competitive ratio = ",(average_revenue/100)/sum_total




# def main():

# if __name__ == "__main__":
# 	main()