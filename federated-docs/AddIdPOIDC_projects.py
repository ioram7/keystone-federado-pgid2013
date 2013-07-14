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

print "Adding Identity Provider"
serviceEndpoint = BASE_URL+":5000/v3/services"

serviceid = "f38007244eab4cf59b09d1e8044f744b"
roleid    = "5f44dd39240e4a868bdbd03981c989a4"
projectid = "06b110f0c4fc4faca72f407925ebfa53"
orgattid  = "0c4c85b5b301456a946d5230bacbc8e1"
orgattid1 = "17b70c92956641258d43c92822570b44"
orgattid2 = "f2b6447dcdf64399b1cb69679753a8eb"
osetid    = "9cf4541e26044b3ab449641a756ad851"

#-----------"Organising Org Sets"----------------------------------------------------------------------------
orgsetEndpoint = BASE_URL+":5000/v3/org_attribute_sets"

# IDPUFRN  Sets
# Set 1 contains brEduAffiliationType=student (orgatt) 
# Create the set
newOrgSet = {"org_attribute_set":{}}
newOrgSet["org_attribute_set"]["name"] = "IdPGoogleOIDCSet"
OrgSet = keystoneRequest(orgsetEndpoint, newOrgSet, "POST")
# Add the attributes
keystoneRequest(orgsetEndpoint+"/"+OrgSet["org_attribute_set"]["id"]+"/attributes/"+orgattid, method="PUT")
keystoneRequest(orgsetEndpoint+"/"+OrgSet["org_attribute_set"]["id"]+"/attributes/"+orgattid1, method="PUT")
keystoneRequest(orgsetEndpoint+"/"+OrgSet["org_attribute_set"]["id"]+"/attributes/"+orgattid2, method="PUT")

print "OK"

#--------"Mapping"----------------------------------------------------------------------------------

print "Mapping Sets"

amEndpoint = BASE_URL+":5000/v3/attribute_set_mappings"
basicMap = {"attribute_set_mapping":{"org_attribute_set_id":"", "os_attribute_set_id":""}}

newMap = basicMap.copy()
newMap["attribute_set_mapping"]["org_attribute_set_id"] = OrgSet["org_attribute_set"]["id"]
newMap["attribute_set_mapping"]["os_attribute_set_id"] = osetid
keystoneRequest(amEndpoint, newMap, "POST")

print "OK"
print "Success, all entities created, demo ready"

