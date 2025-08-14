# Test python version:
# python3 --version
#
# Test if pip is present:
# python3 -m pip --version
#
# If pip is not present, then
# sudo apt update
# sudo apt install python3-venv python3-pip
#
# Create virtual environment:
# python3 -m venv ~/projekte/hel_pip
#
# Activate v-env hel_pip:
# source ~/projekte/hel_pip/bin/activate

# Ensure pip, setuptools, and wheel are up to date
# python3 -m pip install --upgrade pip setuptools wheel

#
# pip install pandas
# python3 -m pip install pandas
# python3 -m pip install bs4
# python3 -m pip install requests
# python3 -m pip install isbnlib isbnlib-dnb

#
# Test if DNB is online:
# Open in Browser:
# https://portal.dnb.de/opac/simpleSearch?query=9783551651051
#

#
# RSYNC from ext4 to exfat:
#
# rsync -hvrltD --delete --modify-window=1 --progress projekte/buecherei /media/helmut/Crucial\ X6/projekte



Magische Tiere Ferien: 9783551653390
Magische Tiere  Witze: 9783551651051

KEINE ISBN Nummer: 9783774000000

Alles ist schwer bevor es leicht ist (Caroline von St. Ange): 9783499011030
Ponyhof Apfelbluete Band 18 (Pippa Young): 9783743211179
Neinhorn und die Schlangeweile (Marc-Uwe Kling): 9783551521286
Die Dinge (Annabell Hirsch): 9783036961637
101 Essays (Brianna Wiest): 9783492071598
Sieh Hin! (Wieteke Van Zeil): 9783865024701
Sommer am Bosporus (Wolfgang Schorlau): 9783462034271
Warrior Cats Season 1, Band 2 Feuer und Eis (Erin Hunter): 9783407742353
Kreuzberg Blues (Wolfgang Schorlau): 9783462002751
Voegel (Kosmos Verlag): 9783440177235
Antonio im Wunderland (Jan Weiler): 9783499242632

Englische Buecher:
Charles Stross, Laundry Files Bd. 1. ISBN:  9781101208847


Abfrage:
---------
curl -o magische_schule.html https://portal.dnb.de/opac/simpleSearch?query=9783551653390

dann mit Beautifulsoup parsen


import requests
from bs4 import BeautifulSoup
ISBN_number = "9783551653390"
url = "https://portal.dnb.de/opac/simpleSearch?query=9783551653390"
headers = {
  "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
  AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36"
}
response = requests.get(url, headers=headers)
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

table = soup.find("table", { "id" : "fullRecordTable" })
for row in table.findAll("tr"):
    cells = row.findAll("td")
    print(cells)


Neues Python Programm mit Funktionen:
-------------------------------------

# 1. source ~/projekte/hb_python_pip/my-venv/bin/activate
# 2. python
# 3. copy & paste

#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re  # regular expressions
import urllib.request  # to download cover image in size small
import time
import datetime


def get_dnb_info(isbn):
   url = 'https://portal.dnb.de/opac/showFullRecord?currentResultId='+isbn+'%26any&currentPosition=0'
   mydict = {'ISBN' : isbn,
      '00_Erstautor' : 'N.N.',
      '00_Erscheinungsjahr' : '1001',
      '00_Kurztitel' : 'Ohne Titel',
      '00_Kartentitel' : 'Ohne Titel',
      '00_Verlag' : 'Ohne Verlag',
      '00_Sachgruppe' : 'Ohne Sachgruppe',
      '00_Preis' : 'EUR 0 (DE)',
      'Link zu diesem Datensatz' : 'Link  not found',
      'Art des Inhalts' : 'Inhalt nicht gefunden',
      'Titel' : 'Titel nicht gefunden',
      'Person(en)' : 'Personen nicht gefunden',
      'Organisation(en)' : 'Organisationen nicht gefunden',
      'Ausgabe' : 'Ausgabe nicht gefunden',
      'Verlag' : 'Verlag nicht gefunden',
      'Zeitliche Einordnung' : 'Erscheinungsdatum nicht gefunden',
      'Umfang/Format' : 'Format nicht gefunden',
      'Andere Ausgabe(n)' : 'Keine weiteren Ausgaben gefunden',
      'ISBN/Einband/Preis' : 'Preis nicht gefunden',
      'EAN' : isbn,
      'Sprache(n)' : 'Sprache nicht gefunden',
      'Beziehungen' : 'Keine Beziehungen gefunden',
      'Zielgruppe' : 'Keine Zielgruppe gefunden',
      'Schlagwörter' : ' Keine Schlagwörter gefunden',
      'Sachgruppe(n)' : 'Keine Sachgruppe gefunden',
      'Literarische Gattung' : 'Gattung nicht gefunden',
      'MARC21xml' : 'Link not found',
      'Bibframe' : 'Link not found',
      'Buchhandel' : 'Link not found'}
   try:
      response = requests.get(url)
      response.raise_for_status()  # Raise an exception for unsuccessful HTTP status codes
   except requests.exceptions.RequestException as e:
      print(f"An error occurred for ISBN {isbn} when retrieving info from DNB ({e}).")
      return mydict
   # Parse the HTML content using BeautifulSoup
   soup = BeautifulSoup(response.text, "html.parser")
   # Die „fullRecordTable“ enthaelt alle Infos, die wir suchen
   table = soup.find('table', attrs={'id':'fullRecordTable'})
   if table is not None:
      parsed = []
      for tr in table.find_all('tr'):
        row = [td.text for td in tr.find_all('td')]
        if len(row) == 2:
           row[0] = row[0].strip()
           row[1] = row[1].strip()
           mydict[row[0]] = row[1]
   #
   if mydict['Person(en)'] != 'Personen nicht gefunden':
      mydict['00_Erstautor'] = mydict['Person(en)'].split()[0] + ' ' + mydict['Person(en)'].split()[1]
   year = re.findall(r'\d+', mydict['Zeitliche Einordnung'])
   if year: # year[] is not empty
      year = year[0]
      if len(year) == 2:
         year = "20" + year
   #
   mydict['00_Erscheinungsjahr'] = year
   try:
      mydict['00_Kurztitel'] = mydict['Titel'].split('/')[0].strip()
   except:
      pass
   try:
      mydict['00_Kartentitel'] = mydict['00_Kurztitel'].split(':')[0].strip()
   except:
      pass
   try:
      mydict['00_Verlag'] = mydict['Verlag'].split(':')[1].strip()
   except:
      pass
   try:
      mydict['00_Preis'] = re.findall(r'EUR \d{1,3}(?:\,\d{3})*.\d\d \(DE\)', mydict['ISBN/Einband/Preis'])[0]
   except:
      try:
         mydict['00_Preis'] = re.findall(r'EUR \d{1,3}(?:\,\d{3})*.\d\d', mydict['ISBN/Einband/Preis'])[0]
      except:
         pass
   try:
      mydict['00_Sachgruppe'] = mydict['Sachgruppe(n)']
   except:
      pass
   #
   # find all links in website
   linklist = []
   for item in soup.find_all(attrs={'class': 'link'}):
      for link in item.find_all('a'):
         linklist.append(link.get('href'))
   #
   if linklist:   # true if list is not empty
      try:
         index_marcxml = [idx for idx, s in enumerate(linklist) if 'marcxml' in s][0]
         mydict['MARC21xml'] = linklist[index_marcxml]
      except:
         pass
      #
      try:
         index_bibframe = [idx for idx, s in enumerate(linklist) if 'bibframe' in s][0]
         mydict['Bibframe'] = linklist[index_bibframe]
      except:
         pass
      #
      try:
         index_buchhandel = [idx for idx, s in enumerate(linklist) if 'buchhandel' in s][0]
         mydict['Buchhandel'] = linklist[index_buchhandel]
      except:
         pass
      #
   return mydict

my_isbn_testliste = ["9783551653390",
"9783551651051",
"9783499011030",
"9783743211179",
"9783551521286",
"9783036961637",
"9783492071598",
"9783865024701",
"9783462034271",
"9783407742353",
"9783462002751",
"9783440177235",
"9783499242632"]

cwd = os.getcwd()  # current working directory
workdir="/home/helmut/projekte/buecherei/"
os.chdir(workdir)

#isbn_textfile = "inventur_text.txt"
#isbn_textfile = "martina_inventurtest_2024-02-20.txt"
#isbn_textfile = "neuerwerbungen_2024-03-10.txt"
#isbn_file = "neuerwerbungen_2025-06-15"
isbn_file = "neuerwerbungen_2025-08-11"
with open(isbn_file+".txt") as file:
    isbn_list = [line.rstrip() for line in file]

#unique ISBN numbers by converting to set and then back to list
myset = set(isbn_list)
isbn_list = list(myset)

#df = get_dnb_info(my_isbn_testliste[0])

print("Start reading DNB Info...")
print("Starting at ", time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
start = datetime.datetime.now()

count = 0
library = [] # list of dicts (list of books)

for isbn in isbn_list:
   print('Reading ISBN no. ',isbn,end='',flush=True)
   library.append(get_dnb_info(isbn))
   time.sleep(2)
   print('. Done.')
   count = count + 1

print(f"Finished reading DNB Info for {count} Books.")
print("Ending at ", time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
end = datetime.datetime.now()
print("Duration: ", end - start)

# List colum names:
# list(df.columns.values)
# extract year from "Zeitliche Einordnung"
# match = re.match(r'.*([1-3][0-9]{3})', df.iloc[26,42])

# Save final Table to CSV via pandas
df = pd.DataFrame(library)
#dfT.to_csv("martina_inventurtest_2025-02-22.csv")
#dfT.to_csv("neuerwerbungen_2024-03-10.csv")
df.to_csv(isbn_file+"_new.csv", index = False)


# get cover images
print("Start downloading cover images...")
print("Starting at ", time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
start = datetime.datetime.now()
savepath="/home/helmut/projekte/buecherei/cover"
os.chdir(savepath)
print("Saving files to folder: ", savepath)
print("current working directory: ", os.getcwd())

for i in isbn_list:
   filename = "cover_"+i+".jpg"
   imgurl = "https://portal.dnb.de/opac/mvb/cover?isbn="+i+"&size=l"
   try:
      urllib.request.urlretrieve(imgurl, filename)
   except:
      print("Cover for ISBN ",i," could not be retrieved. Replace with generic image")
      os.system("cp keine_vorschau_gefunden.jpg "+filename)
   time.sleep(1)

print("Finished downloading cover images.")
print("Ending at ", time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
end = datetime.datetime.now()
print("Duration: ", end - start)

# print Buchkarten
library = []
workdir="/home/helmut/projekte/buecherei/"
os.chdir(workdir)
#df = pd.read_csv('martina_inventurtest_2025-02-22.csv')
#df = pd.read_csv('neuerwerbungen_2024-03-10.csv')
#
# read in CSV using pandas, since this has a stable CSV reader
# then, transform it into a list of dicts to work with
df = pd.read_csv(isbn_file+"_new.csv")
library = df.to_dict('records')
number_of_books = len(library)

# we have to add rows to get "rows modulo 4 == 0"
# wir kopieren einfach den letzten Eintrag so oft, 
# bis wir modulo 4 erreicht haben :)
for i in range((len(library)+2)%4):
   library.append(library[-1])

#noch einmal weil das mit dem Modulo irgendwie schwer ist
library.append(library[-1])

pdflist = ''
# loop over rows to get elements
for i in range(0,number_of_books,4):
   titel = [library[i]['00_Kurztitel'],
            library[i+1]['00_Kurztitel'],
            library[i+2]['00_Kurztitel'],
            library[i+3]['00_Kurztitel']] 
   autor = [library[i]['00_Erstautor'],
            library[i+1]['00_Erstautor'],
            library[i+2]['00_Erstautor'],
            library[i+3]['00_Erstautor']]
   verlag = [library[i]['00_Verlag'],
            library[i+1]['00_Verlag'],
            library[i+2]['00_Verlag'],
            library[i+3]['00_Verlag']]
   jahr = [library[i]['00_Erscheinungsjahr'],
            library[i+1]['00_Erscheinungsjahr'],
            library[i+2]['00_Erscheinungsjahr'],
            library[i+3]['00_Erscheinungsjahr']]
   isbn = [str(library[i]['ISBN']),
            str(library[i+1]['ISBN']),
            str(library[i+2]['ISBN']),
            str(library[i+3]['ISBN'])]
   sachgruppe = [library[i]['00_Sachgruppe'],
            library[i+1]['00_Sachgruppe'],
            library[i+2]['00_Sachgruppe'],
            library[i+3]['00_Sachgruppe']]
   cover = ["cover_"+isbn[0],
            "cover_"+isbn[1],
            "cover_"+isbn[2],
            "cover_"+isbn[3]]
   sedstr = ''
   for n in range(4):
      sedstr = sedstr+'s/Titel'+str(n+1)+'/'+titel[n]+'/g;'+\
               's/Autor'+str(n+1)+'/'+autor[n]+'/g;'+\
               's/Verlag'+str(n+1)+'/'+verlag[n]+'/g;'+\
               's/Jahr'+str(n+1)+'/'+jahr[n]+'/g;'+\
               's/ISBN'+str(n+1)+'/'+isbn[n]+'/g;'+\
               's/Sachgruppe'+str(n+1)+'/'+sachgruppe[n]+'/g;'+\
               's/image'+str(n+1)+'/'+cover[n]+'/g;'
   #
   # special=['"',"'","/","%","|"]
   #
   newfile = "temp"+str(i+1)
   slafile = newfile+".sla"
   sedcommand = 'sed -i "'+ sedstr[0:-1]+'" '+slafile
   if '"' in sedstr:
      sedcommand = "sed -i '"+sedstr[0:-1]+"' "+slafile
   #
   if ("'" in sedstr and '"' in sedstr):
      print("Cannot execute sed command due to quote characters!")
      break
   #
   os.system("cp Buecherkarten_template_v004.sla "+slafile)
   os.system(sedcommand)
   os.system("scribus -g -py to-pdf.py -- "+slafile)
   pdflist = pdflist + newfile+".pdf "

# alle tempfiles erzeugt, jetzt mergen
#os.system("pdfunite "+pdflist+"buecherkarten_neuerwerbungen_2025-06-15.pdf")
os.system("pdfunite "+pdflist+"buecherkarten_neuerwerbungen_2025-08-11.pdf")

####### Testing area for python CLI
linklist = []
for item in soup.find_all(attrs={'class': 'link'}):
   for link in item.find_all('a'):
      linklist.append(link.get('href'))

https://portal.dnb.de/opac/showFullRecord?currentResultId=9783774255715%26any&currentPosition=0
https://portal.dnb.de/opac/showFullRecord?currentResultId=9783440177235%26any&currentPosition=0


wichtig fuer martina:
verlag
zeitliche einordnung
Titel
person(en)
sachgruppe(n)

# Cover laden ueber diese URL.
# size: s, m, l
#https://portal.dnb.de/opac/mvb/cover?isbn=9783742319401&size=m
