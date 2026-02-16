"""
OpenCode Server on Modal with Persistent Storage

This module sets up an OpenCode server on Modal cloud with persistent storage
for long-term job management.
"""

import modal
import os
from pathlib import Path

# Create Modal app
app = modal.App("opencode-server")

# Create persistent volume for long-term storage
# This volume will persist across deployments and container restarts
volume = modal.Volume.from_name("opencode-storage", create_if_missing=True)

# Define the storage path where persistent data will be mounted
STORAGE_PATH = "/storage"

# Create Docker image with required dependencies
image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(
        "fastapi>=0.104.0",
        "uvicorn[standard]>=0.24.0",
        "pydantic>=2.0.0",
        "python-multipart>=0.0.6",
    )
)


@app.function(
    image=image,
    volumes={STORAGE_PATH: volume},
    allow_concurrent_inputs=100,
    container_idle_timeout=300,  # Keep container alive for 5 minutes after last request
    timeout=3600,  # 1 hour timeout for long-running jobs
)
@modal.asgi_app()
def fastapi_app():
    """
    FastAPI application for OpenCode server with persistent storage.
    """
    from fastapi import FastAPI, HTTPException, BackgroundTasks
    from fastapi.responses import JSONResponse
    from pydantic import BaseModel
    import json
    from datetime import datetime
    import uuid
    
    app = FastAPI(
        title="OpenCode Server",
        description="OpenCode server with persistent storage on Modal",
        version="1.0.0"
    )
    
    # Ensure storage directories exist
    jobs_dir = Path(STORAGE_PATH) / "jobs"
    jobs_dir.mkdir(parents=True, exist_ok=True)
    
    class JobRequest(BaseModel):
        """Job request model"""
        code: str
        language: str = "python"
        description: str = ""
    
    class JobStatus(BaseModel):
        """Job status model"""
        job_id: str
        status: str
        created_at: str
        updated_at: str
        result: dict = {}
    
    def save_job(job_id: str, data: dict):
        """Save job data to persistent storage"""
        job_file = jobs_dir / f"{job_id}.json"
        with open(job_file, 'w') as f:
            json.dump(data, f, indent=2)
        # Commit changes to persistent volume
        volume.commit()
    
    def load_job(job_id: str) -> dict:
        """Load job data from persistent storage"""
        job_file = jobs_dir / f"{job_id}.json"
        if not job_file.exists():
            return None
        with open(job_file, 'r') as f:
            return json.load(f)
    
    def execute_job(job_id: str, code: str, language: str):
        """Execute job in background"""
        try:
            job_data = load_job(job_id)
            if not job_data:
                return
            
            job_data['status'] = 'running'
            job_data['updated_at'] = datetime.utcnow().isoformat()
            save_job(job_id, job_data)
            
            # Execute the code (placeholder for actual execution)
            # In a real implementation, you'd use subprocess or exec
            result = {
                'output': f'Executed {language} code',
                'code': code[:100] + '...' if len(code) > 100 else code
            }
            
            job_data['status'] = 'completed'
            job_data['result'] = result
            job_data['updated_at'] = datetime.utcnow().isoformat()
            save_job(job_id, job_data)
            
        except Exception as e:
            job_data = load_job(job_id)
            if job_data:
                job_data['status'] = 'failed'
                job_data['result'] = {'error': str(e)}
                job_data['updated_at'] = datetime.utcnow().isoformat()
                save_job(job_id, job_data)
    
    @app.get("/")
    async def root():
        """Health check endpoint"""
        return {
            "status": "ok",
            "service": "OpenCode Server",
            "storage": "persistent",
            "storage_path": STORAGE_PATH
        }
    
    @app.post("/jobs")
    async def create_job(job: JobRequest, background_tasks: BackgroundTasks):
        """Create a new job"""
        job_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()
        
        job_data = {
            'job_id': job_id,
            'code': job.code,
            'language': job.language,
            'description': job.description,
            'status': 'pending',
            'created_at': now,
            'updated_at': now,
            'result': {}
        }
        
        save_job(job_id, job_data)
        
        # Execute job in background
        background_tasks.add_task(execute_job, job_id, job.code, job.language)
        
        return JSONResponse(
            status_code=201,
            content={
                'job_id': job_id,
                'status': 'pending',
                'message': 'Job created and queued for execution'
            }
        )
    
    @app.get("/jobs/{job_id}")
    async def get_job(job_id: str):
        """Get job status and results"""
        job_data = load_job(job_id)
        if not job_data:
            raise HTTPException(status_code=404, detail="Job not found")
        return job_data
    
    @app.get("/jobs")
    async def list_jobs(limit: int = 100):
        """List all jobs"""
        job_files = sorted(jobs_dir.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True)
        jobs = []
        
        for job_file in job_files[:limit]:
            with open(job_file, 'r') as f:
                job_data = json.load(f)
                # Return summary without full code/result
                jobs.append({
                    'job_id': job_data['job_id'],
                    'status': job_data['status'],
                    'language': job_data['language'],
                    'description': job_data['description'],
                    'created_at': job_data['created_at'],
                    'updated_at': job_data['updated_at']
                })
        
        return {'jobs': jobs, 'count': len(jobs)}
    
    @app.delete("/jobs/{job_id}")
    async def delete_job(job_id: str):
        """Delete a job"""
        job_file = jobs_dir / f"{job_id}.json"
        if not job_file.exists():
            raise HTTPException(status_code=404, detail="Job not found")
        
        job_file.unlink()
        volume.commit()
        
        return {'message': f'Job {job_id} deleted'}
    
    @app.get("/storage/stats")
    async def storage_stats():
        """Get storage statistics"""
        job_files = list(jobs_dir.glob("*.json"))
        total_jobs = len(job_files)
        
        # Calculate storage usage
        total_size = sum(f.stat().st_size for f in job_files)
        
        return {
            'total_jobs': total_jobs,
            'storage_path': STORAGE_PATH,
            'total_size_bytes': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2)
        }
    
    return app


# CLI command to deploy
@app.local_entrypoint()
def main():
    """Local entrypoint for testing"""
    print("OpenCode Server on Modal")
    print("========================")
    print(f"Persistent storage: {STORAGE_PATH}")
    print(f"Volume: opencode-storage")
    print("\nTo deploy: modal deploy modal_app.py")
    print("To run locally: modal serve modal_app.py")
