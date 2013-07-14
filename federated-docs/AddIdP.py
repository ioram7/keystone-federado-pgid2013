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

newService = {"service":{"name":"IdP ECT service", "description": "IdP ECT service", "type":"idp.saml"}} #idpNormal
service = keystoneRequest(serviceEndpoint, newService, "POST")
print "OK"

#----------AddEndpoints-----------------------------------------------------------------------
print "Adding Endpoints"
endpointEndpoint = BASE_URL+":35357/v2.0/endpoints"
idpServiceURL = "https://idp.ect.ufrn.br/simplesaml/saml2/idp/SSOService.php" #LocationidpectNormal
idpcertdata = "MIID/zCCAuegAwIBAgIJAPFeoZxEJcWqMA0GCSqGSIb3DQEBBQUAMIGVMQswCQYDVQQGEwJicjEcMBoGA1UECAwTcmlvIGdyYW5kZSBkbyBub3J0ZTEOMAwGA1UEBwwFbmF0YWwxDTALBgNVBAoMBHVmcm4xDDAKBgNVBAsMA2VjdDEYMBYGA1UEAwwPaWRwLmVjdC51ZnJuLmJyMSEwHwYJKoZIhvcNAQkBFhJrYWR1YXJkb0BnbWFpbC5jb20wHhcNMTMwNDE2MTgzODMxWhcNMjMwNDE2MTgzODMxWjCBlTELMAkGA1UEBhMCYnIxHDAaBgNVBAgME3JpbyBncmFuZGUgZG8gbm9ydGUxDjAMBgNVBAcMBW5hdGFsMQ0wCwYDVQQKDAR1ZnJuMQwwCgYDVQQLDANlY3QxGDAWBgNVBAMMD2lkcC5lY3QudWZybi5icjEhMB8GCSqGSIb3DQEJARYSa2FkdWFyZG9AZ21haWwuY29tMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAycVQRB2UhMYfww0B470pkZBD0cFweDjuic6zpwCzbQW8vFGGYeGzbAb61p2UPRXg5zf4CfHuFCREr2Iz4944PTFErmyWtjoFBgLqkODtAkLqhDLm7xipTaFyR10lDzW5WLwbF4nh6Fl7iN4uyiN1kVCoIVNtyktc8iU1GOdeapA66Il+slevcDrIarc2W5UpYFsuzJoqMFFguOHdaIaxmFnvbPDWjlFBdbgKsJkfoo/yWxeAmNy1+FAWOLcO3yoRGVT99y2PUiI5Z29x8aUYeyhtc+21rDNUAPSU0/pxve/uahthmXEs8tpgnsauoy2SR8Z1YKbR2jG+/o3lN0SjVwIDAQABo1AwTjAdBgNVHQ4EFgQU2TAOD/zFN9B4gMfLUF6iX/BoZiQwHwYDVR0jBBgwFoAU2TAOD/zFN9B4gMfLUF6iX/BoZiQwDAYDVR0TBAUwAwEB/zANBgkqhkiG9w0BAQUFAAOCAQEAwBM84R1Ur9g//Aey/5op1I7C6Hncq9cvAEvbnl4xT7P3jubaDGK770FV8YyltfpiBytGsMjbiSlOBQVBbMPlt+xUJwMEu+amirPPcv9Ww72cnV1A0EWiIOHvzQmbhzn3wgbMsW1XAXfZBCEg3IT80KcC+FLDHaodI35zVOcWBuq54HumE+MReyWmoL7tcCI+NDtBSDiAdncyZX3VhUz4WPYLOEfqZNK0VWzrckJ+9u1xU/VkzIjqX/FBHqUXRhQH6IDInHT46XBDWRw9V/r2oc5rZ8Iz1a7e0HTmqpddSyDg1o2VkuBIb7Z0O8cr6cZ2kwr+NdyJPV1WvQ85kbSjXA=="

newEndpoint = {"endpoint":{}}
newEndpoint["endpoint"]["service_id"] = service["service"]["id"]
newEndpoint["endpoint"]["publicurl"]=idpServiceURL
newEndpoint["endpoint"]["internalurl"]=idpServiceURL #montando endpoint do idpectNormal
newEndpoint["endpoint"]["adminurl"]=idpServiceURL
newEndpoint["endpoint"]["certdata"]=idpcertdata

endpoint = keystoneRequest(endpointEndpoint, newEndpoint, "POST")

print "OK"

#---------AddAttrFederacao--------------------------------------------------------------------
print "Adding Org Attributes"
orgattEndpoint = BASE_URL+":5000/v3/org_attributes"

att = {"org_attribute":{}}
att["org_attribute"]["type"] = "brEduAffiliationType"
att["org_attribute"]["value"] = "student"
orgatt = keystoneRequest(orgattEndpoint, att, "POST")

att1 = {"org_attribute":{}}
att1["org_attribute"]["type"] = "eduPersonPrincipalName"
orgatt1 = keystoneRequest(orgattEndpoint, att1, "POST")

att2 = {"org_attribute":{}}
att2["org_attribute"]["type"] = "brEduAffiliationType"
att2["org_attribute"]["value"] = "employee"
orgatt2 = keystoneRequest(orgattEndpoint, att2, "POST")

print "OK"
#--------Adding Authorised Issuers for Attributes--------------------------------------------------
print "Adding Authorised Issuers for Attributes"

keystoneRequest(orgattEndpoint+"/"+orgatt["org_attribute"]["id"]+"/issuers/"+service["service"]["id"], method="PUT")
keystoneRequest(orgattEndpoint+"/"+orgatt1["org_attribute"]["id"]+"/issuers/"+service["service"]["id"], method="PUT")
keystoneRequest(orgattEndpoint+"/"+orgatt2["org_attribute"]["id"]+"/issuers/"+service["service"]["id"], method="PUT")

print "OK"

#---------------------------------------------------------------------------------------------------------------------------------------------------

print "Adding roles"
roleEndPoint = BASE_URL+":5000/v3/roles"

newRole= {"role":{}}
newRole["role"]["name"] = "federated_role"
role = keystoneRequest(roleEndPoint, newRole, "POST")

print "OK"

#------Adding Projects no Keystone-----------------------------------------------------------------------------------------------------------------------------
print "Adding Projects"
projectEndPoint = BASE_URL+":5000/v3/projects"

newProject= {"project":{}}
newProject["project"]["name"] = "Personal User's Project"
newProject["project"]["description"] = "IdpECT Personal User's Project"
project = keystoneRequest(projectEndPoint, newProject, "POST")

newProject1= {"project":{}}
newProject1["project"]["name"] = "Student Staff Project"
newProject1["project"]["description"] = "IdPEct Student Staff Project"
project1 = keystoneRequest(projectEndPoint, newProject1, "POST")

newProject2= {"project":{}}
newProject2["project"]["name"] = "Employee Staff Project"
newProject2["project"]["description"] = "IdPEct Employee Staff Project"
project2 = keystoneRequest(projectEndPoint, newProject2, "POST")

print "OK"
#-----------"Organising Org Sets"----------------------------------------------------------------------------
orgsetEndpoint = BASE_URL+":5000/v3/org_attribute_sets"

# IDPUFRN  Sets
# Set 1 contains brEduAffiliationType=student (orgatt) 
# Create the set
newOrgSet = {"org_attribute_set":{}}
newOrgSet["org_attribute_set"]["name"] = "IdPectSet1"
OrgSet = keystoneRequest(orgsetEndpoint, newOrgSet, "POST")
# Add the attributes
keystoneRequest(orgsetEndpoint+"/"+OrgSet["org_attribute_set"]["id"]+"/attributes/"+orgatt["org_attribute"]["id"], method="PUT")


# Set 2 contains eduPersonPrincipalName=anything (orgatt1) 
# Create the set
newOrgSet1 = {"org_attribute_set":{}}
newOrgSet1["org_attribute_set"]["name"] = "IdPectSet2"
OrgSet1 = keystoneRequest(orgsetEndpoint, newOrgSet1, "POST")
# Add the attributes
keystoneRequest(orgsetEndpoint+"/"+OrgSet1["org_attribute_set"]["id"]+"/attributes/"+orgatt1["org_attribute"]["id"], method="PUT")

# Set 3 contains brEduAffiliationType=employee (orgatt2) 
# Create the set
newOrgSet2 = {"org_attribute_set":{}}
newOrgSet2["org_attribute_set"]["name"] = "IdPectSet3"
OrgSet2 = keystoneRequest(orgsetEndpoint, newOrgSet2, "POST")
# Add the attributes
keystoneRequest(orgsetEndpoint+"/"+OrgSet2["org_attribute_set"]["id"]+"/attributes/"+orgatt2["org_attribute"]["id"], method="PUT")

print "OK"
#-----------"Organising OS Sets"---------------------------------------------------------------
print "Organising Os Sets"
ossetEndpoint = BASE_URL+":5000/v3/os_attribute_sets"

newOsSet = {"os_attribute_set":{}}
newOsSet["os_attribute_set"]["name"] = "IdpEctSet"
osSet = keystoneRequest(ossetEndpoint, newOsSet, "POST")
# Add the attributes
keystoneRequest(ossetEndpoint+"/"+osSet["os_attribute_set"]["id"]+"/projects/"+project["project"]["id"], method="PUT")
keystoneRequest(ossetEndpoint+"/"+osSet["os_attribute_set"]["id"]+"/roles/"+role["role"]["id"], method="PUT")

newOsSet1 = {"os_attribute_set":{}}
newOsSet1["os_attribute_set"]["name"] = "IdpEctSet1"
osSet1 = keystoneRequest(ossetEndpoint, newOsSet1, "POST")

keystoneRequest(ossetEndpoint+"/"+osSet1["os_attribute_set"]["id"]+"/projects/"+project1["project"]["id"], method="PUT")
keystoneRequest(ossetEndpoint+"/"+osSet1["os_attribute_set"]["id"]+"/roles/"+role["role"]["id"], method="PUT")

newOsSet2 = {"os_attribute_set":{}}
newOsSet2["os_attribute_set"]["name"] = "IdpEctSet2"
osSet2 = keystoneRequest(ossetEndpoint, newOsSet2, "POST")

keystoneRequest(ossetEndpoint+"/"+osSet2["os_attribute_set"]["id"]+"/projects/"+project2["project"]["id"], method="PUT")
keystoneRequest(ossetEndpoint+"/"+osSet2["os_attribute_set"]["id"]+"/roles/"+role["role"]["id"], method="PUT")


print "OK"

#--------"Mapping"----------------------------------------------------------------------------------

print "Mapping Sets"

amEndpoint = BASE_URL+":5000/v3/attribute_set_mappings"
basicMap = {"attribute_set_mapping":{"org_attribute_set_id":"", "os_attribute_set_id":""}}

# Kent: koset1 -> kset2
newMap = basicMap.copy()
newMap["attribute_set_mapping"]["org_attribute_set_id"] = OrgSet["org_attribute_set"]["id"]
newMap["attribute_set_mapping"]["os_attribute_set_id"] = osSet["os_attribute_set"]["id"]
keystoneRequest(amEndpoint, newMap, "POST")

newMap1 = basicMap.copy()
newMap1["attribute_set_mapping"]["org_attribute_set_id"] = OrgSet1["org_attribute_set"]["id"]
newMap1["attribute_set_mapping"]["os_attribute_set_id"] = osSet1["os_attribute_set"]["id"]
keystoneRequest(amEndpoint, newMap1, "POST")

newMap2 = basicMap.copy()
newMap2["attribute_set_mapping"]["org_attribute_set_id"] = OrgSet2["org_attribute_set"]["id"]
newMap2["attribute_set_mapping"]["os_attribute_set_id"] = osSet2["os_attribute_set"]["id"]
keystoneRequest(amEndpoint, newMap2, "POST")

print "OK"
print "Success, all entities created, demo ready"

