import json
import collections
import matplotlib.pyplot as plt

f1 = open("edges_trim_may.txt","w")
f2 = open("user_id_map.txt","r")
f3 = open("business_id_map.txt","r")

business_id = []
user_id = []

user = json.load(f2)
business = json.load(f3)

date = collections.Counter()
with open("yelp_academic_dataset_review.json") as file:
	for line in file:
		review = json.loads(line)
		if review['date'] < '2013-05-31' and int(review['stars'] >= 3):
			print >> f1, user[review["user_id"]], business[review["business_id"]], str(int(review["stars"])/5.0)

f1.close()
import pdb; pdb.set_trace()



