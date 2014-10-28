import requests
import json
import re



## get a list of all trees in synthesis
url = 'http://api.opentreeoflife.org/v2/tree_of_life/about'
payload = {'content-type': 'application/json', 'study_list': 'true'}
response = requests.post(url, params=payload)
json_data = json.loads(response.text)

study_tree = {}
for x in json_data['study_list'] :
	study_tree[x['study_id']] = x['tree_id']


## get newick strings for all trees in synthesis
newicks = {}
for key, val in study_tree.items() :

	url = "".join(['http://api.opentreeoflife.org/phylesystem/v1/study/',key,'/tree/tree',val,'.tre'])
	response = requests.get(url)
	clean_newick = re.sub(r'\[.*?\]', '', response.text) # removes ingroup labels
	newicks[key+":"+val] = clean_newick


## write trees to out file for easier parsing later
out_handle = open('synth_trees.tre', 'w')
for key, val in newicks.items() :
	out_handle.write(key + "\t" + val + "\n")