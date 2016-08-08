import ExtractInfo
import MySQLdb 
f = open('NewAllGamesUrls.txt', 'r')
list = f.readlines()

start=0
urlToParseList=list[start:33562]
label=['Title', 'Publish By', 'Develeoped By', 'Released', 'Platform', 'Genre', 'Perspective', 'Sport', 'Non Sport', 'Misc', 'Rank', 'Score', 'Alternate Titles', 'Part of the Groups', 'The Press Says ','Release Info']

conn = MySQLdb.connect(host = "localhost",
                        user = "root",
                        passwd = "melinda",
                        db = "renewMobygames")

cursor = conn.cursor()
idx=start+1
pltfIdx=0
riId=0


for i in urlToParseList:
  print ("%s %s" % (idx, i))
  d = ExtractInfo.ReleaseInfo(i)
  
  qqq="select count(*) from DevelopedId;"
  rrr="select count(*) from PublishId;"
  cursor.execute(qqq)
  devIdx=cursor.fetchone()
  cursor.execute(rrr)
  pubIdx=cursor.fetchone()

 #Release Info 
  dic = d.getReleaseInfo()
  #print ("%s" %dic)
  for pltf in dic.keys():
      sel="select id from Platform where name='"+pltf.replace("'","''").encode('latin-1')+"';"
      cursor.execute(sel)
      id=cursor.fetchone()
      if(id is None):
        print ("ERROR! No platform found to insert ReleseInfo query14!!!!")
      else:
        list=dic[pltf]
        for l in list:
          riId = riId + 1
          #Insert ReleaseId, GameId, PlatformId 
          insRel="insert into ReleaseIdGamePlatform(relId, gameId, platformId) values(" + str(riId) + "," + str(idx) +"," + str(id[0]) + ");"
          try:
           cursor.execute(insRel)
          except :
           print("ERROR! Same RelId twice!!")
          
          r=l['Release']
          c=l['Country']
          d=l['DevelopedBy']
          p=l['PublishBy']
          
          for pub in p:
            selPub="select id from PublishId where publish='"+pub.replace("'","''").encode('latin-1')+"';"
            #print("INFO selPub: %s" %selPub)
            cursor.execute(selPub)
            idPub=cursor.fetchone()
            if(idPub is None):
              print ("INFO! No PublishedBy found to insert ReleseInfo query14. Insert pub: %s !!!!" % pub)
              insPubId="insert into PublishId(id, publish) values(" + str(pubIdx) + ", '" + pub.replace("'","''")+ "');"
              insGamePub="insert into GamePublish(gameId, publish, publishId) values(" + str(idx) + ", '" + pub.replace("'","''")+ "'," + str(pubIdx) + ");"
              insPub = "insert into ReleasePublish(relId, publishId) values(" + str(riId) + "," + str(pubIdx)+");"
      
              try:
                cursor.execute(insPubId)
              except:
                print("ERROR! When inserting new Publish in PublishId!!")
              try:
                cursor.execute(insGamePub)
              except:
                print("ERROR! When inserting new Publish in GamePublish!!")
               
              try:
                cursor.execute(insPub)
              except:
                print("ERROR! When inserting new Publish in ReleasePublish!!")
               
              pubIdx = pubIdx + 1
                        
            else:
              insPub = "insert into ReleasePublish(relId, publishId) values(" + str(riId) + "," + str(idPub[0])+");"
              try:
                cursor.execute(insPub)
              except :
                print "ERROR! Same RelId, publishId twice!!"
   
          for dev in d:
 #           print("INFO: dev: %s " % dev.encode('latin-1', 'replace'))
          #  print("INFO: dev: %s " % dev.unicode(dev,'latin-1', 'replace'))
            selDev="select id from DevelopedId where developed='"+dev.decode('ascii', 'replace')+"';"
            cursor.execute(selDev)
            idDev=cursor.fetchone()
            if(idDev is None):
              print ("INFO! No DevelopedBy found to insert ReleseInfo query14. Insert dev: %s !!!!" % dev)
              insDevId="insert into DevelopedId(id, developed) values(" + str(devIdx) + ", '" + dev.replace("'","''")+ "');"
              insGameDev="insert into GameDeveloped(gameId, developed, developedId) values(" + str(idx) + ", '" + dev.replace("'","''")+ "'," + str(devIdx) + ");"
              insDev = "insert into ReleaseDeveloped(relId, developedId) values(" + str(riId) + "," + str(devIdx)+");"
              try:
                cursor.execute(insDevId)
              except:
                print("ERROR! When inserting new Developed in DevelopedId!!")
              try:
                cursor.execute(insGameDev)
              except:
                print("ERROR! When inserting new Developed in GameDeveloped!!")
              
              try:
                cursor.execut(insDev)
              except:
                print("ERROR! When inserting new Developed in DevelopedId!!")
              
              devIdx = devIdx + 1
            else:
              insDev = "insert into ReleaseDeveloped(relId, developedId) values(" + str(riId) + "," + str(idDev[0])+");"
              try:
                cursor.execute(insDev)
              except :
                print "ERROR! Same RelId, developedId twice!!"
          
          for cou in c:
            insCou = "insert into ReleaseCountry(relId, country) values(" + str(riId) + ",'" + cou.replace("'","''")+"');"
            try:
              cursor.execute(insCou)
            except :
              print "ERROR when tring to insert RelId, Country !!"
          
          for relD in r:
            insRelD = "insert into ReleaseDate(relId, date) values(" + str(riId) + ",'" + relD.replace("'","''")+"');"
            try:
              cursor.execute(insRelD)
            except :
              print "ERROR when tring to insert RelId, Date !!"

  idx=idx+1
  conn.commit()

cursor.close()
conn.close()
  #w.writerow([o.getTitle()[0]]+[concatRelease(o,'publishBy')]+ [concatRelease(o,'developedBy')] + [concatRelease(o,'released')] + [concatRelease(o,'platform')] + [concatGenre(o,'genre')]+ [concatGenre(o,'perspective')]+ [concatGenre(o,'sport')]+ [concatGenre(o,'nonsport')]+ [concatGenre(o,'misc')]+[concatMobyRankScore(o,'rank')]+[concatMobyRankScore(o,'score')]+[concatAllMainInfo(o,'altTitles')]+[concatAllMainInfo(o,'partGroup')]+[concatAllMainInfo(o,'pressSays')]+[concatAllReleaseInfo(d)])


