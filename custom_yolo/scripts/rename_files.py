import os

def rename_and_sync_folders(images_folder, labels_folder):
    images = {f for f in os.listdir(images_folder) if f.endswith('.jpg')}
    labels = {f for f in os.listdir(labels_folder) if f.endswith('.txt')}

    # Find matching and non-matching files
    matching_files = {f for f in images if f.rsplit('.', 1)[0] in {l.rsplit('.', 1)[0] for l in labels}}
    unmatched_images = images - matching_files
    unmatched_labels = {l for l in labels if l.rsplit('.', 1)[0] not in {f.rsplit('.', 1)[0] for f in images}}

    # Delete unmatched files and print their names
    for unmatched_image in unmatched_images:
        os.remove(os.path.join(images_folder, unmatched_image))
        print(f"Deleted unmatched image: {unmatched_image}")

    for unmatched_label in unmatched_labels:
        os.remove(os.path.join(labels_folder, unmatched_label))
        print(f"Deleted unmatched label: {unmatched_label}")

    # Rename matching files with sequential numbering
    matching_files = sorted(matching_files)  # Sort for consistent numbering
    for index, filename in enumerate(matching_files, start=1):
        # Define new names for image and label
        image_extension = '.jpg'
        label_extension = '.txt'

        new_image_name = f"{index}{image_extension}"
        new_label_name = f"{index}{label_extension}"

        # Rename files
        os.rename(
            os.path.join(images_folder, filename),
            os.path.join(images_folder, new_image_name)
        )
        label_filename = f"{filename.rsplit('.', 1)[0]}.txt"
        os.rename(
            os.path.join(labels_folder, label_filename),
            os.path.join(labels_folder, new_label_name)
        )

    print(f"Renamed {len(matching_files)} pairs of files successfully.")

# Example usage
images_folder = r"/home/emirhan/detection_dataset_files/images/val"
labels_folder = r"/home/emirhan/detection_dataset_files/labels/val"
rename_and_sync_folders(images_folder, labels_folder)
