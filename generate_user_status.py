import json
import collections
import sys

# Map from Business ID to list of Categories
categories = {}

# Map from User ID to []
status = collections.defaultdict(dict)

def add_business(obj):
  categories[obj['business_id']] = obj['categories']

def add_review(obj):
  user = obj['user_id']
  business = obj['business_id']
  votes = obj['votes']
  for category in categories[business]:
    if category not in status[user]:
      status[user][category] = [votes['cool'], votes['funny'], votes['useful'], 1]
    else:
      status[user][category][0] += votes['cool']
      status[user][category][1] += votes['funny']
      status[user][category][2] += votes['useful']
      status[user][category][3] += 1


def print_progress(l):
    sys.stdout.write('\r')
    sys.stdout.write('{0: .1f}%'.format(l/1855381.0 * 100))
    sys.stdout.flush()

def main():
  l = 0
  should_read = False
  with open('yelp', 'r') as dataset:
    for line in dataset:
      print_progress(l)
      # Load an entry
      start = line.find('{')
      if start == -1: continue
      if start > 0:
        try: obj = json.loads(line[start:])
        except: continue
        should_read = obj['type'] in ('business', 'review')  
      elif should_read:
        obj = json.loads(line)
   

      if should_read and obj['type'] == 'business':
        add_business(obj)
      elif should_read and obj['type'] == 'review':
        add_review(obj)
      
      l += 1

  with open('user_status.json', 'w') as out:
    json.dump(status, out)

  import pdb; pdb.set_trace()


if __name__ == '__main__':
  main()