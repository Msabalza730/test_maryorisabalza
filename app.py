import csv
import time

from bs4 import BeautifulSoup
from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

app = Flask(__name__)


def scrape_data():
    """
    Function to do web scrapping using Selenium
    """
    
    url = "https://procesosjudiciales.funcionjudicial.gob.ec/expel-busqueda-avanzada"
    
    # data test
    actor = "0968599020001"
    demandado = "1791251237001"

    # using chrome driver
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    
    driver.get(url)
    wait = WebDriverWait(driver, 50)    

    # Input data: Actor
    input_actor = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[formcontrolname="cedulaActor"]')))
    
    input_actor.send_keys(actor) # Send data
    
    # Input data: Demandado
    input_demandado = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[formcontrolname="cedulaDemandado"]')))
    
    input_demandado.send_keys(demandado)  # Send data
    
    # Scroll down
    scroll = '[formcontrolname="numeroFiscalia"]'
    driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.CSS_SELECTOR, scroll))

    time.sleep(5)

    #Search button submit and click
    boton_buscar = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Enviar formulario']")))
    boton_buscar.click()

    time.sleep(20)
    
    # quit chrome
    driver.quit()

# Endpoint 
@app.route('/scrape')
def run_scraping():
    scrape_data()
    return jsonify({'message': 'Web scraping completed successfully'})

if __name__ == '__main__':
    app.run(debug=True)
