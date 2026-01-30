# pi3-test
A complete test of several web server frameworks to measure their average power-consumption when handling 10 concurrent users on a Raspberry Pi 3.

To run this test, here's the base docker compose file:
```yaml
services:
  # MySQL database
  db:
    image: mysql:8.0
    container_name: mysql_db
    networks:
      - app-network
    environment:
      MYSQL_ROOT_PASSWORD: ${DB_ROOT_PASSWORD}
      MYSQL_DATABASE: ${DB_NAME}
      MYSQL_USER: ${DB_USER}
      MYSQL_PASSWORD: ${DB_PASSWORD}
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Backend
  backend:
    # See below!!
    
  # Frontend Vue.js
  frontend:
    image: pi3-test-frontend:latest
    container_name: vue_frontend
    networks:
      - app-network
    ports:
      - "9000:9000"
    depends_on:
      - backend
    restart: unless-stopped

networks:
  app-network:
    driver: bridge

volumes:
  mysql_data:
```

Then you will need to complete it with the appropriate image for the backend you want to test. See the list below.

## Express.js
1. Create a `.env` file with the appropriate data (see the `example.env` file).
2. Add the following to the `docker-compose.yaml` file:
```yaml
    image: pi3-test-express:latest
    container_name: express_backend
    networks:
      - app-network
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

When launching the stack, the frontend will be available at [`http://localhost:9000`](http://localhost:9000) and the backend at [`http://localhost:3000`](http://localhost:3000).
