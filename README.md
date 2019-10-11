# Storymap API

This application provides an interface for programmatically accessing
information from Storymap features and metadata tables.  

### Application Design
HTTP GET requests are routed through Flask (a Python web framework), to query and return results from the PostgreSQL database. The database, logic layer, and front end are all encapsulated in the single container for convenience of use.

### Application usage
- The application is intended to be used as a stateless utility service. Recommended usage is to start containers when needed. No information is to be saved in the container. In the event of a container or docker error condition, simply kill and restart the container. 

### Utilize a new database version?
- If you would like to use a new or modified database for the application, just replace the file data/storymap.sql in the project source with your new full PosgreSQL dump (see the storymap.sql file for an example). The build process specified in the Dockerfile will perform the SQL restore (progress output will be displayed on cosole), and the new database will be available on next run of the container.
  
  
### Run the application
- The application is ready to be used as a pre-built docker container:  

```console
user@host:~$ docker run -d --rm -p8000:5000 snolan1/storymap_api:release1.0
```  
This will pull the container from docker hub, and start it (-d) detached (in the background). The container will be ephemeral (--rm) and will be deleted when stopped. TCP port 5000 inside of the container will be exposed as 8000 locally, where the application will be available.

- The docker container can also be built and run from scratch locally:
```console
user@host:~$ git clone https://github.com/snolan1/map_db_api.git
Cloning into 'map_db_api'...
remote: Enumerating objects: 129, done.
remote: Counting objects: 100% (129/129), done.
remote: Compressing objects: 100% (96/96), done.
remote: Total 129 (delta 66), reused 88 (delta 28), pack-reused 0
Receiving objects: 100% (129/129), 107.92 KiB | 741.00 KiB/s, done.
Resolving deltas: 100% (66/66), done.

user@host:~$ cd map_db_api/
user@host:~/map_db_api$ docker build --tag=storymap_api .
...build output...
user@host:~$ docker run -d --rm -p8000:5000 storymap_api
```




##### Principals
Arizona Geological Survey  
Stephen Nolan  
Andrew Zaffos  
Haley Snellen  
