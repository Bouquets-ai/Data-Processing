import os
import shutil


def extract_md_files(source_folder, target_folder):
    """
    Extract all .md files from the source folder to the target folder

    :param source_folder: Path to the source folder
    :param target_folder: Path to the target folder
    """
    # Ensure the source folder exists
    if not os.path.exists(source_folder):
        print(f"Error: Source folder '{source_folder}' does not exist")
        return

    # Ensure the target folder exists
    os.makedirs(target_folder, exist_ok=True)

    # Walk through the source folder
    for root, _, files in os.walk(source_folder):
        for file in files:
            if file.lower().endswith('.md'):
                source_path = os.path.join(root, file)
                target_path = os.path.join(target_folder, file)
                # Handle filename conflicts
                counter = 1
                while os.path.exists(target_path):
                    name, ext = os.path.splitext(file)
                    target_path = os.path.join(target_folder, f"{name}_{counter}{ext}")
                    counter += 1

                # Copy the file
                shutil.copy2(source_path, target_path)
                print(f"Copied: {source_path} -> {target_path}")


if __name__ == "__main__":
    # Set source and target folders
    source_folder = 'Internal_Data_Collection'  # Folder to extract from
    target_folder = '.'  # Current directory

    print("Starting .md file extraction...")
    extract_md_files(source_folder, target_folder)
    print("Extraction completed!")