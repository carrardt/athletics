#!/usr/bin/python3

import urllib.request
from html.parser import HTMLParser
import os

def strToHex(id):
  s=""
  for c in str(id):
    s = s + str( 99 - ord(c) )
    s = s + str( ord(c) )
  return s

class FFAAthleteHTMLParser(HTMLParser):
  def __init__(self):
    self.m_db={}
    self.m_club_flag = 0
    super().__init__()
  def handle_data(self, data):
#    print("Data '%s'" % data)
    if self.m_club_flag==0 and data=='Club':
      self.m_club_flag = 1
    elif self.m_club_flag==1 and data==':':
      self.m_club_flag = 2
    elif self.m_club_flag==2:
      self.m_club_flag = 3
    elif self.m_club_flag==3:
      da = data.split(' - ')
      self.m_db["num_club"] = da[0]
      self.m_db["nom_club"] = da[1]
      if len(da) >= 3:
        self.m_db["nom_sl"] = da[2]
      else:
        self.m_db["nom_sl"] = "N/A"
      self.m_club_flag = 999
  def db(self):
    return self.m_db
    
def ffa_athlete(id):
    URL_FMT = "https://bases.athle.fr/asp.net/athletes.aspx?base=resultats&seq=%s"
    parser = FFAAthleteHTMLParser()
    parser.feed( urllib.request.urlopen( URL_FMT % strToHex(id) ).read().decode('utf-8') )
    return parser.db()

class FFAResultsHTMLParser(HTMLParser):
  def __init__(self):
    self.m_db=[]
    self.m_current_row=[]
    self.m_seq_id="-1"
    self.m_cell_enable=False
    super().__init__()
  def handle_starttag(self, tag, attrs):
    if tag=="tr":
      self.m_current_row=[]
      self.m_seq_id="-1"
    elif tag=="td":
      self.m_cell_enable=True
    elif tag=="a":
      for (k,v) in attrs:
        if k=="href" and v.startswith("javascript:bddThrowAthlete('resultats'"):
          self.m_seq_id = v.split(',')[1].strip()
  def handle_endtag(self, tag):
    if tag=="tr":
      self.m_db.append(self.m_current_row+[self.m_seq_id])
    elif tag=="td":
      self.m_cell_enable=False
  def handle_data(self, data):
    if self.m_cell_enable:
      self.m_current_row.append(data)
  def db(self):
    return self.m_db

def ffa_club_resultats(saison,numclub,sexe):
  print( "Requette FFA : saison %d , club %s , sexe %s" % (saison,numclub,sexe) )
  URL_FMT="https://bases.athle.fr/asp.net/liste.aspx?frmpostback=true&frmbase=resultats&frmmode=1&frmespace=0&frmsaison=%d&frmclub=%s&frmnom=&frmprenom=&frmsexe=%s&frmlicence=&frmdepartement=&frmligue=&frmcomprch=&frmposition=%d"
  parser = FFAResultsHTMLParser()
  parser.feed( urllib.request.urlopen( URL_FMT % (int(saison),numclub,sexe,0) ).read().decode('utf-8') )
  db = parser.db()
  num_pages = 1
  header = db[0]
  if len(header)>2 and header[2].find('Page')==0:
    num_pages = int(db[0][2].split('/')[1][:3])
  db = db[3:-1]
  print("\tPage 1 chargée, %d page(s) au total"%(num_pages))
  for i in range(1,num_pages):
    print("\tLecture page %d"%(i+1))
    parser = FFAResultsHTMLParser()
    parser.feed( urllib.request.urlopen( URL_FMT % (int(saison),numclub,sexe,i) ).read().decode('utf-8') )
    db.extend( parser.db()[3:-1] )
  for r in db:
    s = r[2]
    s = s.replace(' - Salle',' En Salle')
    s = s.replace('-Salle',' En Salle')
    s = s.split('/')[0].split('-')[0]
    r[2] = s
  return db

def ffa_club_saison(saison,listeclubs):
  db = []
  for sexe in [ 'F' , 'M' ]:
    for club in listeclubs:
      for r in ffa_club_resultats(saison,club,sexe):
        r.extend( [ club , sexe , saison ] )
        db.append(r)
  return db;

def load_cache_athletes():
  db_dirname = "cache/athletes"
  db_fname = db_dirname+"/seq_id.csv"
  try:
    os.makedirs(db_dirname)
  except:
    print(db_dirname,"exists")
  athletes_db={}
  try:
    os.stat(db_fname)
    fin = open(db_fname,"r")
    for l in [ r.split(';') for r in fin.readlines() ]:
      print("readline",l)
      athletes_db[ l[0] ] = l[1]
  except:
    print("Pas de cache pour les athletes")
  return athletes_db

def write_cache_athletes(athletes_db):
  db_dirname = "cache/athletes"
  db_fname = db_dirname+"/seq_id.csv"
  try:
    os.makedirs(db_dirname)
  except:
    print(db_dirname,"exists")
  fout = open(db_fname,"w")
  for r in athletes_db.items():
    print(r)
    fout.write( ' ; '.join( [ str(x) for x in r ] ) + '\n' )
  fout.close()
  fout = None

if __name__=='__main__':
  athletes_db = load_cache_athletes()
  saison = 2024
  clubs = [ '091083' , '091013' ]
  db = ffa_club_saison(saison,clubs)
  fout = open('saison_%d.csv'%saison,"w")
  for r in db:
    f = ' ; '.join( [ str(x) for x in r ] )
    fout.write( f + '\n' )
    print("Ajout athlete '%s' -> '%s'" % (r[-4],r[1]) )
    athletes_db[ r[-4] ] = r[1]
  fout.close()
  fout = None
  print(athletes_db)
  write_cache_athletes(athletes_db)

