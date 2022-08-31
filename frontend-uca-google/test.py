from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from ast import Pass
from selenium import webdriver
from selenium.common.exceptions import TimeoutException as TE
from selenium.common.exceptions import ElementClickInterceptedException as ECIE
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

#Esto es para saber si el driver de chrome ya esta instalado
# chromedriver_autoinstaller.install()

driver = webdriver.Chrome()
driver.get("http://localhost:3000/")

#Escribimos algo en la barra de busqueda
input_box = driver.find_element_by_xpath("//input[@type='text']")
input_box.send_keys("Ingenieria informatica")
time.sleep(2)

#Apretamos el boton buscar
search_button = driver.find_element_by_xpath("//button[@type='submit']").click()
time.sleep(2)

#Hacemos otra busqueda
input_box = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@type='text']")))
input_box.send_keys("Rector cyt")
time.sleep(2)

#Apretamos el boton buscar
search_button = driver.find_element_by_xpath("//button[@type='submit']").click()
time.sleep(5)

#Cambiamos de pagina
next_page = driver.find_element_by_xpath("//*[@id='__next']/div/div[2]/div/div/button[2]").click()
# next_page.click()

time.sleep(2)
prev_page = driver.find_element_by_xpath("//*[@id='__next']/div/div[2]/div/div/button[1]").click()
time.sleep(2)

#Apretamos en algun link
link_press = driver.find_element_by_xpath("//*[@id='__next']/div/div[2]/div/a[1]/div/div").click()


time.sleep(5)
#assert "Python" in driver.title