# Storymap API

This application provides an interface for programmatically accessing
information from Storymap features and metadata tables.  

### Application Design
HTTP GET requests are routed through Flask (a Python web framework), to query and return results from the PostgreSQL database. The database, logic layer, and front end are all encapsulated in a single docker container for convenience of use.

### Application usage
- The application is intended to be used as a stateless utility service. Recommended usage is to start containers when needed. No information is to be saved in the container. In the event of a container or docker error condition, simply kill and restart the container. 

### Need to utilize a new database version?
- If you would like to use a new or modified database for the application, just replace the file data/storymap.sql in the project source with your new full PosgreSQL dump (see the storymap.sql file for an example) and re-build the container. The build process specified in the Dockerfile will perform the SQL restore (progress output will be displayed on cosole), and the new database will be available on next run of the container.
  
  
### Run the application
- The application is ready to be used as a pre-built docker container:  

```console
user@host:~$ docker run -d --rm -p8000:5000 snolan1/storymap_api:release1.0
```  
This will pull the container from docker hub, and start it (-d) detached (in the background). The container will be ephemeral (--rm) and will be deleted when stopped. TCP port 5000 inside of the container will be exposed as **8000 locally, where the application will be available.**  
(Please note that the container needs to initialize the database and web server processes before serving API requests; it may take a few seconds after starting the container before the service is available)

http://localhost:8000

- The docker container can also be built and run from scratch locally:
```console
user@host:~$ git clone https://github.com/azgs/Storymap_API.git
Cloning into 'Storymap_API'...
remote: Enumerating objects: 153, done.
remote: Counting objects: 100% (153/153), done.
remote: Compressing objects: 100% (116/116), done.
remote: Total 153 (delta 80), reused 96 (delta 31), pack-reused 0
Receiving objects: 100% (153/153), 113.85 KiB | 724.00 KiB/s, done.
Resolving deltas: 100% (80/80), done.

user@host:~$ cd Storymap_API/

user@host:~/Storymap_API$ docker build --tag=storymap_api .
...build output...

user@host:~/Storymap_API$ docker run -d --rm -p8000:5000 storymap_api
```




##### Principals
Arizona Geological Survey  
Stephen Nolan  
Andrew Zaffos  
Haley Snellen  
