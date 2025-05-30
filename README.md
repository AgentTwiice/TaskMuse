# TaskMuse

Monorepo for the TaskMuse project. It contains the backend API and the React Native mobile client.

## Directory structure

```
.
├── backend        # FastAPI application
├── mobile         # React Native app (Expo)
│   ├── app                # Expo Router screens
│   └── src/context        # Shared React contexts
├── scripts        # Helper scripts
├── docker-compose.yml
└── .env.example
```

The backend exposes a `/healthz` endpoint for health checks. The mobile app uses
Expo Router with Login, Register, Home, Task Details and Voice Capture screens.

