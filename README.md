# 291-miniproject-2

## Run

Prerequisites:

- [Docker](https://www.docker.com/products/docker-desktop)

```bash
mkdir mongo_db
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

This command starts the client and server in development mode.

- Check the client at [http://localhost:3000](http://localhost:3000).
- Check the server at [http://localhost:3001](http://localhost:3001).

It supports live reloading, so whenever you change something in your code, it will automatically update!
