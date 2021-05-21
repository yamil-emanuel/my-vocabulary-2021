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

def PushAdjective(eng,data):#CONVERT DATA (STR2DIC)% PUSH IT INTO /vocabulary/adjectives/
  data=eval(data)
  db.child("vocabulary").child("adjectives").child(eng).set(data)
  print("THE DATA WAS UPLOADED SUCCESFULLY \n")

def PushNoun(eng,data):#CONVERT DATA (STR2DIC)% PUSH IT INTO /vocabulary/nouns/
  try:
    data=eval(data)
    db.child("vocabulary").child("nouns").child(eng).set(data)
    print("THE DATA WAS UPLOADED SUCCESFULLY \n")

  except SyntaxError:
    print("WARNING: Data won't be uploaded. SyntaxError.\n")

def PushArticle(date,title,data):
  data=eval(data)
  db.child("news").child(date).child(title).set(data)
  print("THE ARTICLE WAS POSTED SUCCESFULLY.\n")


def AllVerbs():
  result=(db.child("vocabulary").child("verbs").get().val())
  for x in result:
    print (x)

def AllAdjectives():
  result=(db.child("vocabulary").child("adjectives").get().val())
  for x in result:
    print(x)

def AllNouns():
  result=(db.child("vocabulary").child("nouns").get().val())
  for x in result:
    print(x)


def Search(word_type,word):
  root_template='(db.child("vocabulary")'
  word_type_template='.child("{}")'.format(word_type)
  word_template='.child("{}").get().val())'.format(word)
  
  print(exec(root_template+word_type_template,word_template))
  #TERMINAR ESTA FUNCION





