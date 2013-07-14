'''
 * Copyright (c) 2011, University of Kent
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * Redistributions of source code must retain the above copyright notice, this
 * list of conditions and the following disclaimer.
 *
 * Redistributions in binary form must reproduce the above copyright notice,
 * this list of conditions and the following disclaimer in the documentation
 * and/or other materials provided with the distribution.
 *
 * 1. Neither the name of the University of Kent nor the names of its
 * contributors may be used to endorse or promote products derived from this
 * software without specific prior written permission.
 *
 * 2. THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
 * IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
 * THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 * PURPOSE ARE DISCLAIMED.
 *
 * 3. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 *
 * 4. YOU AGREE THAT THE EXCLUSIONS IN PARAGRAPHS 2 AND 3 ABOVE ARE REASONABLE
 * IN THE CIRCUMSTANCES.  IN PARTICULAR, YOU ACKNOWLEDGE (1) THAT THIS
 * SOFTWARE HAS BEEN MADE AVAILABLE TO YOU FREE OF CHARGE, (2) THAT THIS
 * SOFTWARE IS NOT "PRODUCT" QUALITY, BUT HAS BEEN PRODUCED BY A RESEARCH
 * GROUP WHO DESIRE TO MAKE THIS SOFTWARE FREELY AVAILABLE TO PEOPLE WHO WISH
 * TO USE IT, AND (3) THAT BECAUSE THIS SOFTWARE IS NOT OF "PRODUCT" QUALITY
 * IT IS INEVITABLE THAT THERE WILL BE BUGS AND ERRORS, AND POSSIBLY MORE
 * SERIOUS FAULTS, IN THIS SOFTWARE.
 *
 * 5. This license is governed, except to the extent that local laws
 * necessarily apply, by the laws of England and Wales.
'''


'''
Created on 1 Feb 2013

@author: Kristy Siu
'''

import logging
import urlparse
import sys
import uuid
from keystone import exception
sys.path.insert(0, '../')
from os.path import dirname, basename
from time import localtime, strftime, gmtime
import urllib
import webbrowser
import urllib2
import json
import webob.dec
import webob.exc

from rauth.service import OAuth2Service
import re
from datetime import timedelta, datetime
import string
import random
import base64

from keystone.contrib import mapping
from keystone import catalog
LOG = logging.getLogger(__name__)

global oauthSrv
global redirecturi
global state
global endpoint_int
global clientid

class RequestIssuingService(object):
    def __init__(self):
	self.tmpl_req = ""

    # ris.getIdPRequest(CONF.federated.requestSigningKey, CONF.federated.SPName, endpoint)
    def getIdPRequest(self, key, issuer, endpoints):
	global oauthSrv
	global redirecturi
	global state
	global endpoint_int
	global clientid

        endpoint_pub = None
        endpoint_int = None
        endpoint_adm = None
        if not len(endpoints) < 1:
            for e in endpoints:
                if e['interface'] == 'public':
                    endpoint_pub = e['url']
                elif e['interface'] == 'internal':
                    endpoint_int = e['url']
                elif e['interface'] == 'admin':
                    endpoint_adm = e['url']
        else:
            LOG.error('No endpoint found for this service')

	edpid = endpoints[0].get("id",None)
	clientid = endpoints[0].get("client_id",None)
	clientsec = endpoints[0].get("client_secret",None)
	scope = endpoints[0].get("scope",None)

        #OIDC: Append openid scope, if not included on the scope list
        if scope.find("openid") == -1:
            if scope == "" :
                scope = "openid"
            else :
                scope = "openid " + scope

	ruritmp = endpoints[0].get("redirect_uri",None)
	if len(ruritmp) > 1 and ruritmp[-1] == '/' :
		redirecturi = ruritmp
	else :
		redirecturi = ruritmp + "/"

	oauthSrv = OAuth2Service(
	    client_id=clientid,
	    client_secret=clientsec,
	    name=edpid,
	    authorize_url=endpoint_pub,
	    access_token_url=endpoint_int,
	    base_url=endpoint_adm)

	state = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(12))
#	print state

	params = {'scope': scope,
          'response_type': 'code',
          'state' : state,
          'redirect_uri': redirecturi }

	authorize_url = oauthSrv.get_authorize_url(**params)
	spl = authorize_url.partition('?')
	
        resp = {}
        resp['idpRequest'] = '?'+spl[2]
        resp['idpEndpoint'] = spl[0]

#	print ("resp: ", resp)

        return valid_Response(resp)

    def __call__(self):
        return None


class Negotiator(object):

    def __init__(self):
        """ do nothing """
        raise exception.NotImplemented()

    def negotiate(self, data):
        """ do nothing """
        raise exception.NotImplemented()
    

class CredentialValidator(object):
    def __init__(self):
        self.org_mapping_api = mapping.controllers.OrgMappingController()
        self.mapping_api = mapping.controllers.AttributeMappingController()
        self.catalog_api = catalog.controllers.EndpointV3()
    
    def __call__(self):
        return None

    # cred_validator.validate(data['idpResponse'], service['id'])    
    def validate(self, data, realm_id):
        context = {}
        context['is_admin'] = True
        context['query_string'] = {}
        context['query_string']['service_id'] = realm_id
        context['interface'] = 'adminurl'
        context['path'] = ""

	# Default resp values
	name      = "sub"
	expire    = "" 
	issuers   = {}

	# exit if state don't match (no attributes will be returned)
	if state != data["state"] :
		print "State doesn't match."
	        return name, expire, issuers 

	if oauthSrv is None or redirecturi is None :
		print "No oauthSrv or no redirecturi"
	        return name, expire, issuers 

	prms = {
		'code': data["code"],
		'grant_type': 'authorization_code',
		'redirect_uri': redirecturi,
	}
#	print prms

	at_resp = oauthSrv.get_raw_access_token(data=prms)
	rsp = at_resp.content
#	print rsp
	try :
		rsp2 = json.loads(rsp)

		access_token = rsp2['access_token']
#		print access_token
		idtoken = rsp2['id_token']
#		print idtoken
		tt = rsp2['token_type']
#		print tt

	except :
                print "Invalid OpenID Connect access token."
                return name, expire, issuers

	# Validate Token Type

	if tt != 'Bearer' :
                print "Invalid OpenID Connect token type format: "+tt
                return name, expire, issuers

	# Validate ID Token
		
	idts = idtoken.split('.')[1]
#	print idts

	# Base64 Padding
	npad = 4 - (len(idts) % 4)
	pad = ""
	for i in range(0, npad) :
		pad = pad + "="

	azp = ""
	# Base64 Decode	
	try :
		dec_idtoken = base64.b64decode(idts+pad)
		idtoken = json.loads(dec_idtoken)
#		print idtoken

		iss = idtoken['iss']
		exp = idtoken['exp']
		sub = idtoken['sub']
		aud = idtoken['aud']

		if idtoken.get('azp') :
			azp = idtoken['azp']

		#print "iss:"+ idtoken['iss']
		#print "sub:"+ idtoken['sub']
		#print "aud:"+ idtoken['aud']
		#print "exp:"+ idtoken['exp']
		#print "iat:"+ idtoken['iat']

	except :
		print "OpenID Connect id token decoding error."
                return name, expire, issuers
		
	# Format expiration date

	exp = int(exp)
	exp = datetime.fromtimestamp(exp)
	exp = str(exp)
	exps = exp.partition(' ')
	time = exps[2].partition('.')
	expire = exps[0]+'T'+time[0]+'z'
#	print expire

	# Validate Issuer
	if endpoint_int.find(iss) == -1:
                print "Invalid OpenID Connect issuer: "+iss
                return name, expire, issuers

	# Validate Client_ID
	if aud != clientid:
                print "Invalid OpenID Connect audience: "+aud
                return name, expire, issuers

	# Validate AuthoriZed Party
	if azp != "" and azp != clientid:
                print "Invalid OpenID Connect authorized party: "+azp
                return name, expire, issuers

	# Get User Info

	idservice = "userinfo"
	session   = oauthSrv.get_session(access_token)
	resp      = session.get(idservice).json()
#	print resp

	atts      = {}
	for att, value in resp.iteritems():
		if isinstance(value, list):
			try :
				atts[att] += value
			except :
				atts[att] = value

		elif isinstance(value, unicode) :
			try : 
				atts[att].append(value)
			except :
				atts[att] = [value]
		else :
			v = unicode(value)
			try : 
				atts[att].append(v)
			except :
				atts[att] = [v]
#	print atts

	# Validate sub

#	print sub, atts['sub'][0]	
	if sub != atts['sub'][0] :
                print "OpenID Connect user mismatch: "+sub+", "+atts['sub'][0]
                return name, expire, issuers

	# Check valid attributes (registered on mysql tables)

	issuers = self.check_issuers(data, atts, realm_id)

#	print "name   : ",name
#	print "expire : ",expire
#	print "issuers: ",issuers

        return name, expire, issuers 

    def check_issuers(self, data, atts, realm_id):
        context = {"is_admin": True}
        valid_atts = {}
	i = 1
        for att in atts:
           for val in atts[att]:
               org_atts = self.org_mapping_api.list_org_attributes(context)['org_attributes']
               for org_att in org_atts:
                   if org_att['type'] == att:
                       if org_att['value'] == val or org_att['value'] is None:
                           try:
                               self.org_mapping_api.check_attribute_can_be_issued(context, service_id=realm_id, org_attribute_id=org_att['id'])
                               try:
                                   valid_atts[att].append(val)
                               except:
                                   valid_atts[att] = [val]
                           except exception.NotFound:
                               pass
        return valid_atts

def valid_Response(response):
    resp = webob.Response(content_type='application/json')
    resp.body = json.dumps(response)
    return resp
        
