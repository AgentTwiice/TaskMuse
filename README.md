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

