'''
    author : Prabhu Dayal Sahoo
    College : National Institute of Technology Karnataka
    Project Name : RANKING OF SINGERS
    Project Idea : Web Crawler to rank the singers based on the number of songs they have in TOP 50 BOLLYWOOD SONGS in gaana.com
'''


from optparse import OptionParser
import json
import re
import os,errno
import shutil
from datetime import datetime, timedelta
import time
import urllib
import bs4
import requests
import operator

url_base = 'http://gaana.com'

#returns the list of singers
def process():
    
    response = requests.get(url_base)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    #navigates to topcharts
    temp = soup.select('div.top_nav a[href^=/topcharts]')[0]['href']
    url_new = url_base + temp

    response = requests.get(url_new)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    #navigates to top 50 bollywood songs
    temp = soup.select('div[class^=featured_playlist_data] a[href^=/topcharts]')[0]['href']
    url_new = url_base + temp

    #print url_new
    response = requests.get(url_new)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    singers = {}
    
    #element containing info about each song
    #traversing all the 50 songs one by one
    for x in soup.findAll('div', {'class' : 'album-horizantal-listing clearfix _playlist_tracks_row'}):
        
        song = x.find_all('h2',{ 'class' : 'dotes'})
        
        artist = ""
        
        #names of all the singers for this particular song
        artists = x.find_all('a', {'class':'pjax a-d1 _artist'})
        
        if len(artists) and len(song):
            song_name = song[0].find_all('a')
            now_song = song_name[0].text
            
            sing = []
            
            #add this song to the list of songs of this singer/artist
            for i in artists:
                artist = i.text
                singers.setdefault(artist, []).append(now_song)
                
    return singers


def get_singers():
    
    singers = process();

    rank = {}

    #store the number of songs sung by each singer in rank[]
    for x in singers:
        rank[x] = len(singers[x])

    #sort rank[] based on number of songs
    rankx = sorted(rank.items(), key=operator.itemgetter(1))

    fp = os.path.join('gaana', 'Singers and songs.txt')
    f1 = open(fp, 'w')
    
    print >>f1, '*******LIST OF SINGERS IN TOP 50 BOLLYWOOD SONGS*******'
    print >>f1,'------------------------------------'
    print >>f1,'\n'
    
    for x in singers:
        print >>f1,x, ':'
        for y in singers[x]:
            print >>f1,'\t\t', y, '\n'
        
    f1.close()
    
    filename = os.path.join('gaana', 'Singer Ranking.txt')
    f = open(filename, 'w')
    print >>f, '*******RANKING OF SINGERS*******'
    print >>f, '--------------------------------\n'
    i = 1
    for x in reversed(rankx):
        print >>f, i, ' ', x[0], ' - ', x[1]
        i += 1

    f.close()

if __name__ == '__main__':  
    get_singers()
