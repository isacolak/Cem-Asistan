import time
import requests
from selenium import webdriver
from bs4 import BeautifulSoup as bs

base = "https://www.youtube.com/results?search_query="
squery = "suç mahalli"

r = requests.get(base+squery)

page = r.text
soup=bs(page,'html.parser')

vids = soup.findAll('a',attrs={'class':'yt-uix-tile-link'})

videolist=[]
for v in vids:
    tmp = 'https://www.youtube.com' + v['href']
    videolist.append(tmp)

videolist2=[]
for v in vids:
    videolist2.append(v["title"])

video_url = videolist[0]

videos = {}
for v in vids:
	videos[v["title"]] = "https://www.youtube.com"+v["href"]



if squery in videolist2[0].lower():
	url = videos[videolist2[0]]

driver = webdriver.Chrome('C:/Users/Pc/Desktop/İsa/chromedriver.exe')

driver.get(url)
time.sleep(5)

while True:

	if driver.find_element_by_xpath('//*[@id="preskip-component:5"]/span'):
		time.sleep(5)
		driver.find_element_by_xpath('//*[@id="preskip-component:5"]/span').click()
		break

time.sleep(20)

driver.quit()



