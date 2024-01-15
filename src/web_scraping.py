# importa el modulo request para extrar una pagina web
import requests
# importa el modulo bs4 la libreria BeautifulSoup para transformar el codigo en html
from bs4 import BeautifulSoup
#Importar la clase 'datetime' para trabajar con fechas y horas.
from datetime import datetime
# Importa os para interacciones con el sistema de archivos.
import os

#Definir la función 'webscraping' , para convocorla de manera recurrente sin tener que definirla de nuevo.
def webscraping(url_scraping,categoria_scraping='todas'):
    # URL de de telemadrid. Asigna el valor del parámetro url_scraping a la variable url.
    url = url_scraping

    # Realizar la petición, empleando la excepción try.
    try:
        respuesta = requests.get(url)
        #print(respuesta)
        #print(respuesta.text)
        # Verificar si la petición fue exitosa (código 200)
        if respuesta.status_code == 200:
            try:
                # Abre o crea un archivo CSV y escribe la cabecera.
                with open('../data/noticias.csv', 'w') as f:
                    f.write('titulo,url,categoria,fecha'+'\n')
                # Analizar el contenido con BeautifulSoup
            except:
                print("ERROR: no se pudo crear el archivo noticias.csv")
            try:
                #Parsea el HTML de la respuesta.
                soup = BeautifulSoup(respuesta.text, 'html.parser')
                try:
                    # Encuentra todos los articulos de noticias de la web de telemadrid.
                    noticias = soup.find_all('article', class_='card-news')
                    if noticias:
                        #print(noticias)
                        lista_categorias = []
                        for articulo in noticias:
                            #print(articulo)
                            try:
                                # Extrae y limpia el título de la noticia.
                                titulo = articulo.find('a', class_='oop-link').text.strip()
                                # Extrae la URL de la noticia.
                                url_noticia = articulo.find('a', class_='opp-link')['href']
                                #Divide la URL para extraer la categoría.
                                lista_url_noticia = url_noticia.split('/')
                                # Agrega la categoría a la lista.
                                if lista_url_noticia[1] != '':
                                    categoria = lista_url_noticia[1]
                                else:
                                    categoria = lista_url_noticia[3]
                                    # Extrae y formatea la fecha de la noticia.
                                lista_categorias.append(categoria)
                                lista_fecha = url_noticia.split('--')
                                fecha_caracteres = lista_fecha[1].replace('.html', '')
                                # print(fecha_caracteres)
                                # print(fecha_caracteres[0:4])
                                # print(fecha_caracteres[4:6])
                                # print(fecha_caracteres[6:8])
                                # print(fecha_caracteres[8:10])
                                # print(fecha_caracteres[10:12])
                                # print(fecha_caracteres[12:14])
                                fecha = datetime(int(fecha_caracteres[0:4]), int(fecha_caracteres[4:6]),
                                                 int(fecha_caracteres[6:8]))
                                fecha = fecha.strftime("%Y/%m/%d")
                                # Limpia el título de caracteres especiales.
                                titulo = titulo.replace('\'','').replace('"','').replace(',','')
                                if categoria_scraping == 'todas':
                                    try:
                                        # Escribe los datos de la noticia en el archivo CSV.
                                        with open('../data/noticias.csv', 'a') as f:
                                            f.write(titulo+','+url_noticia+','+categoria+','+str(fecha)+'\n')
                                        # Analizar el contenido con BeautifulSoup
                                    except:
                                        print("ERROR: no se pudo anexar la noticia al archivo noticias.csv")
                                else:
                                    if categoria == categoria_scraping:
                                        try:
                                            with open('../data/noticias_'+categoria_scraping+'.csv', 'a') as f:
                                                f.write(titulo + ',' + url_noticia + ',' + categoria + ',' + str(
                                                    fecha) + '\n')
                                            # Analizar el contenido con BeautifulSoup
                                        except:
                                            print("ERROR: no se pudo anexar la noticia al archivo noticias.csv")
                            except:
                                try:
                                    titulo = articulo.find('a', class_='lnk').text.strip()
                                    url_noticia = articulo.find('a', class_='lnk')['href']
                                    lista_url_noticia = url_noticia.split('/')
                                    if lista_url_noticia[1] != '':
                                        categoria = lista_url_noticia[1]
                                    else:
                                        categoria = lista_url_noticia[3]
                                    lista_categorias.append(categoria)
                                    lista_fecha = url_noticia.split('--')
                                    fecha_caracteres = lista_fecha[1].replace('.html', '')
                                    #print(fecha_caracteres)
                                    #print(fecha_caracteres[0:4])
                                    #print(fecha_caracteres[4:6])
                                    #print(fecha_caracteres[6:8])
                                    #print(fecha_caracteres[8:10])
                                    #print(fecha_caracteres[10:12])
                                    #print(fecha_caracteres[12:14])
                                    fecha = datetime(int(fecha_caracteres[0:4]), int(fecha_caracteres[4:6]), int(fecha_caracteres[6:8]))
                                    fecha = fecha.strftime("%Y/%m/%d")
                                    titulo = titulo.replace('\'', '').replace('"', '').replace(',', '')
                                    if categoria_scraping == 'todas':
                                        try:
                                            with open('../data/noticias.csv', 'a') as f:
                                                f.write(titulo + ',' + url_noticia + ',' + categoria + ',' + str(
                                                    fecha) + '\n')
                                            # Analizar el contenido con BeautifulSoup
                                        except:
                                            print("ERROR: no se pudo anexar la noticia al archivo noticias.csv")
                                    else:
                                        if categoria == categoria_scraping:
                                            try:
                                                with open('../data/noticias_' + categoria_scraping + '.csv', 'a') as f:
                                                    f.write(titulo + ',' + url_noticia + ',' + categoria + ',' + str(
                                                        fecha) + '\n')
                                                # Analizar el contenido con BeautifulSoup
                                            except:
                                                print("ERROR: no se pudo anexar la noticia al archivo noticias.csv")
                                except:
                                    pass
                                # Convierte la lista de categorías en un conjunto para eliminar duplicados.
                        #print(lista_categorias)
                        conjunto_categorias = set(lista_categorias)
                        #print(conjunto_categorias)
                    else:
                        print(f"Error La pagina {url} no contiene noticias")
                except:
                        print(f"ERROR: No se pudo encontrar articulos en el codigo html")
            except:
                print(f"ERROR: no se pudo convertir la pagina a codigo html")
        else:
            print(f"Error al obtener la página web. Código de estado: {respuesta.status_code}")
    except:
        print(f"ERROR: No se puede abrir la web pagina {url} o existe un error al procesarla")
    return conjunto_categorias


listado_categorias = webscraping('https://www.telemadrid.es/','todas')
seleccion = 'x'
while seleccion != '0':
    print("Lista de categorias: ")
    i = 1
    for opcion in listado_categorias:
        print(f"{i}.- {opcion}")
        i = i + 1
    print("0.- Salir")
    seleccion = input("Por favor seleccione una opcion indicando un numero:")
    categorias_listas = list(listado_categorias)
    categoria_seleccionada = categorias_listas[int(seleccion)-1]
    webscraping('https://www.telemadrid.es/', categoria_seleccionada)

#Creación de la función descargar noticias csv para obtener un archivo csv que incluya las noticias seleccionadas por categoría.
def descargar_noticias_csv(nombre_archivo):

    #Descarga el archivo CSV de noticias a la máquina local del usuario.

    #nombre_archivo (str): Nombre del archivo CSV a descargar.
    ruta_archivo = os.path.join('../data', nombre_archivo)
    if os.path.exists(ruta_archivo):
        try:
        #descarga del archivo.
            return f"El archivo {nombre_archivo} ha sido descargado exitosamente."
        except Exception as e:
            return f"Ocurrió un error al descargar el archivo: {e}"
    else:
        return "El archivo no existe en el directorio especificado."
print(descargar_noticias_csv('noticias.csv'))