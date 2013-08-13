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

newService = {"service":{"name":"RNP CAFe Expresso", "description": "IdP CAFeExp SAML service", "type":"idp.saml"}} #idpNormal
serviceCAFe = keystoneRequest(serviceEndpoint, newService, "POST")

print "OK"

#----------AddEndpoints-----------------------------------------------------------------------
print "Adding Endpoints"

endpointEndpoint = BASE_URL+":35357/v2.0/endpoints"

# RNP CAFe

idpServiceURL  = "https://idp2.cafeexpresso.rnp.br/idp/profile/SAML2/POST/SSO"
#idpServiceURL = "https://idp.ect.ufrn.br/simplesaml/saml2/idp/SSOService.php" #LocationidpectNormal
idpcertdata = "MIIEODCCAyACAQAwDQYJKoZIhvcNAQEFBQAwgeExSDBGBgNVBAoTP0dJZCBMYWIgLSBMYWJvcmF0b3JpbyBkZSBFeHBlcmltZW50YWNhbyBlbSBHZXN0YW8gZGUgSWRlbnRpZGFkZTEWMBQGA1UECxMNQ0FGZSBFeHByZXNzbzEcMBoGCSqGSIb3DQEJARYNZ2lkbGFiQHJucC5icjEWMBQGA1UEBxMNRmxvcmlhbm9wb2xpczEXMBUGA1UECBMOU2FudGEgQ2F0YXJpbmExCzAJBgNVBAYTAkJSMSEwHwYDVQQDExhpZHAyLmNhZmVleHByZXNzby5ybnAuYnIwHhcNMTMwNTA0MTcwNDEyWhcNMTYwNTAzMTcwNDEyWjCB4TFIMEYGA1UEChM/R0lkIExhYiAtIExhYm9yYXRvcmlvIGRlIEV4cGVyaW1lbnRhY2FvIGVtIEdlc3RhbyBkZSBJZGVudGlkYWRlMRYwFAYDVQQLEw1DQUZlIEV4cHJlc3NvMRwwGgYJKoZIhvcNAQkBFg1naWRsYWJAcm5wLmJyMRYwFAYDVQQHEw1GbG9yaWFub3BvbGlzMRcwFQYDVQQIEw5TYW50YSBDYXRhcmluYTELMAkGA1UEBhMCQlIxITAfBgNVBAMTGGlkcDIuY2FmZWV4cHJlc3NvLnJucC5icjCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBANr2hiGJtelflzHbdtDzrCGXjME/i6xhU7ic9+NLidSruefqQfqgAhPa16YQx0N3mS87m3rgCl+2irfRtwKSm/GIE/TklNXbJMm97QgclsZMQVXrNmyR0K72JYmasK/uwmELQc3UH5jQGIOsnYG8B5vqWug06FRnU0jQ/N+UFoA3Tkh+Iq6pzFt/H1Js8j9XErtK4DvGCN0e3cFDzgtRwqnAPrv3e/vFNjcugFeNsWD97iq+A6lpzASEYiH9WixRBKoWv9pLNgbKUo+mTySS8k/Pp6bdszGewxoEKYYGrfiybw72RmVq4PaoTH7EXwbZibj+RKuQamNOKpgcg3lYRvkCAwEAATANBgkqhkiG9w0BAQUFAAOCAQEABQoWJRy6Vb7eCFfUmH6jYxA96glqMb7GRUqlnW4k5/jbLmCTHaL2anYEYUt0vmiAvvRmjajypjkQIpvDdbX3QIwAGUhnxogiDHA62lDDo0QloQ0GSFaCOzSBCz6zKdoUVH6TO5DAnzaj0dvu0zYD9G3xjifKujX7kI3T622ndizBNtQK0j8XoZLa2XtFf9hrFT8tnIGUY45r/dnxcWjHJtlPMBWSDdkJxNyqr0fYYbFdWxB71aF7L8hqPYdP6A3gQcwW3cDTQxgsUMykOmZ2JtwgedP9i7Rrp81NTyTHDA6PYlkKG//ZqM2IhEzNtz9dNWdQCR/jdczMmXmy5psCww=="
#idpcertdata = "MIID/zCCAuegAwIBAgIJAPFeoZxEJcWqMA0GCSqGSIb3DQEBBQUAMIGVMQswCQYDVQQGEwJicjEcMBoGA1UECAwTcmlvIGdyYW5kZSBkbyBub3J0ZTEOMAwGA1UEBwwFbmF0YWwxDTALBgNVBAoMBHVmcm4xDDAKBgNVBAsMA2VjdDEYMBYGA1UEAwwPaWRwLmVjdC51ZnJuLmJyMSEwHwYJKoZIhvcNAQkBFhJrYWR1YXJkb0BnbWFpbC5jb20wHhcNMTMwNDE2MTgzODMxWhcNMjMwNDE2MTgzODMxWjCBlTELMAkGA1UEBhMCYnIxHDAaBgNVBAgME3JpbyBncmFuZGUgZG8gbm9ydGUxDjAMBgNVBAcMBW5hdGFsMQ0wCwYDVQQKDAR1ZnJuMQwwCgYDVQQLDANlY3QxGDAWBgNVBAMMD2lkcC5lY3QudWZybi5icjEhMB8GCSqGSIb3DQEJARYSa2FkdWFyZG9AZ21haWwuY29tMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAycVQRB2UhMYfww0B470pkZBD0cFweDjuic6zpwCzbQW8vFGGYeGzbAb61p2UPRXg5zf4CfHuFCREr2Iz4944PTFErmyWtjoFBgLqkODtAkLqhDLm7xipTaFyR10lDzW5WLwbF4nh6Fl7iN4uyiN1kVCoIVNtyktc8iU1GOdeapA66Il+slevcDrIarc2W5UpYFsuzJoqMFFguOHdaIaxmFnvbPDWjlFBdbgKsJkfoo/yWxeAmNy1+FAWOLcO3yoRGVT99y2PUiI5Z29x8aUYeyhtc+21rDNUAPSU0/pxve/uahthmXEs8tpgnsauoy2SR8Z1YKbR2jG+/o3lN0SjVwIDAQABo1AwTjAdBgNVHQ4EFgQU2TAOD/zFN9B4gMfLUF6iX/BoZiQwHwYDVR0jBBgwFoAU2TAOD/zFN9B4gMfLUF6iX/BoZiQwDAYDVR0TBAUwAwEB/zANBgkqhkiG9w0BAQUFAAOCAQEAwBM84R1Ur9g//Aey/5op1I7C6Hncq9cvAEvbnl4xT7P3jubaDGK770FV8YyltfpiBytGsMjbiSlOBQVBbMPlt+xUJwMEu+amirPPcv9Ww72cnV1A0EWiIOHvzQmbhzn3wgbMsW1XAXfZBCEg3IT80KcC+FLDHaodI35zVOcWBuq54HumE+MReyWmoL7tcCI+NDtBSDiAdncyZX3VhUz4WPYLOEfqZNK0VWzrckJ+9u1xU/VkzIjqX/FBHqUXRhQH6IDInHT46XBDWRw9V/r2oc5rZ8Iz1a7e0HTmqpddSyDg1o2VkuBIb7Z0O8cr6cZ2kwr+NdyJPV1WvQ85kbSjXA=="
newEndpoint = {"endpoint":{}}
newEndpoint["endpoint"]["service_id"] = serviceCAFe["service"]["id"]
newEndpoint["endpoint"]["publicurl"]=idpServiceURL
newEndpoint["endpoint"]["internalurl"]=idpServiceURL 
newEndpoint["endpoint"]["adminurl"]=idpServiceURL
newEndpoint["endpoint"]["certdata"]=idpcertdata
endpointCAFe = keystoneRequest(endpointEndpoint, newEndpoint, "POST")

