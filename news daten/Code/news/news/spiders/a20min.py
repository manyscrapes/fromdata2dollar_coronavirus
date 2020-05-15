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

class A20minSpider(scrapy.Spider):
	name = '20min'
	allowed_domains = ['20min.ch']
	start_urls = ['https://20min.ch/']

	def parse(self, response):
		url = 'https://www.20min.ch/tools/suchen/'
		# (mac related)
		#path_to_extension = r'/Users/many/Library/Application Support/Google/Chrome/Default/Extensions/cjpalhdlnbpafiamejdnhcphjbkeiagm/1.24.4_0'
		# (windows related)
		path_to_extension = r'C:\Users\Admin\AppData\Local\Google\Chrome\User Data\Default\Extensions\cjpalhdlnbpafiamejdnhcphjbkeiagm\1.26.0_0'
		chrome_options = Options()
		#chrome_options.add_argument('load-extension=' + path_to_extension)
		chrome_options.add_argument('--load-extension=' + path_to_extension)
		# (mac related)
		#self.driver = webdriver.Chrome('/Users/many/Documents/chromedriver', chrome_options=chrome_options)
		# (windows related)
		self.driver = webdriver.Chrome('C:\\Users\\Admin\\Python\\chromedriver.exe', chrome_options=chrome_options)
		self.driver.create_options()
		self.driver.get(url)
		sleep(randint(1,2))
		search = self.driver.find_element_by_xpath('//*[@id="search_form"]/input[4]')
                #hier Suchanfrage anpasssen
		search.send_keys("Corona") #<---- 
		date = self.driver.find_element_by_xpath('//*[@id="slide"]/div/input[2]')
		date.clear()
		date.send_keys("13/04/2020")
		search.send_keys(Keys.RETURN)
		print("Corona search request send!")
		sleep(randint(1,2))
		#search results divided through
		hardcounter = 1
		totalnewscounter = 1
		sitesx = self.driver.find_elements_by_xpath('//*[@id="search_wrapper"]/h2')
		sitesy = sitesx[0].text
		print(sitesy)
		totalnews = re.search(r'\d+', sitesy).group()
		print(totalnews)
		newspersite = self.driver.find_elements_by_class_name('resulttext')
		sitesamount = math.ceil(int(totalnews) / len(newspersite))
		print(sitesamount)
		# mmm
		while hardcounter <= sitesamount: 
			print("***")
			print("***SITESCOUNTER*** " + str(hardcounter) + " / " + str(sitesamount))
			print("***")
			#how many news are displayed on search result site
			news = self.driver.find_elements_by_class_name('resulttext')
			newsamount = len(news)
			newsmax = len(news) * 2 + 3
			newscounter = 1
			controlcounter = 5			
			print("newsamount")
			print(newsamount)
			print("newsmax")
			print(newsmax)
			print("controlcounter")
			print(controlcounter)
			while controlcounter <= newsmax:
				#link
				print("***")
				print("***SITESCOUNTER*** " + str(hardcounter) + " / " + str(sitesamount))
				print("***")
				print("***NEWSCOUNTER*** " + str(newscounter) + " / " + str(newsamount) + "  ||  " + str(totalnewscounter) + " / " + str(totalnews))
				print("***")
				print("***CONTROLCOUNTER*** " + str(controlcounter) + " / " + str(newsmax))
				print("***")
				linklocation = '//*[@id="search_wrapper"]/div[' + str(controlcounter) + ']/div[2]/span/a'
				print(linklocation)
				for a in self.driver.find_elements_by_xpath(linklocation):
					###BRUCHI
  					link = a.get_attribute('href')				
				print(link)
				if link[12:17] == "20min":
					name = "20min"
					#open tab
					self.driver.execute_script("window.open('');")
					self.driver.switch_to.window(self.driver.window_handles[1])
					self.driver.get(link)
					#sleep(1)
					###BRUCHI
					newstext = self.driver.find_elements_by_xpath('//*[@id="story_content"]/div[3]/div[2]')[0].text
					print("newstext: " + newstext)
					tagonnews = self.driver.find_elements_by_xpath('//*[@id="story_content"]/div[2]/div[1]/div/h4')[0].text
					print("tagonnews: " + tagonnews)
					###BRUCHI
					link_cut = link[21:]
					linktag = re.match(r'(\w+)', link_cut).group()
					print("linktag === " + str(linktag))					
					#close tab
					self.driver.close()
					self.driver.switch_to.window(self.driver.window_handles[0])
					self.driver.refresh()
				else:
					name = re.search(r'^(?:https?:\/\/)?(?:[^@\/\n]+@)?(?:www\.)?([^:\/?\n]+)', link).group()
					print("ALERT! " + name + " detected!!!")
					newstext = "-"
					print("newstext: " + newstext)
					tagonnews = "-"
					print("tagonnews: " + tagonnews)
					linktag = tagonnews
					print("linktag === " + str(linktag))
				#title
				###BRUCHI
				title = self.driver.find_elements_by_xpath(linklocation)[0].text
				print("title: " + title)
				#intro
				introlocation = '//*[@id="search_wrapper"]/div[' + str(controlcounter) + ']/div[2]/a'
				###BRUCHI
				intro = self.driver.find_elements_by_xpath(introlocation)[0].text
				print("intro: " + intro)
				#released
				releasedlocation = '//*[@id="search_wrapper"]/div[' + str(controlcounter) + ']/div[2]/div'
				released_raw = self.driver.find_elements_by_xpath(releasedlocation)[0].text
				###BRUCHI
				released = re.search(r'\d{2}/\d{2}/\d{4}', released_raw).group()
				print("released: " + released)
				#yield all
				yield {'Name': name,
				'Date': released,
				'Title': title,
				'Intro': intro,
				'Text': newstext,
				'Link': link,
				'Rubrik': linktag,
				'Tag on News': tagonnews}
				totalnewscounter += 1
				newscounter += 1
				controlcounter += 2
			if hardcounter == 1:
				self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				self.driver.find_element_by_xpath('//*[@id="search_wrapper"]/a[61]').click()
				sleep(randint(1,2))
			else:
				self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				self.driver.find_element_by_xpath('//*[@id="search_wrapper"]/a[62]').click()
				sleep(randint(1,2))
			hardcounter += 1
		self.driver.close()