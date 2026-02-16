#!/usr/bin/env python3
"""
Example client for interacting with the OpenCode Modal Server

Usage:
    python example_client.py <server_url>
    
Example:
    python example_client.py https://your-username--opencode-server-fastapi-app.modal.run
"""

import requests
import json
import time
import sys


def main():
    if len(sys.argv) < 2:
        print("Usage: python example_client.py <server_url>")
        print("Example: python example_client.py https://your-username--opencode-server-fastapi-app.modal.run")
        sys.exit(1)
    
    base_url = sys.argv[1].rstrip('/')
    
    print("=" * 60)
    print("OpenCode Modal Server - Example Client")
    print("=" * 60)
    print()
    
    # 1. Health check
    print("1. Health Check")
    print("-" * 60)
    response = requests.get(f"{base_url}/")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    print()
    
    # 2. Create a job
    print("2. Creating a new job")
    print("-" * 60)
    job_data = {
        "code": """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

for i in range(10):
    print(f"fib({i}) = {fibonacci(i)}")
""",
        "language": "python",
        "description": "Calculate Fibonacci sequence"
    }
    
    response = requests.post(
        f"{base_url}/jobs",
        json=job_data,
        headers={"Content-Type": "application/json"}
    )
    print(f"Status: {response.status_code}")
    result = response.json()
    print(json.dumps(result, indent=2))
    job_id = result.get('job_id')
    print()
    
    # 3. Wait a moment for job to process
    print("3. Waiting for job to process...")
    print("-" * 60)
    time.sleep(2)
    print()
    
    # 4. Get job status
    print("4. Getting job status")
    print("-" * 60)
    response = requests.get(f"{base_url}/jobs/{job_id}")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    print()
    
    # 5. List all jobs
    print("5. Listing all jobs")
    print("-" * 60)
    response = requests.get(f"{base_url}/jobs")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Total jobs: {result['count']}")
    for job in result['jobs'][:5]:  # Show first 5
        print(f"  - {job['job_id']}: {job['status']} ({job['description']})")
    print()
    
    # 6. Get storage stats
    print("6. Storage Statistics")
    print("-" * 60)
    response = requests.get(f"{base_url}/storage/stats")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    print()
    
    # 7. Create another job
    print("7. Creating another job (data processing)")
    print("-" * 60)
    job_data2 = {
        "code": "import json; data = {'key': 'value'}; print(json.dumps(data))",
        "language": "python",
        "description": "JSON data processing example"
    }
    
    response = requests.post(
        f"{base_url}/jobs",
        json=job_data2,
        headers={"Content-Type": "application/json"}
    )
    print(f"Status: {response.status_code}")
    result = response.json()
    print(json.dumps(result, indent=2))
    job_id2 = result.get('job_id')
    print()
    
    # 8. Final stats
    print("8. Final Storage Statistics")
    print("-" * 60)
    response = requests.get(f"{base_url}/storage/stats")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    print()
    
    print("=" * 60)
    print("Example completed successfully!")
    print("=" * 60)
    print()
    print(f"Created job IDs:")
    print(f"  - {job_id}")
    print(f"  - {job_id2}")
    print()
    print("You can check these jobs anytime using:")
    print(f"  curl {base_url}/jobs/{{job_id}}")


if __name__ == "__main__":
    main()
