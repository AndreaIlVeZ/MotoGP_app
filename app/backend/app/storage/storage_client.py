import os
from supabase import create_client, Client
import logging
from pathlib import Path
from io import BytesIO
import tempfile

logger = logging.getLogger(__name__)

class StorageClient:
    """Client for interacting with Supabase Storage"""
    
    def __init__(self):
        """Initialize Supabase client with credentials from environment variables"""
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')
        
        if not supabase_url or not supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
        
        self.client: Client = create_client(supabase_url, supabase_key)
        logger.info("Supabase client initialized successfully")
    
    def create_bucket(self, bucket_name: str, public: bool = False) -> bool:
        """Create a new storage bucket if it doesn't exist
        
        Args:
            bucket_name: Name of the bucket to create
            public: Whether the bucket should be publicly accessible
            
        Returns:
            bool: True if bucket created or already exists
        """
        try:
            # Check if bucket exists
            buckets = self.client.storage.list_buckets()
            bucket_exists = any(bucket['name'] == bucket_name for bucket in buckets)
            
            if bucket_exists:
                logger.info(f"Bucket '{bucket_name}' already exists")
                return True
            
            # Create bucket
            self.client.storage.create_bucket(bucket_name, options={'public': public})
            logger.info(f"Created bucket '{bucket_name}'")
            return True
            
        except Exception as e:
            logger.error(f"Error creating bucket '{bucket_name}': {e}")
            return False
    
    def upload_file(self, bucket_name: str, file_path: str, object_name: str = None, 
                   folder_path: str = None) -> str:
        """Upload a file to Supabase storage
        
        Args:
            bucket_name: Name of the bucket to upload to
            file_path: Local path to the file
            object_name: Name to give the file in storage (defaults to filename)
            folder_path: Optional folder path within bucket (e.g., '2024/motogp/race1')
            
        Returns:
            str: Public URL of uploaded file
        """
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
            response = self.client.storage.from_(bucket_name).upload(
                path=storage_path,
                file=file_content,
                file_options={"content-type": "application/pdf"}
            )
            
            logger.info(f"Uploaded {file_path} to {bucket_name}/{storage_path}")
            
            # Get public URL
            public_url = self.client.storage.from_(bucket_name).get_public_url(storage_path)
            return public_url
            
        except Exception as e:
            logger.error(f"Error uploading file {file_path}: {e}")
            raise
    
    def download_file(self, bucket_name: str, storage_path: str) -> BytesIO:
        """Download a file from Supabase storage
        
        Args:
            bucket_name: Name of the bucket
            storage_path: Path to file in storage
            local_path: Local path to save file
            
        Returns:
            str: Path to downloaded file
        """
        try:
            # Download file content
            response = self.client.storage.from_(bucket_name).download(storage_path)
            
            # Create in-memory file
            file_bytes = BytesIO(response)
            file_bytes.seek(0)  # Reset position to start
            
            logger.info(f"Downloaded {storage_path} from {bucket_name} to memory")
            return file_bytes
            
        except Exception as e:
            logger.error(f"Error downloading file {storage_path}: {e}")
            raise
    
    def list_files(self, bucket_name: str, folder_path: str = None) -> list:
        """List files in a bucket or folder
        
        Args:
            bucket_name: Name of the bucket
            folder_path: Optional folder path to list
            
        Returns:
            list: List of file objects
        """
        try:
            path = folder_path if folder_path else ''
            files = self.client.storage.from_(bucket_name).list(path)
            logger.info(f"Listed {len(files)} files in {bucket_name}/{path}")
            return files
            
        except Exception as e:
            logger.error(f"Error listing files in {bucket_name}: {e}")
            return []
    
    def delete_file(self, bucket_name: str, storage_path: str) -> bool:
        """Delete a file from storage
        
        Args:
            bucket_name: Name of the bucket
            storage_path: Path to file in storage
            
        Returns:
            bool: True if deleted successfully
        """
        try:
            self.client.storage.from_(bucket_name).remove([storage_path])
            logger.info(f"Deleted {storage_path} from {bucket_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting file {storage_path}: {e}")
            return False