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
from datetime import date
import os.path

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

logsFolder = './logs'
statsFolder = './stats'

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
  filename = logsFolder+'/bot.log'

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


def getLastCommentsFileName(postName):
  try:
    xdate = date.today()
    year = str(xdate.year)
    month = str(xdate.month).zfill(2)
    day = str(xdate.day).zfill(2)
    hour = str(datetime.now().hour).zfill(2)

    print(statsFolder+'/'+postName+'/'+year+month+day+hour)
    return statsFolder+'/'+postName+'/'+year+month+day+hour
  except Exception as e:
    log('Error en getLastCommentsFileName: ' + getError(e))


def getLastCommentsCounter(postName):
  try:
    fileName = getLastCommentsFileName(postName)
    fileExists = os.path.exists(fileName)
    lastCommentsCounter = 0

    if (fileExists):
      with open(fileName, 'r') as flast:
        Lines = flast.readlines()
        for line in Lines:
            lastCommentsCounter = int(line.strip())
      flast.close()

    return lastCommentsCounter

  except Exception as e:
    log('Error en getLastCommentsCounter: ' + getError(e))


def saveLastCommentsCounter(postName):
  try:
    print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
    fileName = getLastCommentsFileName(postName)
    print('fffffffffffffffffffffffffffffff')
    lastCommentsCounter = getLastCommentsCounter(postName)

    print('filename', fileName)
    print('lastCommentsCounter', lastCommentsCounter)
    with open(fileName, 'w') as flast:
      print('hhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
      flast.write(str(lastCommentsCounter+1))

  except Exception as e:
    log('Error en saveLastComments: ' + getError(e))


def getPostFileName(postName):
  try:
    folderName = statsFolder+'/'+postName
    fileName = folderName+'/'+postName
    return fileName

  except Exception as e:
    log('Error en getPostFileName: ' + getError(e))


def saveWhoComment(postName, user):
  try:
    fileName = getPostFileName(postName)
    with open(fileName, 'a') as flast:
        flast.write(str(user)+'\n')

  except Exception as e:
    log('Error en saveLastCommentsCounter: ' + getError(e))


def userAlreadyCommentInPost(postName, user):
  try:
    fileName = getPostFileName(postName)
    fileExists = os.path.exists(fileName)

    if (fileExists):
      with open(fileName) as myfile:
        return user in myfile.read()

  except Exception as e:
    log('Error en userAlreadyCommentInPost: ' + getError(e))

  return False


def exceedsLimits(postName):
  hourLimits = 60
  dayLimits = 1440
  currentCount = getLastCommentsCounter(postName)
  return (currentCount+1 > hourLimits or currentCount+1 > dayLimits)


def commentSpam(postName, driver, allowRepeated, followers=[], followings=[]):
  try:
    log ('commentSpam ...')

    usersSent = [""]
    counter = 0

    with open('randomAccounts.txt', newline='\n') as f:
      Lines = f.readlines()
      accountsList = list(Lines)

    log('getting link ...')
    link = 'https://www.instagram.com/p/'+postName+'/'
    driver.get(link)
    time.sleep(5)
    
    while (not exceedsLimits(postName) and counter < len(accountsList)):
      try:
        user = accountsList[counter].strip().replace('\n', '')
        log('starting to comment with user : ' + user)

        if (not allowRepeated and userAlreadyCommentInPost(postName, user)):
          log('El usuario : ' + user + " ya comentó en éste post")

      # [1:]: Elimino el '@' del usuario dato que en followers y followings está sin ese caracter
        # print('user sin @', user[1:])
        userInLists = user[1:] in followers or user in followings
        # print ('userInLists', userInLists)

        if  (not userInLists):
          # clean
          try:
            driver.refresh() # por error al comentar, habilitación del campo
            time.sleep(3)

            #textBox = driver.find_elements_by_xpath("//textarea[contains(@class, 'Ypffh')]")
            #textBox[0].click()
            #textBox[0].send_keys(Keys.BACKSPACE) # (opción 1) para que no acumule usuarios en el control
            #textBox[0].send_keys(Keys.CONTROL + "a") # (opción 2) para que no acumule usuarios en el control (combinado con la línea debajo)
            #textBox[0].send_keys(Keys.DELETE) # para que no acumule usuarios en el control
            #textBox[0].send_keys(Keys.ENTER)
          except:
            pass

          #time.sleep(1)
          # comment
          textBox = driver.find_elements_by_xpath("//textarea[contains(@class, 'Ypffh')]")
          #extBox[0].click()
          textBox[0].send_keys(user)
          textBox[0].send_keys(Keys.ENTER)

          publicar = driver.find_elements_by_xpath("//button[contains(@class, 'sqdOP yWX7d    y3zKF     ')]")
          time.sleep(1)
          publicar[0].click()
          usersSent.append(user)
          time.sleep(15) # 15 seconds
          log ('user ' + user + ' comentó en el post !!')
          saveLastCommentsCounter(postName)
          saveWhoComment(link, user)
        else:
          log ('user ' + user + ' existe en seguidos o seguidores')

      except Exception as e:
        log('Se omite usuario ' + user + ' por error ' + getError(e))
        time.sleep(2)
        pass

      counter += 1

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
    log('followers: ' + ','.join(names))
    return names

  except Exception as e:
    log('getFollowers error ' + getError(e))
    pass
    return []


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
    log('followings: ' + ','.join(names))
    return names

  except Exception as e:
    log('getFollowings error ' + getError(e))
    pass
    return []


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


def process (user, password, postName, chromeDriverPath, bravePath):
  while True:
    log('Starting to process with post ' + postName + ' ...')
    driver = getDriver(chromeDriverPath, bravePath)

    try:
      if (login(user, password, driver)):
        if (not exceedsLimits(postName)):
          disableAlerts(driver) # eliminar alertas de notificación
          followings = getFollowings(driver, user)
          followers = getFollowers(driver, user)
          print(followers)
          print(followings)
          commentSpam(postName, driver, False, followers, followings)
        else:
          log('Se excede límite de comentaros, esperando de 1 hora ...')
          time.sleep(3600)
    except Exception as e:
      log('Se omite repetición de proceso por error ' + getError(e))
      pass

    # https://www.zyxware.com/articles/5552/what-is-close-and-quit-commands-in-selenium-webdriver
    driver.quit()
    log('Esperando 1 minuto ...')
    time.sleep(60) 


def getPosts():
  try:
    with open('posts.txt', newline='\n') as fPosts:
      Lines = fPosts.readlines()
      return list(Lines)
  except Exception as e:
    log('Error getPosts: ' + getError(e))

  return []

def main(argv): # Start here!
  if not os.path.exists(logsFolder):
    os.makedirs(logsFolder)
  if not os.path.exists(statsFolder):
    os.makedirs(statsFolder)

  username, password, chromeDriverPath, bravePath = getInputParams(argv)
  posts = getPosts()

  if (len(posts) == 0):
    log ('No se encontraron posts en el archivo posts.txt')
  else:
    for post in posts:
      if not os.path.exists(statsFolder+'/'+post):
        os.makedirs(statsFolder+'/'+post)
      process (username, password, post, chromeDriverPath, bravePath)


if __name__ == "__main__":
  main(sys.argv[1:])

