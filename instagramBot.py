# Script de python para hacer comentarios en Instagram
#
# Requerimientos:
#    - Python3, pip: https://installpython3.com/
#    - Selenium: pip install -U selenium
#    - Google Chrome
#    - Brave Browser
#    - Google Chrome Driver (necesario para Selenium): https://chromedriver.chromium.org/downloads
#      Nota: depende de la versión de chrome que tengas, actual v89 (ver en las settings de google chrome, puede ser 87, 88, 89, 90...)
#    - Estar registrado con la misma cuenta (mail+password) en cada uno de los sitios debajo (validSites)
#    - (recomendado) una VPN com oAVG VPN, que permite cambiar la IP de la máquina
#
# Ejecución:
#    - Una vez instalado  python3, pip, selenium y descargado Chrome Driver, copiar este último a 
#      una carpeta. Ejemplo:/tmp/chromedriver.v89.exe (será sin extensión en linux, dar permisos +x)
#      Luego llamar al script
#
# Comando para llamar al script
#
#    python3 instagramBot.py -u username -p password -q googleDriverPath+File - browserPathANdFile
#    python3 instagramBot.py -u zaraza -p zaraza -g c:\\temp\\chromedriver.v92.exe -b "C:\\Program Files (x86)\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
#    python3 instagramBot.py -u zaraza -p zaraza -g c:\\temp\\chromedriver.v92.exe -b "C:\Program Files (x86)\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
#
# Referencias
#   - js executor: https://stackoverflow.com/questions/7263824/get-html-source-of-webelement-in-selenium-webdriver-using-python
#
import time
from datetime import datetime

import os
import sys
import getopt

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys

from random import seed
from random import randint


def getInputParams(argv):
  user = ''
  password = ''
  googledriver = ''
  bravepath = ''

  try:
    opts, args = getopt.getopt(argv,"hu:p:g:b:",["uusername=","ppassword=", "ggoogledriver", "bbravepath"])
  except getopt.GetoptError:
    print ('Number of arguments: ' + str(len(sys.argv)) +  ' arguments.')
    print ('Argument List: ' + str(sys.argv))
    print ('instagramBot.py -u <username> -p <password> -g <googledriver> -b <bravepath>')
    sys.exit(2)

  for opt, arg in opts:
    if opt == '-h':
      print ('instagramBot.py -u <username> -p <password> -g <googledriver>')
      sys.exit()
    elif opt in ("-u", "--uusername"):
      user = arg
    elif opt in ("-p", "--ppassword"):
      password = arg
    elif opt in ("-g", "--ggoogledriver"):
      googledriver = arg
    elif opt in ("-b", "--bbravepath"):
      bravepath = arg

  if (len(sys.argv) == 1):
      print ("Error: Tiene que pasar un argumento con usuario, contraseña, ruta+archivo de google chrome driver y de Brave", '\n')
      print ('instagramBot.py -u <username> -p <password> -g <googledriver> - b <bravepath>', '\n')
      print ('Ejemplo: python3 instagramBot.py -u pepe@gmail.com -p strongP1ssw4rd -g c:\\temp\\chromedriver.v89.exe -b C:\\Program Files (x86)\\BraveSoftware\\Brave-Browser\\Application\\brave.exe')
      print('Descargar google chrome diver (no es el browser) aquí: https://chromedriver.chromium.org/downloads')
      print('\n')
      sys.exit()
  elif (len(user) == 0):
      print ('Error: usuario no válido')
      sys.exit()
  elif (len(password) == 0):
      print ('Error: password no válida')
      sys.exit()
  elif (len(googledriver) == 0 or not os.path.isfile(googledriver)):
      print ('Error: path y archivo de google chrome driver no válido')
      sys.exit()
  elif (len(bravepath) == 0 or not os.path.isfile(bravepath)):
      print ('Error: path y archivo de Browser Brave no válido')
      sys.exit()

  return user, password, googledriver, bravepath

def getError(e):
  try:
    # https://stackoverflow.com/questions/33239308/how-to-get-exception-message-in-python-properly
    error = getattr(e, 'message', repr(e))
    return error
  except:
    return ''


def log(msg):
  date = str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

  data = date+': '+msg
  filename = './logs/bot.log'

  print(data)

  with open(filename, "a+") as flog:
    flog.write(data+'\n')
    flog.close()


def getDriver(chromeDriverPath, bravePath):
  d = DesiredCapabilities.CHROME
  d['goog:loggingPrefs'] = { 'browser':'ALL' }

  option = webdriver.ChromeOptions()

  option.add_argument('log-level=3')
  option.add_argument("disable-popup-blocking")
  option.add_argument('start-maximized')
  option.add_argument('disable-infobars')
  option.add_experimental_option('excludeSwitches', ['enable-automation'])
  option.add_experimental_option('excludeSwitches', ['enable-logging'])
  option.add_experimental_option('useAutomationExtension', False)

  option.binary_location = bravePath
  driver = webdriver.Chrome(executable_path=chromeDriverPath, options=option, desired_capabilities=d)
  return driver


def commentSpam (link, driver, user, password, followers, followings):
  try:
    log ('commentSpam ...')

    usersSent = [""]
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    limitComments = 49

    with open('randomAccounts.txt', newline='\n') as f:
      Lines = f.readlines()
      accountsList = list(Lines)

    driver.get(link)
    time.sleep(5) # 5 seconds
    commentBox = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/section[3]/div/form/textarea')
    
    while len(usersSent) < limitComments:
      try:
        counter = 0
        user = accountsList[counter]
        commentBox.click()
        textBox = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/section[3]/div/form/textarea')
        textBox.send_keys(user)
        textBox.send_keys(Keys.ENTER)
        publicar = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[3]/div/form/button[2]')
        publicar.click()
        usersSent.append(user)
        time.sleep(15) # 15 seconds
        
      except Exception as e:
        log('Se omite usuario ' + user + ' por error ' + getError(e))
        time.sleep(1)
        pass

  except Exception as e:
    log('CommentSpam error ' + getError(e))
    pass

def getFollowers(driver, username):
  try:
    log('Getting followers ...')

    driver.get("https://www.instagram.com/"+username)
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
    log('followers: ' + names)
    return names

  except Exception as e:
    log('getFollowers error ' + getError(e))
    pass
    return ''


def getFollowings(driver, username):
  try:
    log('Getting followings ...')

    driver.get("https://www.instagram.com/"+username)

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
    log('followings: ' + names)
    return names

  except Exception as e:
    log('getFollowings error ' + getError(e))
    pass
    return ''


def disableAlerts(driver):
  try:
    element = driver.find_elements_by_xpath("//button[contains(@class, 'aOOlW   HoLwm ')]")
    if (element):
      time.sleep(2)
      element[0].click()

  except Exception as e:
    log('disableAlerts error ' + getError(e))
    pass


def login(username, password, driver):
  try:

    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(5) # esperar a que la página se muestre

    username_element = driver.find_element_by_xpath("//input[@name=\"username\"]")
    username_element.send_keys(username)

    password_element = driver.find_element_by_xpath("//input[@name=\"password\"]")
    password_element.send_keys(password)
    
    login_button = driver.find_element_by_xpath('//button[@type="submit"]')
    login_button.click()
    
    time.sleep(10) # Esperar fin login

    return True

  except Exception as e:
    log('login error ' + getError(e))
    return False


def process (user, password, chromeDriverPath, bravePath):
  while True:
    log('Starting to process ...')
    driver = getDriver(chromeDriverPath, bravePath)

    try:
      if (login(user, password, driver)):
        disableAlerts(driver) # eliminar alertas de notificación
        followings = getFollowings(driver, user)
        followers = getFollowers(driver, user)
        print(followers)
        print(followings)
        # commentSpam("https://www.instagram.com/p/CR1panuC2W7/", driver, user, password, followers, followings)
    except Exception as e:
      log('Se omite repetición de proceso por error ' + getError(e))
      pass

    # https://www.zyxware.com/articles/5552/what-is-close-and-quit-commands-in-selenium-webdriver
    driver.quit() 
    log('Esperando 1 minuto ...')
    time.sleep(60) 


def main(argv): # Start here!
  if not os.path.exists('./logs/'):
    os.makedirs('./logs/')

  username, password, chromeDriverPath, bravePath = getInputParams(argv)
  process (username, password, chromeDriverPath, bravePath)


if __name__ == "__main__":
  main(sys.argv[1:])

