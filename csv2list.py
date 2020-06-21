#!/usr/bin/env python
# python 3.8

# Create data structure of candidates, parties, constituencies

'''
    candidate_registry
    {
        'number' :
                'province' : 'A',
                'mandates' : '3',
                'candidates' : {
                    'idx' : {'name' : 'B', 'party': 'C', 'capital': 100},
                    'idx' : {'name' : 'B', 'party': 'C', 'capital': 100}
                }
        ...
                
    }
'''

'''
Add '#coding=utf-8' line if you encounter a similar error given below:

'SyntaxError: Non-ASCII character '\xd1' in file csv2json.py on line 53, but no encoding declared; see http://python.org/dev/peps/pep-0263/ for details
'''

import json, re

csv_file = 'list2.csv'
mn_candidate_registry_file = 'candidates_mn.json'
ub_candidate_registry_file = 'candidates_ub.json'
party_registry_file = 'parties.json'
ub_compact_registry_file = 'candidates_ub_compact.json'
mn_compact_registry_file = 'candidates_mn_compact.json'

mn_candidate_registry = {}
ub_candidate_registry = {}
party_registry = {}
max_capital = 0

# read a file with candidate list line by line
with open(csv_file, 'r') as f:
    lines = f.readlines()

    cand_idx = 0    # candidate index
    const_idx = ''  # constituency index
    province = ''   # province name
    mandates = ''   # number of mandates in a constituency

    # parse each line
    for line in lines[1:]:

        line_elements = line.split(',')

        cand_name = line_elements[-9]
        cand_party = line_elements[-8].strip(' ')


        cand_capital = line_elements[-1].rstrip('\n') # last element ends with 'new-line'
        if cand_capital == '':                        # empty capital
            cand_capital = '0'
        cand_capital = int(float(cand_capital))
        if max_capital < cand_capital: # get max capital
            max_capital = cand_capital

        # a line contains constituency, province, mandates and also candidate name and party
        if line_elements[0] != '':

            # 2 types of province name: simple and complex within double quotes
            elements = []
            if line_elements[0].startswith('"'):

                province = re.match("(\".+\")", line).group(1)
                elements = line[len(province):].split(',')
            else:
                province = line_elements[0].strip()
                elements = line_elements

            const_idx = elements[1].split('-')[0].strip() # 26-р тойрог
            mandates = elements[2].split(' ')[0].strip() # 3 мандат
            
            #print (const_idx, province, mandates)
            cand_idx += 1

            mn_candidate_registry[const_idx] = {}
            mn_candidate_registry[const_idx]['province'] = province
            mn_candidate_registry[const_idx]['mandates'] = mandates
            mn_candidate_registry[const_idx]['candidates'] = {}

        # a line contains only candidate name and party
        else:
            cand_idx += 1

        mn_candidate_registry[const_idx]['candidates'][str(cand_idx)] = {'name': cand_name, 'party': cand_party, 'capital': cand_capital}

    #print(mn_candidate_registry)

# get UB candidates, all parties
party_name_registry = {}
party_idx = 1
for c in mn_candidate_registry:
    if int(c) > 20:
        ub_candidate_registry[c] = mn_candidate_registry[c]

    for constit in mn_candidate_registry[c]['candidates']:
        cand_party = mn_candidate_registry[c]['candidates'][constit]['party']
        if cand_party not in party_name_registry:
            party_name_parts = cand_party.split(' ')
            short_name = ''
            for part in party_name_parts:
                if part != '':
                    short_name = short_name + part[0].upper()
            party_name_registry[cand_party] = {}
            party_name_registry[cand_party]['short'] = short_name
            party_name_registry[cand_party]['idx'] = str(party_idx) # insert str index
            party_idx += 1
            #print (party_name_registry)

party_index_registry = {}
for party in party_name_registry:
    print (party)
    party_idx = party_name_registry[party]['idx']
    party_short = party_name_registry[party]['short']
    party_index_registry[party_idx] = {}
    party_index_registry[party_idx]['name'] = party
    party_index_registry[party_idx]['short'] = party_short

party_registry['name'] = party_name_registry
party_registry['index'] = party_index_registry

# get total mandates, parties in all constituencies
mn_mandates = 0
mn_parties = {}
mn_persons = 0
mn_capital = 0
for c in mn_candidate_registry:
    mn_mandates = mn_mandates + int(mn_candidate_registry[c]['mandates'])

    # get total number of persons
    mn_persons += len(mn_candidate_registry[c]['candidates'])

    # get parties with its candidates
    for idx in mn_candidate_registry[c]['candidates']:
        # calculate capital
        mn_capital += mn_candidate_registry[c]['candidates'][idx]['capital']

        # count party
        party = mn_candidate_registry[c]['candidates'][idx]['party']
        capital = mn_candidate_registry[c]['candidates'][idx]['capital']
        if party not in mn_parties:
            mn_parties[party] = {}
            mn_parties[party]['person'] = 1
            mn_parties[party]['capital'] = capital
        else:
            mn_parties[party]['person'] += 1
            mn_parties[party]['capital'] += capital

# get total mandates, parties in UB constituencies
ub_mandates = 0
ub_parties = {}
ub_persons = 0
ub_capital = 0
for c in ub_candidate_registry:
    ub_mandates = ub_mandates + int(ub_candidate_registry[c]['mandates'])

    # get total number of persons
    ub_persons += len(ub_candidate_registry[c]['candidates'])

    # get parties with its candidates
    for idx in ub_candidate_registry[c]['candidates']:
        # calculate capital in UB
        ub_capital += ub_candidate_registry[c]['candidates'][idx]['capital']

        # count party in UB
        party = ub_candidate_registry[c]['candidates'][idx]['party']
        capital = ub_candidate_registry[c]['candidates'][idx]['capital']
        if party not in ub_parties:
            ub_parties[party] = {}
            ub_parties[party]['person'] = 1
            ub_parties[party]['capital'] = capital
        else:
            ub_parties[party]['person'] += 1
            ub_parties[party]['capital'] += capital

# make compact registries
mn_compact_registry = {'mandates': mn_mandates, 'parties': mn_parties}
ub_compact_registry = {'mandates': ub_mandates, 'parties': ub_parties}

print ('MN: mandates = %s, parties = %s, persons = %s, capital = %s (max %s)' % (mn_mandates, len(mn_compact_registry['parties']), mn_persons, mn_capital, max_capital))
print (mn_compact_registry)
print ('UB: mandates = %s, parties = %s, persons = %s, capital = %s' % (ub_mandates, len(ub_compact_registry['parties']), ub_persons, ub_capital))
print (ub_compact_registry)
print ('UB/MN: mandates = %.5s, parties = %.5s, persons = %.5s, capital = %.5s' % (ub_mandates/mn_mandates, len(ub_compact_registry['parties'])/len(mn_compact_registry['parties']), ub_persons/mn_persons, ub_capital/mn_capital))

with open(mn_candidate_registry_file,'w') as f:
    f.write(json.dumps(mn_candidate_registry, sort_keys=True, indent=4))

with open(ub_candidate_registry_file,'w') as f:
    f.write(json.dumps(ub_candidate_registry, sort_keys=True, indent=4))

with open(party_registry_file,'w') as f:
    f.write(json.dumps(party_registry, sort_keys=True, indent=4))

with open(mn_compact_registry_file,'w') as f:
    f.write(json.dumps(mn_compact_registry, sort_keys=True, indent=4))

with open(ub_compact_registry_file,'w') as f:
    f.write(json.dumps(ub_compact_registry, sort_keys=True, indent=4))

