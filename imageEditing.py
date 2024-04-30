import os
import cv2

def update_annotation(annotation, crop_height):
    # Splits annotation line and converts to float
    class_id, x_center, y_center, width, height = map(float, annotation.split())

    # Adjust y_center for the cropped image
    y_center = (y_center - (1/3)) / (2/3)

    # If the bounding box is not in the cropped area, return None
    if y_center < 0 or y_center > 1:
        return None

    # Return the updated annotation line
    return f"{class_id} {x_center} {y_center} {width} {height}\n"

def crop_images_and_labels(image_directory, annotations_directory, output_image_directory, output_annotations_directory):
    # Create output directories if they don't exist
    os.makedirs(output_image_directory, exist_ok=True)
    os.makedirs(output_annotations_directory, exist_ok=True)

    # Process each image and its corresponding annotation
    for image_name in os.listdir(image_directory):
        # Check for corresponding annotation file
        annotation_name = image_name.replace('.PNG', '.txt')
        if not os.path.exists(os.path.join(annotations_directory, annotation_name)):
            continue  # Skip images without annotations

        # Load image
        image_path = os.path.join(image_directory, image_name)
        image = cv2.imread(image_path)

        # Calculate new height for the crop
        height, width, _ = image.shape
        new_height = height * (2/3)
        
        # Crop the bottom two-thirds
        cropped_image = image[int(height/3):, :]

        # Write cropped image to file
        cv2.imwrite(os.path.join(output_image_directory, image_name), cropped_image)

        # Update annotations
        with open(os.path.join(annotations_directory, annotation_name), 'r') as file:
            annotations = file.readlines()
        
        updated_annotations = [update_annotation(ann, new_height) for ann in annotations]
        updated_annotations = [ann for ann in updated_annotations if ann is not None]

        # Write updated annotations to file
        with open(os.path.join(output_annotations_directory, annotation_name), 'w') as file:
            file.writelines(updated_annotations)

# Define directories
image_directory = '/home/pederu/Documents/YOLOv8_project/dataset/images/val'
annotations_directory = '/home/pederu/Documents/YOLOv8_project/dataset/labels/val'
output_image_directory = '/home/pederu/Documents/YOLOv8_project/cropped_dataset/images/val'
output_annotations_directory = '/home/pederu/Documents/YOLOv8_project/cropped_dataset/labels/val'

# Run the cropping function
crop_images_and_labels(image_directory, annotations_directory, output_image_directory, output_annotations_directory)
print("Done")
