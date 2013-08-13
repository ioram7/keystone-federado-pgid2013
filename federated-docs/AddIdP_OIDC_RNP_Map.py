import urllib
import urllib2
import json


BASE_URL = "http://openstack.bsbbs.com.br" 


def keystoneRequest(endpoint, data = {}, method = "GET"):
    headers = {'X-Auth-Token': 'admin'} #auth_token definido no keystone.conf
    if method == "GET":        
        req = urllib2.Request(endpoint, headers = headers)
        response = urllib2.urlopen(req)
    elif method == "PUT":
        req = urllib2.Request(endpoint, headers = headers)        
        req.get_method = lambda: 'PUT'
        response = urllib2.urlopen(req)
        return
    elif method == "POST":
        data = json.dumps(data)
        headers['Content-Type'] = 'application/json'
        req = urllib2.Request(endpoint, data, headers)
        response = urllib2.urlopen(req)
    return json.loads(response.read())

#--------"Mapping"----------------------------------------------------------------------------------

print "Mapping Sets"

orgSetRNPPub2 = 'a55850602ddc427fa6d0fc369fed1433';
osSetPubM     = '480f349db8334e0ea70d0baac3649e75';

amEndpoint = BASE_URL+":5000/v3/attribute_set_mappings"
basicMap = {"attribute_set_mapping":{"org_attribute_set_id":"", "os_attribute_set_id":""}}

# RNP Public
newMap = basicMap.copy()
newMap["attribute_set_mapping"]["org_attribute_set_id"] = orgSetRNPPub2;
newMap["attribute_set_mapping"]["os_attribute_set_id"] = osSetPubM;
keystoneRequest(amEndpoint, newMap, "POST")

print "OK"
print "Success, all entities created, demo ready"

