# API Documentation

## OpenCode Modal Server REST API

Base URL: `https://your-username--opencode-server-fastapi-app.modal.run`

### Endpoints

---

## Health Check

**GET** `/`

Check if the server is running and get basic information.

### Response

```json
{
  "status": "ok",
  "service": "OpenCode Server",
  "storage": "persistent",
  "storage_path": "/storage"
}
```

---

## Create Job

**POST** `/jobs`

Create a new code execution job.

### Request Body

```json
{
  "code": "string (required) - The code to execute",
  "language": "string (default: python) - Programming language",
  "description": "string (default: '') - Job description"
}
```

### Example Request

```bash
curl -X POST https://your-url.modal.run/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "code": "print(\"Hello, World!\")",
    "language": "python",
    "description": "Simple hello world"
  }'
```

### Response (201 Created)

```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "message": "Job created and queued for execution"
}
```

---

## Get Job Status

**GET** `/jobs/{job_id}`

Retrieve the status and results of a specific job.

### Parameters

- `job_id` (path, required): UUID of the job

### Example Request

```bash
curl https://your-url.modal.run/jobs/550e8400-e29b-41d4-a716-446655440000
```

### Response (200 OK)

```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "code": "print(\"Hello, World!\")",
  "language": "python",
  "description": "Simple hello world",
  "status": "completed",
  "created_at": "2026-02-16T22:00:00.000000",
  "updated_at": "2026-02-16T22:00:05.123456",
  "result": {
    "output": "Executed python code",
    "code": "print(\"Hello, World!\")"
  }
}
```

### Response (404 Not Found)

```json
{
  "detail": "Job not found"
}
```

---

## List Jobs

**GET** `/jobs`

List all jobs with pagination.

### Query Parameters

- `limit` (optional, default: 100): Maximum number of jobs to return

### Example Request

```bash
curl https://your-url.modal.run/jobs?limit=10
```

### Response (200 OK)

```json
{
  "jobs": [
    {
      "job_id": "550e8400-e29b-41d4-a716-446655440000",
      "status": "completed",
      "language": "python",
      "description": "Simple hello world",
      "created_at": "2026-02-16T22:00:00.000000",
      "updated_at": "2026-02-16T22:00:05.123456"
    },
    {
      "job_id": "660e8400-e29b-41d4-a716-446655440001",
      "status": "pending",
      "language": "python",
      "description": "Another job",
      "created_at": "2026-02-16T22:01:00.000000",
      "updated_at": "2026-02-16T22:01:00.000000"
    }
  ],
  "count": 2
}
```

---

## Delete Job

**DELETE** `/jobs/{job_id}`

Delete a specific job and its data from storage.

### Parameters

- `job_id` (path, required): UUID of the job

### Example Request

```bash
curl -X DELETE https://your-url.modal.run/jobs/550e8400-e29b-41d4-a716-446655440000
```

### Response (200 OK)

```json
{
  "message": "Job 550e8400-e29b-41d4-a716-446655440000 deleted"
}
```

### Response (404 Not Found)

```json
{
  "detail": "Job not found"
}
```

---

## Storage Statistics

**GET** `/storage/stats`

Get statistics about the persistent storage usage.

### Example Request

```bash
curl https://your-url.modal.run/storage/stats
```

### Response (200 OK)

```json
{
  "total_jobs": 42,
  "storage_path": "/storage",
  "total_size_bytes": 1048576,
  "total_size_mb": 1.0
}
```

---

## Job Status Values

Jobs can have the following status values:

- `pending` - Job created and waiting to be executed
- `running` - Job is currently being executed
- `completed` - Job finished successfully
- `failed` - Job execution failed

---

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request

```json
{
  "detail": "Error description"
}
```

### 404 Not Found

```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error

```json
{
  "detail": "Internal server error"
}
```

---

## Rate Limits

The server supports up to 100 concurrent requests. Additional requests will be queued.

---

## Authentication

Currently, the API does not require authentication. In production, you should:

1. Add API key authentication
2. Use Modal's secrets for credentials
3. Implement rate limiting per user
4. Add request logging

Example authentication header (for future implementation):

```bash
curl https://your-url.modal.run/jobs \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"code": "..."}'
```

---

## Python SDK Example

```python
import requests


class OpenCodeClient:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
    
    def health_check(self):
        """Check server health"""
        response = requests.get(f"{self.base_url}/")
        return response.json()
    
    def create_job(self, code, language="python", description=""):
        """Create a new job"""
        response = requests.post(
            f"{self.base_url}/jobs",
            json={
                "code": code,
                "language": language,
                "description": description
            }
        )
        return response.json()
    
    def get_job(self, job_id):
        """Get job status and results"""
        response = requests.get(f"{self.base_url}/jobs/{job_id}")
        return response.json()
    
    def list_jobs(self, limit=100):
        """List all jobs"""
        response = requests.get(f"{self.base_url}/jobs", params={"limit": limit})
        return response.json()
    
    def delete_job(self, job_id):
        """Delete a job"""
        response = requests.delete(f"{self.base_url}/jobs/{job_id}")
        return response.json()
    
    def get_stats(self):
        """Get storage statistics"""
        response = requests.get(f"{self.base_url}/storage/stats")
        return response.json()


# Usage
client = OpenCodeClient("https://your-url.modal.run")
result = client.create_job("print('Hello!')", language="python", description="Test")
print(result)
```

---

## JavaScript/Node.js Example

```javascript
class OpenCodeClient {
  constructor(baseUrl) {
    this.baseUrl = baseUrl.replace(/\/$/, '');
  }

  async healthCheck() {
    const response = await fetch(`${this.baseUrl}/`);
    return await response.json();
  }

  async createJob(code, language = 'python', description = '') {
    const response = await fetch(`${this.baseUrl}/jobs`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code, language, description })
    });
    return await response.json();
  }

  async getJob(jobId) {
    const response = await fetch(`${this.baseUrl}/jobs/${jobId}`);
    return await response.json();
  }

  async listJobs(limit = 100) {
    const response = await fetch(`${this.baseUrl}/jobs?limit=${limit}`);
    return await response.json();
  }

  async deleteJob(jobId) {
    const response = await fetch(`${this.baseUrl}/jobs/${jobId}`, {
      method: 'DELETE'
    });
    return await response.json();
  }

  async getStats() {
    const response = await fetch(`${this.baseUrl}/storage/stats`);
    return await response.json();
  }
}

// Usage
const client = new OpenCodeClient('https://your-url.modal.run');
const result = await client.createJob("console.log('Hello!')", 'javascript', 'Test');
console.log(result);
```
