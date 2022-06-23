# Recursos necesarios
- python3 (instalar via apt)
- pip3 (instalar via apt)
- scrapy (instalar via pip3)
- cron (instalar via apt)
- unittest (instalar via pip3)
# Ejecutando el crawler
Para iniciar el archivo 'spider_runner.py' ejecutar el siguiente comando: 
```
python3 spider_runner.py
```
esto inicia el crawler que iniciara la descarga de datos del dominio uc.edu.py que se almacenan en el directorio /spiders/uc_data.
# Daemonizando el proceso de Crawling
Luego de instalar el paquete cron via apt se debe ejecutar el archivo 'daemonSchedule.py' mediante el comando
```
python3 daemonSchedule.py
```
A continuacion se muestra un editor con un archivo temporal en el cual se debe agregar una linea de acuerdo a los siguientes criterios:

“minutos” “horas” “día del mes” “día de la semana” “usuario” “comando o script”

```
# Edit this file to introduce tasks to be run by cron.
# Each task to run has to be defined through a single line 
# indicating with different fields when the task will be run 
# and what command to run for the task
# To define the time you can provide concrete values for 
# minute (m), hour (h), day of month (dom), month (mon), 
# and day of week (dow) or use '*' in these fields (for 'any').
# Notice that tasks will be started based on the cron's system 
# daemon's notion of time and timezones.
#Output of the crontab jobs (including errors) is sent through 
# email to the user the crontab file belongs to (unless redirected).
# For example, you can run spider_runner 
#at 00 a.m every day with:
# For more information see the manual pages of crontab(5) and cron(8) #.
#mh dom mon dow command
0 0 * * * python3 [path of spider_runner.py]
```
Esta ultima linea hace que el crawler se ejecute automaticamente por ejemplo todos los dias a las 00:00 am

# Testeo
Para el testeo se debe ejecutar 'test.py'
```
python3 -m unittest test.spiderTest
```
Se incluye en el testeo:

- Funcionamiento adecuado del crawler con su respectivo log
- Verificacion de la creacion adecuada del directorio

# Version actual
- Extracción y almacenamiento del contenido HTML de cada página independiente dentro del dominio.
- Almacenamiento del contenido HTML en una estructura de archivos JSON en la carpeta ‘uc_data’
- Filtro de enlaces (links) encargado de omitir links repetidos y links externos al dominio de uc.edu.py
- Protocolo que evita escanear información innecesaria o privada de un sitio web
- Control de internal server error (500)
- Servicio o scheduler configurable (requiere configuracion por parte del administrador)
