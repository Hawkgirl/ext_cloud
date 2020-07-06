#!  /home/padmin/bhanum/env/bin/python
import logging
logger = logging.getLogger('openstackexporter')
hdlr = logging.FileHandler('/tmp/openstackexporter.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)

logger.info('start exporter')




import warnings
warnings.filterwarnings("ignore")

from ext_cloud import get_ext_cloud


cloud_obj = get_ext_cloud("openstack")
dic = {}
cloud_obj.resources.list_metrics_all(dic)

dic2 = {}
for key in dic:
  metric = key.replace('.','/')
  index = metric.rfind('/')
  newkey = 'http://172.31.216.249:9091/metrics/job/' + metric[0:index]
  if newkey in dic2:
      dic2[newkey] += metric[index+1:] + ' ' + str(dic[key]) + '\n'
  else:
      dic2[newkey] = metric[index+1:] + ' ' + str(dic[key]) + '\n'

#for key in dic2:
#    print(key, dic2[key])
logger.info('metrics count {a}'.format(a=len(dic)))


import requests
for key in dic2:
    #r=requests.delete(url=key) 
    r=requests.post(url=key,data=dic2[key]) 
    print(r.url)
    print(r)
    print(r.text)


logger.info('end exporter')
exit(0)
