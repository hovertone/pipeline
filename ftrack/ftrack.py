
import ftrack_api





session = ftrack_api.Session(server_url='',
                             api_key='',
                             api_user='e.desheviy')

#print session.types.keys()
# print session.query("Sequence")
# for i in session.query("Sequence"):
#     print i

active_projects = session.query('Project where status is active')
print active_projects[4]['name']
print active_projects[4]['children'][1]['children']

for i in active_projects[4]['children'][1]['children']:
    print i

x = "VASA"



