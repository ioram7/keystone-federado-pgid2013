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

newService = {"service":{"name":"GID Lab OIDC", "description": "RNP GidLAB OIDC", "type":"idp.oidc"}} #idpNormal
serviceROIDC = keystoneRequest(serviceEndpoint, newService, "POST")

print "OK"

#----------AddEndpoints-----------------------------------------------------------------------
print "Adding Endpoints"

endpointEndpoint = BASE_URL+":35357/v2.0/endpoints"

# RNP OIDC

idpPublicURL    = "http://openid-provider.gidlab.rnp.br:8080/openid-connect-server/"
# idpPublicURL    = "https://accounts.google.com/o/oauth2/auth"
idpInternalURL  = "http://openid-provider.gidlab.rnp.br:8080/openid-connect-server/"
#idpInternalURL  = "https://accounts.google.com/o/oauth2/token"
idpAdminURL     = "http://openid-provider.gidlab.rnp.br:8080/openid-connect-server/"
#idpAdminURL     = "https://www.googleapis.com/oauth2/v3/userinfo"
idpRedirectUri  = "https://localhost:8080/"
idpClientId     = "subject-12345"
idpClientSecret = ""
idpScope        = ""
idpNameField    = "sub"

newEndpoint = {"endpoint":{}}
newEndpoint["endpoint"]["service_id"] = serviceROIDC["service"]["id"]
newEndpoint["endpoint"]["publicurl"]=idpPublicURL
newEndpoint["endpoint"]["internalurl"]=idpInternalURL
newEndpoint["endpoint"]["adminurl"]=idpAdminURL
newEndpoint["endpoint"]["client_id"]=idpClientId
newEndpoint["endpoint"]["client_secret"]=idpClientSecret
newEndpoint["endpoint"]["redirect_uri"]=idpRedirectUri
newEndpoint["endpoint"]["scope"]=idpScope
endpointROIDC = keystoneRequest(endpointEndpoint, newEndpoint, "POST")

