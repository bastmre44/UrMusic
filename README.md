# UrMusic
*Frontend y backend para segundo proyecto de AYED*

**Información importante:**
- Para correr el programa, se necesita instalar las librerias que se encuentran en el archivo requirements.txt dentro del folder UrMusic. 

**Notas:**

El folder static, contiene los archivos css y js que se usan en la pagina web.

El folder templates, contiene los archivos html que se usan en la pagina web.

El folder ScriptsSecundarios, contiene los archivos python que se usan en la pagina web indirectamente.

El script más importante para el frontend es el archivo programaprincipal.py, que se encarga de correr el servidor y manejar las rutas de la pagina web.

Para el backend, todo se localiza en el archivo recommendation_system.py, que se encarga de manejar la recomendación de canciones.

Hay 2 archivos HTML en UrMusic/templates que son los que se pueden cambiar para alterar la organización de la página:
index.html es el de búsqueda y resultados.html es el que te muestra los artistas.

Para cambiar o agregar estilos de los componentes, es el archivo CSS que está en UrMusic/static/style.css

El script que genera los artistas con sus datos en la interfaz es el que está en UrMusic/static/main2.js

**Credenciales para la base de datos en Neo4j SandBox** 

User: neo4j
URL: neo4j+s://ad86f838.databases.neo4j.io
Contraseña: 69W0amO7JsyNTTrsb506RR_6hUBxlzfZTPM-znz-Unw

***¿Como correr el programa?:***

1. Run el archivo programaprincipal.py. 
2. Abre el archivo index.html en tu navegador.
3. ¡Listo! Ya puedes buscar un artista y recibir recomendaciones.
4. Al parar el script programaprincipal.py, ya no funcionarán las recomendaciones. 
