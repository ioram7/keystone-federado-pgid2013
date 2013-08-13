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

#print "Adding Identity Providers"
serviceEndpoint = BASE_URL+":5000/v3/services"

#---------AddAttrFederacao--------------------------------------------------------------------
#print "Adding Org Attributes"

orgattEndpoint = BASE_URL+":5000/v3/org_attributes"

#att = {"org_attribute":{}}
#att["org_attribute"]["type"] = "email"
#att["org_attribute"]["value"] = "marina@gidlab.br"
#orgattEMIoram = keystoneRequest(orgattEndpoint, att, "POST")

#print "OK"

#-----------"Adding Org Sets"----------------------------------------------------------------------------
orgsetEndpoint = BASE_URL+":5000/v3/org_attribute_sets"

# RNP IDPUFRN  Sets

# Set 1 contains eduPersonPrincipalName=anything (orgattName) 
# Create the set
newOrgSet = {"org_attribute_set":{}}
newOrgSet["org_attribute_set"]["name"] = "RNP_Public_OIDC"
OrgSetRNPPub = keystoneRequest(orgsetEndpoint, newOrgSet, "POST")

print "OK"

print "Success, all entities created, demo ready"

