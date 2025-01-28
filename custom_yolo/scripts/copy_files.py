import os
import shutil

def copy_files(source_folder, destination_folder):
    """
    Copies all files from source_folder to destination_folder.

    :param source_folder: Path to the source folder.
    :param destination_folder: Path to the destination folder.
    """
    if not os.path.exists(source_folder):
        print(f"Source folder '{source_folder}' does not exist.")
        return

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
        print(f"Destination folder '{destination_folder}' created.")

    for item in os.listdir(source_folder):
        source_path = os.path.join(source_folder, item)
        destination_path = os.path.join(destination_folder, item)

        if os.path.isfile(source_path):
            shutil.copy2(source_path, destination_path)
            print(f"Copied '{source_path}' to '{destination_path}'")

if __name__ == "__main__":
    source_folder = r"/home/emirhan/Downloads/data_f1/labels/val"
    destination_folder = r"/home/emirhan/detection_dataset_files/labels/val"

    copy_files(source_folder, destination_folder)