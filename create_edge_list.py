import json

business_id = []
user_id = []

f1 = open("edges.txt","w")
with open("yelp_academic_dataset_review.json") as file:
	for line in file:
		review = json.loads(line)
		print >> f1, review["user_id"], review["business_id"], review["stars"]
f1.close()

