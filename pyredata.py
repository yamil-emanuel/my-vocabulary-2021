import pyrebase

config = {
  "apiKey": "apiKey",
  "authDomain": "vocabularyapp-aa8a1-default-rtdb.firebaseapp.com",
  "databaseURL": "https://vocabularyapp-aa8a1-default-rtdb.firebaseio.com/",
  "storageBucket": "vocabularyapp-aa8a1-default-rtdb.appspot.com",
  "serviceAccount": "/home/yamil/Documents/PYTHON/vocabularyapp-aa8a1-firebase-adminsdk-74tde-abc1940438.json"
}

#CONNECTING TO THE DATASET
firebase = pyrebase.initialize_app(config)
db=firebase.database()

def PushVerb(eng,data): #CONVERT DATA (STR2DIC)% PUSH IT INTO /vocabulary/verbs/... 
  data=eval(data)
  db.child("vocabulary").child("verbs").child(eng).set(data)
  print("THE DATA WAS UPLOADED SUCCESFULLY \n")

def PushAdjective(eng,data):
  data=eval(data)
  db.child("vocabulary").child("adjectives").child(eng).set(data)
  print("THE DATA WAS UPLOADED SUCCESFULLY \n")

def AllVerbs():
  result=(db.child("vocabulary").child("verbs").get().val())
  for x in result:
    print (x)

