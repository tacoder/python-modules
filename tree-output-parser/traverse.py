import json
from pprint import pprint

with open('HDDJsonTreeWithAggregationSize.json') as f:
    data = json.load(f)

pprint(data)
