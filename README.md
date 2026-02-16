# OpenCode Modal Server

A persistent OpenCode server deployed on Modal cloud with long-term job storage capabilities.

## Overview

This project sets up an OpenCode server on Modal cloud infrastructure with persistent storage for managing long-term jobs. The server uses Modal's Volume feature to ensure data persistence across deployments and container restarts.

## Features

- 🚀 **Fast deployment** on Modal cloud
- 💾 **Persistent storage** using Modal Volumes
- 🔄 **Long-term job management** with job tracking
- 📊 **Job status monitoring** and retrieval
- 🔒 **Secure storage** for code and results
- ⚡ **Auto-scaling** with Modal's infrastructure

## Prerequisites

1. Python 3.11 or higher
2. Modal account (sign up at https://modal.com)
3. Modal token configured locally

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/GindaChen/opencode-modal-server.git
cd opencode-modal-server
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up Modal

If you haven't already, install Modal and authenticate:

```bash
pip install modal
modal token new
```

This will open a browser window to authenticate with Modal.

## Deployment

### Deploy to Modal

Deploy the server to Modal cloud:

```bash
modal deploy modal_app.py
```

This will:
- Create a persistent volume named `opencode-storage`
- Deploy the FastAPI server
- Provide you with a public URL to access the server

### Run locally for testing

To test the server locally before deploying:

```bash
modal serve modal_app.py
```

## Usage

Once deployed, you'll get a URL like `https://your-username--opencode-server-fastapi-app.modal.run`

### API Endpoints

#### 1. Health Check

```bash
curl https://your-url.modal.run/
```

Response:
```json
{
  "status": "ok",
  "service": "OpenCode Server",
  "storage": "persistent",
  "storage_path": "/storage"
}
```

#### 2. Create a Job

```bash
curl -X POST https://your-url.modal.run/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "code": "print(\"Hello, World!\")",
    "language": "python",
    "description": "Simple hello world example"
  }'
```

Response:
```json
{
  "job_id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "pending",
  "message": "Job created and queued for execution"
}
```

#### 3. Get Job Status

```bash
curl https://your-url.modal.run/jobs/123e4567-e89b-12d3-a456-426614174000
```

Response:
```json
{
  "job_id": "123e4567-e89b-12d3-a456-426614174000",
  "code": "print(\"Hello, World!\")",
  "language": "python",
  "description": "Simple hello world example",
  "status": "completed",
  "created_at": "2026-02-16T22:00:00",
  "updated_at": "2026-02-16T22:00:05",
  "result": {
    "output": "Executed python code",
    "code": "print(\"Hello, World!\")"
  }
}
```

#### 4. List All Jobs

```bash
curl https://your-url.modal.run/jobs
```

Response:
```json
{
  "jobs": [
    {
      "job_id": "123e4567-e89b-12d3-a456-426614174000",
      "status": "completed",
      "language": "python",
      "description": "Simple hello world example",
      "created_at": "2026-02-16T22:00:00",
      "updated_at": "2026-02-16T22:00:05"
    }
  ],
  "count": 1
}
```

#### 5. Delete a Job

```bash
curl -X DELETE https://your-url.modal.run/jobs/123e4567-e89b-12d3-a456-426614174000
```

#### 6. Storage Statistics

```bash
curl https://your-url.modal.run/storage/stats
```

Response:
```json
{
  "total_jobs": 42,
  "storage_path": "/storage",
  "total_size_bytes": 1048576,
  "total_size_mb": 1.0
}
```

## Architecture

### Persistent Storage

The server uses Modal's Volume feature to create a persistent storage layer:

- **Volume Name**: `opencode-storage`
- **Mount Path**: `/storage`
- **Data Structure**: Jobs are stored as JSON files in `/storage/jobs/`

Each job is stored as a separate JSON file named by its UUID, ensuring data persistence across:
- Container restarts
- Deployments
- Auto-scaling events

### Container Configuration

- **Idle Timeout**: 5 minutes (keeps container alive after last request)
- **Job Timeout**: 1 hour (maximum time for a single job)
- **Concurrent Inputs**: Up to 100 concurrent requests
- **Python Version**: 3.11

## Configuration

Edit `config.py` to customize settings:

```python
APP_NAME = "opencode-server"
VOLUME_NAME = "opencode-storage"
STORAGE_PATH = "/storage"
CONTAINER_IDLE_TIMEOUT = 300  # seconds
JOB_TIMEOUT = 3600  # seconds
MAX_CONCURRENT_INPUTS = 100
```

## Development

### Project Structure

```
opencode-modal-server/
├── modal_app.py       # Main Modal application
├── config.py          # Configuration settings
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

### Adding Features

The FastAPI app in `modal_app.py` can be extended with additional endpoints and functionality. The persistent volume ensures all data is retained.

## Monitoring

### View Logs

```bash
modal app logs opencode-server
```

### Check Volume

```bash
modal volume ls
```

## Troubleshooting

### Volume Not Found

If you get a volume not found error, ensure it's created:

```bash
modal volume create opencode-storage
```

### Deployment Issues

Check Modal logs:

```bash
modal app logs opencode-server --follow
```

### Authentication Issues

Re-authenticate with Modal:

```bash
modal token new
```

## Cost Considerations

Modal charges based on:
- CPU/GPU usage
- Storage (persistent volumes)
- Network egress

The `container_idle_timeout` setting helps minimize costs by shutting down idle containers after 5 minutes.

## Security

- Jobs are isolated in separate container executions
- Persistent storage is private to your Modal account
- Use Modal's secrets feature for sensitive configuration

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions:
- GitHub Issues: https://github.com/GindaChen/opencode-modal-server/issues
- Modal Documentation: https://modal.com/docs

## Acknowledgments

Built with:
- [Modal](https://modal.com) - Serverless cloud platform
- [FastAPI](https://fastapi.tiangolo.com) - Modern web framework
- [Pydantic](https://pydantic.dev) - Data validation