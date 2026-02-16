# Quick Start Deployment Guide

## Step-by-Step Setup

### 1. Prerequisites Check

Make sure you have:
- [ ] Python 3.11+ installed (`python --version`)
- [ ] pip installed (`pip --version`)
- [ ] Git installed (`git --version`)

### 2. Modal Setup

```bash
# Install Modal
pip install modal

# Authenticate with Modal (opens browser)
modal token new
```

### 3. Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

### 4. Test Locally (Optional)

```bash
# Run server locally for testing
modal serve modal_app.py
```

This will give you a local URL like `http://localhost:8000`. Open it in your browser or test with curl:

```bash
curl http://localhost:8000/
```

### 5. Deploy to Modal Cloud

```bash
# Deploy the application
modal deploy modal_app.py
```

You'll see output like:

```
✓ Created objects.
├── 🔨 Created mount /home/runner/work/opencode-modal-server/opencode-modal-server
├── 🔨 Created image im-...
├── 🔨 Created volume vol-...
└── 🔨 Created function fastapi_app
✓ App deployed! 🎉

View it at: https://your-username--opencode-server-fastapi-app.modal.run
```

### 6. Test Your Deployment

```bash
# Replace with your actual URL
export OPENCODE_URL="https://your-username--opencode-server-fastapi-app.modal.run"

# Health check
curl $OPENCODE_URL/

# Create a test job
curl -X POST $OPENCODE_URL/jobs \
  -H "Content-Type: application/json" \
  -d '{"code": "print(\"Hello from Modal!\")", "language": "python", "description": "Test job"}'

# Check storage stats
curl $OPENCODE_URL/storage/stats
```

### 7. Use the Example Client

```bash
python example_client.py $OPENCODE_URL
```

## Troubleshooting

### "modal: command not found"

```bash
pip install --upgrade modal
```

### "Authentication required"

```bash
modal token new
```

### "Volume not found"

The volume will be created automatically on first deployment. If you see this error:

```bash
modal volume create opencode-storage
```

### View Logs

```bash
modal app logs opencode-server
```

## Next Steps

- Customize the job execution logic in `modal_app.py`
- Add authentication/authorization
- Implement more sophisticated job processing
- Add webhook notifications for job completion
- Set up monitoring and alerts

## Updating Your Deployment

After making changes:

```bash
# Redeploy
modal deploy modal_app.py
```

Your persistent volume and data will remain intact across deployments!

## Stopping the Service

To remove the deployment:

```bash
modal app stop opencode-server
```

Note: This stops the app but preserves the volume. To delete the volume:

```bash
modal volume delete opencode-storage
```

**WARNING**: Deleting the volume will permanently delete all stored jobs!
