# pi3-test
A complete test of several web server frameworks to measure their average power-consumption when handling 10 concurrent users on a Raspberry Pi 3.

To run this test, here's the base docker compose file:
```yaml
services:
  # MongoDB database
  db:
    image: mongo:6.0
    container_name: mongodb_db
    networks:
      - app-network
    environment:
      MONGO_INITDB_DATABASE: transport_db
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db
    restart: unless-stopped
    command: ["mongod", "--replSet", "rs0", "--bind_ip_all", "--quiet"]
    healthcheck:
      test: "mongosh --eval \"try { rs.status().ok } catch (e) { rs.initiate({ _id: 'rs0', members: [{ _id: 0, host: 'db:27017' }] }); }\" || exit 1"
      interval: 10s
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
      - "9000:9000"
    depends_on:
      - backend
    restart: unless-stopped

networks:
  app-network:
    driver: bridge

volumes:
  mongo_data:
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
      MONGO_URI: mongodb://db:27017/transport_db?replicaSet=rs0
      NODE_ENV: production
    ports:
      - "3000:3000"
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped
```

When launching the stack, the frontend will be available at [`http://localhost:9000`](http://localhost:9000) and the backend at [`http://localhost:3000`](http://localhost:3000).
