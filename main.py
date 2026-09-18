from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
import zipfile
import os
from openai import OpenAI

client = OpenAI()

aria_label_curso = "LENGUAJES DE PROGRAMACION II [ Mod 2, ABR-SEP26 Ves"
link = "https://virtual3.itsqmet.edu.ec:84/"
user = "pnavarrete@itsqmet.edu.ec"
actividad = "ACTIVIDAD CONTACTO DOCENTE 1"
carpeta_temp = "temp"

instrucciones_actividad = """
Resuelva los siguientes ejercicios en Java utilizando Clases y Objetos:

1. Crea una clase Rectangulo que modele rectángulos por medio de cuatro puntos (los 
vértices). Dispondrá de dos constructores: uno que cree un rectángulo partiendo de sus 
cuatro vértices y otro que cree un rectángulo partiendo de la base y la altura, de forma 
que su vértice inferior izquierdo esté en (0,0). La clase también incluirá un método para 
calcular la superficie y otro que desplace el rectángulo en el plano. 

2. Define una clase Linea con dos atributos: _puntoA y _puntoB. Son dos puntos por  
los que pasa la línea en un espacio de dos dimensiones. La clase dispondrá de los 
siguientes métodos: 
Linea() 
Constructor predeterminado que crea una línea con sus dos puntos como (0,0) y (0,0). 
Linea(Punto, Punto) 
Constructor que recibe como parámetros dos objetos de la clase Punto,  
que son utilizados para inicializar los atributos. 
mueveDerecha(double) 
Desplaza la línea a la derecha la distancia que se indique. 
mueveIzquierda(double) 
Desplaza la línea a la izquierda la distancia que se indique. 
mueveArriba(double) 
Desplaza la línea hacia arriba la distancia que se indique. 
mueveAbajo(double) 
Desplaza la línea hacia abajo la distancia que se indique. 
Accedentes y mutadores. 
Método que nos permita mostrar la información de la línea de la siguiente forma: 
[puntoA,puntoB]. Por ejemplo: [(0.0,0.0),(1.0,1.0)]. 

3. Desarrolla una clase Cafetera con atributos _capacidadMaxima (la cantidad máxima 
de café que puede contener la cafetera) y _cantidadActual (la cantidad actual de café 
que hay en la cafetera). Implementa, al menos, los siguientes métodos: 
Constructor predeterminado: establece la capacidad máxima en 1000 (c.c.)  
y la actual en cero (cafetera vacía). 
Constructor con la capacidad máxima de la cafetera; inicializa la cantidad actual de 
café igual a la capacidad máxima. 
Constructor con la capacidad máxima y la cantidad actual. Si la cantidad actual es 
mayor que la capacidad máxima de la cafetera, la ajustará al máximo. 
Accedentes y mutadores. 
llenarCafetera(): pues eso, hace que la cantidad actual sea igual a la capacidad.  
servirTaza(int): simula la acción de servir una taza con la capacidad indicada.  
Si la cantidad actual de café “no alcanza” para llenar la taza, se sirve lo que quede. 
vaciarCafetera(): pone la cantidad de café actual en cero.  
agregarCafe(int): añade a la cafetera la cantidad de café indicada. 

4. Crea una clase Fecha con atributos para el día, el mes y el año de la fecha.  
Incluye, al menos, los siguientes métodos: 
Constructor predeterminado con el 1-1-1900 como fecha por defecto. 
Constructor parametrizado con día, mes y año. 
leer(): pedirá al usuario el día (1 a 31), el mes (1 a 12) y el año (1900 a 2050). 
bisiesto(): indicará si el año de la fecha es bisiesto o no. 
diasMes(int): devolverá el número de días del mes que se le indique  
(para el año de la fecha). 
valida(): comprobará si la fecha es correcta (entre el 1-1-1900 y el 31-12-2050); 
si el día no es correcto, lo pondrá a 1; si el mes no es correcto, lo pondrá a 1;  
y si el año no es correcto, lo pondrá a 1900. Será un método auxiliar (privado). 
Este método se llamará en el constructor parametrizado y en leer(). 
Accedentes y mutadores. 
corta(): mostrará la fecha en formato corto (02-09-2003). 
diasTranscurridos(): devolverá el número de días transcurridos  
desde el 1-1-1900 hasta la fecha. 
diaSemana(): devolverá el día de la semana de la fecha  
(0 para domingo, ..., 6 para sábado). El 1-1-1900 fue domingo. 
larga(): mostrará la fecha en formato largo, empezando por el día de la semana 
(martes 2 de septiembre de 2003). 
fechaTras(long): hará que la fecha sea la correspondiente a haber transcurrido 
los días que se indiquen desde el 1-1-1900. 
diasEntre(Fecha): devolverá el número de días entre la fecha y la proporcionada. 
siguiente(): pasará al día siguiente. 
anterior(): pasará al día anterior. 
copia(): devolverá un clon de la fecha. 
igualQue(Fecha): indica si la fecha es la misma que la proporcionada. 
menorQue(Fecha): indica si la fecha es anterior a la proporcionada. 
mayorQue(Fecha): indica si la fecha es posterior a la proporcionada. 

5. Crea las siguientes clases (cada una en su archivo): 
Motor: con métodos para arrancar el motor y apagarlo. 
Rueda: con métodos para inflar la rueda y desinflarla. 
Ventana: con métodos para abrirla y cerrarla. 
Puerta: con una ventana y métodos para abrir la puerta y cerrar la puerta. 
Coche: con un motor, cuatro ruedas y dos puertas; con los métodos que te parezcan adecuados 

6. Desarrolla una clase Cancion con los siguientes atributos: 
titulo: una variable String que guarda el título de la canción. 
autor: una variable String que guarda el autor de la canción. 
y los siguientes métodos: 
Cancion(String, String): constructor que recibe como parámetros el título y el 
autor de la canción (por este orden). 
Cancion(): constructor predeterminado que inicializa el título y el autor a cadenas 
vacías. 
dameTitulo(): devuelve el título de la canción. 
dameAutor(): devuelve el autor de la canción. 
ponTitulo(String):  establece el título de la canción. 
ponAutor(String): establece el autor de la canción.

7. Desarrolla una clase CD con los siguientes atributos: 
canciones: un array de objetos de la clase Cancion. 
contador: la siguiente posición libre del array canciones. 
y los siguientes métodos: 
CD(): constructor predeterminado (creará el array canciones). 
numeroCanciones(): devuelve el valor del contador de canciones. 
dameCancion(int): devuelve la Cancion que se encuentra en la posición indicada. 
grabaCancion(int, Cancion): cambia la Cancion de la posición indicada por la 
nueva Cancion proporcionada. 
agrega(Cancion): agrega al final del array la Cancion proporcionada. 
elimina(int): elimina la Cancion que se encuentra en la posición indicada. 
"""

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

def obtener_sesion(driver):
    session = requests.Session()

    for cookie in driver.get_cookies():
        session.cookies.set(
            cookie["name"],
            cookie["value"],
            domain=cookie.get("domain"),
            path=cookie.get("path", "/")
        )

    return session

def obtener_respuesta(prompt):
    response = client.chat.completions.create(
        model="gpt-5.6-terra",
        messages=[
            {"role": "user", "content": prompt}
        ],
    )
    return response.choices[0].message.content

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

esperar_elemento(driver, f".//div[@class='fileuploadsubmission']/a")
time.sleep(1)

elemento_descargar = obtener_elemento(driver, f".//div[@class='fileuploadsubmission']/a")
nombre_archivo = elemento_descargar.text
url_archivo = elemento_descargar.get_attribute('href')
print(f"Nombre del archivo: {nombre_archivo}, url: {url_archivo}")
print("Descargando...")

session = obtener_sesion(driver)

respuesta = session.get(url_archivo)
respuesta.raise_for_status()

print(respuesta.status_code)
print(respuesta.headers.get("Content-Type"))
with open(f"{carpeta_temp}/{nombre_archivo}", "wb") as f:
    f.write(respuesta.content)

print("Descarga completada")

print("Descomprimiendo...")

with zipfile.ZipFile(f"{carpeta_temp}/{nombre_archivo}", "r") as zip_ref:
    zip_ref.extractall(f"{carpeta_temp}")
    archivos = zip_ref.namelist()

os.remove(f"{carpeta_temp}/{nombre_archivo}")

print("Descomprimido")
print(archivos)

time.sleep(1000)
driver.quit()