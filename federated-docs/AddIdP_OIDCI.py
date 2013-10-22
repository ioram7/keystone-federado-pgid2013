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

newService = {"service":{"name":"Google (OIDCI)", "description": "IdP Google OIDC implicit service", "type":"idp.oidci"}} #idpNormal
serviceGOIDCI = keystoneRequest(serviceEndpoint, newService, "POST")

print "OK"

#----------AddEndpoints-----------------------------------------------------------------------
print "Adding Endpoints"

endpointEndpoint = BASE_URL+":35357/v2.0/endpoints"

# Google OIDCI

idpPublicURL    = "https://accounts.google.com/o/oauth2/auth"
idpInternalURL  = "https://accounts.google.com/o/oauth2/token"
idpAdminURL     = "https://www.googleapis.com/oauth2/v3/userinfo"
idpRedirectUri  = "https://localhost:8080/"
idpClientId     = "800550332219-rgimrn586j5cnrd5vvk31iovcom2gbb6.apps.googleusercontent.com"
idpClientSecret = "GUpzyfiMqH5u06Wz8OJ-ReX_"
idpScope        = "profile email"
idpNameField    = "sub"
newEndpoint = {"endpoint":{}}
newEndpoint["endpoint"]["service_id"] = serviceGOIDCI["service"]["id"]
newEndpoint["endpoint"]["publicurl"]=idpPublicURL
newEndpoint["endpoint"]["internalurl"]=idpInternalURL
newEndpoint["endpoint"]["adminurl"]=idpAdminURL
newEndpoint["endpoint"]["client_id"]=idpClientId
newEndpoint["endpoint"]["client_secret"]=idpClientSecret
newEndpoint["endpoint"]["redirect_uri"]=idpRedirectUri
newEndpoint["endpoint"]["scope"]=idpScope
endpointGOIDCI = keystoneRequest(endpointEndpoint, newEndpoint, "POST")

print "OK"

#--------Adding Authorised Issuers for Attributes--------------------------------------------------
print "Adding Authorised Issuers for Attributes"

orgattEndpoint = BASE_URL+":5000/v3/org_attributes"

#Google OIDCI
keystoneRequest(orgattEndpoint+"/fc22cc8fa4984d65878b5a1f4622cd5d/issuers/"+serviceGOIDCI["service"]["id"], method="PUT")
keystoneRequest(orgattEndpoint+"/780a45e46cc44fd286d67a19f10c997b/issuers/"+serviceGOIDCI["service"]["id"], method="PUT")
keystoneRequest(orgattEndpoint+"/0497c7b597f048818f8bd7a7bac6bded/issuers/"+serviceGOIDCI["service"]["id"], method="PUT")
keystoneRequest(orgattEndpoint+"/93d48f156f0c450988a99c309d1cbd67/issuers/"+serviceGOIDCI["service"]["id"], method="PUT")
keystoneRequest(orgattEndpoint+"/3ccb510149e4466c85fd33f30d597910/issuers/"+serviceGOIDCI["service"]["id"], method="PUT")
keystoneRequest(orgattEndpoint+"/213cabfcbdc8419a9b2d061c199a1f55/issuers/"+serviceGOIDCI["service"]["id"], method="PUT")
keystoneRequest(orgattEndpoint+"/7852e31d1d504e17b14cb2d5b2b41194/issuers/"+serviceGOIDCI["service"]["id"], method="PUT")
keystoneRequest(orgattEndpoint+"/e00c95ab578b47e694aaed94bf9c318a/issuers/"+serviceGOIDCI["service"]["id"], method="PUT")

print "OK"

print "Success, all entities created, demo ready"

