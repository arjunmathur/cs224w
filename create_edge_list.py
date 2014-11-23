import json
import collections

business_id = []
user_id = []

def create_edges():
  f1 = open("edges.txt","w")
  with open("yelp_academic_dataset_review.json") as file:
  	for line in file:
  		review = json.loads(line)
  		print >> f1, review["user_id"], review["business_id"], review["stars"]
  f1.close()


def create_mean_edges():
  ''' Createe edges with weights that model deviation
      from a users average ratings.'''

  mean_rating = collections.defaultdict(int)
  counts = collections.defaultdict(int)
  with open("edges.txt") as f:
    for line in f:
      (user, business, rating) = line.split()
      mean_rating[user] += int(rating)
      counts[user] += 1

  # Calculate averages
  for user in mean_rating:
    mean_rating[user] /= float(counts[user])

  with open('mean_ratings.json', 'w') as mean_out:
    json.dump(dict(mean_rating), mean_out)

  with open('edges_mean.json', 'w') as edges_out:
    with open('edges.txt') as f:
      for line in f:
        (user, business, rating) = line.split()
        print >> edges_out, user, business, int(rating) - mean_rating[user]

create_mean_edges()