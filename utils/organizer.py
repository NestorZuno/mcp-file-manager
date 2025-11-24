import os
import shutil

def organize_by_extension(path):
    results = []

    for filename in os.listdir(path):
        full_path = os.path.join(path, filename)

        if os.path.isfile(full_path):
            ext = os.path.splitext(filename)[1].lower()
            folder = ext.replace('.', '') if ext else "sin_extension"

            target_folder = os.path.join(path, folder)

            os.makedirs(target_folder, exist_ok=True)

            new_path = os.path.join(target_folder, filename)

            shutil.move(full_path, new_path)
            results.append(f"Movido: {filename} → {folder}/")

    return results
