import os
import shutil
from sklearn.model_selection import train_test_split

# Base directory for the dataset
data_dir = '/home/pederu/Documents/YOLOv8_project/dataset'

# Directories for images and labels
images_dir = os.path.join(data_dir, 'images/all')
labels_dir = os.path.join(data_dir, 'labels/all')

# Function to create necessary subdirectories
def create_subdirectories():
    for subdir in ['train', 'val', 'test']:
        for dir in [images_dir, labels_dir]:
            os.makedirs(os.path.join(dir, subdir), exist_ok=True)

# Split filenames and move files
def split_and_move_files():
    # List of image filenames (without extension)
    filenames = [os.path.splitext(file)[0] for file in os.listdir(images_dir) if file.endswith('.png') or file.endswith('.PNG')]
    
    # First, split off the test set
    remaining_filenames, test_filenames = train_test_split(filenames, test_size=0.1, random_state=42)
    
    # Then split the remaining files into train and validation sets
    train_filenames, val_filenames = train_test_split(remaining_filenames, test_size=0.2, random_state=42)  # 20% of 90% is 18% of the total

    # Function to move files from source to destination directory
    def move_files(file_list, source_base_dir, target_sub_dir, file_extension):
        for filename in file_list:
            source_path = os.path.join(source_base_dir, filename + file_extension)
            target_path = os.path.join(source_base_dir, target_sub_dir, filename + file_extension)
            if os.path.exists(source_path):
                shutil.move(source_path, target_path)
            else:
                print(f"Warning: {source_path} does not exist.")

    # Function to write filenames to a text file
    def write_filenames(file_list, directory, subdir):
        with open(os.path.join(directory, subdir + '_filenames.txt'), 'w') as file:
            for filename in file_list:
                file.write(filename + '\n')

    # Move image files (.png) and write filenames
    move_files(train_filenames, images_dir, 'train', '.PNG')
    write_filenames(train_filenames, images_dir, 'train')

    move_files(val_filenames, images_dir, 'val', '.PNG')
    write_filenames(val_filenames, images_dir, 'val')

    move_files(test_filenames, images_dir, 'test', '.PNG')
    write_filenames(test_filenames, images_dir, 'test')

    # Move label files (.txt) and write filenames
    move_files(train_filenames, labels_dir, 'train', '.txt')
    write_filenames(train_filenames, labels_dir, 'train')

    move_files(val_filenames, labels_dir, 'val', '.txt')
    write_filenames(val_filenames, labels_dir, 'val')

    move_files(test_filenames, labels_dir, 'test', '.txt')
    write_filenames(test_filenames, labels_dir, 'test')

if __name__ == "__main__":
    create_subdirectories()
    split_and_move_files()
    print("Dataset successfully organized into training, validation, and test sets.")
