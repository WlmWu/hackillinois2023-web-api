import firebase_admin
from firebase_admin import credentials, messaging
from firebase_admin import firestore

class FCMserver():
    def __init__(self, collection='Customers', uid='0001') -> None:
        self.collection = collection
        self.uid = uid
        cred = credentials.Certificate("certificate.json")
        firebase_admin.initialize_app(cred)
        # self.token = 'cVvrg1UxQmi3vgHqEyOMQX:APA91bE_Iddbxh1imtKWXVj5ky6tQQwfXYCu0a71xv7Z0fYA_s1fKdrPftZa5JQTa0Lra7b7Hxo68BHdFDG4qkV9mn7MNJgtkr6EqeAOtNKv4TCqCk0zDaLCqbidkkTkuxfcvRCYpXoU'
        self.db = firestore.client()
        self.docs = self.db.collection(self.collection)

    def sending_notification(self, customer):
        self.uid = customer['id']
        self.dic = self.getOne()

        message = messaging.Message(
        notification=messaging.Notification(
                title='Checkout Now!',
                body='Tap here to complete the payment',
            ),
            data={
                'making_payment': 'True',
            },
            token=self.dic['DToken'],
        )
        response = messaging.send(message)
        # print(f"send push to {self.dic['DToken']}")
        print(response)
        return response

    def getAll(self) -> list:
        res = []
        for doc in self.docs.get():
            d = doc.to_dict()
            d['id'] = doc.id
            res.append(d)
        return res
    
    def getOne(self) -> dict:
        for doc in self.docs.get():
            d = doc.to_dict()
            if doc.id == self.uid:
                d['id'] = self.uid
                return d
    
if __name__ == '__main__':
    fcm = FCMserver()
    # print(fcm.getOne())
    fcm.sending_notification(customer={'id':'0001'})