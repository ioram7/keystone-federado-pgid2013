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

newService = {"service":{"name":"Google OIDC", "description": "Google OpenID Connect", "type":"idp.oidc"}} #idpNormal
service = keystoneRequest(serviceEndpoint, newService, "POST")
print "OK"

#----------AddEndpoints-----------------------------------------------------------------------
print "Adding Endpoints"
endpointEndpoint = BASE_URL+":35357/v2.0/endpoints"
idpPublicURL     = "https://accounts.google.com/o/oauth2/auth"
idpInternalURL   = "https://accounts.google.com/o/oauth2/token"
idpAdminURL      = "https://www.googleapis.com/oauth2/v1/tokeninfo"
idpClientId      = "800550332219-rgimrn586j5cnrd5vvk31iovcom2gbb6.apps.googleusercontent.com"
idpClientSecret  = "GUpzyfiMqH5u06Wz8OJ-ReX_"
idpRedirectUri   = "https://localhost:8080/"
idpScope         = ""

newEndpoint = {"endpoint":{}}
newEndpoint["endpoint"]["service_id"] = service["service"]["id"]
newEndpoint["endpoint"]["publicurl"]=idpPublicURL
newEndpoint["endpoint"]["internalurl"]=idpInternalURL
newEndpoint["endpoint"]["adminurl"]=idpAdminURL
newEndpoint["endpoint"]["client_id"]=idpClientId
newEndpoint["endpoint"]["client_secret"]=idpClientSecret
newEndpoint["endpoint"]["redirect_uri"]=idpRedirectUri
newEndpoint["endpoint"]["scope"]=idpScope

endpoint = keystoneRequest(endpointEndpoint, newEndpoint, "POST")

print "OK"

#---------AddAttrFederacao--------------------------------------------------------------------
print "Adding Org Attributes"
orgattEndpoint = BASE_URL+":5000/v3/org_attributes"

att = {"org_attribute":{}}
att["org_attribute"]["type"] = "email_verified"
att["org_attribute"]["value"] = "true"
orgatt = keystoneRequest(orgattEndpoint, att, "POST")

att1 = {"org_attribute":{}}
att1["org_attribute"]["type"] = "sub"
orgatt1 = keystoneRequest(orgattEndpoint, att1, "POST")

att2 = {"org_attribute":{}}
att2["org_attribute"]["type"] = "email"
orgatt2 = keystoneRequest(orgattEndpoint, att2, "POST")

print "OK"
#--------Adding Authorised Issuers for Attributes--------------------------------------------------
print "Adding Authorised Issuers for Attributes"

keystoneRequest(orgattEndpoint+"/"+orgatt["org_attribute"]["id"]+"/issuers/"+service["service"]["id"], method="PUT")
keystoneRequest(orgattEndpoint+"/"+orgatt1["org_attribute"]["id"]+"/issuers/"+service["service"]["id"], method="PUT")
keystoneRequest(orgattEndpoint+"/"+orgatt2["org_attribute"]["id"]+"/issuers/"+service["service"]["id"], method="PUT")

print "OK"

#---------------------------------------------------------------------------------------------------------------------------------------------------

#print "Adding roles"
#roleEndPoint = BASE_URL+":5000/v3/roles"
#
#newRole= {"role":{}}
#newRole["role"]["name"] = "federated_role"
#role = keystoneRequest(roleEndPoint, newRole, "POST")
#
#print "OK"
roleid = "5f44dd39240e4a868bdbd03981c989a4"

#------Adding Projects no Keystone-----------------------------------------------------------------------------------------------------------------------------
print "Adding Projects"
projectEndPoint = BASE_URL+":5000/v3/projects"

newProject= {"project":{}}
newProject["project"]["name"] = "Google User's Project"
newProject["project"]["description"] = "IdpECT Personal User's Project"
project = keystoneRequest(projectEndPoint, newProject, "POST")

print "OK"
#-----------"Organising Org Sets"----------------------------------------------------------------------------
orgsetEndpoint = BASE_URL+":5000/v3/org_attribute_sets"

# IDPUFRN  Sets
# Set 1 contains brEduAffiliationType=student (orgatt) 
# Create the set
newOrgSet = {"org_attribute_set":{}}
newOrgSet["org_attribute_set"]["name"] = "IdPGoogleSet"
OrgSet = keystoneRequest(orgsetEndpoint, newOrgSet, "POST")
# Add the attributes
keystoneRequest(orgsetEndpoint+"/"+OrgSet["org_attribute_set"]["id"]+"/attributes/"+orgatt["org_attribute"]["id"], method="PUT")
keystoneRequest(orgsetEndpoint+"/"+OrgSet["org_attribute_set"]["id"]+"/attributes/"+orgatt1["org_attribute"]["id"], method="PUT")
keystoneRequest(orgsetEndpoint+"/"+OrgSet["org_attribute_set"]["id"]+"/attributes/"+orgatt2["org_attribute"]["id"], method="PUT")

print "OK"
#-----------"Organising OS Sets"---------------------------------------------------------------
print "Organising Os Sets"
ossetEndpoint = BASE_URL+":5000/v3/os_attribute_sets"

newOsSet = {"os_attribute_set":{}}
newOsSet["os_attribute_set"]["name"] = "IdpGoogleSet"
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

