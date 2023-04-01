import requests
from fcmServer import FCMserver
import json
from enum import Enum


TIMEOUT = 30
class Status(str, Enum):
    CHECKING = 'checking'
    PENDDING = 'pending'
    CHECKED = 'checked'
    TIMEOUT = 'timedout'

class Examiner():
    def __init__(self) -> None:
        self.svr = FCMserver()
        self.pendingCustomers = {}
        # self.timer = 0

    def make_request(self, customer: dict):
        self.svr.sending_notification(customer)

    def handleRecv(self, rcv: dict):
        rtn = None
        if rcv['status'] == Status.CHECKING:
            # receive from web
            rtn = self.checking(rcv['id'], rcv)
    
        elif rcv['status'] == Status.CHECKED:
            # receive from app 
            rtn = self.checkDone(rcv['id'], rcv)
        
        return rtn

    def checking(self, id, data: dict):
        rtn = None
        if not id in self.pendingCustomers:
            data['status'] = Status.PENDDING.value
            self.pendingCustomers[id] = data
            self.pendingCustomers[id]['time'] = self.timer
            rtn = self.pendingCustomers[id]
            self.make_request(data)
        
        if self.pendingCustomers[id]['status'] == Status.CHECKED.value:
            rtn = self.pendingCustomers[id]
            del self.pendingCustomers[id]

        # elif self.pendingCustomers[id]['status'] == Status.TIMEOUT.value:
        #     rtn = self.pendingCustomers[id]
        #     del self.pendingCustomers[id]
        
        else:
            rtn = self.pendingCustomers[id]
        
        return rtn
    
    def checkDone(self, id, data: dict):
        if not id in self.pendingCustomers:
            return 'ERROR'

        if self.pendingCustomers[id]['status'] == Status.PENDDING:
            self.pendingCustomers[id]['accepted'] = data['accepted']
            self.pendingCustomers[id]['status'] = Status.CHECKED.value
            return 'SUCCESS'
        
        return 'ERROR'
        
    
if __name__ == '__main__':
    pass