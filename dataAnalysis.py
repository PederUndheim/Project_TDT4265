import os
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import matplotlib.patches as patches
import random
from collections import defaultdict


image_directory = '/home/pederu/Documents/YOLOv8_project/dataset/images/all'
annotations_directory = '/home/pederu/Documents/YOLOv8_project/dataset/labels/all'
class_names = ['car', 'truck', 'bus', 'motorcycle', 'bicycle', 'scooter', 'person', 'rider']
class_names_map = {
    0: 'car', 1: 'truck', 2: 'bus', 3: 'motorcycle',
    4: 'bicycle', 5: 'scooter', 6: 'person', 7: 'rider', 8: 'corner'
}

def check_image_sizes(image_dir):
    """Check the sizes of images in the dataset."""
    image_sizes = {}
    for file in os.listdir(image_dir):
        if file.endswith('.png') or file.endswith('.PNG'):
            with Image.open(os.path.join(image_dir, file)) as img:
                width, height = img.size
                if (width, height) in image_sizes:
                    image_sizes[(width, height)] += 1
                else:
                    image_sizes[(width, height)] = 1
    
    # Display image sizes
    plt.bar(range(len(image_sizes)), list(image_sizes.values()), align='center')
    plt.xticks(range(len(image_sizes)), list(image_sizes.keys()), rotation=45)
    plt.xlabel('Image size (width, height)')
    plt.ylabel('Number of images')
    plt.title('Image sizes in our dataset')
    plt.show()
#check_image_sizes(image_directory)



def check_class_balance(annotations_dir, class_names):
    """Check the balance of classes in a directory of annotation files."""
    class_counts = {name: 0 for name in class_names}  # Initialize counts with class names

    # Iterate over each annotation file
    for filename in os.listdir(annotations_dir):
        if filename.endswith('.txt'):
            with open(os.path.join(annotations_dir, filename), 'r') as file:
                for line in file:
                    class_id = int(line.split()[0])  # Assuming class_id is the first item
                    class_counts[class_names[class_id]] += 1

    # Display class distribution
    fig, ax = plt.subplots()
    bars = ax.bar(class_counts.keys(), class_counts.values())
    plt.xlabel('Class')
    plt.ylabel('Number of instances')
    plt.title('Class distribution in dataset')

    # Annotate each bar with the count of instances
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

    plt.show()
#check_class_balance(annotations_directory, class_names)



def plot_bounding_boxes(image_dir, annotations_dir, num_images=5):
    """Plot images with bounding boxes to verify annotations, with different colors for each class."""
    # Define a color map for bounding boxes based on class
    color_map = {
        0: 'red', 1: 'blue', 2: 'green', 3: 'yellow',
        4: 'yellow', 5: 'orange', 6: 'cyan', 7: 'magenta'
    }
    class_names = {
        0: 'car', 1: 'truck', 2: 'bus', 3: 'motorcycle',
        4: 'bicycle', 5: 'scooter', 6: 'person', 7: 'rider'
    }

    image_files = [os.path.join(image_dir, img) for img in os.listdir(image_dir) if img.endswith('.PNG')]
    if len(image_files) > num_images:
        image_files = random.sample(image_files, num_images)
    else:
        image_files = image_files[:num_images]

    fig, axes = plt.subplots(num_images, 1, figsize=(10, 20))

    if num_images == 1:
        axes = [axes]  # Ensure axes is iterable if there's only one image

    for ax, img_path in zip(axes, image_files):
        image = Image.open(img_path)
        ax.imshow(image)
        ax.axis('off')

        annotation_path = os.path.join(annotations_dir, os.path.basename(img_path).replace('PNG', 'txt'))
        if os.path.exists(annotation_path):
            with open(annotation_path, 'r') as file:
                for line in file:
                    elements = line.split()
                    class_id = int(elements[0])
                    x_center = float(elements[1])
                    y_center = float(elements[2])
                    width = float(elements[3])
                    height = float(elements[4])
                    x = (x_center - width / 2) * image.width
                    y = (y_center - height / 2) * image.height
                    width = width * image.width
                    height = height * image.height

                    # Get color and label from maps
                    color = color_map.get(class_id, 'white')  # Default to white if class_id not in map
                    label = class_names.get(class_id, 'Unknown')  # Default to 'Unknown' if class_id not in map

                    # Draw rectangle and label
                    rect = patches.Rectangle((x, y), width, height, linewidth=2, edgecolor=color, facecolor='none')
                    ax.add_patch(rect)
                    ax.text(x, y, label, color=color, fontsize=12, verticalalignment='top', bbox=dict(facecolor='black', alpha=0.5))

    plt.show()
#plot_bounding_boxes(image_directory, annotations_directory)



def analyze_bounding_boxes(annotations_dir, class_names):
    """Analyze and plot bounding box sizes and aspect ratios for different classes, with improved layout and fixed axes."""
    sizes = defaultdict(list)
    aspect_ratios = defaultdict(list)

    # Iterate over annotation files
    for filename in os.listdir(annotations_dir):
        if filename.endswith('.txt'):
            with open(os.path.join(annotations_dir, filename), 'r') as file:
                for line in file:
                    elements = line.split()
                    class_id = int(elements[0])
                    if class_names[class_id] == 'motorcycle':
                        continue  # Skip 'motorcycle' class
                    width = float(elements[3])
                    height = float(elements[4])
                    area = width * height
                    aspect_ratio = width / height if height != 0 else 0
                    sizes[class_names[class_id]].append(area)
                    aspect_ratios[class_names[class_id]].append(aspect_ratio)

    num_classes = len(class_names) - 1  # Adjust count for skipped class
    fig, axs = plt.subplots(num_classes, 2, figsize=(10, num_classes * 3), tight_layout=True)

    # Determine global maximum values to fix axes scale
    max_size = max(max(sizes[class_name]) for class_name in sizes if sizes[class_name])
    max_aspect_ratio = max(max(aspect_ratios[class_name]) for class_name in aspect_ratios if aspect_ratios[class_name])

    for i, class_name in enumerate(name for name in class_names.values() if name != 'motorcycle'):
        n, bins, patches = axs[i][0].hist(sizes[class_name], bins=20, color='blue', alpha=0.7, log=True)
        axs[i][0].set_title(f'Size distribution for {class_name}')
        axs[i][0].set_xlabel('Area')
        axs[i][0].set_ylabel('Frequency')
        axs[i][0].set_xlim([0, max_size])  # Fix x-axis for size

        n, bins, patches = axs[i][1].hist(aspect_ratios[class_name], bins=20, color='green', alpha=0.7, log=True)
        axs[i][1].set_title(f'Aspect ratio distribution for {class_name}')
        axs[i][1].set_xlabel('Aspect ratio (Width/Height)')
        axs[i][1].set_ylabel('Frequency')
        axs[i][1].set_xlim([0, max_aspect_ratio])  # Fix x-axis for aspect ratio

    plt.show()
#analyze_bounding_boxes(annotations_directory, class_names_map)



def plot_dataset_bounding_box_centers(image_directory, annotations_directory, class_names, image_size=(1024, 128)):
    """Plot the center points of bounding boxes for all images in the dataset on a blank canvas with an outline of the image dimensions."""
    # Define a color map for bounding boxes based on class
    color_map = {
        'car': 'red', 'truck': 'blue', 'bus': 'green', 'motorcycle': 'yellow',
        'bicycle': 'purple', 'scooter': 'orange', 'person': 'cyan', 'rider': 'magenta', 'corner': 'black'
    }

    # Create a blank canvas the exact size of the image dimensions
    aspect_ratio = image_size[0] / image_size[1]
    fig, ax = plt.subplots(figsize=(10, 10 / aspect_ratio))
    ax.set_xlim(0, image_size[0])
    ax.set_ylim(image_size[1], 0)

    # Draw a rectangle representing the image boundary
    rect = patches.Rectangle((0, 0), image_size[0], image_size[1], linewidth=1, edgecolor='black', facecolor='none', linestyle="--")
    ax.add_patch(rect)

    # Process each image and its corresponding annotation
    for filename in os.listdir(annotations_directory):
        if filename.endswith('.txt'):
            annotation_path = os.path.join(annotations_directory, filename)
            # Load annotations
            with open(annotation_path, 'r') as file:
                for line in file:
                    elements = line.split()
                    class_id = int(elements[0])
                    x_center = float(elements[1]) * image_size[0]
                    y_center = float(elements[2]) * image_size[1]
                    # Plot each point exactly as it appears in the image
                    ax.scatter(x_center, y_center, color=color_map[class_names[class_id]], label=class_names[class_id], s=20, edgecolors='black', alpha=0.6)

    # Create a legend with unique entries
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), loc='upper right', title="Classes")
    
    plt.axis('on')  # Show the axes
    plt.grid(False)  # Disable grid
    plt.show()
#plot_dataset_bounding_box_centers(image_directory, annotations_directory, class_names_map)



def collect_all_bounding_box_centers(annotations_directory, class_names):
    centers = []
    for filename in os.listdir(annotations_directory):
        file_path = os.path.join(annotations_directory, filename)
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split()
                # Assuming label files contain: class_index x_center y_center width height
                class_id = int(parts[0])
                x_center, y_center = float(parts[1]), float(parts[2])
                centers.append((class_id, x_center, y_center))
    return centers
def plot_centers_on_image(image_path, centers, class_names, class_order):
    image = cv2.imread(image_path)
    if image is None:
        print("Failed to load image.")
        return
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    height, width, _ = image.shape

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(image)
    
    # Define a color map for bounding boxes based on class
    color_map = {
        'car': 'red', 'truck': 'blue', 'bus': 'green', 'motorcycle': 'yellow',
        'bicycle': 'purple', 'scooter': 'orange', 'person': 'cyan', 'rider': 'magenta', 'corner': 'black'
    }
    
    # Plot points based on class order determined by frequency
    for class_name in class_order:
        class_id = class_names.index(class_name)
        # Filter and collect only coordinates
        filtered_centers = [(x, y) for cid, x, y in centers if cid == class_id]
        centers_x = [x * width for x, y in filtered_centers]
        centers_y = [y * height for x, y in filtered_centers]

        ax.scatter(centers_x, centers_y, color=color_map[class_name], label=class_name, s=5, alpha=0.4)

    # Create a legend with unique entries
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), loc='upper right', title="Classes")
    
    plt.show()
def get_sorted_class_order(annotations_dir, class_names):
    class_counts = {name: 0 for name in class_names}
    for filename in os.listdir(annotations_dir):
        if filename.endswith('.txt'):
            with open(os.path.join(annotations_dir, filename), 'r') as file:
                for line in file:
                    class_id = int(line.split()[0])
                    class_counts[class_names[class_id]] += 1
    # Sort classes by count in descending order
    sorted_classes = sorted(class_counts, key=class_counts.get, reverse=True)
    return sorted_classes
centers = collect_all_bounding_box_centers(annotations_directory, class_names)
class_order = get_sorted_class_order(annotations_directory, class_names)
first_image_path = os.path.join(image_directory, sorted(os.listdir(image_directory))[0])
#plot_centers_on_image(first_image_path, centers, class_names, class_order)