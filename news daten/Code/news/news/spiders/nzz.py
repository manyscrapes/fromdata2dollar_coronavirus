# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from time import sleep
from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from random import randint
import csv
import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import re
import math
from bs4 import BeautifulSoup

class NzzSpider(scrapy.Spider):
	name = 'nzz'
	allowed_domains = ['nzz.ch']
	start_urls = ['http://nzz.ch/']

	def parse(self, response):
		#login
		url = 'https://abo.nzz.ch/registrieren/'
		# (mac related)
		#path_to_extension = r'/Users/many/Library/Application Support/Google/Chrome/Default/Extensions/cjpalhdlnbpafiamejdnhcphjbkeiagm/1.24.4_0'
		# (windows related)
		path_to_extension = r'C:\Users\Admin\AppData\Local\Google\Chrome\User Data\Default\Extensions\cjpalhdlnbpafiamejdnhcphjbkeiagm\1.26.0_0'
		chrome_options = Options()
		#chrome_options.add_argument('load-extension=' + path_to_extension)
		chrome_options.add_argument("--disable-infobars")
		chrome_options.add_argument('--load-extension=' + path_to_extension)
		chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2})
		# (mac related)
		#self.driver = webdriver.Chrome('/Users/many/Documents/chromedriver', chrome_options=chrome_options)
		# (windows related)
		self.driver = webdriver.Chrome('C:\\Users\\Admin\\Python\\chromedriver.exe', chrome_options=chrome_options)
		self.driver.create_options()
		self.driver.get(url)
		sleep(randint(1,2))
		login = self.driver.find_element_by_xpath('//*[@id="c1-login-field"]')	
		login.send_keys("admin@mail.com")
		login.send_keys(Keys.RETURN)
		sleep(randint(1,2))
		passw = self.driver.find_element_by_xpath('//*[@id="c1-password-field"]')
		passw.send_keys("password")
		passw.send_keys(Keys.RETURN)
		sleep(randint(1,2))
		#search
		#hier Suchanfrage anpasssen
		suche = "Corona"
		url = 'https://www.nzz.ch/suche?q=' + suche
		self.driver.get(url)
		print(str(suche) + " search request send!")
		sleep(randint(1,2))
		#search results = totalnews
		totalnewscounter = 1
		sitesx = self.driver.find_elements_by_xpath('//*[@id="__layout"]/div/div[1]/div/section/div/div[3]/div[2]/div/div/div')
		sitesy = sitesx[0].text
		print("sitesy: " + str(sitesy))
		totalnews = re.search(r'\d+', sitesy).group()
		print("totalnews: " + str(totalnews))
		# crawl search results
		searchsubmaxcounterbefore = 0
		while totalnewscounter <= int(totalnews): 
			self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			searchsubcounter = 1
			searchsubmax = self.driver.find_elements_by_xpath(".//article[@class='teaser--article teaser--paginated']")
			searchsubmaxcounter = len(searchsubmax) - searchsubmaxcounterbefore
			print("***")
			print("calculating: " + str(len(searchsubmax)) + " - " + str(searchsubmaxcounterbefore) + " = " + str(searchsubmaxcounter))
			while searchsubcounter <= searchsubmaxcounter:
				print("***")
				print("***COUNTER*** " + str(totalnewscounter) + " / " + str(totalnews))
				print("***")
				print("***SUBCOUNTER*** " + str(searchsubcounter) + " / " + str(searchsubmaxcounter))
				print("***")
				# name
				name = "nzz"
				# title
				titlexpath = '/html/body/div/div/div/div[1]/div/section/div/div[3]/div[2]/div/div/article[' + str(totalnewscounter) + ']/div/div[2]/a/h2/span'
				othertitlexpath = '/html/body/div/div/div/div[1]/div/section/div/div[3]/div[2]/div/div/article[' + str(totalnewscounter) + ']/div/div/a/h2/span'
				if self.driver.find_elements_by_xpath(titlexpath):
					title = self.driver.find_elements_by_xpath(titlexpath)[0].text
					print("title: " + title)
				elif self.driver.find_elements_by_xpath(othertitlexpath):
					title = self.driver.find_elements_by_xpath(othertitlexpath)[0].text
					print("title: " + title)
				else:
					title = "-"
					print("no title found")				
				# intro
				introxpath = '/html/body/div/div/div/div[1]/div/section/div/div[3]/div[2]/div/div/article[' + str(totalnewscounter) + ']/div/div[2]/div[1]'
				otherintroxpath = '/html/body/div/div/div/div[1]/div/section/div/div[3]/div[2]/div/div/article[' + str(totalnewscounter) + ']/div/div/div[1]'
				if self.driver.find_elements_by_xpath(introxpath):
					intro = self.driver.find_elements_by_xpath(introxpath)[0].text
					print("intro: " + intro)
				elif self.driver.find_elements_by_xpath(otherintroxpath):
					intro = self.driver.find_elements_by_xpath(otherintroxpath)[0].text
					print("intro: " + intro)
				else:
					intro = "-"
					print("no intro found")
				# author
				authorxpath = '/html/body/div/div/div/div[1]/div/section/div/div[3]/div[2]/div/div/article[' + str(totalnewscounter) + ']/div/div[2]/div[2]/div[1]/div/span'
				if self.driver.find_elements_by_xpath(authorxpath):
					author = self.driver.find_elements_by_xpath(authorxpath)[0].text
					print("author: " + author)
				else:
					author = "none"
					print("no author found")
				# link & linktag
				linkxpath = '/html/body/div/div/div/div[1]/div/section/div/div[3]/div[2]/div/div/article[' + str(totalnewscounter) + ']/div/div[2]/a'
				otherlinkxpath = '/html/body/div/div/div/div[1]/div/section/div/div[3]/div[2]/div/div/article[' + str(totalnewscounter) + ']/div/div/a'
				if self.driver.find_elements_by_xpath(linkxpath):
					for a in self.driver.find_elements_by_xpath(linkxpath):
						link = a.get_attribute('href')
					print("link: " + link)
				elif self.driver.find_elements_by_xpath(otherlinkxpath):
					for a in self.driver.find_elements_by_xpath(otherlinkxpath):
						link = a.get_attribute('href')
					print("link: " + link)
				else:
					link = "-"
					print("no link found")			
				link_cut = link[19:]
				linktag = re.match(r'(\w+)', link_cut).group()
				print("linktag: " + str(linktag))
				checkflagxpath = '/html/body/div/div/div/div[1]/div/section/div/div[3]/div[2]/div/div/article[' + str(totalnewscounter) + ']/div/div[2]'
				if self.driver.find_elements_by_xpath(checkflagxpath):
					checkflag = self.driver.find_element_by_xpath(checkflagxpath).get_attribute("class")
					print("Attribute >Class< = " + checkflag)
					if checkflag == "teaser__content teaser__content--with-flag teaser__content--paginated":
						flagxpath = '/html/body/div/div/div/div[1]/div/section/div/div[3]/div[2]/div/div/article[' + str(totalnewscounter) + ']/div/div[2]/a/div'							
						flag = self.driver.find_elements_by_xpath(flagxpath)[0].text
						print("flag: " + flag)
					else:
						flag = "none"
						print("no flag found")
				else:
					checkflag = "none"
					print("no flag found")	
				#open tab
				self.driver.execute_script("window.open('');")
				self.driver.switch_to.window(self.driver.window_handles[1])
				self.driver.get(link)
				self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				#sleep(1)
				# released
				releasedxpath = '//*[@id="__layout"]/div/div[3]/div[4]/div[2]/div/section/div[1]/div[2]/div[2]/div[1]/time'
				otherreleasedxpath = '/html/body/div/div/div/div[3]/div[2]/div[2]/div/section/div[1]/div[3]/div[2]/div[1]/time'
				if self.driver.find_elements_by_xpath(releasedxpath):
					released_raw = self.driver.find_elements_by_xpath(releasedxpath)[0].text
					released = re.search(r'\d{2}.\d{2}.\d{4}', released_raw).group()
					print("released: " + released)
				elif self.driver.find_elements_by_xpath(otherreleasedxpath):
					released_raw = self.driver.find_elements_by_xpath(otherreleasedxpath)[0].text
					released = re.search(r'\d{2}.\d{2}.\d{4}', released_raw).group()
					print("released: " + released)				
				else:
					released = "-"
					print("no date found")
				#get newstext
				articlecomponent = self.driver.find_elements_by_xpath(".//p[@class='articlecomponent text regwalled']")
				articlecomponents = len(articlecomponent)
				print("articlecomponent: " + str(articlecomponents))
				textcomponent = self.driver.find_elements_by_xpath(".//p[@class='articlecomponent text']")
				textcomponents = len(textcomponent)
				print("textcomponent: " + str(textcomponents))
				newstextcomponents = articlecomponents + textcomponents				
				newstextcomponent = 1
				newstext = ""
				while newstextcomponent <= newstextcomponents:
					newstextcomponentxpath = '/html/body/div/div/div/div[3]/div[4]/div[2]/div/section/p[' + str(newstextcomponent) + ']'
					othernewstextcomponentxpath = '/html/body/div/div/div/div[3]/div[2]/div[2]/div/section/p[' + str(newstextcomponent) + ']'
					if self.driver.find_elements_by_xpath(newstextcomponentxpath):
						newstext = newstext + self.driver.find_elements_by_xpath(newstextcomponentxpath)[0].text + " "
						newstextcomponent += 1
					elif self.driver.find_elements_by_xpath(othernewstextcomponentxpath):
						newstext = newstext + self.driver.find_elements_by_xpath(othernewstextcomponentxpath)[0].text + " "
						newstextcomponent += 1
					else:
						newstext = "no newstext found"
						newstextcomponent += 1
				print("newstext: " + newstext)
				#close tab
				self.driver.close()
				self.driver.switch_to.window(self.driver.window_handles[0])
				#yield all
				yield {'Name': name,
				'Date': released,
				'Title': title,
				'Intro': intro,
				'Text': newstext,
				'Link': link,
				'Rubrik': linktag,
				'flag': flag,
				'author': author}
				searchsubcounter += 1
				totalnewscounter += 1
			print("***")
			print("scrolling down")
			print("***")
			self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			sleep(1)
			self.driver.find_element_by_xpath('//*[@id="__layout"]/div/div[1]/div/section/div/div[3]/div[2]/div/button').click()
			print("***")
			print("click click")
			print("***")
			sleep(1)
			searchsubmaxcounterbefore = totalnewscounter - 1
		self.driver.close()