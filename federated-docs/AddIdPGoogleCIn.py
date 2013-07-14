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
roleid = "5f44dd39240e4a868bdbd03981c989a4"

#----------AddEndpoints-----------------------------------------------------------------------
#---------AddAttrFederacao--------------------------------------------------------------------
print "Adding Org Attributes"
orgattEndpoint = BASE_URL+":5000/v3/org_attributes"

att = {"org_attribute":{}}
att["org_attribute"]["type"] = "hd"
att["org_attribute"]["value"] = "cin.ufpe.br"
orgatt = keystoneRequest(orgattEndpoint, att, "POST")

print "OK"
#--------Adding Authorised Issuers for Attributes--------------------------------------------------
print "Adding Authorised Issuers for Attributes"

keystoneRequest(orgattEndpoint+"/"+orgatt["org_attribute"]["id"]+"/issuers/"+serviceid, method="PUT")

print "OK"

#------Adding Projects no Keystone-----------------------------------------------------------------------------------------------------------------------------
print "Adding Projects"
projectEndPoint = BASE_URL+":5000/v3/projects"

newProject= {"project":{}}
newProject["project"]["name"] = "CIn UFPE"
newProject["project"]["description"] = "CIn UFPE's Project"
project = keystoneRequest(projectEndPoint, newProject, "POST")

print "OK"
#-----------"Organising Org Sets"----------------------------------------------------------------------------
orgsetEndpoint = BASE_URL+":5000/v3/org_attribute_sets"

# Attributes:
orgatt1id = "699121ec38964d4b80ab13d28318a875"
orgatt2id = "0b699e172a074a3388eaedd0fd04c0d3"
orgatt3id = "18fa80e43ef74734ad04a5cbc83302a8"

# Create the set
newOrgSet = {"org_attribute_set":{}}
newOrgSet["org_attribute_set"]["name"] = "IdPCInSet"
OrgSet = keystoneRequest(orgsetEndpoint, newOrgSet, "POST")
# Add the attributes
keystoneRequest(orgsetEndpoint+"/"+OrgSet["org_attribute_set"]["id"]+"/attributes/"+orgatt["org_attribute"]["id"], method="PUT")
keystoneRequest(orgsetEndpoint+"/"+OrgSet["org_attribute_set"]["id"]+"/attributes/"+orgatt1id, method="PUT")
keystoneRequest(orgsetEndpoint+"/"+OrgSet["org_attribute_set"]["id"]+"/attributes/"+orgatt2id, method="PUT")
keystoneRequest(orgsetEndpoint+"/"+OrgSet["org_attribute_set"]["id"]+"/attributes/"+orgatt3id, method="PUT")

print "OK"
#-----------"Organising OS Sets"---------------------------------------------------------------
print "Organising Os Sets"
ossetEndpoint = BASE_URL+":5000/v3/os_attribute_sets"

newOsSet = {"os_attribute_set":{}}
newOsSet["os_attribute_set"]["name"] = "IdpCInSet"
osSet = keystoneRequest(ossetEndpoint, newOsSet, "POST")
# Add the attributes
keystoneRequest(ossetEndpoint+"/"+osSet["os_attribute_set"]["id"]+"/projects/"+project["project"]["id"], method="PUT")
keystoneRequest(ossetEndpoint+"/"+osSet["os_attribute_set"]["id"]+"/roles/"+roleid, method="PUT")

print "OK"

#--------"Mapping"----------------------------------------------------------------------------------

print "Mapping Sets"

amEndpoint = BASE_URL+":5000/v3/attribute_set_mappings"
basicMap = {"attribute_set_mapping":{"org_attribute_set_id":"", "os_attribute_set_id":""}}

newMap = basicMap.copy()
newMap["attribute_set_mapping"]["org_attribute_set_id"] = OrgSet["org_attribute_set"]["id"]
newMap["attribute_set_mapping"]["os_attribute_set_id"] = osSet["os_attribute_set"]["id"]
keystoneRequest(amEndpoint, newMap, "POST")

print "OK"
print "Success, all entities created, demo ready"

