from supabase import create_client, Client
from app.config import settings
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class SupabaseStorageClient:
    """Client for managing PDF files in Supabase Storage"""
    
    def __init__(self):
        self.client: Client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_ANON_KEY
        )
        self.bucket = settings.SUPABASE_BUCKET
    
    def upload_pdf(
        self, 
        file_path: str, 
        storage_path: str,
        overwrite: bool = False
    ) -> Optional[str]:
        """
        Upload a PDF file to Supabase Storage
        
        Args:
            file_path: Local path to PDF file
            storage_path: Path in storage (e.g., '2024/MotoGP/Qatar/FP1.pdf')
            overwrite: Whether to overwrite existing file
            
        Returns:
            Public URL of uploaded file or None if failed
        """
        try:
            with open(file_path, 'rb') as f:
                response = self.client.storage.from_(self.bucket).upload(
                    path=storage_path,
                    file=f,
                    file_options={
                        "content-type": "application/pdf",
                        "upsert": overwrite
                    }
                )
            
            # Get public URL
            url = self.client.storage.from_(self.bucket).get_public_url(storage_path)
            logger.info(f"Uploaded PDF to: {url}")
            return url
            
        except Exception as e:
            logger.error(f"Failed to upload {file_path}: {e}")
            return None
    
    def download_pdf(self, storage_path: str, local_path: str) -> bool:
        """
        Download a PDF from Supabase Storage
        
        Args:
            storage_path: Path in storage
            local_path: Local path to save file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            data = self.client.storage.from_(self.bucket).download(storage_path)
            
            with open(local_path, 'wb') as f:
                f.write(data)
            
            logger.info(f"Downloaded PDF to: {local_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to download {storage_path}: {e}")
            return False
    
    def get_public_url(self, storage_path: str) -> str:
        """Get public URL for a stored PDF"""
        return self.client.storage.from_(self.bucket).get_public_url(storage_path)
    
    def list_pdfs(self, folder: str = "") -> list:
        """List all PDFs in a folder"""
        try:
            files = self.client.storage.from_(self.bucket).list(folder)
            return [f for f in files if f.get('name', '').endswith('.pdf')]
        except Exception as e:
            logger.error(f"Failed to list files in {folder}: {e}")
            return []
    
    def delete_pdf(self, storage_path: str) -> bool:
        """Delete a PDF from storage"""
        try:
            self.client.storage.from_(self.bucket).remove([storage_path])
            logger.info(f"Deleted PDF: {storage_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete {storage_path}: {e}")
            return False


# Singleton instance
storage_client = SupabaseStorageClient()