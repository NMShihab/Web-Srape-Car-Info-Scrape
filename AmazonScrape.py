""" Import all necessary library """
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd 
from openpyxl import Workbook
import numpy as np

# Initialize path of chrome driver
PATH = "C:\Program Files (x86)/chromedriver.exe"

def headlessBrowser():
    """Function that give us access of headless chrome browser"""
    options = webdriver.ChromeOptions()
    options.headless = False
    browser = webdriver.Chrome(executable_path=PATH,options=options)
    return browser

def getAmazonData(url, name):
    browser = headlessBrowser()
    browser.get(url)
    time.sleep(6)
    
    try:
        searchField = browser.find_element_by_id('twotabsearchtextbox')
        # print("Search Field : ",searchField)
        searchField.send_keys(str(name))
        searchButton = browser.find_element_by_id('nav-search-submit-button')
        searchButton.click()
        time.sleep(3)
        
        product_image_element = browser.find_elements_by_class_name("s-product-image-container")
        # print("alllink: ",product_image_element)
        
        all_links = []
        
        for elem in product_image_element:
            try:
                link = elem.find_element_by_tag_name('a').get_attribute("href")
                if link:
                    all_links.append(link)
            except:
                pass
                      
        print("list of link: ",all_links)
        file_name = str(str(name)+".txt")
        np.savetxt(file_name, all_links,fmt='%s')
        browser.quit()
        
        
    
    except  Exception as e:
        print("Exception: ",e)
    

list_of_search_keys = ["camera","mouse","monitor","mobile phone","Iphone 14"]
for keys in list_of_search_keys:
    getAmazonData("https://www.amazon.com/", keys)
    time.sleep(2)

# getAmazonData("https://www.amazon.com/", "Wireless Gaming Mouse")