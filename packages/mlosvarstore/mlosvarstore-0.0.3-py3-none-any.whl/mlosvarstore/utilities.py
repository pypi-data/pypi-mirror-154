import os
import json
import sys
_uhome=os.path.expanduser('~')
_wp = os.path.join(_uhome, 'wp')
fnxc=os.path.join(_wp,"mos.json")
if(os.path.exists(fnxc)):
    with open(fnxc, 'r') as infile:
        data=json.load( infile)
        _mosroot=data["mosroot"]
sys.path.append(_mosroot)
# class mlosutil:
#     def __init__(self):
#         self._uhome=os.path.expanduser('~')
#         self._wp = os.path.join(self._uhome, 'wp')
#     def getmlosconf(self):
#         fnxc=os.path.join(self._wp,"mos.json")
#         if(os.path.exists(fnxc)):
#             with open(fnxc, 'r') as infile:
#                 data=json.load( infile)
#         self._mosroot=data["mosroot"]
#         self._mosbase=data["mosbase"]
#         self._wp=data["wp"]
#         return self._wp, self._mosroot, self._mosbase

#     def getparam(self,type,config):
#         config={
#             "project":"ppaul_braintoy.ai",
#             "project":"f18e4c99410d4c369b9573f48abc9722",
#             "rawdb":"Iris",
#             "dbset":"tst",
#             "param":"a5ad_1654710126086470:32710f66-8b9e-fd7c-47ed-331b0ab06fb6|/Users/padmapolashpaul/wp/mos/ppaul_braintoy.ai/f18e4c99410d4c369b9573f48abc9722/tmp|ppaul_braintoy.ai|f18e4c99410d4c369b9573f48abc9722|Iris|tst|80|0:0"
#         }
#         return config
#     def execute(self,_cdir,script_name,script_type):
#         config={}
#         conf=self.getparam("gendbs",config)
#         wp,mosroot,mosbase=self.getmlosconf()
#         _script_name=os.path.join(_cdir,script_name)
#         cmd= "cd "+mosroot+" \n python3 "+ _script_name +  "  --o '"+conf["param"]+"'"
#         os.system(cmd)
