from jenkins import Jenkins
import simplejson as json

jk = Jenkins(
    "https://jenkins.kyoffice.cn",
    username='yaoshaoqiang',
    password='w9vM7BQoED6fg.uheO'
)
data = jk.get_build_info(name='test', number=25)
print(json.dumps(data,indent=4) )
