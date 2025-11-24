import os
import hashlib

def hash_file(path):
    """Calcula el hash MD5 de un archivo."""
    h = hashlib.md5()
    try:
        with open(path, "rb") as f:
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                h.update(chunk)
        return h.hexdigest()
    except Exception as e:
        return None

def find_duplicates(folder_path):
    """
    Encuentra duplicados optimizando la búsqueda y EVITANDO carpetas de sistema.
    """
    files_by_size = {}
    duplicates = []
    
    # LISTA NEGRA: Carpetas que el script debe ignorar por completo
    IGNORED_DIRS = {'venv', '.git', '__pycache__', '.idea', '.vscode', 'node_modules', 'bin', 'Lib', 'site-packages'}

    # PASO 1: Agrupar por tamaño
    for root, dirs, files in os.walk(folder_path):
        
        # Filtramos las carpetas prohibidas para que os.walk no entre en ellas
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

        for filename in files:
            full_path = os.path.join(root, filename)
            try:
                # Omitir enlaces simbólicos
                if os.path.islink(full_path):
                    continue

                file_size = os.path.getsize(full_path)
                
                if file_size not in files_by_size:
                    files_by_size[file_size] = []
                files_by_size[file_size].append(full_path)
            except OSError:
                continue 

    # PASO 2: Comparar Hash solo donde hubo colisión de tamaño
    for size, paths in files_by_size.items():
        if len(paths) < 2:
            continue
        
        hashes = {}
        for path in paths:
            file_hash = hash_file(path)
            if not file_hash:
                continue

            if file_hash in hashes:
                duplicates.append({
                    "original": hashes[file_hash],
                    "duplicate": path,
                    "size_bytes": size
                })
            else:
                hashes[file_hash] = path

    return duplicates