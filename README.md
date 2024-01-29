# Pruebas para el aplicativo Urban.Routes (Happy Path)

### Acerca del proyecto

- El objetivo de este proyecto es la automatización de pruebas para comprobar que las pruebas positivas para el aplicativo Urban.Routes sean exitosas. Dichas pruebas cubren todo el proceso de ordenar un taxi, desde llenar las direcciones de ruta hasta esperar a que un conductor acepte nuestro pedido. El proceso de las pruebas parte con el modo personal y la tarifa comfort
- El proyecto contiene los siguientes archivos:
  1. data.py : Donde colocaremos nuestra url a la base de datos cada vez que queramos ejectura las pruebas, ademas, aqui se situan los datos a probar en los diferentes campos
  2. main.py : Aqui se situan las pruebas a ejecutar, se incluyen tanto los localizadores como las funciones necesarias para correr las pruebas
### Para clonar el repositorio en tu computadora

- Abre tu consola e ingresa el siguiente comando : 'git clone git@github.com:username/qa-project-07.git'

### Tecnologias

- Pycharm --Versión 2023.2.5
- Python --Versión 3.12.1
- Banco de pruebas para Urban.Routes

### Librerias necesarias (pycharm)

- Pytest (Comando en terminal : pip install pytest)
- Requests (Comando en terminal : pip install requests)
- Selenium (Comando en terminal: pip install selenium)

### Pasos para la ejecucion de pruebas

1. Abre el archivo en PyCharm
2. Inicia el servidor del banco de pruebas para Urban.Routes
3. Pegar la Url del banco de pruebas en el parametro 'URL_SERVICE' del archivo 'configuration.py'
4. Ejecuta todas las pruebas con el comando 'pytest main.py'


##### Meza Olivas Javier - 7Mo Sprint