import urllib2
import libxml2dom
import codecs
import re

def getUrlList(mobygameUrl):
  doc = libxml2dom.parseString(mobygameUrl, html=1)
  """mof_object_list - id of the table containing the list of all games"""
  table = doc.getElementById("mof_object_list"); 
  urlList=[]
  if(table is None):
    print ("ERROR! No table found!")

  tbody = table.getElementsByTagName("tbody");  
  if(len(tbody) > 1):
    print ("ERROR! More then one tbody in table found!")
  elif(len(tbody) == 0):
    print ("ERROR! No tbody found")
  
  allTr = tbody[0].getElementsByTagName("tr");
  for tr in allTr:
    urlList.append(tr.getElementsByTagName("a")[0].getAttribute("href"))
  return urlList

def getNextUrls(mobygameUrl):
  nexturl = re.findall('<a href="([^"]*)">Next</a>', mobygameUrl)
  
  if(len(nexturl)>1):
    print ("ERROR! More then one Next button found!")
  elif (len(nexturl)==0):
    print ("No more Next!")
  
  return nexturl

class GameInfo():
  def __init__(self, gameUrl):
    openGame = urllib2.urlopen(gameUrl).read()
    self.docGame = libxml2dom.parseString(openGame, html=1)
  
  def getTitle(self):
    """gameTitle - id of the div containing 2 childs: the url of that game and the game title"""
    title=[]
    title.append(self.docGame.getElementById("gameTitle").childNodes[0].childNodes[0].nodeValue.encode("utf-8"))
    return title
  
  def getGameRelease(self):
    """coreGameRelease" - id of the div containing: Published by, Developed by, Released, and Platforms"""
    coreRelease = self.docGame.getElementById("coreGameRelease");
    #get index of publish by , developed by, release and platform in core div
    index=0
    indexPub=None
    indexD=None
    indexR=None
    indexPlf=None
    for child in coreRelease.childNodes:
        if (child.childNodes.length > 0):
          if(child.childNodes[0].nodeValue == "Published by"):
            indexPub = index
          elif(child.childNodes[0].nodeValue == "Developed by"):
            indexD = index
          elif(child.childNodes[0].nodeValue == "Released"):
            indexR = index
          elif(child.childNodes[0].nodeValue == "Platforms") or \
                (child.childNodes[0].nodeValue == "Platform"):
            indexPlf = index
        index = index+1
    #print "%s %s %s %s" %(indexPub, indexD, indexR, indexPlf) 
    publishBy=[];
    developedBy=[];
    released=[];
    platform=[];
    if(indexPub is not None):
      for inChild in coreRelease.childNodes[indexPub+1].getElementsByTagName("a") :
         publishBy.append(inChild.childNodes[0].nodeValue.encode("utf-8"));
    if(indexD is not None):
      for inChild in coreRelease.childNodes[indexD+1].getElementsByTagName("a") :
         developedBy.append(inChild.childNodes[0].nodeValue.encode("utf-8"));
    if(indexR is not None):
      for inChild in coreRelease.childNodes[indexR+1].getElementsByTagName("a") :
         released.append(inChild.childNodes[0].nodeValue.encode("utf-8"));
    if(indexPlf is not None):
      for inChild in coreRelease.childNodes[indexPlf+1].getElementsByTagName("a") :
         platform.append(inChild.childNodes[0].nodeValue.encode("utf-8"));

    #print "%s;%s;%s;%s" %(publishBy, developedBy, released, platform) 
    return {'publishBy': publishBy, 'developedBy': developedBy, 'released': released, 'platform': platform}

  def getGameGenre(self):
    """coreGameGenre" - id for genre, perspective, sport ou non-sport and misc
    for core genre there is another div which encapsulate all"""
    coreGenre = self.docGame.getElementById("coreGameGenre").childNodes[0]; 
    #get index of genre and perspective in core div

    index=0
    indexGenre=None
    indexPersp=None
    indexSport=None
    indexNonSport=None
    indexMisc=None

    for child in coreGenre.childNodes:
        if (child.childNodes.length > 0):
          if(child.childNodes[0].nodeValue == "Genre"):
            indexGenre = index
          elif(child.childNodes[0].nodeValue == "Perspective"):
            indexPersp = index
          elif(child.childNodes[0].nodeValue == "Sport"):
            indexSport = index
          elif(child.childNodes[0].nodeValue == "Non-Sport"):
            indexNonSport = index
          elif(child.childNodes[0].nodeValue == "Misc"):
            indexMisc = index
        index = index+1
  
    #print "%s %s %s %s %s" %(indexGenre, indexPersp, indexSport, indexNonSport, indexMisc) 

    genre=[];
    perspective=[];
    sport=[];
    nonsport=[];
    misc=[];

    if(indexGenre is not None):
       for inChild in coreGenre.childNodes[indexGenre+1].getElementsByTagName("a") :
           genre.append(inChild.childNodes[0].nodeValue.encode("utf-8"));

    if(indexPersp is not None):
       for inChild in coreGenre.childNodes[indexPersp+1].getElementsByTagName("a") :
           perspective.append(inChild.childNodes[0].nodeValue.encode("utf-8"));

    if(indexSport is not None):
       for inChild in coreGenre.childNodes[indexSport+1].getElementsByTagName("a") :
           sport.append(inChild.childNodes[0].nodeValue.encode("utf-8"));

    if(indexNonSport is not None):
       for inChild in coreGenre.childNodes[indexNonSport+1].getElementsByTagName("a") :
           nonsport.append(inChild.childNodes[0].nodeValue.encode("utf-8"));

    if(indexMisc is not None):
       for inChild in coreGenre.childNodes[indexMisc+1].getElementsByTagName("a") :
           misc.append(inChild.childNodes[0].nodeValue.encode("utf-8"));

    #print "%s;%s;%s;%s;%s" %(genre, perspective, sport, nonsport, misc)
      
    return {'genre': genre, 'perspective': perspective, 'sport': sport, 'nonsport':nonsport, 'misc':misc}
    
  def getAllMainInfo(self):
    """get the description
    search for a div that has an attribut class="rightPanelMain"
    look into all its childrens. If the child name in text, then get the value
    Look for the h2 
    Alternate Titles
    Part of the Following Groups
    The Press Says
    """
    allDiv = self.docGame.getElementsByTagName("div")
    descDiv=None
    description=[];
    for div in allDiv:
        for atr in div.attributes:
            if(atr.nodeValue=="rightPanelMain"):
              descDiv=div

    #description deprecated
    #if(descDiv is not None):
    #    for child in descDiv.childNodes:
    #      if (child.nodeName=="text"):
    #        description.append(child.nodeValue.encode("utf-8"))
    h2=descDiv.getElementsByTagName("h2")
    j=0
    idxAltTitle=None
    idxGrpPart=None
    idxPress=None
    parent={}
    for h in h2:
        if h.firstChild.nodeValue == "Alternate Titles":
          parent['Alternate Titles']=h.parentNode
          idxAltTitle=j
        elif h.firstChild.nodeValue == "Part of the Following Groups":
         parent['Part of the Following Groups']=h.parentNode 
         idxGrpPart=j
        elif h.firstChild.nodeValue == "The Press Says":
          parent['The Press Says']=h.parentNode 
          idxPress=j
        j=j+1
    
    for val in parent.values():
      allCh=val.childNodes
      k=0
      for ch in allCh:
        if (idxAltTitle is not None and ch == h2[idxAltTitle]):
          idxT=k
        elif (idxGrpPart is not None and ch == h2[idxGrpPart]):
          idxG=k
        elif (idxPress is not None and ch == h2[idxPress]):
          idxP=k
        k=k+1

    #get Alternate Titles
    altTitles=[]
    if (idxAltTitle is not None):
      liT=parent['Alternate Titles'].childNodes[idxT+1].getElementsByTagName("li")
      for i in liT:
        if(i.lastChild.firstChild.nodeName == "text"):
          altTitles.append(i.firstChild.nodeValue.encode("utf-8") + i.lastChild.firstChild.nodeValue.encode("utf-8"))
        elif(i.lastChild.firstChild.firstChild.nodeName == "text"):
          altTitles.append(i.firstChild.nodeValue.encode("utf-8") + i.lastChild.firstChild.firstChild.nodeValue.encode("utf-8"))
        else:
          print("ERROR: Problems with alternate title!!!")

    
    #get Part of the Following Groups
    partGroup=[]
    if(idxGrpPart is not None):
      liG=parent['Part of the Following Groups'].childNodes[idxG+1].getElementsByTagName("li")
      for i in liG:
        partGroup.append(i.firstChild.firstChild.nodeValue.encode("utf-8"))

    #get The Press Says
    pressSays=[]
    if (idxPress is not None):
      tbody=parent['The Press Says'].childNodes[idxP+1].getElementsByTagName("tbody")
      if (tbody.length > 0):
        tr=tbody[0].getElementsByTagName("tr")
        for i in tr:
          info=[]
          td=i.getElementsByTagName("td")
          info.append(td[0].firstChild.firstChild.nodeValue.encode("utf-8"))
          info.append(td[1].firstChild.nodeValue.encode("utf-8"))
          info.append(td[len(td)-1].firstChild.nodeValue.encode("utf-8"))
          pressSays.append(info)

    return {'altTitles': altTitles, 'partGroup': partGroup, 'pressSays': pressSays}

  def getMobyRankScore(self): 
    """coreGameRank is the id for the MobyRank div
    coreGameScore is the id for the MobyScore div 
    gamePlatform is the id for the platform name for which are the rank/score"""
    rankscore={}
    if self.docGame.getElementById("gamePlatform") is not None:
        rank = self.docGame.getElementById("coreGameRank").childNodes[0].childNodes[1].childNodes[1].childNodes[1].childNodes[0].childNodes[1].childNodes[0].nodeValue.encode("utf-8")
        score = self.docGame.getElementById("coreGameScore").childNodes[1].childNodes[0].nodeValue.encode("utf-8")
        rankscore[self.docGame.getElementById("gamePlatform").childNodes[0].childNodes[0].nodeValue.encode("utf-8")]=[rank, score]
    else:
        for i in self.docGame.getElementById("coreGameRank").getElementsByTagName("tbody")[0].getElementsByTagName("tr"):
          td = i.getElementsByTagName("td")
          if td.length==3:
            rank = td[1].firstChild.firstChild.firstChild.nodeValue.encode("utf-8")
            score = td[2].firstChild.firstChild.firstChild.nodeValue.encode("utf-8")
            rankscore[td[0].firstChild.nodeValue.encode("utf-8")] = [rank, score]
    
    return rankscore    


class ReleaseInfo():
  def __init__(self, gameUrl):
    openGame = urllib2.urlopen(gameUrl.replace("\n","")+"/release-info").read()
    self.docGame = libxml2dom.parseString(openGame, html=1)
  
  def getReleaseInfo(self):
    allDiv = self.docGame.getElementsByTagName("div")
    descDiv=None
    for div in allDiv:
      for atr in div.attributes:
        if(atr.nodeValue=="rightPanelMain"):
          descDiv=div
            
    h2=descDiv.getElementsByTagName("h2")
    allCh=descDiv.childNodes
    k=0
    pos={}
    for ch in allCh:
      for h in h2:
        if (ch == h):
         pos[h.firstChild.nodeValue]=k 
      k=k+1
    
    releaseInfo={}
    allpos=pos.values()
    allpos.sort()
    allpos.append(allCh.length)
    for p in pos.keys():
      releaseInfo[p.encode("utf-8")]=[]
    i=0
    gr={}
    gr["PublishBy"]=[]
    gr["DevelopedBy"]=[]
    gr["Country"]=[]
    gr["Release"]=[]
    while i < len(allpos)-1:
      divList = descDiv.childNodes[allpos[i]+1:allpos[i+1]]
      foundStyle="false"
      dic=[]
      for d in divList:
        if d.hasAttribute("class"):
          if(foundStyle=="true"):
            dic.append(gr)
            foundStyle="false"
            gr={}
            gr["PublishBy"]=[]
            gr["DevelopedBy"]=[]
            gr["Country"]=[]
            gr["Release"]=[]
          if d.firstChild.firstChild.nodeValue=="Published by":
            allDChilds=d.childNodes 
            aChNb=0
            for iii in allDChilds:
              if iii.hasAttribute("href"):
                aChNb = aChNb + 1
                gr["PublishBy"].append(iii.firstChild.nodeValue.encode("utf-8"))
                #gr["PublishBy"].append(d.lastChild.firstChild.nodeValue.encode("utf-8"))
          elif d.firstChild.firstChild.nodeValue=="Developed by":
            allDChilds=d.childNodes 
            aChNb=0
            for iii in allDChilds:
              if iii.hasAttribute("href"):
                aChNb = aChNb + 1
                gr["DevelopedBy"].append(iii.firstChild.nodeValue.encode("utf-8"))
                #gr["DevelopedBy"].append(d.lastChild.firstChild.nodeValue.encode("utf-8"))
        elif d.hasAttribute("style"):
          foundStyle="true"
          for info in d.childNodes:
            if info.nodeName=="div":
              if info.firstChild.firstChild.nodeValue=="Country" or info.firstChild.firstChild.nodeValue=="Countries":
                span=info.childNodes[1].getElementsByTagName("span")
                ctr = len(span)
                for s in span:
                  if(len(s.childNodes)>0):
                    gr["Country"].append(s.lastChild.nodeValue.encode("utf-8"))
                  else:
                    gr["Country"].append("NULL")
              elif(info.firstChild.firstChild.nodeValue=="Release Date"):
                nb=0
                while nb < ctr:
                  if(len(info.childNodes)>0):
                    try:  
                      gr["Release"].append(info.childNodes[1].firstChild.nodeValue.encode("utf-8"))
                    except:  
                      print("Info: Release without info! ")
                    nb=nb+1

      dic.append(gr)
      ctr=0
      gr={}
      gr["PublishBy"]=[]
      gr["DevelopedBy"]=[]
      gr["Country"]=[]
      gr["Release"]=[]

      releaseInfo[h2[i].firstChild.nodeValue]=dic
      i=i+1

    return releaseInfo  
  

class MobyRankScore():
  def __init__(self, gameUrl):
    openGame = urllib2.urlopen(gameUrl.replace("\n","")+"/mobyrank").read()
    self.docGame = libxml2dom.parseString(openGame, html=1)
  
    allDiv = self.docGame.getElementsByTagName("div")
    self.descDiv=None
    for div in allDiv:
      for atr in div.attributes:
        if(atr.nodeValue=="rightPanelMain"):
          self.descDiv=div
    

  def getMobyRankScorePress(self):
    rankscorepress={}
    score=[]
    source=[]
    platform=[]
    ch=self.descDiv.childNodes
    for d in ch:
      if (d.nodeName=="div" and d.hasAttribute("class")):
        if(d.getAttribute("class")=="floatholder mobyrank scoresource"):
          score.append(d.childNodes[1].firstChild.nodeValue.encode("utf-8"))
          if(d.childNodes[3].childNodes.length == 2):
            source.append(d.childNodes[3].childNodes[1].nodeValue.encode("utf-8"))
            platform.append(d.childNodes[3].firstChild.firstChild.nodeValue.encode("utf-8"))
          elif(d.childNodes[3].childNodes.length == 1):
            source.append(d.childNodes[3].firstChild.nodeValue.encode("utf-8"))
            platform.append("")

    
    idx=0
    for i in source:
      rankscorepress[i, platform[idx]]=[score[idx]]
      idx=idx+1
    
    return rankscorepress
    
  def getMobyRankScoreUsers(self):
    uservotescore={}
    category=[]
    score=[]
    platform=[]
    found="false";
    ch=self.descDiv.childNodes
    for d in ch:
      if (d.nodeName=="div" and d.hasAttribute("class")):
        if(d.getAttribute("class")=="floatholder"):
          table=d.getElementsByTagName("table")
          if (table.length > 0):
            if(table[0].hasAttribute("class")):
              if(table[0].getAttribute("class")=="reviewList pct100"):
                found="true"
                thead=table[0].getElementsByTagName("thead")
                th=thead[0].getElementsByTagName("th")
                tbody=table[0].getElementsByTagName("tbody")
                tr=tbody[0].getElementsByTagName("tr")
                for i in tr:
                  td=i.getElementsByTagName("td")
                  if (td.length == 3):
                    if (th[0].firstChild.nodeValue=="Platform"):
                      platform.append(td[0].firstChild.nodeValue.encode("utf-8"))
                    elif (th[0].firstChild.nodeValue=="Category"):
                      category.append(td[0].firstChild.nodeValue.encode("utf-8"))
                    else:
                      print("ERROR: Our Users Say table is different!!")
                    
                    score.append(td[2].firstChild.nodeValue.encode("utf-8"))
                  else:
                    print("Info: Our Users Say line table does not have 3 columns!!")
    
    if found=="true":
      idx=0
      list=[]
      if len(platform)==0:
        for j in category:
          list.append([j, score[idx]])
          idx=idx+1
        uservotescore["Category"] = list
      elif len(category)==0:
        for j in platform:
          list.append([j, score[idx]])
          idx=idx+1
        uservotescore["Platform"] = list
    
    return uservotescore


class RatingSystems():
  def __init__(self, gameUrl):
    openGame = urllib2.urlopen(gameUrl.replace("\n","")+"/rating-systems").read()
    self.docGame = libxml2dom.parseString(openGame, html=1)
  
    allDiv = self.docGame.getElementsByTagName("div")
    self.descDiv=None
    for div in allDiv:
      for atr in div.attributes:
        if(atr.nodeValue=="rightPanelMain"):
          self.descDiv=div
   

  def getRatings(self):
    h2=self.descDiv.getElementsByTagName("h2")
    allCh=self.descDiv.childNodes
    k=0
    pos={}
    for ch in allCh:
      for h in h2:
        if (ch == h):
         pos[h.firstChild.nodeValue]=k 
      k=k+1
    
    rating={}
    for p in pos.keys():
      rating[p.encode("utf-8")]={}
      if(self.descDiv.childNodes[pos[p]+1].nodeName=="table"):
        tr=self.descDiv.childNodes[pos[p]+1].getElementsByTagName("tr")
        if len(tr) > 0:
          for r in tr:
            list=""
            td=r.getElementsByTagName("td")
            for t in td[2].childNodes:
              if (t.nodeName=="text"):
                if (t.nodeValue!="unknown" and t.nodeValue.strip() != ""):
                  list = list + " " + t.nodeValue.encode("utf-8") 
              elif(t.nodeName=="a"):
                list = list + " " + t.firstChild.nodeValue.encode("utf-8")
            
            if(len(list)>0):
              rating[p][td[0].firstChild.nodeValue.encode("utf-8")]=list
        else:
          print ("Info: No table found for rating!!")
    return rating
