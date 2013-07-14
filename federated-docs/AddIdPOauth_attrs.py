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

serviceid = "7c3a3df54c9f42f4aa5a742f369fde01"
endpointid = "02c1ca9f4e804f749a7bb64d2fbd46d0"
tenantid = "7a68f9383ec04779a7e5f7ea1edfa7ec"
roleid = "5f44dd39240e4a868bdbd03981c989a4"

#---------AddAttrFederacao--------------------------------------------------------------------
print "Adding Org Attributes"
orgattEndpoint = BASE_URL+":5000/v3/org_attributes"

att1 = {"org_attribute":{}}
att1["org_attribute"]["type"] = "email"
orgatt1 = keystoneRequest(orgattEndpoint, att1, "POST")

att2 = {"org_attribute":{}}
att2["org_attribute"]["type"] = "verified"
att2["org_attribute"]["value"] = "True"
orgatt2 = keystoneRequest(orgattEndpoint, att2, "POST")

att3 = {"org_attribute":{}}
att3["org_attribute"]["type"] = "username"
orgatt3 = keystoneRequest(orgattEndpoint, att2, "POST")


print "OK"
#--------Adding Authorised Issuers for Attributes--------------------------------------------------
print "Adding Authorised Issuers for Attributes"

keystoneRequest(orgattEndpoint+"/"+orgatt1["org_attribute"]["id"]+"/issuers/"+serviceid, method="PUT")
keystoneRequest(orgattEndpoint+"/"+orgatt2["org_attribute"]["id"]+"/issuers/"+serviceid, method="PUT")
keystoneRequest(orgattEndpoint+"/"+orgatt3["org_attribute"]["id"]+"/issuers/"+serviceid, method="PUT")

print "OK"

#-----------"Organising Org Sets"----------------------------------------------------------------------------
orgsetEndpoint = BASE_URL+":5000/v3/org_attribute_sets"

# IDPUFRN  Sets
# Set 1 contains brEduAffiliationType=student (orgatt) 
# Create the set
newOrgSet = {"org_attribute_set":{}}
newOrgSet["org_attribute_set"]["name"] = "IdPFBSet1"
OrgSet1 = keystoneRequest(orgsetEndpoint, newOrgSet, "POST")
# Add the attributes
keystoneRequest(orgsetEndpoint+"/"+OrgSet1["org_attribute_set"]["id"]+"/attributes/"+orgatt1["org_attribute"]["id"], method="PUT")
keystoneRequest(orgsetEndpoint+"/"+OrgSet1["org_attribute_set"]["id"]+"/attributes/"+orgatt2["org_attribute"]["id"], method="PUT")
keystoneRequest(orgsetEndpoint+"/"+OrgSet1["org_attribute_set"]["id"]+"/attributes/"+orgatt3["org_attribute"]["id"], method="PUT")

print "OK"
#-----------"Organising OS Sets"---------------------------------------------------------------
print "Organising Os Sets"
ossetEndpoint = BASE_URL+":5000/v3/os_attribute_sets"

newOsSet = {"os_attribute_set":{}}
newOsSet["os_attribute_set"]["name"] = "IdpFBSet1"
osSet1 = keystoneRequest(ossetEndpoint, newOsSet, "POST")
# Add the attributes
keystoneRequest(ossetEndpoint+"/"+osSet1["os_attribute_set"]["id"]+"/projects/"+tenantid, method="PUT")
keystoneRequest(ossetEndpoint+"/"+osSet1["os_attribute_set"]["id"]+"/roles/"+roleid, method="PUT")

print "OK"

#--------"Mapping"----------------------------------------------------------------------------------

print "Mapping Sets"

amEndpoint = BASE_URL+":5000/v3/attribute_set_mappings"
basicMap = {"attribute_set_mapping":{"org_attribute_set_id":"", "os_attribute_set_id":""}}

# Kent: koset1 -> kset2
newMap = basicMap.copy()
newMap["attribute_set_mapping"]["org_attribute_set_id"] = OrgSet1["org_attribute_set"]["id"]
newMap["attribute_set_mapping"]["os_attribute_set_id"] = osSet1["os_attribute_set"]["id"]
keystoneRequest(amEndpoint, newMap, "POST")

print "OK"
print "Success, all entities created, demo ready"

