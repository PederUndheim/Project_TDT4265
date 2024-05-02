import os
import shutil

base_path = "data/"
def move_files(source_dir, destination_dir, file_list, suffix):
    for filename in file_list:
        source_path = os.path.join(base_path + source_dir, (filename + suffix))
        destination_path = os.path.join(base_path + destination_dir + "/" + source_dir, filename)
        shutil.move(source_path, destination_path  + suffix.lower())

def read_file_list(file_path):
    with open(base_path + file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def main():
    # Define directories
    source_images_dir = 'images'
    source_labels_dir = 'labels'
    destination_train_dir = 'train'
    destination_test_dir = 'test'
    destination_val_dir = 'val'

    # Read file lists
    train_files = read_file_list('train_filenames.txt')
    test_files = read_file_list('test_filenames.txt')
    val_files = read_file_list('val_filenames.txt')

    
    # Move files
    move_files(source_images_dir, destination_train_dir, train_files, ".PNG")
    move_files(source_images_dir, destination_test_dir, test_files, ".PNG")
    move_files(source_images_dir, destination_val_dir, val_files, ".PNG")
    

    move_files(source_labels_dir, destination_train_dir, train_files, ".txt")
    move_files(source_labels_dir, destination_test_dir, test_files, ".txt")
    move_files(source_labels_dir, destination_val_dir, val_files, ".txt")


if __name__ == "__main__":
    main()
