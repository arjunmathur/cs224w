import json
import collections

business_id = []
user_id = []

f1 = open("edges_high.txt","w")
f2 = open("user_id_map.txt","r")
f3 = open("business_id_map.txt","r")

user = json.load(f2)
business = json.load(f3)

with open("yelp_academic_dataset_review.json") as file:
	for line in file:
		review = json.loads(line)
		if int(review["stars"])/5.0 >= 0.6:
			print >> f1, user[review["user_id"]], business[review["business_id"]], str(int(review["stars"])/5.0)

f1.close()

