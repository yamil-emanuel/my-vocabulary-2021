import csv
import datetime
import pyredata


template='''{{"TITLE": "{}",
  "SUBTITLE" : "{}",
  "TEXT" : "{}",
  "TAGS" : "{}"
}}'''



def Date():
    #RETURNS THE CURRENT DAY AS YYYY-M-DD
    date=datetime.datetime.now()
    year=str(date.year)
    month=str(date.month)
    day=str(date.day)
    push_date=(year+"-"+month+"-"+day)
    return push_date


if __name__ == "__main__":
    
    #OPENS THE ARTICLES.CSV FILE
    with open ("ARTICLES.csv","r") as vocabulary_csv:
        data_input=csv.reader(vocabulary_csv, delimiter=',', quotechar='|')
        for row in data_input:

            date=Date()
            title=row[0]
            subtitle=row[1]
            text=row[2]
            tags=row[3]
            
            #SKIPS THE FIRST ROW.
            if row[0] != "TITLE":
                #COMPLETING THE TEMPLATE
                data=template.format(title,subtitle,text,tags)
                #UPLOADING THE DATA TO THE DATASET
                pyredata.PushArticle(date,title,data)


            



