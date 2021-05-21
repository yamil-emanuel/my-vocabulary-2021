
from os import name, replace
import requests
from bs4 import BeautifulSoup
from GrammarData import *
from pyredata import *
import re
import csv


def CreateErrorLog():
    if error_log != None:
        with open ("ERROR_LOG.txt","a") as error_log_file:
            for error in error_log:
                error_log_file.write(error)
            error_log_file.close()

    else:
        pass


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
        self.total_data=None

    def VerbCheckerGerman(self,ger):
        #Pulling Information for RegularCheck.
        if 'ü' in ger:
            ger_umlaud=ger.replace("ü","u3")
            url_r=requests.get(('https://www.verbformen.com/conjugation/?w={}').format(ger_umlaud))
            soup = BeautifulSoup(url_r.content, 'lxml')
        else:
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
            try:
                if 'sich' in ger_prepositions.keys():
                    return 1 #yes
                else: 
                    return 0 #no
            except AttributeError:
                print(("Critical Error at {}'s german prepositions. Data not found.").format(self.eng))
                error_message=("{} -GERMAN-VERB-REFLEXIVE DATA IS MISSING.\n").format(self.eng)
                error_log.append(error_message)
                return "NOT FOUND"

        def PrepositionsAndCasesCheck():
            #Get the preposition's data.
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
                if x == "als" or x == "wie":
                    german_prepositions_dictionary[x]="1"
                else:     
                    x=x.split('+')
                    
                    if x[0]!='acc.':
                        try:
                            german_prepositions_dictionary[x[0]]=x[1]

                        except IndexError:

                            print(("Critical Error at {}'s german prepositions. Data not found.").format(self.eng))
                            error_message=("{} - GERMAN-PREPOSITIONS DATA IS MISSING.\n").format(self.eng)
                            error_log.append(error_message)
                    else:
                        german_prepositions_dictionary["acc"]="1"



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
            if "ü" in self.ger:
                ger_umlaud_correction=self.ger.replace("ü","ue")
                url_definition=requests.get(('https://www.duden.de/rechtschreibung/{}').format(ger_umlaud_correction))
                
            else:
                url_definition=requests.get(('https://www.duden.de/rechtschreibung/{}').format(ger))

            soup_definition_german = BeautifulSoup(url_definition.content, 'lxml')
            #Get relevant data for the R's functions (RegularCheck and ReflexiveCheck).
            raw_data=list(soup_definition_german.find_all(attrs={'class':'enumeration__text'}))
            
            try:
                final_data=raw_data[0].get_text()

            except IndexError:
                print(("Critical Error at {}'s german definition. Data not found.").format(self.eng))
                final_data="NOT FOUND"
                error_message=("{} - GERMAN-DEFINITION DATA IS MISSING\n").format(self.eng)
                error_log.append(error_message)
            
            return final_data

        def FillGermanDataTemplate(self): #Filling the template with verb's data.
            
            ger_prepositions_final={}

            #Converting every preposition in the list into dictionaries keys, value will be filled manually. 
            for element in self.ger_prepositions:
                try:
                    temp=('''{{"CASE":"{}","EXAMPLE":"None"}}''').format(self.ger_prepositions.get(element))
                    ger_prepositions_final[element]=temp
                except AttributeError:
                    print(("Critical Error at {}'s prepositions. Data not found.").format(self.eng))
                    error_message=("{} -GERMAN-PREPOSITION DATA IS MISSING.\n").format(self.eng)
                    error_log.append(error_message)
                    

            ger_prepositions_final=str(ger_prepositions_final).replace("'{","{").replace("}'",'}')

            data_verbs_german=(template_german_verb).format(self.ger_auxiliar_verb,self.ger_definition,self.ger,self.ger_is_reflexive,self.ger_is_separable,ger_prepositions_final)
            return data_verbs_german

        self.ger_definition=Definition()
        self.ger_is_separable=SeparableCheck()
        self.ger_is_regular=RegularCheck()
        self.ger_prepositions=PrepositionsAndCasesCheck()
        ger_prepositions=self.ger_prepositions
        self.ger_auxiliar_verb=PastCheck()
        self.ger_is_reflexive=ReflexiveCheck(self,ger_prepositions)

        data_verbs_german=FillGermanDataTemplate(self) #Filling the template with verb's data.
        return data_verbs_german

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

        def FillEnglishDataTemplate(self): #Filling the template with verb's data.

            eng_prepositions={}
            #Converting every preposition in the list into dictionaries keys, value will be filled manually. 
            
            for preposition in self.eng_prepositions:
                eng_prepositions[preposition]="None"

            data_verbs_english=(template_english_verb).format(self.eng_definition,self.eng,self.eng_is_regular,self.eng_is_transitive,eng_prepositions)
            return data_verbs_english

        self.eng_definition=Definition()
        self.eng_is_regular=RegularEnglish()
        self.eng_is_transitive=TransitiveEnglish()
        self.eng_prepositions=PrepositionsEnglish()
        self.data_verbs_english=FillEnglishDataTemplate(self)
        return self.data_verbs_english

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
                return 0 #no
            else:
                return 1 #yes

        
        def FillSpanishDataTemplate(self): #Filling the template with verb's data.
            data_verbs_spanish=(template_spanish_verb).format(self.spa_definition,self.spa_is_regular,self.spa)
            return data_verbs_spanish



        self.spa_definition=Definition()
        self.spa_is_regular=RegularSpanish()
        self.data_verbs_spanish=FillSpanishDataTemplate(self)
        return self.data_verbs_spanish

    def VerbChecker(self,eng,spa,ger): #GATHERS VERB'S RELATED DATA

        self.data_verbs_spanish=self.VerbCheckerSpanish(spa) #SPANISH DATA
        sdc="SPANISH DATA -{}- COMPLETED"
        print((sdc).format(spa))

        self.data_verbs_english=self.VerbCheckerEnglish(eng) #ENGLISH DATA
        edc="ENGLISH DATA -{}- COMPLETED"
        print((edc).format(eng))

        self.data_verbs_german=self.VerbCheckerGerman(ger) #GERMAN DATA
        gdc="GERMAN DATA -{}- COMPLETED"
        print((gdc).format(ger))

        total_data=self.data_verbs_english+'\n'+self.data_verbs_german+'\n'+self.data_verbs_spanish
        
        return total_data

class Adjective:
    def __init__(self,eng,spa,ger):
        self.eng=eng
        self.spa=spa
        self.ger=ger
        self.eng_definition=None
        self.spa_definition=None
        self.ger_definition=None

    def EnglishChecker(self,eng):
        def Definition(eng):
            url_definition=requests.get(('https://www.lexico.com/en/definition/{}').format(self.eng))
            soup_definition_english = BeautifulSoup(url_definition.content, 'lxml')
            raw_data=list(soup_definition_english.find_all(attrs={'class':'ind'}))
            final_data=raw_data[0].get_text()

            return final_data    
        
        def FillEnglishTemplate(self):
            self.eng_definition=Definition(eng) 
            eng_data=template_eng_adjective.format(self.eng_definition,self.eng)
            return eng_data


        self.eng_definition=Definition(eng)    
        eng_data=FillEnglishTemplate(self)        
        return eng_data

    def SpanishChecker(self,spa):
        def Definition(spa):
            #making request
            url_definition=requests.get(('https://dle.rae.es/{}?m=form').format(self.spa))
            soup_definition_spanish = BeautifulSoup(url_definition.content, 'lxml')
            #Get relevant data spanish definition of the verb.
            raw_data=(soup_definition_spanish.find_all(attrs={'class':'j'}))
            #Cleaning the data.
            raw_data=raw_data[0].get_text()
            filtered_data=(raw_data.split(' '))[2:]
            definition= " ".join(filtered_data)
            return definition

        def FillSpanishTemplate(self):
            self.spa_definition=Definition(spa)
            spa_data=template_spa_adjective.format(self.spa_definition,self.spa)
            return spa_data

        spa_data=FillSpanishTemplate(self)
        return spa_data

    def GermanChecker(self,ger):
        def Definition(self,ger):
            if "ü" in self.ger:
                ger_umlaud_correction=self.ger.replace("ü","ue")
                url_definition=requests.get(('https://www.duden.de/rechtschreibung/{}').format(ger_umlaud_correction))

            elif "ö" in self.ger:
                ger_umlaud_correction=self.ger.replace("ö","oe")
                url_definition=requests.get(('https://www.duden.de/rechtschreibung/{}').format(ger_umlaud_correction)) 

            elif "ä" in self.ger:
                ger_umlaud_correction=self.ger.replace("ä","ae")
                url_definition=requests.get(('https://www.duden.de/rechtschreibung/{}').format(ger_umlaud_correction)) 

            elif "ß" in self.ger:
                ger_umlaud_correction=self.ger.replace("ß","sz")
                url_definition=requests.get(('https://www.duden.de/rechtschreibung/{}').format(ger_umlaud_correction))

            else:
                url_definition=requests.get(('https://www.duden.de/rechtschreibung/{}').format(self.ger))

            soup_definition_german = BeautifulSoup(url_definition.content, 'lxml')
            #Get relevant data for the R's functions (RegularCheck and ReflexiveCheck).
            raw_data=list(soup_definition_german.find_all(attrs={'class':'enumeration__text'}))
            try:
                final_data=raw_data[0].get_text()
            except IndexError:
                print(("Critical Error at {}'s german definition. Data not found.").format(self.eng))
                final_data="NOT FOUND"
                error_message=("{} - GERMAN-DEFINITION DATA IS MISSING.\n").format(self.eng)
                error_log.append(error_message)

            return final_data
        
        def FillGermanTemplate(self):          
            self.ger_definition=Definition(self,ger)
            ger_data=template_ger_adjective.format(self.ger_definition,self.ger)

            return ger_data

        ger_data=FillGermanTemplate(self)
        return ger_data
            
    def AdjectiveChecker(self,eng,spa,ger):

        self.data_adjectives_eng=self.EnglishChecker(self) #ENG DATA IN TEMPLATE
        edc="ENGLISH DATA -{}- COMPLETED"
        print((edc).format(self.eng))

        self.data_adjectives_spa=self.SpanishChecker(self) #SPA DATA IN TEMPLATE
        sdc="SPANISH DATA -{}- COMPLETED"
        print((sdc).format(self.spa))

        self.data_adjectives_ger=self.GermanChecker(self.ger) #GER DATA
        gdc="GERMAN DATA -{}- COMPLETED"
        print((gdc).format(self.ger))

        self.total_data=self.data_adjectives_eng+'\n'+self.data_adjectives_spa+'\n'+self.data_adjectives_ger 
        return self.total_data



        
        def FillSpanishDataTemplate(self): #Filling the template with verb's data.
            data_verbs_spanish=(template_spanish_verb).format(self.spa_definition,self.spa_is_regular,self.spa)
            return data_verbs_spanish



        self.spa_definition=Definition()
        self.spa_is_regular=RegularSpanish()
        self.data_verbs_spanish=FillSpanishDataTemplate(self)
        return self.data_verbs_spanish

    def VerbChecker(self,eng,spa,ger): #GATHERS VERB'S RELATED DATA
        self.data_verbs_spanish=self.VerbCheckerSpanish(spa) #SPANISH DATA
        self.data_verbs_english=self.VerbCheckerEnglish(eng) #ENGLISH DATA
        self.data_verbs_german=self.VerbCheckerGerman(ger) #GERMAN DATA
        self.total_data='{\n  '+'"'+self.eng+'":{'+self.data_verbs_english,self.data_verbs_german,self.data_verbs_spanish+'}'
        
        for part in self.total_data:
            part=part.replace('\\',"").replace("'",'"')
            print(part)

class Noun:
    def __init__(self,eng,spa,ger):
        self.eng=eng
        self.spa=spa
        self.ger=ger

    def EnglishChecker(self,eng):
        def Definition(eng):
            url_definition=requests.get(('https://www.lexico.com/en/definition/{}').format(self.eng))
            soup_definition_english = BeautifulSoup(url_definition.content, 'lxml')
            raw_data=list(soup_definition_english.find_all(attrs={'class':'ind'}))
            final_data=raw_data[0].get_text()

            return final_data

        def Plural(self):

            if re.search("s$",self.eng) or re.search("x$",self.eng) or re.search("ch$",self.eng) or re.search("sh$",self.eng):
                eng_plural=eng+"es"
                return eng_plural
                
            elif re.search("y$",self.eng) and self.eng[-2] not in vowels:
                eng_plural=eng[:-1]+"ies"
                return eng_plural
            
            else:
                eng_plural=self.eng+"s"
                return eng_plural      
        
        def FillEnglishTemplate(self):
            eng_data=template_eng_noun.format(self.eng_definition, "None",self.eng_plural, self.eng)
            return eng_data

        self.eng_definition=Definition(self)
        self.eng_plural=Plural(self)
        self.eng_noun_data=FillEnglishTemplate(self)
        return self.eng_noun_data

    def SpanishChecker(self,spa):
        def Definition(spa):

            #making request
            url_definition=requests.get(('https://dle.rae.es/{}?m=form').format(self.spa))
            soup_definition_spanish = BeautifulSoup(url_definition.content, 'lxml')
            #Get relevant data spanish definition.
            raw_data_definition=(soup_definition_spanish.find_all(attrs={'class':'j'}))
            #Cleaning the data.
            raw_data_definition=raw_data_definition[0].get_text()
            filtered_data_definition=(raw_data_definition.split(' '))[2:]
            definition= " ".join(filtered_data_definition)

            #Get word's gender data.
            raw_data_gender=(soup_definition_spanish.find_all(attrs={'class':'d'}))
            raw_data_gender=raw_data_gender[0].get_text()
            if "y f." in raw_data_gender:
                gender="mf"
            elif "f." in raw_data_gender:
                gender="f"
            elif "m.":
                gender="m"

            if "y f." in definition:
                definition=definition.replace("y f. ","")
            elif "m." in definition:
                definition=definition.replace("m.","")
            elif "f." in definition:
                definition=definition.replace("f.","")
            
            return definition,gender
            
        def Articles(self):
            gender=self.spa_gender
            if gender=="f":
                return "la","las"
            elif gender=="m":
                return "el","los"
            elif gender=="mf":
                return "el/la","los/las"

        def Plural(self):
            
            if re.search("ch$",self.spa) or re.search("s$",self.spa) or re.search("x$",self.spa):
                plural=self.spa+"es"
                return plural

            elif re.search("y$",self.spa) and self.spa [-2] in vowels:
                plural=self.spa+"es"
                return plural

            elif re.search("í$",self.spa) or re.search("ú$",self.spa):
                plural=self.spa+"es"
                return plural

            elif re.search("é",self.spa):
                plural=self.spa.replace('é','e')+"s"
                return plural
                
            elif self.spa[-1] not in vowels:
                if re.search("ción$",self.spa):
                    plural=self.spa.replace("ó","o")+"es"
                    return plural

                else:    
                    plural=self.spa+"es"
                    return plural

            else:
                return self.spa+"s"

        def FillSpanishTemplate(self):
            spa_noun_data=template_spa_noun.format(self.spa_article_singular, self.spa_article_plural, self.spa_definition, "None", self.spa_plural, self.spa)
            return spa_noun_data


        self.spa_definition,self.spa_gender=Definition(spa)
        self.spa_article_singular, self.spa_article_plural = Articles(self)
        self.spa_plural=Plural(self)
        self.spa_noun_data=FillSpanishTemplate(self)
        return self.spa_noun_data

    def GermanChecker(self,ger):
        def Definition(self,ger):
            if "ü" in self.ger:
                ger_umlaud_correction=self.ger.replace("ü","ue")
                url_definition=requests.get(('https://www.duden.de/rechtschreibung/{}').format(ger_umlaud_correction))

            elif "ö" in self.ger:
                ger_umlaud_correction=self.ger.replace("ö","oe")
                url_definition=requests.get(('https://www.duden.de/rechtschreibung/{}').format(ger_umlaud_correction)) 

            elif "ä" in self.ger:
                ger_umlaud_correction=self.ger.replace("ä","ae")
                url_definition=requests.get(('https://www.duden.de/rechtschreibung/{}').format(ger_umlaud_correction)) 

            elif "ß" in self.ger:
                ger_umlaud_correction=self.ger.replace("ß","sz")
                url_definition=requests.get(('https://www.duden.de/rechtschreibung/{}').format(ger_umlaud_correction))

            else:
                url_definition=requests.get(('https://www.duden.de/rechtschreibung/{}').format(self.ger))

            soup_definition_german = BeautifulSoup(url_definition.content, 'lxml')
            #Get relevant data for the R's functions (RegularCheck and ReflexiveCheck).
            raw_data=list(soup_definition_german.find_all(attrs={'class':'enumeration__text'}))
            try:
                final_data=raw_data[0].get_text()
            except IndexError:
                print(("Critical Error at {}'s german definition. Data not found.").format(self.eng))
                final_data="NOT FOUND"
                error_message=("{} - GERMAN-DEFINITION DATA IS MISSING.\n").format(self.eng)

            return final_data
        
        def ExtraData(self):
            url_extradata=requests.get(('https://www.verbformen.com/declension/nouns/{}.htm').format(self.ger))
            soup_extradata_german = BeautifulSoup(url_extradata.content, 'lxml')
            
            #Gathering the plural.
            raw_data=list(soup_extradata_german.find_all(attrs={'class':'vStm rCntr'}))
            plural_raw=(raw_data[0].get_text())
            plural_raw=plural_raw.split("·")
            plural=plural_raw[1].replace("\n","")

            #Gathering the article
            article_raw= list(soup_extradata_german.find_all(attrs={'class':'vGrnd rCntr'}))
            article_raw=article_raw[0].get_text()
            article_raw=article_raw.split(" ")
            article=article_raw[0].replace("\n","")
            
            
            
            
            return article,plural
            
        def FillGermanTemplate(self):
            ger_data=template_ger_noun.format(self.ger_article,self.ger_definition,"None",self.ger_plural, self.ger)
            return ger_data

        self.ger_definition=Definition(self,ger)
        self.ger_article,self.ger_plural=ExtraData(self)
        self.ger_data=FillGermanTemplate(self)
        return self.ger_data

    def NounChecker(self,eng,spa,ger):
        self.eng_noun_data=self.EnglishChecker(eng) #ENGLISH DATA
        edc="ENGLISH DATA -{}- COMPLETED"
        print((edc).format(eng))
        
        self.spa_noun_data=self.SpanishChecker(spa) #SPANISH DATA
        sdc="SPANISH DATA -{}- COMPLETED"
        print((sdc).format(spa))
        
        self.ger_noun_data=self.GermanChecker(ger) #GERMAN DATA
        gdc="GERMAN DATA -{}- COMPLETED"
        print((gdc).format(ger))

        final_data= self.eng_noun_data +'\n'+ self.spa_noun_data + '\n' + self.ger_noun_data
        return final_data


def VerbProcessor(eng,spa,ger):
    word=Verb(eng,spa,ger)
    data=word.VerbChecker(word.eng, word.spa, word.ger)
    PushVerb(word.eng,data)

def AdjectiveProcessor(eng,spa,ger):
    word=Adjective(eng,spa,ger)
    data=word.AdjectiveChecker(word.eng,word.spa,word.ger)
    PushAdjective(word.eng,data)

def NounProcessor(eng,spa,ger):
    word=Noun(eng,spa,ger)
    data=word.NounChecker(word.eng,word.spa,word.ger)
    PushNoun(word.eng,data)

if __name__ == "__main__":

    error_log=[]

    #OPEN THE VOCABULARY FILE, READ THE WORDS AND PROCESS THEM.
    with open ("VOCABULARY.csv","r") as vocabulary_csv:
        data_input=csv.reader(vocabulary_csv, delimiter=',', quotechar='|')
        for row in data_input:
            eng=row[1].lower()
            spa=row[2].lower()
            ger=row[3].lower()
            word_type=row[0].upper()

            if word_type=='NOUN':
                ger=ger.capitalize()
                NounProcessor(eng,spa,ger)
            
            elif word_type=='ADJECTIVE':
                AdjectiveProcessor(eng,spa,ger)
            
            elif word_type=="VERB":
                VerbProcessor(eng,spa,ger)
    
    #OVERWRITE THE VOCABULARY.CSV FILE AND LEAVE IT EMPTY.
    with open ("VOCABULARY.csv","w") as vocabulary_csv:
        vocabulary_writer=csv.writer(vocabulary_csv, delimiter=",", quotechar='|')
        vocabulary_writer.writerow(["WORD_TYPE","ENGLISH","SPANISH","GERMAN"])
    
    CreateErrorLog()


    



#---------------------------#

## CSV file. url for pushing the missing data. gathering it. run a function that automatically upload the missing data. 
