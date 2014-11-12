import json
import fnmatch
import datetime
import git as git
import os, fnmatch
import collections
from itertools import tee, izip



def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename

def get_modified_files (limit_date, reindex, file_names) :

	phylesystem = os.getcwd() # needed to find git log
	g = git.Git(phylesystem) 
	limit = '--since=' + limit_date # set limit date since last index run
	files_changed = collections.OrderedDict()
	
	if reindex == True :
		for f in file_names :
                        print "Checking file %s for updates..." %f
			sha_log = g.log("--format=%H", f).split("\n")
			date_log = g.log("--format=%cd", f).split("\n")
                        
			if len(sha_log)>=1 and len(date_log) >=1 :
                                sha = sha_log[0]
                                date = date_log[0]
                                #print sha
                                #print date
				files_changed[f] = {'sha' : sha, 'date' : date}

	else :
		for f in file_names :
                        print "Checking file %s for updates..." %f
			sha = g.log("--format=%H", limit, f).split("\n")[0]
			date = g.log("--format=%cd", limit, f).split("\n")[0]
			if len(sha_log) >=1  and len(date_log) >=1 :
			    sha = sha_log[0]
                            date = date_log[0]	
                            files_changed[str(f)] = {'sha' : sha, 'date' : date}

	return files_changed

def build_json (user, files_changed, out_file) :
	
	now = datetime.datetime.now()
	current_date = "-".join([str(now.year), str(now.month), str(now.day)])
	files = collections.OrderedDict()

	## builds a dict of file name key and when it was updated according to git
	for key, val in files_changed.items() :
		files[key] = {'last_updated' : val}

	## build the rest of the dict needed to dump the json log file
	attributes = collections.OrderedDict()
	attributes['run_date'] = current_date
	attributes['cutoff_date'] = limit_date
	attributes['user'] = user
	attributes['files'] = files
	json_obj = json.dumps(attributes, ensure_ascii=False)

	with open (out_file, 'w') as outfile :
		json.dump(attributes, outfile, indent=4)
	



## some basic params

user = "" # attributes the update to someone for book keeping
limit_date_set = "" # if no previous json file is found, this date is used as the search limit for changes
reindex = True # if True, it will ignore the limit_date and reindex all nexson files
phylesystem_dir = "" # full path to phylesystem/study directory
previous_json_file = 'phylesystem_index.json' # previous json file to check for run date
out_file = 'phylesystem_index.json' # change as needed


if os.path.isfile(previous_json_file) :
	handle = open(previous_json_file, 'r')
	json_data = json.load(handle)
	limit_date = json_data['run_date']
else :
	limit_date = limit_date_set

file_names = []
for filename in find_files(phylesystem_dir, '*.json') :
    file_names.append(filename)

files_changed = get_modified_files(limit_date, reindex, file_names)

if len(files_changed) > 0 :
    build_json(user, files_changed, out_file)
else:
    print "There were no changes found in the nexson files."