from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

aria_label_curso = "LENGUAJES DE PROGRAMACION II [ Mod 2, ABR-SEP26 Ves"
link = "https://virtual3.itsqmet.edu.ec:84/"
user = "pnavarrete@itsqmet.edu.ec"
actividad = "ACTIVIDAD CONTACTO DOCENTE 1"

def esperar_elemento(driver, xpath, type=By.XPATH, timeout=20):
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((type, xpath))
        )
    except Exception as e:
        print(f"Error al esperar el elemento: {xpath}", e)
        driver.quit()   

def obtener_elemento(driver, xpath, type=By.XPATH):
    try:
        return driver.find_element(type, xpath)
    except Exception as e:
        print(f"Error al obtener el elemento: {xpath}", e)
        driver.quit()

options = webdriver.EdgeOptions()
options.add_experimental_option("detach", False)
options.add_argument("--start-maximized")
service = Service("msedgedriver.exe")
driver = webdriver.Edge(service=service)

driver.get(link)

esperar_elemento(driver, f".//div[@data-test-id='{user}']")
obtener_elemento(driver, f".//div[@data-test-id='{user}']").click()

esperar_elemento(driver, f"//a[.//*[contains(text(), '{aria_label_curso}')]]")
aula = obtener_elemento(driver, f"//a[.//*[contains(text(), '{aria_label_curso}')]]")

driver.execute_script("arguments[0].click();", aula)

time.sleep(1)  # Espera para que la página cargue completamente

driver.get(driver.current_url + "&section=6") # para pvc

esperar_elemento(driver, f".//a/span[text()='{actividad}']")
actividad = obtener_elemento(driver, f".//a/span[text()='{actividad}']")
driver.execute_script("arguments[0].click();", actividad)

esperar_elemento(driver, f".//a[text()='Calificar']")
obtener_elemento(driver, f".//a[text()='Calificar']").click()

time.sleep(1000)
driver.quit()