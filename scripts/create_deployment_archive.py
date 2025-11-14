"""
Create deployment archive for cluster
"""
import tarfile
import os
from pathlib import Path

def create_archive():
    """Create tar.gz archive for deployment"""
    base_dir = Path(__file__).parent.parent
    
    # Files and directories to include
    items_to_include = [
        'flower_server',
        'flower_client', 
        'output',
        'scripts'
    ]
    
    # Exclude patterns
    exclude_patterns = [
        '__pycache__',
        '*.pyc',
        '*.pyo',
        '*.pt',
        'models',
        '.git'
    ]
    
    archive_name = 'federated_learning.tar.gz'
    
    print(f"Creating archive: {archive_name}")
    print(f"Base directory: {base_dir}")
    
    with tarfile.open(archive_name, 'w:gz') as tar:
        for item in items_to_include:
            item_path = base_dir / item
            if item_path.exists():
                print(f"Adding: {item}")
                
                # Add directory with filtering
                if item_path.is_dir():
                    for root, dirs, files in os.walk(item_path):
                        # Filter out excluded directories
                        dirs[:] = [d for d in dirs if not any(pattern in d for pattern in exclude_patterns)]
                        
                        for file in files:
                            file_path = Path(root) / file
                            # Skip excluded files
                            if any(pattern in str(file_path) for pattern in exclude_patterns):
                                continue
                            
                            arcname = file_path.relative_to(base_dir)
                            tar.add(file_path, arcname=arcname, recursive=False)
                else:
                    tar.add(item_path, arcname=item)
    
    archive_path = base_dir / archive_name
    size_mb = archive_path.stat().st_size / (1024 * 1024)
    print(f"\nArchive created: {archive_name}")
    print(f"  Size: {size_mb:.2f} MB")
    print(f"  Location: {archive_path}")
    
    return archive_path

if __name__ == "__main__":
    create_archive()

