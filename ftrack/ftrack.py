
import ftrack_api





session = ftrack_api.Session(server_url='https://ftrack.x-plarium.com/',
                             api_key='4b42ec75-12e4-4be7-88ed-5e8b0e424945',
                             api_user='a.gamaiunov')

#print session.types.keys()
# print session.query("Sequence")
# for i in session.query("Sequence"):
#     print i

active_projects = session.query('Project where status is active')
print(active_projects)
# print active_projects[4]['name']
# print active_projects[4]['children'][1]['children']
#
# for i in active_projects[4]['children'][1]['children']:
#     print i

