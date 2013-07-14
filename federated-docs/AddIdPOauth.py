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

#----------AddEndpoints-----------------------------------------------------------------------
print "Adding Endpoints"
endpointEndpoint = BASE_URL+":35357/v2.0/endpoints"
serviceid = "7c3a3df54c9f42f4aa5a742f369fde01"
idppuburl = "https://graph.facebook.com/oauth/authorize"
idpinturl = "https://graph.facebook.com/oauth/access_token"
idpadmurl = "https://graph.facebook.com/"
redirecturi = "https://localhost:8080"
clientid = "600041930027373"
clientsec = "451567ba4bc0451b49d1e0099340e38e"
idservice = "me"

newEndpoint = {"endpoint":{}}
newEndpoint["endpoint"]["service_id"] = serviceid
newEndpoint["endpoint"]["publicurl"]=idppuburl
newEndpoint["endpoint"]["internalurl"]=idpinturl
newEndpoint["endpoint"]["adminurl"]=idpadmurl
newEndpoint["endpoint"]["redirect_uri"]=redirecturi
newEndpoint["endpoint"]["client_id"]=clientid
newEndpoint["endpoint"]["client_secret"]=clientsec
newEndpoint["endpoint"]["id_service"]=idservice

endpoint = keystoneRequest(endpointEndpoint, newEndpoint, "POST")

print "OK"
