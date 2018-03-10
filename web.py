from selenium import webdriver
import time
import urllib
#import urllib2

refreshrate=int(5)
driver = webdriver.Firefox()
driver.get('.pagina/index.html')
while True:
    time.sleep(refreshrate)
    driver.refresh()