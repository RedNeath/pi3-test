# pi3-test
A complete test of several web server frameworks to measure their average power-consumption when handling 10 concurrent users on a Raspberry Pi 3.

To run this test, here's the base docker compose file:
```yaml
services:
  # MariaDB database
  db:
    image: linuxserver/mariadb:latest
    container_name: mariadb
    networks:
      - app-network
    environment:
      PUID: ${PUID:-1000}
      PGID: ${PGID:-1000}
      TZ: ${TZ:-UTC}
      MYSQL_ROOT_PASSWORD: ${DB_ROOT_PASSWORD}
      MYSQL_DATABASE: ${DB_NAME}
      MYSQL_USER: ${DB_USER}
      MYSQL_PASSWORD: ${DB_PASSWORD}
    ports:
      - "3306:3306"
    volumes:
      - mariadb_data:/config
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 60s
      timeout: 5s
      retries: 5

  # Backend
  backend:
    # See below!!
    
  # Frontend Vue.js
  frontend:
    image: redneath/pi3-test-frontend:latest
    container_name: vue_frontend
    networks:
      - app-network
    ports:
      - "9000:80"
    depends_on:
      - backend
    restart: unless-stopped

networks:
  app-network:
    driver: bridge

volumes:
  mariadb_data:
```

Then you will need to complete it with the appropriate image for the backend you want to test. See the list below.

## Express.js
1. Create a `.env` file with the appropriate data (see the `example.env` file).
2. Add the following to the `docker-compose.yaml` file:
```yaml
    image: redneath/pi3-test-express:latest
    container_name: express_backend
    networks:
      - app-network
    working_dir: /app
    environment:
      DB_HOST: db
      DB_USER: ${DB_USER}
      DB_PASSWORD: ${DB_PASSWORD}
      DB_NAME: ${DB_NAME}
      NODE_ENV: production
    ports:
      - "3000:3000"
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped
```
3. Once the compose stack is launched, connect to the `express_backend` (`docker exec -it express_backend sh`) container and execute the following commands:
```sh
npm install -g sequelize-cli
npm run db:setup
```

When launching the stack, the frontend will be available at [`http://localhost:9000`](http://localhost:9000) and the backend at [`http://localhost:3000`](http://localhost:3000).

# Conduct the test
Once you have a running backend, you can run the test using the `clients.py` script at the root of this repository. You will just need to change the URI for the IP address of your pi 3.

And to measure the power consumption during the test, you'd preferrably want to use a "connected" plug, but if you don't have one, you can use the monitor argument of the clients script. It will keep an eye on the CPU load, and thus estimate roughly the power used by the pi 3.
