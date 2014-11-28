import json

user_id = []

count = 0
f1 = open("user_review_rating.txt","w")
with open("yelp_academic_dataset_user.json") as file:
	for line in file:
		count += 1
		user = json.loads(line)
		print >> f1, user["review_count"], user["average_stars"]
		#user_id.append(user["user_id"])

f1.close()
