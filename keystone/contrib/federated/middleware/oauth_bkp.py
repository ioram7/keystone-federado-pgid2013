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
#from datetime import timedelta, datetime

from keystone.contrib import mapping
from keystone import catalog
LOG = logging.getLogger(__name__)

global oauthSrv
global redirecturi
global idservice

class RequestIssuingService(object):
    def __init__(self):
	self.tmpl_req = ""

    # ris.getIdPRequest(CONF.federated.requestSigningKey, CONF.federated.SPName, endpoint)
    def getIdPRequest(self, key, issuer, endpoints):
	global oauthSrv
	global redirecturi
	global idservice

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
        idservice = endpoints[0].get("id_service",None)
	scope = endpoints[0].get("scope",None)

	ruritmp = endpoints[0].get("redirect_uri",None)
	if len(ruritmp) > 1 and ruritmp[-1] == '/' :
		redirecturi = ruritmp
	else :
		redirecturi = ruritmp + "/"

#	print ("edp:  ", edpid)
#	print ("clid: ", clientid)
#	print ("clsc: ", clientsec)
#	print ("rusi: ", redirecturi)

	oauthSrv = OAuth2Service(
	    client_id=clientid,
	    client_secret=clientsec,
	    name=edpid,
	    authorize_url=endpoint_pub,
	    access_token_url=endpoint_int,
	    base_url=endpoint_adm)

#	print ("oath: ", oauthSrv)

	params = {'scope': scope,
          'response_type': 'code', # always code here
          'state' : 'abcdefgh', # Random string
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

	#Ioram
#	print (data)
#	print (realm_id)

#       print ("oath: ", oauthSrv)
#       print ("ruri: ", redirecturi)
#	print ("code: ", data["code"])

	name = "error"
	#hardcoded - MUDAR
	expire = "2014-06-01T00:00:00z" 
	resp = {}
	issuers = {}
	atts = {}

	if oauthSrv is None or redirecturi is None or idservice is None:
		print "No oauthSrv or no redirecturi or no idservice"
	else :
		print "Aqui"
#		prms = {
#		    'code': data["code"],
#		    'grant_type': 'authorization_code',
#		    'redirect_uri': redirecturi,
#		}
#		print prms

#		at_resp = oauthSrv.get_raw_access_token(data=prms)
#		rsp = at_resp.content
#		print rsp

		#access_token=CAAIhvCYW8W0BAJ75zTWxXYZCZAjZBlHHK0MJQQoV9s4ZC9vb8rbRjvP9PZCyXMZBdWbGzt4qNcPVKChJZAexFLrjFwhG1r2grj01lzsbnUSvZCMVQwhKZA0eIpvTwa075Q6Pb2v5ZAgS7ffhAeFsEygTnJcWH5CsPNp44ZD&expires=5157384

#		access_token = ''
#		exp = ''

#		now = datetime.now()
#		print now

#		for r in rsp.split('&') :
#			part = r.partition('=')
#			if part[0] == 'access_token' :
#				access_token = part[2]
#			elif (part[0] == 'expire') or (part[0] == 'expires_in') :
#				exp = part[2]
#				expi = int(part[2])
#				exp = now + timedelta(0,expi,0)
#			print part[0] + " : " + part[2]

	        session = oauthSrv.get_auth_session(data = {'code': data["code"], 'redirect_uri': redirecturi})
#		session = oauthSrv.get_session(access_token)
		resp = session.get(idservice).json()
		print resp
		#hardcoded - MUDAR
		name = resp['username']

	        for att, value in resp.iteritems():
#			print att, value
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
#		print atts

	print "name   : ",name
	print "expire : ",expire

		issuers = self.check_issuers(data, atts, realm_id)

	print "issuers: ",issuers

#######
#name   :  _3409b1498beb31e0194afe984c61fda80de968c6e7
#expires:  2013-07-08T03:22:36Z
#issuers:  {'eduPersonPrincipalName': ['studentstudent@idp.ect.ufrn.br'], 'brEduAffiliationType': ['student']}	
#######

        return name, expire, issuers 

    def check_issuers(self, data, atts, realm_id):
#	print ("check_issuers")
        context = {"is_admin": True}
        valid_atts = {}
	i = 1
        for att in atts:
#	   print("Att: "+att)
           for val in atts[att]:
#	       uv = unicode(val)
#	       print("Val: "+uv)
               org_atts = self.org_mapping_api.list_org_attributes(context)['org_attributes']
               for org_att in org_atts:
#		   print ("OrgType: "+org_att['type'])
#		   if org_att['value'] is not None : 
#			   print ("OrgVal : "+org_att['value'])
#		   else :
#			   print ("OrgVal : None")
                   if org_att['type'] == att:
#		       print("OrgType == att")
                       if org_att['value'] == val or org_att['value'] is None:
#			   print("OrgVal == val, or none")
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
        
