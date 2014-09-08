from pymongo import Connection
from pymongo.errors import ConnectionFailure
from bson.objectid import ObjectId
from bs4 import BeautifulSoup
from urlparse import urljoin
import hashlib
import datetime
import requests
import sys

class Crawler:

    #init func
    def __init__(self):
        self.c = Connection(host='localhost',port=27017)
        self.dbh = self.c['crawler']
        #-----------------------------------------
        # for debug purpose
        self.dbh.drop_collection('links')


    # add a url
    def addlink(self,url,state=0):
        entry = { "_id":hashlib.md5(url).hexdigest(),
                  "url":url,
                  "state":state
                  }
        return self.dbh.links.insert(entry)

    # get a free url
    def getlink(self):
        entry = self.dbh.links.find_one({"state":0})
        return entry

    # update a url state
    def setstate(self,url,state):
        hash_u = hashlib.md5(url).hexdigest()
        entry = self.dbh.links.find_one({"_id":hash_u})
        entry['state'] = state
        self.dbh.links.save(entry)

    # update a url state
    def urlexists(self,url):
        hash_u = hashlib.md5(url).hexdigest()
        return self.dbh.links.find_one({"_id":hash_u})


    # update a url state
    def setstate_hash(self,url_hash,state):
        entry = self.dbh.links.find_one({"_id":url_hash})
        entry['state'] = state
        self.dbh.links.save(entry)
        return entry

    # crawl
    def crawl(self):
        url = self.getlink()
        while url != None:
            print '->',url['url']
            done = False
            retry = 0
            while done == False and retry<5:
                try:
                    r = requests.get(url['url'])
                    done = True
                    self.setstate_hash(url['_id'],1)
                    self.extractURL(r.text,url['url'])
                    #print '---------------------------------'
                    #self.save_file(r.text,hashlib.md5(url['url']).hexdigest())

                except Exception,e:
                    done = False
                    print 'Error',e
                    retry += 1
            url = self.getlink()
            if retry == 5:
                self.setstate_hash(url['_id'],2)

    # try to save the file
    def save_file(self,src,filename):
        try:
            print '---------------------------------'
            f = open(str(hashlib.md5(url).hexdigest()),'wb')
            f.write(src)
            f.close()
        except:
            print '-> ','error saving file'

    # extract the url and save it.
    def extractURL(self,src,baseurl):
        soup = BeautifulSoup(src)
        for i in soup.findAll('a'):
            try:
                link = i['href']
                link = urljoin(baseurl,link)
                link = link.split('#')[0]
                # check if the url added
                if self.urlexists(link) == None:
                    self.addlink(link,0)
            except:
                print '-> -',i

        for i in soup.findAll('img'):
            try:
                link = i['src']
                link = urljoin(baseurl,link)
                link = link.split('#')[0]
                # check if the url added
                if self.urlexists(link) == None:
                    self.addlink(link,0)
            except:
                print '-> -',i

        for i in soup.findAll('link'):
            try:
                link = i['href']
                link = urljoin(baseurl,link)
                link = link.split('#')[0]
                # check if the url added
                if self.urlexists(link) == None:
                    self.addlink(link,0)
            except:
                print '-> -',i



# for testing
c = Crawler()
c.addlink('http://www.codeproject.com/',0)
c.crawl()


