import pyrebase
import uuid
import json

class firebase_manager():
    config = {
    "apiKey": "AIzaSyBqY-XjWFglTx7dBPCNz6DTeXSH8Isx7jk",
    "authDomain": "movies-web-scraping.firebaseapp.com",
    "databaseURL": "https://movies-web-scraping.firebaseio.com",
    "storageBucket": "movies-web-scraping.appspot.com",
    "serviceAccount": "C:\\MyRepositories\\credentials\\firebase\\movies-web-scraping-firebase-adminsdk-4yec8-d38d7cb985.json"
    }

    db = None

    def initialize_firebase_db(self):
        firebase = pyrebase.initialize_app(self.config)
        self.db = firebase.database()

    def store_to_db(self, table, data):
        try:
            # data['download_links'] = dict()
            # json_data = json.dumps(data)
            #self.db.child(table).child(str(uuid.uuid4())).set(data)
            self.db.child(table).push(data)
        except Exception as error:
            print('Um erro ocorreu: ' + repr(error))
        

    def clean_table(self, table):
        self.db.child(table).remove()

    def get_table(self, table):
        result = self.db.child(table).get()
        return result.val()
