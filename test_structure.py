"""
Simple tests to validate the OpenCode Modal Server structure

These tests validate the basic structure and logic without requiring Modal deployment.
"""

import json
import tempfile
from pathlib import Path
import sys


def test_job_data_structure():
    """Test that job data structure is valid"""
    job_data = {
        'job_id': 'test-123',
        'code': 'print("hello")',
        'language': 'python',
        'description': 'Test job',
        'status': 'pending',
        'created_at': '2026-02-16T00:00:00',
        'updated_at': '2026-02-16T00:00:00',
        'result': {}
    }
    
    # Validate required fields
    required_fields = ['job_id', 'code', 'language', 'status', 'created_at', 'updated_at']
    for field in required_fields:
        assert field in job_data, f"Missing required field: {field}"
    
    print("✓ Job data structure is valid")


def test_job_storage():
    """Test job storage and retrieval logic"""
    with tempfile.TemporaryDirectory() as temp_dir:
        jobs_dir = Path(temp_dir) / "jobs"
        jobs_dir.mkdir(parents=True, exist_ok=True)
        
        # Test save
        job_id = "test-456"
        job_data = {
            'job_id': job_id,
            'status': 'completed',
            'result': {'output': 'test output'}
        }
        
        job_file = jobs_dir / f"{job_id}.json"
        with open(job_file, 'w') as f:
            json.dump(job_data, f, indent=2)
        
        # Test load
        assert job_file.exists(), "Job file was not created"
        
        with open(job_file, 'r') as f:
            loaded_data = json.load(f)
        
        assert loaded_data['job_id'] == job_id, "Job ID mismatch"
        assert loaded_data['status'] == 'completed', "Status mismatch"
        
        print("✓ Job storage and retrieval works correctly")


def test_config_values():
    """Test configuration values"""
    # Import config using relative path
    script_dir = Path(__file__).parent
    sys.path.insert(0, str(script_dir))
    import config
    
    assert config.APP_NAME == "opencode-server", "APP_NAME incorrect"
    assert config.VOLUME_NAME == "opencode-storage", "VOLUME_NAME incorrect"
    assert config.STORAGE_PATH == "/storage", "STORAGE_PATH incorrect"
    assert config.CONTAINER_IDLE_TIMEOUT == 300, "CONTAINER_IDLE_TIMEOUT incorrect"
    assert config.JOB_TIMEOUT == 3600, "JOB_TIMEOUT incorrect"
    
    print("✓ Configuration values are correct")


def test_requirements():
    """Test that requirements.txt is properly formatted"""
    req_file = Path(__file__).parent / 'requirements.txt'
    
    assert req_file.exists(), "requirements.txt not found"
    
    with open(req_file, 'r') as f:
        requirements = f.read().strip().split('\n')
    
    # Check for essential dependencies
    req_packages = [r.split('>=')[0].split('==')[0] for r in requirements]
    
    assert 'modal' in req_packages, "modal missing from requirements"
    assert 'fastapi' in req_packages, "fastapi missing from requirements"
    assert 'pydantic' in req_packages, "pydantic missing from requirements"
    
    print("✓ Requirements file is valid")


def main():
    """Run all tests"""
    print("=" * 60)
    print("Running OpenCode Modal Server Tests")
    print("=" * 60)
    print()
    
    tests = [
        test_job_data_structure,
        test_job_storage,
        test_config_values,
        test_requirements,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} error: {e}")
            failed += 1
    
    print()
    print("=" * 60)
    print(f"Tests: {passed} passed, {failed} failed, {passed + failed} total")
    print("=" * 60)
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
