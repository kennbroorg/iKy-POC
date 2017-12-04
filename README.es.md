![Logo of the project](static/images/iKy.png)

# iKy POC
La POC consiste en recolectar datos en base a un e-mail ingresado, formatearlos y realizar una presentación visual de los mismos. Tal visualización fue la que despertó interés sobre todo en áreas relacionadas con el principio de un perfilamiento.

## Motivación
Este proyecto nace como una POC (Proof Of Concept) para la [#eko13](https://www.ekoparty.org). El interés de varias personas por el proyecto nos entusiasmó, por lo que liberamos el código de la POC y creamos un nuevo proyecto en serio.

## Capturas de pantalla


## Software utilizado
* Flask
* jquery
* d3.js
* datasploit

## Instalación
Para la instalación se deberá tener python 2 y pip. Se deberá clonar el repositorio :

```shell
git clone https://github.com/kennbroorg/iKy-POC.git
cd iKy-POC
git submodule init
git submodule update
```

Se deberán instalar las librerías requeridas :

```shell
pip install -r requirements.txt
```

## Configuración
El proyecto Datasploit necesita de la configuración de las APIs de los servicios a utilizar. Para mayor información referirse a [How to Generate Api Keys](https://datasploit.readthedocs.io/en/latest/apiGeneration/).

Como la POC utiliza datasploit desde pip, ejecutando el siguiente comando se pueden configurar las APIs necesarias.

```shell
python src/datasploit/datasploit_config.py
```

Las APIs (que necestan key) utilizadas en esta POC son :
- FullContact
- GitHub
- Twitter
- MailBoxLayer

De todas maneras el programa se encarga de validarlas, reportando que es lo que falta.

## Utilización
El proyecto es simple. Ejecutar el httpData.py para levantar el servidor :

```shell
python httpData.py
```

Los parámetros por defecto son :
* ip : 127.0.0.1
* port : 5500

Pero pueden cambiarse :

```shell
python httpData.py -h
python httpData.py -i 127.0.0.1
python httpData.py -p 5500
python httpData.py -i 127.0.0.1 -p 5500
```

Una vez ejecutado el servidor, desde el navegador ingresar a la ip:puerto elegido.

## Contribuciones
No para este proyecto. Pronto liberaremos un proyecto mejorado de este y allí se podrá contribuir.

## Licencia
Este proyecto esta bajo la licencia del MIT. Para mayor detalle ver [LICENSE.md](LICENSE.md).
