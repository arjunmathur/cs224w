import json

business_id = []
user_id = []

count = 0
f1 = open("business_id.txt","w")
with open("yelp_academic_dataset_business.json") as file:
	for line in file:
		count += 1
		business = json.loads(line)
		print >> f1, business["business_id"]
		#business_id.append(business["business_id"])	
f1.close()

count = 0
f1 = open("user_id.txt","w")
with open("yelp_academic_dataset_user.json") as file:
	for line in file:
		count += 1
		user = json.loads(line)
		print >> f1, user["user_id"]
		#user_id.append(user["user_id"])

f1.close()
