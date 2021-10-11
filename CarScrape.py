""" Import all necessary library """
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd 
from openpyxl import Workbook





# Initialize path of chrome driver
PATH = "C:\Program Files (x86)/chromedriver.exe"

# Initialize necessary value
carList = []
dataSheet = []
simpleData = []


def headlessBrowser():
    """Function that give us access of headless chrome browser"""
    options = webdriver.ChromeOptions()
    options.headless = False
    browser = webdriver.Chrome(PATH,options=options)
    return browser


def getCarData(carUrl):
    """ This function scrape specific car data """

    
    browser = headlessBrowser()
    browser.get(carUrl)

    time.sleep(5)
    try:
        """ Scrape Name And Price Data"""
        priceBox = browser.find_element_by_class_name("price-box")
        price = priceBox.find_element_by_tag_name("h2")
        carPrice = price.text

        pName = browser.find_element_by_class_name("bigger")       
        carNameText = pName.text
        # Extract name from text
        splitName = carNameText.split()
        nameList = splitName[1:-2]
        carName = " ".join(nameList)
        
        

    except Exception as e:
        carName = ""
        carPrice = ""
        print("Error: ",e)

    

    try:
        """ Scrape Summary Table Data """

        summaryTable = browser.find_elements_by_id("summary-table")
        keys=[]
        values=[]
        
        tableKey = summaryTable[1].find_elements_by_tag_name("th")
        tableBody = summaryTable[1].find_elements_by_tag_name("td")

        tableKey = tableKey[1:]
        
        # List all keys of summary
        for key in tableKey:
            keys.append(key.text)

        # List all value of summary   
        for tb in tableBody:
            values.append(tb.text)
           

        # Create Summary
        summary = dict(zip(keys, values))

        
        
    except Exception as e:
        summary = []
        print("Error: ",e)


    try:
        """ Scrape Option Table Data """

        optionTable = browser.find_element_by_id("options-table")

        options =[]
        tableOption = optionTable.find_elements_by_tag_name("td")
        

        # Grab all options in a list
        for option in tableOption:
            options.append(option.text)
            
    except Exception as e:
        options = []
        print("Error: ",e)
    
    # Create data list
    dataArray = [carName,carPrice,summary,options]
    dataSheet.append(dataArray)

    # Quit browser after all scrape done 
    browser.quit()







def scrapeWeb(radiusValue,zipValue):
    """ This function create data list according to given radius and zip """

    webDriver = headlessBrowser()
    webDriver.get("https://www.tred.com/buy?body_style=&distance=50&exterior_color_id=&make=&miles_max=100000&miles_min=0&model=&page_size=24&price_max=100000&price_min=0&query=&requestingPage=buy&sort=desc&sort_field=updated&status=active&year_end=2022&year_start=1998&zip=")

    time.sleep(5)   
    try:
        """ Search In The Website Using Radius and Zip Field """

        zipClass = WebDriverWait(webDriver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "zip"))
        )
        
        zipField = zipClass.find_element_by_class_name("form-control")

        radiusClass = webDriver.find_element_by_class_name("radius")
        radiusField = radiusClass.find_element_by_class_name("form-control")

       

        radiusField.send_keys(str(radiusValue))
        radiusField.send_keys(Keys.RETURN)

        zipField.send_keys(str(zipValue))
        zipField.send_keys(Keys.RETURN)

    except Exception as e:
        print("Someting wrong: ", e)
    
    # Gave some time to load search data
    time.sleep(5)

    try:   
        """ Access All Search Result Link """     
        searchContent = WebDriverWait(webDriver, 10).until(
            EC.presence_of_element_located((By.ID, "cars"))
        )

        carContent = searchContent.find_element_by_class_name("inventory")
        allLinktag = carContent.find_elements_by_tag_name('a')

        # Extract link from web element and list in a array
        for e in allLinktag:
            url = e.get_attribute("href")
            carList.append(url)
            
    except:
        print("Car element doen't find")
        webDriver.quit()

    cList = carList[0:3]

    # Go through all links and grap data from them
    for carUrl in cList:
        getCarData(carUrl)

   
    # Quit driver 
    webDriver.quit()



# Call function 
scrapeWeb(200,1216)

# print(dataSheet)

# Create data frame
df = pd.DataFrame(dataSheet,columns=['Name', 'Price', 'Vehicle Summary','Vechile Options'])

print(df.Name)


# Convert data frame to xl
# df.to_excel("carInfo.xlsx") 