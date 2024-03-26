## Address Book Application
#TODO Technical Description here

## Useful Commands
#TODO query a list of currently supported formats

## Tests
To run the tests, you can use the following command:
```bash
python -m unittest discover -s tests
```

## Docker Setup
### Building and Running

To build and run the Docker environment for Python 3.7 and execute all unit tests, use the following command:

```bash
docker-compose up --build
```
This command builds the Docker image if necessary (or rebuilds if the Dockerfile has changed) and starts the containers defined in docker-compose.yml.

### Interacting with the Docker Container

To keep the container running after the initial command (CMD in Dockerfile) finishes, enabling you to enter the container's bash and run commands manually, you will need to modify the docker-compose.yml file:

1. Uncomment the line `command: tail -f /dev/null` in docker-compose.yml to override the last CMD command in the Dockerfile. This change will keep the container running indefinitely by executing a command that does nothing but keeps the process alive.

2. After making the change, start the container in detached mode: 
   ```bash
   docker-compose up --build -d
   ```

3. Accessing the Container's Bash: 
   ```bash
   docker exec -it al-address-book-app /bin/bash
   ```

4. Running the tests or run Python and import the module manually 
   ```bash
   python -m unittest discover -s tests
   ```

5. To stop running the container run: 
   ```bash
   docker-compose down
   ```
To clean up unused Docker images, which helps in freeing up disk space, use:
```bash
docker image prune -a
```

## Generate Sphinx Documentation
To generate the Sphinx documentation, use the following command on Linux:
```bash
generate_docs.sh
```
and .bat file for Windows:
```bash
generate_docs.bat
```
The script will generate the documentation in the `docs` directory. To view the documentation, open the `index.html` file in the `docs` directory in a web browser.
