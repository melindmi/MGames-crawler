import ExtractInfo
import MySQLdb 
f = open('NewAllGamesUrls.txt', 'r')
list = f.readlines()

start=33561
urlToParseList=list[start:33562]
#urlToParseList=list[start:15]
label=['Title', 'Publish By', 'Developed By', 'Released', 'Platform', 'Genre', 'Perspective', 'Sport', 'Non Sport', 'Misc', 'Rank', 'Score', 'Alternate Titles', 'Part of the Groups', 'The Press Says ','Release Info']

conn = MySQLdb.connect (host = "localhost",
                        user = "root",
                        passwd = "melinda",
                        db = "newMobygames")

cursor = conn.cursor()
idx=start+1
pltfIdx=0

for i in urlToParseList:
  print "%s %s" %(idx, i)
  o = ExtractInfo.GameInfo(i)
  d = ExtractInfo.ReleaseInfo(i)
  g = ExtractInfo.MobyRankScore(i)
  rs = ExtractInfo.RatingSystems(i)

  #Main page  
  query1="insert into Games(id, title, releaseDate) values("+str(idx)+", '"+o.getTitle()[0].replace("'","''")+"', '"+o.getGameRelease()['released'][0]+"');"
  try:
    cursor.execute(query1)
  except :
    print("Info: Exception query1: ")
    print (query1) 
  
  for j in o.getGameRelease()['platform']:
    sel="select id from Platform where name='"+j.replace("'","''")+"';"
    cursor.execute(sel)
    newPltfId=cursor.fetchone()
    if(newPltfId is None):
      query2="insert into Platform(name) values('"+j.replace("'","''")+"');"
      try:
        cursor.execute(query2)
        newPltfId = pltfIdx+1
        pltfIdx=pltfIdx+1
      except :
        print("Info: Exception query2: ")
        print (query2)
    else:
      #when the fetchone return someting it will be in a form of a tale, as ex: (3L,)
      #we must take only the number so at the position 0
      newPltfId = newPltfId[0]
    if(j in o.getMobyRankScore().keys()):
      query3="insert into GamePlatformRankScore(gameId, platformId, rank, score) values("+str(idx)+","+str(newPltfId)+","+str(o.getMobyRankScore()[j][0].replace("...", "NULL"))+","+str(o.getMobyRankScore()[j][1].replace("...", "NULL"))+");"
    else:
      query3="insert into GamePlatformRankScore(gameId, platformId, rank, score) values("+str(idx)+","+str(newPltfId)+",NULL, NULL);"
    try: 
      cursor.execute(query3)
    except:    
      print("Info: Exception query3: ")
      print(query3)

  for k in o.getGameRelease()['publishBy']:
    query4="insert into GamePublish(gameId, publish) values("+str(idx)+",'"+k.replace("'","''")+"');"
    try:
      cursor.execute(query4)
    except:
      print("Info: Exception query4: ")
      print(query4)
  
  for k in o.getGameRelease()['developedBy']:
    query5="insert into GameDeveloped(gameId, developed) values("+str(idx)+",'"+k.replace("'","''")+"');"
    try:
      cursor.execute(query5)
    except:
      print("Info: Exception query5: ")
      print(query5)

  for k in o.getGameGenre()['genre']:
    query6="insert into GameGenre(gameId, genre) values("+str(idx)+",'"+k.replace("'","''")+"');"
    try:
      cursor.execute(query6)
    except:
      print("Info: Exception query6: ")
      print(query6)
  
  for k in o.getGameGenre()['perspective']:
    query7="insert into GamePerspective(gameId, perspective) values("+str(idx)+",'"+k.replace("'","''")+"');"
    try:
      cursor.execute(query7)
    except:
      print("Info: Exception query7: ")
      print(query7)
  
  for k in o.getGameGenre()['sport']:
    query8="insert into GameSport(gameId, sport) values("+str(idx)+",'"+k.replace("'","''")+"');"
    try:
      cursor.execute(query8)
    except:
      print("Info: Exception query8: ")
      print(query8)
  
  for k in o.getGameGenre()['nonsport']:
    query9="insert into GameNonSport(gameId, nonsport) values("+str(idx)+",'"+k.replace("'","''")+"');"
    try:
      cursor.execute(query9)
    except:
      print("Info: Exception query9: ")
      print(query9)
  
  for k in o.getGameGenre()['misc']:
    query10="insert into GameMisc(gameId, misc) values("+str(idx)+",'"+k.replace("'","''")+"');"
    try:
      cursor.execute(query10)
    except:
      print("Info: Exception query10: ")
      print (query10)
  
  for k in o.getAllMainInfo()['altTitles']:
    query11="insert into GameAlternateTitle(gameId, altTitle) values("+str(idx)+",'"+(unicode(k, errors='replace').encode('ascii', 'replace').replace('?', ' ')).replace("'","''")+"');"
    #print query11
    try:
      cursor.execute(query11)
    except:
      print("Info: Exception query11: ")
      print (query11)

  for k in o.getAllMainInfo()['partGroup']:
    query12="insert into GamePartOfGroups(gameId, partGroup) values("+str(idx)+",'"+k.replace("'","''")+"');"
    try:
      cursor.execute(query12)
    except:
      print("Info: Exception query12: ")
      print (query12)
  
  for k in o.getAllMainInfo()['pressSays']:
    sel="select id from Platform where name='"+k[1].replace("'","''")+"';"
    cursor.execute(sel)
    id=cursor.fetchone()
    if(id is None):
      query13="insert into GamePressSaysMain(gameId, platformId, press, score) values("+str(idx)+",NULL,'"+k[0].replace("'","''")+"',"+k[2]+");"
    else:
      query13="insert into GamePressSaysMain(gameId, platformId, press, score) values("+str(idx)+","+str(id[0])+",'"+k[0].replace("'","''")+"',"+k[2]+");"
    try:
      cursor.execute(query13)
    except:
      print("Info: Exception query13: ")
      print (query13)

 #Release Info 
  dic = d.getReleaseInfo()
  for pltf in dic.keys():
      sel="select id from Platform where name='"+pltf.replace("'","''")+"';"
      cursor.execute(sel)
      id=cursor.fetchone()
      if(id is None):
        print "ERROR! No platform found to insert ReleseInfo query14!!!!"
      else:
        list=dic[pltf]
        for l in list:
          r=l['Release']
          c=l['Country']
          d=l['DevelopedBy']
          p=l['PublishBy']
          if (len(r) != len(c)):
            print("ERROR! Country and Release have different length - query14!!")
          elif(len(d)>1):
            print("ERROR! DevelopedBy have more then one value - query14!!!")
          elif(len(p)>1):
            print("ERROR! PublishBy have more then one value - query14!!!")
          else:  
            x=0
            while x < len(r):
              if (len(d)==0):
                dev="NULL"
              else:
                dev=d[0].replace("'","''")  
              if(len(p)==0):
                pub="NULL"
              else:
                pub=p[0].replace("'","''")
              query14 = "insert into GameReleaseInfo(gameId, platformId, publish, developed, country, releaseDate) values("+str(idx)+","+str(id[0])+",'"+pub+"','"+dev+"','"+c[x].replace("'","''")+"','"+r[x].replace("'","''")+"');"
              try:
                cursor.execute(query14)
              except :
                print "INFO: Same Pltf, Pub, Dev, Release, Country twice!!"
                
              x=x+1

  #Rating system
  rate=rs.getRatings();
  for j in rate.keys():
    sel="select * from Platform where name='"+j.replace("'","''")+"';"
    cursor.execute(sel)
    id=cursor.fetchone()
    if(id is None):
        print "ERROR! No platform found to insert Rating query15!!!!"
    else:
      for s in rate[j].keys():
        query15="insert into GameRatingSys(gameId, platformId, system, value) values("+str(idx)+","+str(id[0])+",'"+s.replace("'","''")+"','"+rate[j][s]+"');"
        try:
          cursor.execute(query15)
        except :
          print "INFO: Exception query15!!"
          print query15

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
      sel="select platformId from GameReleaseInfo where gameId="+ str(idx) +";"
      cursor.execute(sel)
      id=cursor.fetchone()
      if(id is None):
        print "ERROR! No platform found in GamePlatformRankScore to insert Rating query17!!!!"
        id[0]='NULL'
      for k in rsusers[j]:
        query17="insert into GameRankScoreUsers(gameId, platformId, category, score) values("+str(idx)+","+str(id[0])+",'"+k[0].replace("'","''")+"','"+k[1]+"');"
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


