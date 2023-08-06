from audioop import add
import algosdk
from anssdk.name import Name
from anssdk.address import Address
from anssdk.helper.validation import is_valid_name, is_valid_address

class ANS:
    def __init__(self, client, indexer=None):
        if(indexer):
            self.indexer=indexer
        self.client=client
    
    def name(self, name):
        name = name.split('.algo')[0]
        if(is_valid_name(name)):
            return Name(name, self.client)

    def address(self, address):
        if(self.indexer is None):
            raise Exception('Algod indexer must be set up')
        
        if(is_valid_address(address)):
            return Address(address, self.client, self.indexer)
        
        raise Exception('Address {address} is invalid'.format(address = address))
        
    
