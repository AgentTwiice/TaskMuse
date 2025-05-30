# TaskMuse

Monorepo for the TaskMuse project. It contains the backend API and the React Native mobile client.

## Directory structure

```
.
├── backend        # FastAPI application
├── mobile         # React Native app (Expo)
├── scripts        # Helper scripts
├── docker-compose.yml
└── .env.example
```

The backend exposes a `/healthz` endpoint for health checks and simple
authentication routes under `/auth`.


## GitHub Pages Preview

The contents of the `docs/` folder can be served using GitHub Pages. Navigate to
**Settings → Pages** in your repository and select `docs/` as the source. After
a few moments, your documentation will be available at the provided URL.
