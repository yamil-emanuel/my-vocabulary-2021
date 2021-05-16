from os import name
import requests
from bs4 import BeautifulSoup
from GrammarData import *


#REFLEXIVEENGLISH, PREPOSITIONSSPANISH, REFLEXIVESPANISH


class Verb:
    def __init__(self,eng,spa,ger):
        self.eng=eng
        self.spa=spa
        self.ger=ger
        self.ger_definition=None
        self.ger_is_separable=None
        self.ger_prepositions=None
        self.ger_auxiliar_verb=None
        self.ger_is_reflexive=None
        self.ger_is_regular=None
        self.eng_definition=None
        self.eng_is_regular=None
        self.eng_is_transitive=None
        self.eng_prepositions=None
        self.spa_definition=None
        self.spa_is_regular=None

    def VerbCheckerGerman(self,ger):
        #Pulling Information for RegularCheck.
        url_r=requests.get(('https://www.verbformen.com/conjugation/?w={}').format(ger))
        soup = BeautifulSoup(url_r.content, 'lxml')

        #Get relevant data for RegularCheck.
        r_data=soup.find_all('p')[0].get_text()
        r=r_data.split(' ')

        def RegularCheck ():
            #Cheking if the verb is regular or not.
            if 'regular' in r or 'regular.' in r and (r.index("regular.")-1) != "not" :
                is_regular="yes"
                return is_regular
            else:
                is_regular="no"
                return is_regular

        def ReflexiveCheck(self,ger_prepositions):
            #If 'sich' exists in preposition's dictionary means that the verb can be used reflexively. 
            if 'sich' in ger_prepositions.keys():
                return 1 #yes
            else: 
                return 0 #no

        def PrepositionsAndCasesCheck():
            #Get the preposition's data.
            url_p=requests.get(('https://www.woerter.net/verbs/usages/{}.htm').format(ger))
            soup = BeautifulSoup(url_r.content, 'lxml')
            #Filtering the results
            p_data=soup.find_all('p')[6].get_text()
            #Cleaning them
            p_data=p_data.replace('\n','').replace(')','').replace('(','').replace(' ',"")
            #Creating a list.
            prepositions_raw=p_data.split(',')
            #german_prepositions_dictionary will contain the processed information as {preposition:case}
            german_prepositions_dictionary={}
            for x in prepositions_raw:     
                x=x.split('+')
                if x[0]!='acc.':
                    german_prepositions_dictionary[x[0]]=x[1]
                else:
                    pass
            return german_prepositions_dictionary

        def PastCheck():
            if 'haben' in r or "haben." in r:
                auxiliar_verb='haben'
                return auxiliar_verb
            else:
                auxiliar_verb="sein"
                return auxiliar_verb

        def SeparableCheck():
            if "separable." in r and (r.index("separable.")-1) != "not":
                is_separable=1 #yes
                return is_separable
            else:
                is_separable=0 #no
                return is_separable
        
        def Definition():
            url_definition=requests.get(('https://www.duden.de/rechtschreibung/{}').format(ger))
            soup_definition_german = BeautifulSoup(url_definition.content, 'lxml')
            #Get relevant data for the R's functions (RegularCheck and ReflexiveCheck).
            raw_data=list(soup_definition_german.find_all(attrs={'class':'enumeration__text'}))
            final_data=raw_data[0].get_text()
            return final_data

        self.ger_definition=Definition()
        
        self.ger_is_separable=SeparableCheck()
        self.ger_is_regular=RegularCheck()
        self.ger_prepositions=PrepositionsAndCasesCheck()
        ger_prepositions=self.ger_prepositions
        self.ger_auxiliar_verb=PastCheck()
        self.ger_is_reflexive=ReflexiveCheck(self,ger_prepositions)

    def VerbCheckerEnglish(self,eng):
        def TransitiveEnglish():
            url_transitive=requests.get(('https://www.merriam-webster.com/dictionary/{}').format(eng))
            soup = BeautifulSoup(url_transitive.content, 'lxml')
            #Getting transitives data. 
            transitive_data=soup.find_all('a')[28].get_text()
            #filtering using CSS selector.
            intransitive_data=list(soup.select('a:is(.important-blue-link)')) 
            if intransitive_data[1].get_text() == "transitive verb" or intransitive_data[2].get_text() == "transitive verb":
                if intransitive_data[1].get_text() == "intransitive verb" or intransitive_data[2].get_text() == "intransitive verb":
                    return 2 #BOTH
                else:
                    return 1#TRANSITIVE
            else:
                return 0#INTRANSITIVE
        
        def PrepositionsEnglish():
            url_prepositions=requests.get(('https://inspirassion.com/en/prep/{}').format(eng))
            soup_prepositions_english= BeautifulSoup(url_prepositions.content, 'lxml')
            #Filtering using CSS selector.
            prueba=list(soup_prepositions_english.find_all(attrs={'class':'text-token text-success font-weight-bold text-result'}))
            english_prepositions=[]
            prepositions_list=[]
            #Creating a new list with all the possible prepositions.
            for x in prueba:
                #Transforming to text
                base=(x.get_text())
                #Erasing possible spaces
                string=base.replace(' ','')
                #Checking if the string value is a valid preposition or not and 
                #adding it to the preposition_list
                if string in english_prepositions_dictionary:
                    prepositions_list.append(string)

            return prepositions_list

        def RegularEnglish():
            url_regular_english=requests.get(('https://www.the-conjugation.com/english/verb/{}.php').format(eng))
            soup_regular_english= BeautifulSoup(url_regular_english.content, 'lxml')
            gross=list(soup_regular_english.find_all(attrs={'class':'tempscorps'}))

            #Getting all the past simple values
            past_simple=gross[2].get_text()
            #Filtering them
            filtered_past_simple=((past_simple.split(' '))[-1])

            #Getting all the past perfect values
            past_perfect=(gross[6].get_text())
            #Filtering them
            filtered_past_perfect=((past_perfect.split(' '))[-1])

            if filtered_past_simple[-2:]!= "ed" and filtered_past_perfect[-2:] !="ed":
                return 1
            else:
                return 0

        def Definition():
            url_definition=requests.get(('https://www.lexico.com/en/definition/{}').format(eng))
            soup_definition_english = BeautifulSoup(url_definition.content, 'lxml')
            #Get relevant data for the R's functions (RegularCheck and ReflexiveCheck).
            raw_data=list(soup_definition_english.find_all(attrs={'class':'ind'}))
            final_data=raw_data[0].get_text()
            return final_data
        
        def ReflexiveEnglish():
            pass
        
        
        self.eng_definition=Definition()
        self.eng_is_regular=RegularEnglish()
        self.eng_is_transitive=TransitiveEnglish()
        self.eng_prepositions=PrepositionsEnglish()
        
    def VerbCheckerSpanish(self,spa):
        def Definition():
            #making request
            url_definition=requests.get(('https://dle.rae.es/{}?m=form').format(spa))
            soup_definition_spanish = BeautifulSoup(url_definition.content, 'lxml')
            #Get relevant data spanish definition of the verb.
            raw_data=(soup_definition_spanish.find_all(attrs={'class':'j'}))
            #Cleaning the data.
            raw_data=raw_data[0].get_text()
            filtered_data=(raw_data.split(' '))[2:]
            definition= " ".join(filtered_data)
            return definition
        def PrepositionsSpanish():
            pass
        def ReflexiveSpanish():
            pass
        def RegularSpanish():
            url_regular_spanish=requests.get(('https://www.wordreference.com/conj/EsVerbs.aspx?v={}').format(spa))
            soup = BeautifulSoup(url_regular_spanish.content, 'lxml')
            #B corresponds to irregular forms in the conjugation's table.
            regular_raw_data=soup.find_all('b')

            temporal_list=[]

            #Filtering results and adding the filtered data into the temporal_list.
            for element in regular_raw_data:
                if element.get_text() =="Open All" or element.get_text() =="Desktop View":
                    pass
                elif element.get_text()=="es" or element.get_text()=="és":
                    pass
                else:
                    temporal_list.append(element.get_text())

            #If there is an element in temporal_list means that irregular forms where found in the conjugation's table.
            if len(temporal_list)>0:
                return "no"
            else:
                return "yes"

        
        self_spa_definition=Definition()
        self_spa_is_regular=RegularSpanish()

    def VerbChecker(self,eng,spa,ger):
        self.VerbCheckerSpanish(spa)
        self.VerbCheckerEnglish(eng)
        self.VerbCheckerGerman(ger)
    



#instance
play=Verb('play','jugar','spielen')
spa=play.spa
eng=play.eng
ger=play.ger
#Search and organize data.
play.VerbChecker(eng,spa,ger)


#print it.
print(play.ger_prepositions, play.eng_prepositions)

"""
'DEFINITION':{} 
'IS_SEPARABLE':{}
'PREPOSITIONS':{}
'AUXILIAR_VERB':{}
'IS_REGULAR':{}

'DEFINITION':{}
'IS_REGULAR':{}
'IS_TRANSITIVE':{}
'PREPOSITIONS':{}

'DEFINITION':{}
'IS_REGULAR':{}



"""