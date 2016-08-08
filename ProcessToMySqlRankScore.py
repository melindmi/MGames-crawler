import ExtractInfo
import MySQLdb 
f = open('AllGamesUrls.txt', 'r')
list = f.readlines()

start=11402
urlToParseList=list[start:11403]
label=['Title', 'Publish By', 'Develeoped By', 'Released', 'Platform', 'Genre', 'Perspective', 'Sport', 'Non Sport', 'Misc', 'Rank', 'Score', 'Alternate Titles', 'Part of the Groups', 'The Press Says ','Release Info']

conn = MySQLdb.connect (host = "localhost",
                        user = "root",
                        passwd = "melinda",
                        db = "mobygames")

cursor = conn.cursor()
idx=start+1
pltfIdx=1

for i in urlToParseList:
  print "%s %s" %(idx, i)
  g = ExtractInfo.MobyRankScore(i)

  #Moby Rank Score Press
  rspress=g.getMobyRankScorePress();
  for j in rspress.keys():
    if(j[1] != ''):
      sel="select * from Platform where name='"+j[1].replace("'","''")+"';"
      cursor.execute(sel)
      id=cursor.fetchone()
      if(id is None):
        print "ERROR! No platform found to insert Rating query16!!!!"
      else:
        query16="insert into GameRankScorePress(gameId, platformId, press, rankscore) values("+str(idx)+","+str(id[0])+",'"+j[0].replace("'","''")+"','"+rspress[j][0]+"');"
    else:
      query16="insert into GameRankScorePress(gameId, platformId, press, rankscore) values("+ str(idx)+","+"NULL"+",'"+j[0].replace("'","''")+"','"+rspress[j][0]+"');"
    try:
      cursor.execute(query16)
    except:
      print "INFO: Exception query16!!"
      print query16
  
  #Moby Rank Score Users
  rsusers=g.getMobyRankScoreUsers();
  if(len(rsusers.keys()) == 1):
    j=rsusers.keys()[0];
    if(j=='Platform'):
      for k in rsusers[j]:
        sel="select * from Platform where name='"+k[0].replace("'","''")+"';"
        cursor.execute(sel)
        id=cursor.fetchone()
        if(id is None):
          print "ERROR! No platform found to insert Rating query17!!!!"
        else:
          query17="insert into GameRankScoreUsers(gameId, platformId, category, score) values("+str(idx)+","+str(id[0])+",'"+"NULL"+"','"+k[1]+"');"
          try:
            cursor.execute(query17)
          except:
            print "INFO: Exception query17!!"
            print query17
    elif(j=='Category'):
      for k in rsusers[j]:
        query17="insert into GameRankScoreUsers(gameId, platformId, category, score) values("+str(idx)+","+"NULL"+",'"+k[0].replace("'","''")+"','"+k[1]+"');"
        try:
          cursor.execute(query17)
        except:
          print "INFO: Exception query17!!"
          print query17
  else:
    print "Info! no moby rank score from users found query17!"

  idx=idx+1

cursor.close()
conn.close()
  #w.writerow([o.getTitle()[0]]+[concatRelease(o,'publishBy')]+ [concatRelease(o,'developedBy')] + [concatRelease(o,'released')] + [concatRelease(o,'platform')] + [concatGenre(o,'genre')]+ [concatGenre(o,'perspective')]+ [concatGenre(o,'sport')]+ [concatGenre(o,'nonsport')]+ [concatGenre(o,'misc')]+[concatMobyRankScore(o,'rank')]+[concatMobyRankScore(o,'score')]+[concatAllMainInfo(o,'altTitles')]+[concatAllMainInfo(o,'partGroup')]+[concatAllMainInfo(o,'pressSays')]+[concatAllReleaseInfo(d)])


