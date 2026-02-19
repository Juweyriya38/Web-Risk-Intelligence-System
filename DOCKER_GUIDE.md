# Docker Quick Start Guide

## Services Running

✅ **API Service**: Running on http://localhost:8001
- Health Check: http://localhost:8001/api/v1/health
- API Docs: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

## Docker Commands

### Start Services
```bash
docker-compose up -d
```

### Stop Services
```bash
docker-compose down
```

### View Logs
```bash
docker-compose logs -f
```

### Restart Services
```bash
docker-compose restart
```

### Rebuild and Start
```bash
docker-compose up -d --build
```

### Check Status
```bash
docker-compose ps
```

## Test the API

### Health Check
```bash
curl http://localhost:8001/api/v1/health
```

### Analyze a Domain
```bash
curl -X POST http://localhost:8001/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"domain":"example.com"}'
```

### Analyze with Pretty Output
```bash
curl -X POST http://localhost:8001/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"domain":"google.com"}' | python3 -m json.tool
```

## CLI Usage (Inside Docker)

### Analyze a Domain
```bash
docker exec risk-intelligence-api python main_cli.py analyze example.com
```

### JSON Output
```bash
docker exec risk-intelligence-api python main_cli.py analyze example.com --json
```

### Verbose Mode
```bash
docker exec risk-intelligence-api python main_cli.py analyze example.com --verbose
```

## Troubleshooting

### Port Already in Use
If you get "port already in use" error:
```bash
# Stop any existing containers
docker-compose down

# Kill process on port 8001
fuser -k 8001/tcp

# Start again
docker-compose up -d
```

### View Container Logs
```bash
docker logs risk-intelligence-api
```

### Access Container Shell
```bash
docker exec -it risk-intelligence-api /bin/bash
```

## Notes

- The API runs on **port 8001** (mapped from internal port 8000)
- Configuration is mounted from `./config/settings.yaml`
- The container runs as non-root user for security
