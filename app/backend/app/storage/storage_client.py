import os
import requests
import logging
from io import BytesIO
from pathlib import Path
from contextlib import contextmanager
import tempfile

logger = logging.getLogger(__name__)

class StorageClient:
    """Client for interacting with Supabase Storage using REST API"""
    
    def __init__(self):
        """Initialize Supabase storage client with REST API"""
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_KEY')
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
        
        # Setup headers for all requests
        self.headers = {
            'apikey': self.supabase_key,
            'Authorization': f'Bearer {self.supabase_key}'
        }
        
        self.storage_url = f"{self.supabase_url}/storage/v1"
        logger.info("Supabase storage client initialized (REST API)")
    
    def list_buckets(self) -> list:
        """List all storage buckets"""
        try:
            response = requests.get(
                f"{self.storage_url}/bucket",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error listing buckets: {e}")
            raise
    
    def create_bucket(self, bucket_name: str, public: bool = False) -> bool:
        """Create a new storage bucket"""
        try:
            # Check if bucket exists
            buckets = self.list_buckets()
            if any(bucket['name'] == bucket_name for bucket in buckets):
                logger.info(f"Bucket '{bucket_name}' already exists")
                return True
            
            # Create bucket
            response = requests.post(
                f"{self.storage_url}/bucket",
                headers=self.headers,
                json={'name': bucket_name, 'public': public}
            )
            response.raise_for_status()
            logger.info(f"Created bucket '{bucket_name}'")
            return True
            
        except Exception as e:
            logger.error(f"Error creating bucket '{bucket_name}': {e}")
            return False
        
    def create_folder(self, bucket_name: str, folder_path: str) -> bool:
        """Create a folder in a bucket by uploading a placeholder file"""
        try:
            placeholder_path = f"{folder_path.strip('/')}/.placeholder"
            response = requests.post(
                f"{self.storage_url}/object/{bucket_name}/{placeholder_path}",
                headers={**self.headers, 'Content-Type': 'application/octet-stream'},
                data=b''  # Empty content
            )
            response.raise_for_status()
            logger.info(f"Created folder '{folder_path}' in bucket '{bucket_name}'")
            return True
            
        except Exception as e:
            logger.error(f"Error creating folder '{folder_path}': {e}")
            return False
    
    def upload_file(self, bucket_name: str, file_path: str, object_name: str = None, 
                   folder_path: str = None) -> str:
        """Upload a file to Supabase storage"""
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            
            # Use filename if object_name not provided
            if object_name is None:
                object_name = os.path.basename(file_path)
            
            # Construct full path with folder if provided
            if folder_path:
                storage_path = f"{folder_path.strip('/')}/{object_name}"
            else:
                storage_path = object_name
            
            # Read file content
            with open(file_path, 'rb') as f:
                file_content = f.read()
            
            # Upload to Supabase
            response = requests.post(
                f"{self.storage_url}/object/{bucket_name}/{storage_path}",
                headers={**self.headers, 'Content-Type': 'application/pdf'},
                data=file_content
            )
            response.raise_for_status()
            
            logger.info(f"Uploaded {file_path} to {bucket_name}/{storage_path}")
            
            # Get public URL
            public_url = f"{self.supabase_url}/storage/v1/object/public/{bucket_name}/{storage_path}"
            return public_url
            
        except Exception as e:
            logger.error(f"Error uploading file {file_path}: {e}")
            raise
    
    def download_file(self, bucket_name: str, storage_path: str) -> BytesIO:
        """Download a file from Supabase storage and return as in-memory file"""
        try:
            # Download file content
            response = requests.get(
                f"{self.storage_url}/object/{bucket_name}/{storage_path}",
                headers=self.headers
            )
            response.raise_for_status()
            
            # Create in-memory file
            file_bytes = BytesIO(response.content)
            file_bytes.seek(0)  # Reset position to start
            
            logger.info(f"Downloaded {storage_path} from {bucket_name} to memory")
            return file_bytes
            
        except Exception as e:
            logger.error(f"Error downloading file {storage_path}: {e}")
            raise
    
    @contextmanager
    def download_file_temp(self, bucket_name: str, storage_path: str):
        """Download a file to temporary location, auto-delete after use"""
        temp_file = None
        try:
            # Download file content
            response = requests.get(
                f"{self.storage_url}/object/{bucket_name}/{storage_path}",
                headers=self.headers
            )
            response.raise_for_status()
            
            # Create temporary file with same extension
            suffix = Path(storage_path).suffix
            temp_file = tempfile.NamedTemporaryFile(
                mode='wb',
                suffix=suffix,
                delete=False
            )
            
            # Write content
            temp_file.write(response.content)
            temp_file.flush()
            temp_path = temp_file.name
            temp_file.close()
            
            logger.info(f"Downloaded {storage_path} to temporary file {temp_path}")
            
            # Yield the temporary file path
            yield temp_path
            
        except Exception as e:
            logger.error(f"Error downloading file {storage_path}: {e}")
            raise
            
        finally:
            # Clean up: delete temporary file
            if temp_file and os.path.exists(temp_file.name):
                try:
                    os.unlink(temp_file.name)
                    logger.info(f"Deleted temporary file {temp_file.name}")
                except Exception as e:
                    logger.warning(f"Could not delete temp file {temp_file.name}: {e}")
    
    def list_files(self, bucket_name: str, folder_path: str = None) -> list:
        """List files in a bucket or folder"""
        try:
            path = folder_path if folder_path else ''
            response = requests.post(
                f"{self.storage_url}/object/list/{bucket_name}",
                headers=self.headers,
                json={'prefix': path}
            )
            response.raise_for_status()
            files = response.json()
            logger.info(f"Listed {len(files)} files in {bucket_name}/{path}")
            return files
            
        except Exception as e:
            logger.error(f"Error listing files in {bucket_name}: {e}")
            return []
    
    def delete_file(self, bucket_name: str, storage_path: str) -> bool:
        """Delete a file from storage"""
        try:
            response = requests.delete(
                f"{self.storage_url}/object/{bucket_name}/{storage_path}",
                headers=self.headers
            )
            response.raise_for_status()
            logger.info(f"Deleted {storage_path} from {bucket_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting file {storage_path}: {e}")
            return False
        

    def upload_from_memory(self, bucket_name: str, file_content: bytes, 
                        object_name: str, folder_path: str = None, 
                        content_type: str = 'application/octet-stream') -> str:
        """Upload file content directly from memory to Supabase storage"""
        try:
            # Construct full path with folder if provided
            if folder_path:
                storage_path = f"{folder_path.strip('/')}/{object_name}"
            else:
                storage_path = object_name
            
            # Upload to Supabase
            response = requests.post(
                f"{self.storage_url}/object/{bucket_name}/{storage_path}",
                headers={**self.headers, 'Content-Type': content_type},
                data=file_content
            )
            response.raise_for_status()
            
            logger.info(f"Uploaded {object_name} to {bucket_name}/{storage_path}")
            
            # Get public URL
            public_url = f"{self.supabase_url}/storage/v1/object/public/{bucket_name}/{storage_path}"
            return public_url
            
        except Exception as e:
            logger.error(f"Error uploading from memory: {e}")
            raise
        