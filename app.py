# app.py
# python 3.8

# http://kaffeine.herokuapp.com/ - gives my app a caffeine shot every 30 minutes
# https://medium.com/@morgannewman/how-to-keep-your-free-heroku-app-online-forever-4093ef69d7f5

from flask import Flask, render_template, request
import os, json
app = Flask(__name__)
 
poll_data = {
   'title' : '"Сонгууль 2020" таавар',
   'question' : 'Та сонголтоо хийнэ үү?'
}

results_filenames = {'mn':'results_mn.json', 'ub':'results_ub.json'}
candidate_compact_filenames = {'mn':'candidates_mn_compact.json', 'ub':'candidates_ub_compact.json'}

party_filename = 'parties.json'

candidate_registry = {'mn': None, 'ub': None}

party_registry = {}

'''
    list.json
    {
        'mandates' : 'N',
        'parties' :
                'A' : {
                    'capital': capital, 'person': persons}
                },
                'B' : {
                    'capital': capital, 'person': persons}
                }
        }
        ...
                
    }
'''

'''
    result.json
    {
        'name' : {
                'A' : votes,
                'B' : votes
        }
        ...
                
    }
'''

# get party registry
with open(party_filename, 'r') as f:
    party_registry = json.load(f)

# get candidate registry
for region in candidate_registry:
    with open(candidate_compact_filenames[region], 'r') as f:
        candidate_registry[region] = json.load(f)

    # set maximum vote limit of each party (min of party persons and mandates)
    for party in candidate_registry[region]['parties']:
        candidate_registry[region]['parties'][party]['limit'] = min(candidate_registry[region]['parties'][party]['person'], candidate_registry[region]['mandates'])

# init results files
for region in candidate_registry:
    if not os.path.exists(results_filenames[region]):
        with open(results_filenames[region], 'w') as f:
            pass

@app.route('/')
def root():

    return render_template('hello.html', data=poll_data)

@app.route('/hello')
def hello():

    if request.args['username'] == '':
        return render_template('error_username.html', data=poll_data)

    poll_data['username'] = request.args.get('username')[:20]
    poll_data['region'] = request.args.get('region')

    region = request.args['region']
    poll_data['mandates'] = candidate_registry[region]['mandates']
    poll_data['parties'] = candidate_registry[region]['parties']

    return render_template('poll.html', data=poll_data, party=party_registry['name'])

@app.route('/poll')
def poll():

    # evaluate request
    your_votes = {}
    sum_votes = 0
    for k in request.args.keys():
        if 'prty' in k:
            value = request.args[k] # get votes
            if value == '':         # empty vote -> 0
                value = 0
            else:
                value = int(value)  # convert to number
            idx = k.replace('prty', '')
            your_votes[idx] = value
            sum_votes += value

    region = request.args['region']
    if sum_votes > candidate_registry[region]['mandates']:
        error_data = {}
        error_data['title'] = poll_data['title']
        error_data['mandates'] = candidate_registry[region]['mandates']
        error_data['sum_votes'] = sum_votes
        return render_template('error.html', data=error_data)

    # get previous results
    results = {}
    with open(results_filenames[region], 'r') as f:
        context = f.read()
        if context != '':
            results = json.loads(context)

    username = request.args['username']
    results[username] = your_votes

    # update results
    with open(results_filenames[region], 'w') as f:
        f.write(json.dumps(results))

    # show result
    results_data = {}
    results_data['title'] = poll_data['title']
    results_data['region'] = region
    results_data['results'] = results

    # get parties in this poll (used to print party header)
    values = results.values() # get values view
    iter_value = iter(values) # get iterator of values view
    first_value = next(iter_value) # get the first value

    # data: contains results
    # parties: dict obj with party indices
    # party_idx: dict obj with party full and short names
    return render_template('results.html', data=results_data, parties = first_value, party_idx=party_registry['index'])

@app.route('/results')
def show_results():

    region = request.args['region']

    # get results
    results = {}    
    with open(results_filenames[region], 'r') as f:
        results = json.load(f)

    # show results
    results_data = {}
    results_data['title'] = poll_data['title']
    results_data['region'] = region
    results_data['results'] = results

    # get parties in this poll (used to print party header)
    values = results.values() # get values view
    iter_value = iter(values) # get iterator of values view
    first_value = next(iter_value) # get the first value

    # data: contains results
    # parties: dict obj with party indices
    # party_idx: dict obj with party full and short names
    return render_template('results.html', data=results_data, parties = first_value, party_idx=party_registry['index'])

if __name__ == "__main__":
    app.run(debug=True)
