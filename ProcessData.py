import ExtractInfo
import urllib2
import csv
import codecs

f = open('AllGamesUrls.txt', 'r')
list = f.readlines()
#urlToParseList = []
#urlToParseList.append(list[0])
urlToParseList=list[1:10]
label=['Title', 'Publish By', 'Developed By', 'Released', 'Platform', 'Genre', 'Perspective', 'Sport', 'Non Sport', 'Misc', 'Rank', 'Score', 'Alternate Titles', 'Part of the Groups', 'The Press Says ','Release Info']
w = csv.writer(file('data.csv', 'wb'))
w.writerow(label)

def concatRelease(o, name):
  p=o.getGameRelease()[name]
  rez=""
  j=1
  for i in p:
    rez=rez+i
    if(len(p)>j):
      rez=rez+", "
    j=j+1  
  return unicode(rez, errors='replace').encode('ascii', 'replace').replace('?', ' ')
 
def concatGenre(o, name):
  p=o.getGameGenre()[name]
  rez=""
  j=1
  for i in p:
    rez=rez+i
    if(len(p)>j):
      rez=rez+", "
    j=j+1  
  return unicode(rez, errors='replace').encode('ascii', 'replace').replace('?', ' ')

def concatAllMainInfo(o, name):
  p=o.getAllMainInfo()[name]
  rez=""
  j=1
  for i in p:
    rez=rez+i
    if(len(p)>j):
      rez=rez+", "
    j=j+1  
  return unicode(rez).encode('ascii', 'replace').replace('?', ' ')

def concatMobyRankScore(o, name):
  p=o.getMobyRankScore()[name]
  pltf=o.getMobyRankScore()['platform']
  rez=""
  j=1
  for i in p:
    rez=rez+pltf[j-1]+": "+i
    if (len(p)>j):
      rez=rez+", "
    j=j+1 
  return unicode(rez, errors='replace').encode('ascii', 'replace').replace('?',' ')


def concatAllReleaseInfo(d):
  p=d.getReleaseInfo()
  keys=p.keys()
  rez=""
  print keys
  for k in keys:
    h=k+":: "
    j=1
    r=""
    for i in p[k]:
      r=r+i
      if(len(p[k])>j):
        r=r+", "
      j=j+1
    r=h+r
    rez=rez+r
  
  return unicode(rez).encode('ascii', 'replace').replace('?', ' ')

for i in urlToParseList:
  print i
  o = ExtractInfo.GameInfo(i)
  d = ExtractInfo.ReleaseInfo(i)
  g = ExtractInfo.MobyRankScore(i)
  r = ExtractInfo.RatingSystems(i)
  #print g.getMobyRankScorePress()
  print g.getMobyRankScoreUsers()
  #print r.getRatings()
  #print d.getReleaseInfo()
  #print o.getAllMainInfo()['pressSays']
  #print o.getTitle()[0]
  #w.writerow([o.getTitle()[0]]+[concatRelease(o,'publishBy')]+ [concatRelease(o,'developedBy')] + [concatRelease(o,'released')] + [concatRelease(o,'platform')] + [concatGenre(o,'genre')]+ [concatGenre(o,'perspective')]+ [concatGenre(o,'sport')]+ [concatGenre(o,'nonsport')]+ [concatGenre(o,'misc')]+[concatMobyRankScore(o,'rank')]+[concatMobyRankScore(o,'score')]+[concatAllMainInfo(o,'altTitles')]+[concatAllMainInfo(o,'partGroup')]+[concatAllMainInfo(o,'pressSays')]+[concatAllReleaseInfo(d)])

  #w.writerow(o.getTitle()+o.getGameRelease()['publishBy']+o.getGameRelease()['developedBy']+o.getGameRelease()['released']+o.getGameRelease()['platform']+o.getGameGenre()['genre']+o.getGameGenre()['perspective']+o.getGameGenre()['sport']+o.getGameGenre()['nonsport']+o.getGameGenre()['misc']+[concatMobyRankScore(o,'rank')]+[concatMobyRankScore(o,'score')]);

