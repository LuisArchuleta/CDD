import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

download_path = os.path.join(os.getcwd(), "datos_conagua")
if not os.path.exists(download_path):
    os.makedirs(download_path)

# 1. Configuración inicial
chrome_options = Options()
# chrome_options.add_argument("--headless") # Opcional
prefs = {"download.default_directory": download_path}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_experimental_option("detach", True)#dejar ventana abierta. 

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
actions = ActionChains(driver)
wait = WebDriverWait(driver, 15)

try:
    driver.get("https://cucapa-clicom.cicese.mx/") # O la URL exacta de descarga
    
    btn_pestana_descarga = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Descarga de Datos")))
    btn_pestana_descarga.click()
    print("Entrando a la sección de Descarga de Datos...")

except Exception as e:
    print(f"Error al dar clic: {e}")

try:
    print("Intentando seleccionar el estado por índice...")
    
    # 1. Buscamos todos los 'select' que hay en la página
    dropdowns = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "select")))
    
    # El primer dropdown (índice 0) suele ser el de ESTADO
    menu_estado = dropdowns[0]
    
    # 2. Asegurarnos de que sea visible y darle clic
    driver.execute_script("arguments[0].scrollIntoView();", menu_estado)
    time.sleep(1) # Pausa breve para el scroll
    
    # 3. Usar la clase Select para elegir Sinaloa
    select_estado = Select(menu_estado)
    
    # Intentamos por texto visible
    select_estado.select_by_visible_text("Sinaloa")
    
    print("¡Sinaloa seleccionado correctamente!")
    
    # Esperamos a que la página reaccione y cargue las estaciones
    time.sleep(3)

except Exception as e:
    print(f"Error al seleccionar por índice: {e}")
    # Si falla por texto, intentamos por valor (Sinaloa suele ser el valor '25' en sistemas de México)
    try:
        select_estado.select_by_value("25")
        print("Seleccionado por valor (25).")
    except:
        print("También falló la selección por valor.")

try:
    
    print("Buscando el cuadro de búsqueda...")
    # Buscamos todos los inputs y filtramos el que es de texto y está visible
    todos_los_inputs = driver.find_elements(By.TAG_NAME, "input")
    input_estacion = None
    
    for i in todos_los_inputs:
        tipo = i.get_attribute("type")
        # El cuadro de búsqueda suele ser el único input tipo 'text' visible
        if tipo == "text" and i.is_displayed():
            input_estacion = i
            break
            
    if input_estacion:
        print("Cuadro encontrado. Ingresando 'CULIACAN (CAADES)'...")
        # Limpiamos e ingresamos
        input_estacion.clear()
        input_estacion.send_keys("CULIACAN (CAADES)")
        
        # Localizar el botón Buscar (Opción A que ya sabemos que funciona)
        print("Presionando botón Buscar...")
        boton_buscar = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='Buscar']")))
        boton_buscar.click()
        
        # Esperamos a que la lista de resultados cargue
        time.sleep(4)
    else:
        print("No se encontró el cuadro de texto. Probando alternativa...")
        # Alternativa extrema: Inyectar por selector genérico si el loop falla
        driver.execute_script("document.querySelector('input[type=\"text\"]').value = 'CULIACAN (CAADES)';")
        driver.find_element(By.XPATH, "//*[text()='Buscar']").click()

except Exception as e:
    print(f"Error en el Paso 3: {e}")

# --- PASO 4: DOBLE CLIC EN EL RESULTADO ---
try:
    print("Buscando 'CULIACAN (CAADES), SIN' en la lista de resultados...")
    
    # 1. Localizamos el elemento en la lista. 
    # Usamos un XPATH que busque el texto exacto que aparece en tu captura.
    selector_resultado = "//*[contains(text(), 'CULIACAN (CAADES), SIN')]"
    
    # Esperamos a que el elemento sea visible y esté listo
    estacion_resultado = wait.until(EC.visibility_of_element_located((By.XPATH, selector_resultado)))
    
    # 2. Scroll para asegurar que el elemento esté centrado y Selenium no falle
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", estacion_resultado)
    time.sleep(1) # Pausa para que el scroll termine
    
    # 3. Ejecutar el DOBLE CLIC
    print("Realizando doble clic...")
    actions.double_click(estacion_resultado).perform()
    
    print("¡Estación movida a 'Seleccionadas' con éxito!")
    time.sleep(2) # Espera para ver el cambio en pantalla

except Exception as e:
    print(f"Error en el Paso 4 (Doble Clic): {e}")

# --- PASO 5: CICLO DE DESCARGAS (VERSION POR CLASE) ---
try:
    # Verificamos los nombres. A veces llevan acento: Precipitación, Evaporación
    variables_a_descargar = ["Tmax", "Tmin", "Precipitación", "Evaporación"]
    print("Iniciando ciclo de descargas...")

    for var in variables_a_descargar:
        print(f"\n--- Procesando: {var} ---")
        
        # 1. Refrescar dropdowns
        dropdowns = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "select")))
        menu_variable = dropdowns[1] 
        Select(menu_variable).select_by_visible_text(var)
        time.sleep(3) # Aumentamos a 3 segundos para que el botón se estabilice

        # 2. LOCALIZACIÓN DINÁMICA DEL BOTÓN
        print("Buscando botón de generación por XPATH relativo...")
        try:
            # Buscamos cualquier elemento que tenga el texto 'Descargar' y sea clicable
            # Usamos un punto (.) para buscar dentro de cualquier etiqueta
            boton_generar = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Descargar')]")))
        except:
            print("No se halló por texto, intentando por clase de botón...")
            # En portales de este tipo, el botón de descarga suele ser el primero con clase 'btn'
            botones_btn = driver.find_elements(By.CLASS_NAME, "btn")
            # Filtramos los que son visibles y están cerca del formulario
            boton_generar = [b for b in botones_btn if b.is_displayed()][-1] # Usualmente es el último de la sección

        # 3. EJECUTAR CLIC
        if boton_generar:
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", boton_generar)
            time.sleep(1)
            # Forzamos el click con JS para evitar errores de intercepción
            driver.execute_script("arguments[0].click();", boton_generar)
            print("Botón gris presionado.")
        else:
            print("FALLA CRÍTICA: No se encontró ningún botón de descarga.")
            continue

        # 4. MANEJO DEL ENLACE AZUL (.csv)
        try:
            print("Esperando enlace azul...")
            # El enlace azul suele estar en un contenedor con ID 'mensaje' o similar
            enlace_csv = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, ".csv")))
            print(f"¡Enlace encontrado! Descargando {var}...")
            
            driver.execute_script("arguments[0].click();", enlace_csv)
            time.sleep(7) # Tiempo para que baje el archivo
            
            # 5. CERRAR POP-UP con ESC
            actions.send_keys(webdriver.common.keys.Keys.ESCAPE).perform()
            time.sleep(1)
            
        except Exception as e_link:
            print(f"No apareció el link azul para {var}. Revisa si la ventana emergente se bloqueó.")

    print("\n¡Ciclo terminado!")

except Exception as e:
    print(f"Error general: {e}")

    # # --- PASO 5: CICLO DE DESCARGAS ---
    # try:
    #     # Asegúrate de que estos nombres sean idénticos a los del menú
    #     variables_a_descargar = ["Tmax", "Tmin", "Precipitación", "Evaporación"]
        
    #     print("Iniciando ciclo de descargas...")

    #     for var in variables_a_descargar:
    #         print(f"\n--- Procesando: {var} ---")
            
    #         # 1. Refrescar el menú de variables
    #         dropdowns = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "select")))
    #         menu_variable = dropdowns[1] 
    #         Select(menu_variable).select_by_visible_text(var)
    #         time.sleep(2) 

    #         # 2. Clic en el botón para GENERAR el archivo (el botón gris)
    #         # Probamos primero con el clic normal de Selenium que es más "humano"
    #         try:
    #             boton_generar = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Descargar']")))
    #             boton_generar.click()
    #         except:
    #             # Si falla el clic normal, usamos el de JavaScript que no falla
    #             boton_generar = driver.find_element(By.XPATH, "//input[@value='Descargar']")
    #             driver.execute_script("arguments[0].click();", boton_generar)
            
    #         print("Botón presionado. Esperando ventana emergente...")

    #         # 3. MANEJO DEL ENLACE AZUL (El que sale en la ventanita)
    #         try:
    #             # Esperamos hasta 10 segundos a que aparezca el link del CSV
    #             enlace_csv = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, ".csv")))
    #             print(f"¡Ventana emergente detectada! Descargando {var}...")
                
    #             # Clic en el enlace azul
    #             enlace_csv.click()
                
    #             # Espera para que inicie la descarga antes de seguir con la otra variable
    #             time.sleep(6)
                
    #             # 4. CERRAR LA VENTANA EMERGENTE (Crucial para que no tape el menú)
    #             # Buscamos el botón de cerrar (suele ser una X o un botón que dice 'Cerrar' o 'Close')
    #             try:
    #                 # Intentamos cerrar con la tecla Escape o buscando el botón
    #                 actions.send_keys(webdriver.common.keys.Keys.ESCAPE).perform()
    #                 # Opcional: buscar botón cerrar por texto si el ESC no funciona
    #                 # driver.find_element(By.XPATH, "//*[contains(text(), 'Cerrar')]").click()
    #             except:
    #                 pass

    #         except Exception as e_link:
    #             print(f"No apareció el enlace para {var}. Error: {e_link}")

    #     print("\n¡Ciclo terminado con éxito!")

    # except Exception as e:
    #     print(f"Error general en el ciclo: {e}")