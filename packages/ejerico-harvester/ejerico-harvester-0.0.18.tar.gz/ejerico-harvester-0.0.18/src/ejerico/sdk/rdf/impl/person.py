"""TODO doc"""

import sys
import logging 

from functools  import reduce 

from rdflib import plugin
from rdflib import Graph, Literal, URIRef
from rdflib import RDF, FOAF, XSD, SDO
from rdflib.store import Store, VALID_STORE

from ejerico.sdk.utils import format_email
from ejerico.sdk.utils import ORCIDResolver

class PersonImpl(object):

    def __init__(self):
        object.__init__(self)
        self.address = None
        self.affiliation = None
        self.email = None
        self.familyName = None
        self.givenName = None
        self.name = None
        self.nationality = None
        self.phone = None
        self.qualification = None
        self.url = None
    
    def prepare(self):
        logging.debug("[Person::prepare] entering method")

        if self.email is not None:
            self.email = format_email(self.email)
            for e in [self.email, "mailto:{}" if "mailto:" not in self.email else self.email]:
                if e not in self.alias: self.alias.append(e)
        
        if self.familyName and self.givenName:
            self.name = self.name if self.name is not None else "{} {}".format(self.familyName, self.givenName)
            self.familyName = self.givenName = None

        if self.name is not None:
            self.name = self.name.strip() 
            self.name = None if '' == self.name else self.name 

        is_orcidID =  reduce(lambda x,y: x or "edmo.seadatanet.org" in y, self.alias, False)
        if not is_orcidID and self.name:
            orcidID = ORCIDResolver.instance().resolve(self.email) if self.email is not None else None
            orcidID = orcidID or ORCIDResolver.instance().resolve(self.name) if self.name is not None else None
            orcidID = orcidID or ORCIDResolver.instance().resolve({"family-name": self.familyName, "given-names": self.givenName}) 
            if orcidID is not None:
                logging.warning("[PersonImpl] found orcid")