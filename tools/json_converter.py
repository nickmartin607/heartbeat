import json

INPUT_FILE = 'hb.json'
OUTPUT_FILE = 'seed.json'

def echo(d):
    [print('{}\t{}\n'.format(k,v)) for k,v in d.items()]
def readfile():
    with open(INPUT_FILE) as infile:
        data = {}
        for entry in json.loads(infile.readline()):
            model = entry.get('model')
            if model not in data:
                data[model] = []
            data[model].append(entry)
    return data
def writefile(data):
    with open(OUTPUT_FILE, 'w') as outfile:
        outfile.write(json.dumps(data))

def editdata(data):
    models_to_save = {
        'hbh': 'heartbeat.host',    'hbs': 'heartbeat.service',
        'hbt': 'heartbeat.team',    'ag': 'auth.group',     'au': 'auth.user',
    }
    models_to_delete = [
        'admin.logentry',           'auth.permission',
        'authentication.account',   'contenttypes.contenttype',
        'heartbeat.inject',         'heartbeat.check',
        'heartbeat.credential',     'heartbeat.schedule',
    ]
    fields_to_delete = [
        'date_joined', 'last_login', 'timestamp', 'last_name', 'first_name',
        'points_earned', 'credential', 'expected_result', 'status',
    ]
    fields_to_rename = {
        # 'visible': 'enabled',
    }
    new_data = {}
    for model, model_data in data.items():
        if model not in models_to_delete:
            new_model = []
            for instance in model_data:
                new_instance = instance.copy()
                fields = new_instance.get('fields').copy()
                for key, value in instance.get('fields').items():
                    if key in fields_to_delete:
                        fields.pop(key)
                    elif key in fields_to_rename:
                        fields[fields_to_rename.get(key)] = fields.pop(key)
                new_instance['fields'] = fields
                new_model.append(new_instance)
            new_data[model] = new_model
    return new_data
                
    





if __name__ == '__main__':
    data = readfile()
    data = editdata(data)
    writefile(data)

























# groups = {e.get('pk'):e.get('fields').get('name') for e in models.get(GROUPS)}
# users = {e.get('pk'):{'group':e.get('fields').get('groups')[0], 'fields':e.get('fields')} for e in models.get(USERS)}
# teams = {e.get('pk'):{'group':e.get('fields').get('group'), 'fields':e.get('fields')} for e in models.get(TEAMS)}
# hosts = {e.get('pk'):{'team':e.get('fields').get('team'), 'fields':e.get('fields')} for e in models.get(HOSTS)}
# services = {e.get('pk'):{'host':e.get('fields').get('host'), 'fields':e.get('fields')} for e in models.get(SERVICES)}
    
# team_pks = {k:v.get('fields').get('name') for k,v in teams.items()}
# host_pks = {k:v.get('fields').get('name') for k,v in hosts.items()}

# echo(team_pks)
# print("")
# echo(host_pks)