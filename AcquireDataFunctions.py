import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def login(username, password, driver):
    driver.get("https://www.instagram.com/accounts/login/")
    count = 0
    
    while count < 15:
    	try:
    		username_element = driver.find_element_by_xpath("//input[@name=\"username\"]")
    		password_element = driver.find_element_by_xpath("//input[@name=\"password\"]")
    		break
    	except:
    		time.sleep(1)
    		count = count + 1
    		print(count)
    
    username_element.send_keys(username)
    password_element.send_keys(password)
    
    login_button = driver.find_element_by_xpath('//button[@type="submit"]')
    login_button.click()
    
    time.sleep(2)

    driver.get("https://www.instagram.com/"+username)
    
def get_followers(driver):

    driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a').click() #clicks followers
    time.sleep(1)

    scroll_div = driver.find_element_by_xpath('/html/body/div[5]/div/div/div[2]') #caja donde scrolleo
    previous_height = 0
    current_height = 1
    while previous_height != current_height:
        
        previous_height = current_height
        current_height = driver.execute_script('arguments[0].scrollTo(0, arguments[0].scrollHeight); return arguments[0].scrollHeight;', scroll_div)
        time.sleep(1)

    links = scroll_div.find_elements_by_tag_name('a')
    names = [name.text for name in links if name.text != '']

    driver.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/div/div[2]/button').click() #close button
    return names



def get_following(driver):
    
    driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a').click() #clicks following
    time.sleep(1)

    scroll_div = driver.find_element_by_xpath('/html/body/div[5]/div/div/div[2]') #caja donde scrolleo
    previous_height = 0
    current_height = 1
    while previous_height != current_height:
        
        previous_height = current_height
        current_height = driver.execute_script('arguments[0].scrollTo(0, arguments[0].scrollHeight); return arguments[0].scrollHeight;', scroll_div)
        time.sleep(1)

    links = scroll_div.find_elements_by_tag_name('a')
    names = [name.text for name in links if name.text != '']

    driver.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/div/div[2]/button').click() #close button
    return names

