import ExtractInfo
import urllib2
import libxml2dom
import csv

mobygame = urllib2.urlopen("http://www.mobygames.com/browse/games/list-games/").read()
file = open("AllGamesUrls.txt", 'w')

for firstUrls in ExtractInfo.getUrlList(mobygame):
  file.write("http://www.mobygames.com"+firstUrls+"\n")

next=ExtractInfo.getNextUrls(mobygame)
while len(next) == 1:
  urlNext = urllib2.urlopen("http://www.mobygames.com"+next[0]).read()
  urlList = ExtractInfo.getUrlList(urlNext)
  #urlToParseList=[]
  for url in urlList:
    file.write("http://www.mobygames.com"+url+"\n")
    #urlToParseList.append("http://www.mobygames.com"+url)
  next=ExtractInfo.getNextUrls(urlNext)  

file.close()
#w = csv.writer(file('data.csv', 'wb'))

#for i in urlToParseList:
#  o = ExtractInfo.GameInfo(i)
#  w.writerow(o.getTitle()+o.getGameRelease()['publishBy']+o.getGameRelease()['developedBy']+o.getGameRelease()['released']+o.getGameRelease()['platform']+o.getGameGenre()['genre']+o.getGameGenre()['perspective']+o.getGameGenre()['sport']+o.getGameGenre()['nonsport']+o.getGameGenre()['misc']+o.getDescription());

