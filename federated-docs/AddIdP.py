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

print "Adding Identity Providers"
serviceEndpoint = BASE_URL+":5000/v3/services"

newService = {"service":{"name":"RNP UFRN", "description": "IdP ECT SAML service", "type":"idp.saml"}} #idpNormal
serviceRNP = keystoneRequest(serviceEndpoint, newService, "POST")

newService = {"service":{"name":"Facebook", "description": "IdP Facebook OAuth service", "type":"idp.oauth"}} #idpNormal
serviceFB = keystoneRequest(serviceEndpoint, newService, "POST")

newService = {"service":{"name":"Google (OAuth)", "description": "IdP Google OAuth service", "type":"idp.oauth"}} #idpNormal
serviceGOA = keystoneRequest(serviceEndpoint, newService, "POST")

newService = {"service":{"name":"Google (OIDC)", "description": "IdP Google OIDC service", "type":"idp.oidc"}} #idpNormal
serviceGOIDC = keystoneRequest(serviceEndpoint, newService, "POST")

print "OK"

#----------AddEndpoints-----------------------------------------------------------------------
print "Adding Endpoints"

endpointEndpoint = BASE_URL+":35357/v2.0/endpoints"

# RNP

idpServiceURL = "https://idp.ect.ufrn.br/simplesaml/saml2/idp/SSOService.php" #LocationidpectNormal
idpcertdata = "MIID/zCCAuegAwIBAgIJAPFeoZxEJcWqMA0GCSqGSIb3DQEBBQUAMIGVMQswCQYDVQQGEwJicjEcMBoGA1UECAwTcmlvIGdyYW5kZSBkbyBub3J0ZTEOMAwGA1UEBwwFbmF0YWwxDTALBgNVBAoMBHVmcm4xDDAKBgNVBAsMA2VjdDEYMBYGA1UEAwwPaWRwLmVjdC51ZnJuLmJyMSEwHwYJKoZIhvcNAQkBFhJrYWR1YXJkb0BnbWFpbC5jb20wHhcNMTMwNDE2MTgzODMxWhcNMjMwNDE2MTgzODMxWjCBlTELMAkGA1UEBhMCYnIxHDAaBgNVBAgME3JpbyBncmFuZGUgZG8gbm9ydGUxDjAMBgNVBAcMBW5hdGFsMQ0wCwYDVQQKDAR1ZnJuMQwwCgYDVQQLDANlY3QxGDAWBgNVBAMMD2lkcC5lY3QudWZybi5icjEhMB8GCSqGSIb3DQEJARYSa2FkdWFyZG9AZ21haWwuY29tMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAycVQRB2UhMYfww0B470pkZBD0cFweDjuic6zpwCzbQW8vFGGYeGzbAb61p2UPRXg5zf4CfHuFCREr2Iz4944PTFErmyWtjoFBgLqkODtAkLqhDLm7xipTaFyR10lDzW5WLwbF4nh6Fl7iN4uyiN1kVCoIVNtyktc8iU1GOdeapA66Il+slevcDrIarc2W5UpYFsuzJoqMFFguOHdaIaxmFnvbPDWjlFBdbgKsJkfoo/yWxeAmNy1+FAWOLcO3yoRGVT99y2PUiI5Z29x8aUYeyhtc+21rDNUAPSU0/pxve/uahthmXEs8tpgnsauoy2SR8Z1YKbR2jG+/o3lN0SjVwIDAQABo1AwTjAdBgNVHQ4EFgQU2TAOD/zFN9B4gMfLUF6iX/BoZiQwHwYDVR0jBBgwFoAU2TAOD/zFN9B4gMfLUF6iX/BoZiQwDAYDVR0TBAUwAwEB/zANBgkqhkiG9w0BAQUFAAOCAQEAwBM84R1Ur9g//Aey/5op1I7C6Hncq9cvAEvbnl4xT7P3jubaDGK770FV8YyltfpiBytGsMjbiSlOBQVBbMPlt+xUJwMEu+amirPPcv9Ww72cnV1A0EWiIOHvzQmbhzn3wgbMsW1XAXfZBCEg3IT80KcC+FLDHaodI35zVOcWBuq54HumE+MReyWmoL7tcCI+NDtBSDiAdncyZX3VhUz4WPYLOEfqZNK0VWzrckJ+9u1xU/VkzIjqX/FBHqUXRhQH6IDInHT46XBDWRw9V/r2oc5rZ8Iz1a7e0HTmqpddSyDg1o2VkuBIb7Z0O8cr6cZ2kwr+NdyJPV1WvQ85kbSjXA=="
newEndpoint = {"endpoint":{}}
newEndpoint["endpoint"]["service_id"] = serviceRNP["service"]["id"]
newEndpoint["endpoint"]["publicurl"]=idpServiceURL
newEndpoint["endpoint"]["internalurl"]=idpServiceURL 
newEndpoint["endpoint"]["adminurl"]=idpServiceURL
newEndpoint["endpoint"]["certdata"]=idpcertdata
endpointRNP = keystoneRequest(endpointEndpoint, newEndpoint, "POST")

# Facebook

idpPublicURL    = "https://graph.facebook.com/oauth/authorize"
idpInternalURL  = "https://graph.facebook.com/oauth/access_token"
idpAdminURL     = "https://graph.facebook.com/me"
idpRedirectUri  = "https://localhost:8080"
idpClientId     = "600041930027373"
idpClientSecret = "451567ba4bc0451b49d1e0099340e38e"
idpScope        = "email"
idpNameField    = "username"
newEndpoint = {"endpoint":{}}
newEndpoint["endpoint"]["service_id"] = serviceFB["service"]["id"]
newEndpoint["endpoint"]["publicurl"]=idpPublicURL
newEndpoint["endpoint"]["internalurl"]=idpInternalURL
newEndpoint["endpoint"]["adminurl"]=idpAdminURL
newEndpoint["endpoint"]["client_id"]=idpClientId
newEndpoint["endpoint"]["client_secret"]=idpClientSecret
newEndpoint["endpoint"]["redirect_uri"]=idpRedirectUri
newEndpoint["endpoint"]["scope"]=idpScope
newEndpoint["endpoint"]["name_field"]=idpNameField
endpointFB = keystoneRequest(endpointEndpoint, newEndpoint, "POST")

# Google OAuth

idpPublicURL    = "https://accounts.google.com/o/oauth2/auth"
idpInternalURL  = "https://accounts.google.com/o/oauth2/token"
idpAdminURL     = "https://www.googleapis.com/oauth2/v3/userinfo"
idpRedirectUri  = "https://localhost:8080/"
idpClientId     = "800550332219-rgimrn586j5cnrd5vvk31iovcom2gbb6.apps.googleusercontent.com"
idpClientSecret = "GUpzyfiMqH5u06Wz8OJ-ReX_"
idpScope        = "profile email"
idpNameField    = "sub"
newEndpoint = {"endpoint":{}}
newEndpoint["endpoint"]["service_id"] = serviceGOA["service"]["id"]
newEndpoint["endpoint"]["publicurl"]=idpPublicURL
newEndpoint["endpoint"]["internalurl"]=idpInternalURL
newEndpoint["endpoint"]["adminurl"]=idpAdminURL
newEndpoint["endpoint"]["client_id"]=idpClientId
newEndpoint["endpoint"]["client_secret"]=idpClientSecret
newEndpoint["endpoint"]["redirect_uri"]=idpRedirectUri
newEndpoint["endpoint"]["scope"]=idpScope
newEndpoint["endpoint"]["name_field"]=idpNameField
endpointGOA = keystoneRequest(endpointEndpoint, newEndpoint, "POST")

# Google OIDC (Igual, sem o name_field)

newEndpoint = {"endpoint":{}}
newEndpoint["endpoint"]["service_id"] = serviceGOIDC["service"]["id"]
newEndpoint["endpoint"]["publicurl"]=idpPublicURL
newEndpoint["endpoint"]["internalurl"]=idpInternalURL
newEndpoint["endpoint"]["adminurl"]=idpAdminURL
newEndpoint["endpoint"]["client_id"]=idpClientId
newEndpoint["endpoint"]["client_secret"]=idpClientSecret
newEndpoint["endpoint"]["redirect_uri"]=idpRedirectUri
newEndpoint["endpoint"]["scope"]=idpScope
endpointGOA = keystoneRequest(endpointEndpoint, newEndpoint, "POST")

print "OK"

#---------AddAttrFederacao--------------------------------------------------------------------
print "Adding Org Attributes"

orgattEndpoint = BASE_URL+":5000/v3/org_attributes"

# SAML

att = {"org_attribute":{}}
att["org_attribute"]["type"] = "brEduAffiliationType"
att["org_attribute"]["value"] = "student"
orgattStud = keystoneRequest(orgattEndpoint, att, "POST")

att = {"org_attribute":{}}
att["org_attribute"]["type"] = "eduPersonPrincipalName"
orgattName = keystoneRequest(orgattEndpoint, att, "POST")

att = {"org_attribute":{}}
att["org_attribute"]["type"] = "brEduAffiliationType"
att["org_attribute"]["value"] = "employee"
orgattEmp = keystoneRequest(orgattEndpoint, att, "POST")

# OAuth

att = {"org_attribute":{}}
att["org_attribute"]["type"] = "email"
orgattEmail = keystoneRequest(orgattEndpoint, att, "POST")

att = {"org_attribute":{}}
att["org_attribute"]["type"] = "email"
att["org_attribute"]["value"] = "ioram7@gmail.com"
orgattEMIoram = keystoneRequest(orgattEndpoint, att, "POST")

att = {"org_attribute":{}}
att["org_attribute"]["type"] = "email"
att["org_attribute"]["value"] = "iss@cin.ufpe.br"
orgattEMCIn = keystoneRequest(orgattEndpoint, att, "POST")

att = {"org_attribute":{}}
att["org_attribute"]["type"] = "email"
att["org_attribute"]["value"] = "iss@cesar.org.br"
orgattEMCESAR = keystoneRequest(orgattEndpoint, att, "POST")

att = {"org_attribute":{}}
att["org_attribute"]["type"] = "hd"
att["org_attribute"]["value"] = "cin.ufpe.br"
orgattHDCIn = keystoneRequest(orgattEndpoint, att, "POST")

att = {"org_attribute":{}}
att["org_attribute"]["type"] = "hd"
att["org_attribute"]["value"] = "cesar.org.br"
orgattHDCESAR = keystoneRequest(orgattEndpoint, att, "POST")

att = {"org_attribute":{}}
att["org_attribute"]["type"] = "verified"
att["org_attribute"]["value"] = "True"
orgattVerfd = keystoneRequest(orgattEndpoint, att, "POST")

att = {"org_attribute":{}}
att["org_attribute"]["type"] = "email_verified"
att["org_attribute"]["value"] = "True"
orgattEMVerfd = keystoneRequest(orgattEndpoint, att, "POST")

att = {"org_attribute":{}}
att["org_attribute"]["type"] = "username"
orgattUsername = keystoneRequest(orgattEndpoint, att, "POST")

att = {"org_attribute":{}}
att["org_attribute"]["type"] = "sub"
orgattSub = keystoneRequest(orgattEndpoint, att, "POST")

print "OK"
#--------Adding Authorised Issuers for Attributes--------------------------------------------------
print "Adding Authorised Issuers for Attributes"

#RNP

keystoneRequest(orgattEndpoint+"/"+orgattName["org_attribute"]["id"]+"/issuers/"+serviceRNP["service"]["id"], method="PUT")
keystoneRequest(orgattEndpoint+"/"+orgattStud["org_attribute"]["id"]+"/issuers/"+serviceRNP["service"]["id"], method="PUT")
keystoneRequest(orgattEndpoint+"/"+orgattEmp["org_attribute"]["id"]+"/issuers/"+serviceRNP["service"]["id"], method="PUT")

#FB

keystoneRequest(orgattEndpoint+"/"+orgattUsername["org_attribute"]["id"]+"/issuers/"+serviceFB["service"]["id"], method="PUT")
keystoneRequest(orgattEndpoint+"/"+orgattEmail["org_attribute"]["id"]+"/issuers/"+serviceFB["service"]["id"], method="PUT")
keystoneRequest(orgattEndpoint+"/"+orgattEMIoram["org_attribute"]["id"]+"/issuers/"+serviceFB["service"]["id"], method="PUT")
keystoneRequest(orgattEndpoint+"/"+orgattVerfd["org_attribute"]["id"]+"/issuers/"+serviceFB["service"]["id"], method="PUT")

#Google OAuth
keystoneRequest(orgattEndpoint+"/"+orgattSub["org_attribute"]["id"]+"/issuers/"+serviceGOA["service"]["id"], method="PUT")
keystoneRequest(orgattEndpoint+"/"+orgattEmail["org_attribute"]["id"]+"/issuers/"+serviceGOA["service"]["id"], method="PUT")
keystoneRequest(orgattEndpoint+"/"+orgattEMIoram["org_attribute"]["id"]+"/issuers/"+serviceGOA["service"]["id"], method="PUT")
keystoneRequest(orgattEndpoint+"/"+orgattEMCIn["org_attribute"]["id"]+"/issuers/"+serviceGOA["service"]["id"], method="PUT")
keystoneRequest(orgattEndpoint+"/"+orgattEMCESAR["org_attribute"]["id"]+"/issuers/"+serviceGOA["service"]["id"], method="PUT")
keystoneRequest(orgattEndpoint+"/"+orgattEMVerfd["org_attribute"]["id"]+"/issuers/"+serviceGOA["service"]["id"], method="PUT")
keystoneRequest(orgattEndpoint+"/"+orgattHDCIn["org_attribute"]["id"]+"/issuers/"+serviceGOA["service"]["id"], method="PUT")
keystoneRequest(orgattEndpoint+"/"+orgattHDCESAR["org_attribute"]["id"]+"/issuers/"+serviceGOA["service"]["id"], method="PUT")

#Google OIDC
keystoneRequest(orgattEndpoint+"/"+orgattSub["org_attribute"]["id"]+"/issuers/"+serviceGOIDC["service"]["id"], method="PUT")
keystoneRequest(orgattEndpoint+"/"+orgattEmail["org_attribute"]["id"]+"/issuers/"+serviceGOIDC["service"]["id"], method="PUT")
keystoneRequest(orgattEndpoint+"/"+orgattEMIoram["org_attribute"]["id"]+"/issuers/"+serviceGOIDC["service"]["id"], method="PUT")
keystoneRequest(orgattEndpoint+"/"+orgattEMCIn["org_attribute"]["id"]+"/issuers/"+serviceGOIDC["service"]["id"], method="PUT")
keystoneRequest(orgattEndpoint+"/"+orgattEMCESAR["org_attribute"]["id"]+"/issuers/"+serviceGOIDC["service"]["id"], method="PUT")
keystoneRequest(orgattEndpoint+"/"+orgattEMVerfd["org_attribute"]["id"]+"/issuers/"+serviceGOIDC["service"]["id"], method="PUT")
keystoneRequest(orgattEndpoint+"/"+orgattHDCIn["org_attribute"]["id"]+"/issuers/"+serviceGOIDC["service"]["id"], method="PUT")
keystoneRequest(orgattEndpoint+"/"+orgattHDCESAR["org_attribute"]["id"]+"/issuers/"+serviceGOIDC["service"]["id"], method="PUT")

print "OK"

#---------------------------------------------------------------------------------------------------------------------------------------------------

print "Adding roles"
roleEndPoint = BASE_URL+":5000/v3/roles"

newRole= {"role":{}}
newRole["role"]["name"] = "federated_admin"
roleAdmin = keystoneRequest(roleEndPoint, newRole, "POST")

newRole= {"role":{}}
newRole["role"]["name"] = "federated_member"
roleMember = keystoneRequest(roleEndPoint, newRole, "POST")

print "OK"

#------Adding Projects no Keystone-----------------------------------------------------------------------------------------------------------------------------
print "Adding Tenants"
projectEndPoint = BASE_URL+":5000/v3/projects"

# Shared

newProject= {"project":{}}
newProject["project"]["name"] = "Public"
newProject["project"]["description"] = "Public Shared Project"
tenantPublic = keystoneRequest(projectEndPoint, newProject, "POST")

# RNP/UFRN

newProject= {"project":{}}
newProject["project"]["name"] = "RNP Student"
newProject["project"]["description"] = "RNP Student's Project"
tenantRNPStud = keystoneRequest(projectEndPoint, newProject, "POST")

newProject= {"project":{}}
newProject["project"]["name"] = "RNP Employee"
newProject["project"]["description"] = "RNP Employee's Project"
tenantRNPEmp = keystoneRequest(projectEndPoint, newProject, "POST")

# CIn
newProject= {"project":{}}
newProject["project"]["name"] = "CIn/UFPE"
newProject["project"]["description"] = "CIn/UFPE Project"
tenantCIn = keystoneRequest(projectEndPoint, newProject, "POST")

# CESAR
newProject= {"project":{}}
newProject["project"]["name"] = "CESAR"
newProject["project"]["description"] = "CESAR Project"
tenantCESAR = keystoneRequest(projectEndPoint, newProject, "POST")

print "OK"

#-----------"Adding Org Sets"----------------------------------------------------------------------------
orgsetEndpoint = BASE_URL+":5000/v3/org_attribute_sets"

# RNP IDPUFRN  Sets

# Set 1 contains eduPersonPrincipalName=anything (orgattName) 
# Create the set
newOrgSet = {"org_attribute_set":{}}
newOrgSet["org_attribute_set"]["name"] = "RNP_Public"
OrgSetRNPPub = keystoneRequest(orgsetEndpoint, newOrgSet, "POST")
# Add the attributes
keystoneRequest(orgsetEndpoint+"/"+OrgSetRNPPub["org_attribute_set"]["id"]+"/attributes/"+orgattName["org_attribute"]["id"], method="PUT")

# Set 2 contains brEduAffiliationType=student (orgattStud) 
# Create the set
newOrgSet = {"org_attribute_set":{}}
newOrgSet["org_attribute_set"]["name"] = "RNP_Student"
OrgSetRNPStud = keystoneRequest(orgsetEndpoint, newOrgSet, "POST")
# Add the attributes
keystoneRequest(orgsetEndpoint+"/"+OrgSetRNPStud["org_attribute_set"]["id"]+"/attributes/"+orgattName["org_attribute"]["id"], method="PUT")
keystoneRequest(orgsetEndpoint+"/"+OrgSetRNPStud["org_attribute_set"]["id"]+"/attributes/"+orgattStud["org_attribute"]["id"], method="PUT")

# Set 3 contains brEduAffiliationType=employee (orgattEmp) 
# Create the set
newOrgSet = {"org_attribute_set":{}}
newOrgSet["org_attribute_set"]["name"] = "RNP_Employee"
OrgSetRNPEmp = keystoneRequest(orgsetEndpoint, newOrgSet, "POST")
# Add the attributes
keystoneRequest(orgsetEndpoint+"/"+OrgSetRNPEmp["org_attribute_set"]["id"]+"/attributes/"+orgattName["org_attribute"]["id"], method="PUT")
keystoneRequest(orgsetEndpoint+"/"+OrgSetRNPEmp["org_attribute_set"]["id"]+"/attributes/"+orgattEmp["org_attribute"]["id"], method="PUT")

# Facebook

# Set 4 contains email (Facebook Public) 
# Create the set
newOrgSet = {"org_attribute_set":{}}
newOrgSet["org_attribute_set"]["name"] = "Facebook_User"
OrgSetFBPub = keystoneRequest(orgsetEndpoint, newOrgSet, "POST")
# Add the attributes
keystoneRequest(orgsetEndpoint+"/"+OrgSetFBPub["org_attribute_set"]["id"]+"/attributes/"+orgattUsername["org_attribute"]["id"], method="PUT")
keystoneRequest(orgsetEndpoint+"/"+OrgSetFBPub["org_attribute_set"]["id"]+"/attributes/"+orgattEmail["org_attribute"]["id"], method="PUT")
keystoneRequest(orgsetEndpoint+"/"+OrgSetFBPub["org_attribute_set"]["id"]+"/attributes/"+orgattVerfd["org_attribute"]["id"], method="PUT")

# Set 5 contains email (Facebook Admin)
# Create the set
newOrgSet = {"org_attribute_set":{}}
newOrgSet["org_attribute_set"]["name"] = "Facebook_Admin"
OrgSetFBAdm = keystoneRequest(orgsetEndpoint, newOrgSet, "POST")
# Add the attributes
keystoneRequest(orgsetEndpoint+"/"+OrgSetFBAdm["org_attribute_set"]["id"]+"/attributes/"+orgattUsername["org_attribute"]["id"], method="PUT")
keystoneRequest(orgsetEndpoint+"/"+OrgSetFBAdm["org_attribute_set"]["id"]+"/attributes/"+orgattEMIoram["org_attribute"]["id"], method="PUT")
keystoneRequest(orgsetEndpoint+"/"+OrgSetFBAdm["org_attribute_set"]["id"]+"/attributes/"+orgattVerfd["org_attribute"]["id"], method="PUT")

# Google

# Set 6 contains email (Google Public) 
# Create the set
newOrgSet = {"org_attribute_set":{}}
newOrgSet["org_attribute_set"]["name"] = "Google_User"
OrgSetGooglePub = keystoneRequest(orgsetEndpoint, newOrgSet, "POST")
# Add the attributes
keystoneRequest(orgsetEndpoint+"/"+OrgSetGooglePub["org_attribute_set"]["id"]+"/attributes/"+orgattSub["org_attribute"]["id"], method="PUT")
keystoneRequest(orgsetEndpoint+"/"+OrgSetGooglePub["org_attribute_set"]["id"]+"/attributes/"+orgattEmail["org_attribute"]["id"], method="PUT")
keystoneRequest(orgsetEndpoint+"/"+OrgSetGooglePub["org_attribute_set"]["id"]+"/attributes/"+orgattEMVerfd["org_attribute"]["id"], method="PUT")

# Set 7 contains email (Google Admin)
# Create the set
newOrgSet = {"org_attribute_set":{}}
newOrgSet["org_attribute_set"]["name"] = "Google_Admin"
OrgSetGoogleAdm = keystoneRequest(orgsetEndpoint, newOrgSet, "POST")
# Add the attributes
keystoneRequest(orgsetEndpoint+"/"+OrgSetGoogleAdm["org_attribute_set"]["id"]+"/attributes/"+orgattSub["org_attribute"]["id"], method="PUT")
keystoneRequest(orgsetEndpoint+"/"+OrgSetGoogleAdm["org_attribute_set"]["id"]+"/attributes/"+orgattEMIoram["org_attribute"]["id"], method="PUT")
keystoneRequest(orgsetEndpoint+"/"+OrgSetGoogleAdm["org_attribute_set"]["id"]+"/attributes/"+orgattEMVerfd["org_attribute"]["id"], method="PUT")

# Set 8 contains email (CIn Public) 
# Create the set
newOrgSet = {"org_attribute_set":{}}
newOrgSet["org_attribute_set"]["name"] = "CIn_User"
OrgSetCInM = keystoneRequest(orgsetEndpoint, newOrgSet, "POST")
# Add the attributes
keystoneRequest(orgsetEndpoint+"/"+OrgSetCInM["org_attribute_set"]["id"]+"/attributes/"+orgattSub["org_attribute"]["id"], method="PUT")
keystoneRequest(orgsetEndpoint+"/"+OrgSetCInM["org_attribute_set"]["id"]+"/attributes/"+orgattEmail["org_attribute"]["id"], method="PUT")
keystoneRequest(orgsetEndpoint+"/"+OrgSetCInM["org_attribute_set"]["id"]+"/attributes/"+orgattEMVerfd["org_attribute"]["id"], method="PUT")
keystoneRequest(orgsetEndpoint+"/"+OrgSetCInM["org_attribute_set"]["id"]+"/attributes/"+orgattHDCIn["org_attribute"]["id"], method="PUT")

# Set 9 contains email (CIn Admin)
# Create the set
newOrgSet = {"org_attribute_set":{}}
newOrgSet["org_attribute_set"]["name"] = "CIn_Admin"
OrgSetCInAdm = keystoneRequest(orgsetEndpoint, newOrgSet, "POST")
# Add the attributes
keystoneRequest(orgsetEndpoint+"/"+OrgSetCInAdm["org_attribute_set"]["id"]+"/attributes/"+orgattSub["org_attribute"]["id"], method="PUT")
keystoneRequest(orgsetEndpoint+"/"+OrgSetCInAdm["org_attribute_set"]["id"]+"/attributes/"+orgattEMCIn["org_attribute"]["id"], method="PUT")
keystoneRequest(orgsetEndpoint+"/"+OrgSetCInAdm["org_attribute_set"]["id"]+"/attributes/"+orgattEMVerfd["org_attribute"]["id"], method="PUT")
keystoneRequest(orgsetEndpoint+"/"+OrgSetCInAdm["org_attribute_set"]["id"]+"/attributes/"+orgattHDCIn["org_attribute"]["id"], method="PUT")

# Set 10 contains email (CESAR Public) 
# Create the set
newOrgSet = {"org_attribute_set":{}}
newOrgSet["org_attribute_set"]["name"] = "Google_User"
OrgSetCESARM = keystoneRequest(orgsetEndpoint, newOrgSet, "POST")
# Add the attributes
keystoneRequest(orgsetEndpoint+"/"+OrgSetCESARM["org_attribute_set"]["id"]+"/attributes/"+orgattSub["org_attribute"]["id"], method="PUT")
keystoneRequest(orgsetEndpoint+"/"+OrgSetCESARM["org_attribute_set"]["id"]+"/attributes/"+orgattEmail["org_attribute"]["id"], method="PUT")
keystoneRequest(orgsetEndpoint+"/"+OrgSetCESARM["org_attribute_set"]["id"]+"/attributes/"+orgattEMVerfd["org_attribute"]["id"], method="PUT")
keystoneRequest(orgsetEndpoint+"/"+OrgSetCESARM["org_attribute_set"]["id"]+"/attributes/"+orgattHDCESAR["org_attribute"]["id"], method="PUT")

# Set 11 contains email (CESAR Admin)
# Create the set
newOrgSet = {"org_attribute_set":{}}
newOrgSet["org_attribute_set"]["name"] = "Google_Admin"
OrgSetCESARAdm = keystoneRequest(orgsetEndpoint, newOrgSet, "POST")
# Add the attributes
keystoneRequest(orgsetEndpoint+"/"+OrgSetCESARAdm["org_attribute_set"]["id"]+"/attributes/"+orgattSub["org_attribute"]["id"], method="PUT")
keystoneRequest(orgsetEndpoint+"/"+OrgSetCESARAdm["org_attribute_set"]["id"]+"/attributes/"+orgattEMCESAR["org_attribute"]["id"], method="PUT")
keystoneRequest(orgsetEndpoint+"/"+OrgSetCESARAdm["org_attribute_set"]["id"]+"/attributes/"+orgattEMVerfd["org_attribute"]["id"], method="PUT")
keystoneRequest(orgsetEndpoint+"/"+OrgSetCESARAdm["org_attribute_set"]["id"]+"/attributes/"+orgattHDCESAR["org_attribute"]["id"], method="PUT")

print "OK"

#-----------"Adding OS Sets"---------------------------------------------------------------
print "Adding Os Sets"
ossetEndpoint = BASE_URL+":5000/v3/os_attribute_sets"

# Public Member
newOsSet = {"os_attribute_set":{}}
newOsSet["os_attribute_set"]["name"] = "Public_Member"
osSetPubM = keystoneRequest(ossetEndpoint, newOsSet, "POST")
# Add the attributes
keystoneRequest(ossetEndpoint+"/"+osSetPubM["os_attribute_set"]["id"]+"/projects/"+tenantPublic["project"]["id"], method="PUT")
keystoneRequest(ossetEndpoint+"/"+osSetPubM["os_attribute_set"]["id"]+"/roles/"+roleMember["role"]["id"], method="PUT")

# Public Admin
newOsSet = {"os_attribute_set":{}}
newOsSet["os_attribute_set"]["name"] = "Public_Admin"
osSetPubA = keystoneRequest(ossetEndpoint, newOsSet, "POST")
# Add the attributes
keystoneRequest(ossetEndpoint+"/"+osSetPubA["os_attribute_set"]["id"]+"/projects/"+tenantPublic["project"]["id"], method="PUT")
keystoneRequest(ossetEndpoint+"/"+osSetPubA["os_attribute_set"]["id"]+"/roles/"+roleAdmin["role"]["id"], method="PUT")

# RNP Student (Admin)
newOsSet = {"os_attribute_set":{}}
newOsSet["os_attribute_set"]["name"] = "RNP_Student"
osSetRNPStud = keystoneRequest(ossetEndpoint, newOsSet, "POST")
# Add the attributes
keystoneRequest(ossetEndpoint+"/"+osSetRNPStud["os_attribute_set"]["id"]+"/projects/"+tenantRNPStud["project"]["id"], method="PUT")
keystoneRequest(ossetEndpoint+"/"+osSetRNPStud["os_attribute_set"]["id"]+"/roles/"+roleAdmin["role"]["id"], method="PUT")

# RNP Employee (Admin)
newOsSet = {"os_attribute_set":{}}
newOsSet["os_attribute_set"]["name"] = "RNP_Employee"
osSetRNPEmp = keystoneRequest(ossetEndpoint, newOsSet, "POST")
# Add the attributes
keystoneRequest(ossetEndpoint+"/"+osSetRNPEmp["os_attribute_set"]["id"]+"/projects/"+tenantRNPEmp["project"]["id"], method="PUT")
keystoneRequest(ossetEndpoint+"/"+osSetRNPEmp["os_attribute_set"]["id"]+"/roles/"+roleAdmin["role"]["id"], method="PUT")

# CIn Public
newOsSet = {"os_attribute_set":{}}
newOsSet["os_attribute_set"]["name"] = "CIn_Member"
osSetCInM = keystoneRequest(ossetEndpoint, newOsSet, "POST")
# Add the attributes
keystoneRequest(ossetEndpoint+"/"+osSetCInM["os_attribute_set"]["id"]+"/projects/"+tenantCIn["project"]["id"], method="PUT")
keystoneRequest(ossetEndpoint+"/"+osSetCInM["os_attribute_set"]["id"]+"/roles/"+roleMember["role"]["id"], method="PUT")

# CIn Admin
newOsSet = {"os_attribute_set":{}}
newOsSet["os_attribute_set"]["name"] = "CIn_Admin"
osSetCInA = keystoneRequest(ossetEndpoint, newOsSet, "POST")
# Add the attributes
keystoneRequest(ossetEndpoint+"/"+osSetCInA["os_attribute_set"]["id"]+"/projects/"+tenantCIn["project"]["id"], method="PUT")
keystoneRequest(ossetEndpoint+"/"+osSetCInA["os_attribute_set"]["id"]+"/roles/"+roleAdmin["role"]["id"], method="PUT")

# CESAR Public
newOsSet = {"os_attribute_set":{}}
newOsSet["os_attribute_set"]["name"] = "CESAR_Member"
osSetCESARM = keystoneRequest(ossetEndpoint, newOsSet, "POST")
# Add the attributes
keystoneRequest(ossetEndpoint+"/"+osSetCESARM["os_attribute_set"]["id"]+"/projects/"+tenantCESAR["project"]["id"], method="PUT")
keystoneRequest(ossetEndpoint+"/"+osSetCESARM["os_attribute_set"]["id"]+"/roles/"+roleMember["role"]["id"], method="PUT")

# CESAR Admin
newOsSet = {"os_attribute_set":{}}
newOsSet["os_attribute_set"]["name"] = "CESAR_Admin"
osSetCESARA = keystoneRequest(ossetEndpoint, newOsSet, "POST")
# Add the attributes
keystoneRequest(ossetEndpoint+"/"+osSetCESARA["os_attribute_set"]["id"]+"/projects/"+tenantCESAR["project"]["id"], method="PUT")
keystoneRequest(ossetEndpoint+"/"+osSetCESARA["os_attribute_set"]["id"]+"/roles/"+roleAdmin["role"]["id"], method="PUT")

print "OK"

#--------"Mapping"----------------------------------------------------------------------------------

print "Mapping Sets"

amEndpoint = BASE_URL+":5000/v3/attribute_set_mappings"
basicMap = {"attribute_set_mapping":{"org_attribute_set_id":"", "os_attribute_set_id":""}}

# RNP Public
newMap = basicMap.copy()
newMap["attribute_set_mapping"]["org_attribute_set_id"] = OrgSetRNPPub["org_attribute_set"]["id"]
newMap["attribute_set_mapping"]["os_attribute_set_id"] = osSetPubM["os_attribute_set"]["id"]
keystoneRequest(amEndpoint, newMap, "POST")

# RNP Student
newMap = basicMap.copy()
newMap["attribute_set_mapping"]["org_attribute_set_id"] = OrgSetRNPStud["org_attribute_set"]["id"]
newMap["attribute_set_mapping"]["os_attribute_set_id"] = osSetRNPStud["os_attribute_set"]["id"]
keystoneRequest(amEndpoint, newMap, "POST")

# RNP Employee
newMap = basicMap.copy()
newMap["attribute_set_mapping"]["org_attribute_set_id"] = OrgSetRNPEmp["org_attribute_set"]["id"]
newMap["attribute_set_mapping"]["os_attribute_set_id"] = osSetRNPEmp["os_attribute_set"]["id"]
keystoneRequest(amEndpoint, newMap, "POST")

# Facebook Public
newMap = basicMap.copy()
newMap["attribute_set_mapping"]["org_attribute_set_id"] = OrgSetFBPub["org_attribute_set"]["id"]
newMap["attribute_set_mapping"]["os_attribute_set_id"] = osSetPubM["os_attribute_set"]["id"]
keystoneRequest(amEndpoint, newMap, "POST")

# Facebook Admin
newMap = basicMap.copy()
newMap["attribute_set_mapping"]["org_attribute_set_id"] = OrgSetFBAdm["org_attribute_set"]["id"]
newMap["attribute_set_mapping"]["os_attribute_set_id"] = osSetPubA["os_attribute_set"]["id"]
keystoneRequest(amEndpoint, newMap, "POST")

# Google Public
newMap = basicMap.copy()
newMap["attribute_set_mapping"]["org_attribute_set_id"] = OrgSetGooglePub["org_attribute_set"]["id"]
newMap["attribute_set_mapping"]["os_attribute_set_id"] = osSetPubM["os_attribute_set"]["id"]
keystoneRequest(amEndpoint, newMap, "POST")

# Google Admin
newMap = basicMap.copy()
newMap["attribute_set_mapping"]["org_attribute_set_id"] = OrgSetGoogleAdm["org_attribute_set"]["id"]
newMap["attribute_set_mapping"]["os_attribute_set_id"] = osSetPubA["os_attribute_set"]["id"]
keystoneRequest(amEndpoint, newMap, "POST")

# CIn Member
newMap = basicMap.copy()
newMap["attribute_set_mapping"]["org_attribute_set_id"] = OrgSetCInM["org_attribute_set"]["id"]
newMap["attribute_set_mapping"]["os_attribute_set_id"] = osSetCInM["os_attribute_set"]["id"]
keystoneRequest(amEndpoint, newMap, "POST")

# CIn Admin
newMap = basicMap.copy()
newMap["attribute_set_mapping"]["org_attribute_set_id"] = OrgSetCInAdm["org_attribute_set"]["id"]
newMap["attribute_set_mapping"]["os_attribute_set_id"] = osSetCInA["os_attribute_set"]["id"]
keystoneRequest(amEndpoint, newMap, "POST")

# CESAR Public
newMap = basicMap.copy()
newMap["attribute_set_mapping"]["org_attribute_set_id"] = OrgSetCESARM["org_attribute_set"]["id"]
newMap["attribute_set_mapping"]["os_attribute_set_id"] = osSetCESARM["os_attribute_set"]["id"]
keystoneRequest(amEndpoint, newMap, "POST")

# CESAR Admin
newMap = basicMap.copy()
newMap["attribute_set_mapping"]["org_attribute_set_id"] = OrgSetCESARAdm["org_attribute_set"]["id"]
newMap["attribute_set_mapping"]["os_attribute_set_id"] = osSetCESARA["os_attribute_set"]["id"]
keystoneRequest(amEndpoint, newMap, "POST")

print "OK"
print "Success, all entities created, demo ready"

