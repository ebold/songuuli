#!/usr/bin/env python

import json

ub_data_file = 'candidates_ub_compact.json'
all_data_file = 'candidates_all_compact.json'

ub_data_obj = {}
all_data_obj = {}

with open(ub_data_file, 'r') as f:
    ub_data_obj = json.load(f)


party_resource = []

for party in ub_data_obj['parties']:
    resource_obj = ub_data_obj['parties'][party] # get party resource
    resource_obj['name'] = party                 # extend party resource with its name
    resource_obj['cpp'] = int(resource_obj['capital']/resource_obj['person'])
    party_resource.append(resource_obj)

sorted_capital = sorted(party_resource, key=lambda x : x['capital'], reverse=True)

print ('Sorted by capital')
i = 1
for e in sorted_capital:
    print (i, e)
    i += 1


sorted_cpp = sorted(party_resource, key=lambda x : x['cpp'], reverse=True)

print ('Sorted by capital/person')
i = 1
for e in sorted_cpp:
    print (i, e)
    i += 1


