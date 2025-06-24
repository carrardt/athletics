import urllib.request
from html.parser import HTMLParser

class FFAResultsHTMLParser(HTMLParser):
  def __init__(self):
    self.m_db=[]
    self.m_current_row=[]
    self.m_cell_enable=False
    super().__init__()
  def handle_starttag(self, tag, attrs):
    if tag=="tr":
      self.m_current_row=[]
    elif tag=="td":
      self.m_cell_enable=True
  def handle_endtag(self, tag):
    if tag=="tr":
      self.m_db.append(self.m_current_row)
    elif tag=="td":
      self.m_cell_enable=False
  def handle_data(self, data):
    if self.m_cell_enable:
      self.m_current_row.append(data)
  def db(self):
    return self.m_db

def ffa_results(saison,numclub,sexe):
  print("Requette FFA ...")
  URL_FMT="https://bases.athle.fr/asp.net/liste.aspx?frmpostback=true&frmbase=resultats&frmmode=1&frmespace=0&frmsaison=%d&frmclub=%s&frmnom=&frmprenom=&frmsexe=%s&frmlicence=&frmdepartement=&frmligue=&frmcomprch=&frmposition=%d"
  parser = FFAResultsHTMLParser()
  parser.feed( urllib.request.urlopen( URL_FMT % (int(saison),numclub,sexe,0) ).read().decode('utf-8') )
  db = parser.db()
  num_pages = 1
  header = db[0]
  if len(header)>2 and header[2].find('Page')==0:
    num_pages = int(db[0][2].split('/')[1][:3])
  db = db[3:-1]
  print("Page 1 chargée, %d page(s) au total"%(num_pages))
  for i in range(1,num_pages):
    print("lecture page %d"%(i+1))
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

#db = ffa_results(2025,'091013','M')
#print(db)
#print(len(db))

