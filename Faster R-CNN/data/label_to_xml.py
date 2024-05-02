import os
import xml.etree.ElementTree as ET

# Set to test, val, and train
dataset_type = "test"
classes = ["car",   "truck",   "bus",   "motorcycle",   "bicycle",   "scooter",   "person",   "rider"]

def convert_labels_to_xml(source_dir, destination_dir):
    # Create destination directory if it doesn't exist
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # Iterate through label files in source directory
    for filename in os.listdir(source_dir):
        if filename.endswith('.txt'):
            label_file_path = os.path.join(source_dir, filename)
            xml_filename = os.path.splitext(filename)[0] + '.xml'
            xml_file_path = os.path.join(destination_dir, xml_filename)

            # Create XML tree
            root = ET.Element('annotation')
            folder = ET.SubElement(root, 'folder')
            folder.text = ''
            filename_element = ET.SubElement(root, 'filename')
            filename_element.text =os.path.splitext(filename)[0] + '.png'
            path = ET.SubElement(root, 'path')
            path.text = 'data/' + dataset_type + "/images/" + os.path.splitext(filename)[0] + '.png'
            source = ET.SubElement(root, 'source')
            database = ET.SubElement(source, 'database')
            database.text = 'ntnu.ai'
            segmented = ET.SubElement(root, 'segmented')
            segmented.text = '0'

            # Read labels from file and add to XML
            with open(label_file_path, 'r') as label_file:
                lines = label_file.readlines()
                for line in lines:
                    parts = line.strip().split()
                    obj = ET.SubElement(root, 'object')
                    name = ET.SubElement(obj, 'name')
                    name.text = classes[int(parts[0])]
                    pose = ET.SubElement(obj, 'pose')
                    pose.text = 'Unspecified'
                    truncated = ET.SubElement(obj, 'truncated')
                    truncated.text = '0'
                    difficult = ET.SubElement(obj, 'difficult')
                    difficult.text = '0'
                    occluded = ET.SubElement(obj, 'occluded')
                    occluded.text = '0'
                    bndbox = ET.SubElement(obj, 'bndbox')
                    xmin = ET.SubElement(bndbox, 'xmin')
                    xmin.text = str(int(float(parts[1]) * 1024 - float(parts[3]) * 1024/2))
                    xmax = ET.SubElement(bndbox, 'xmax')
                    xmax.text = str(int(float(parts[1]) * 1024 + float(parts[3]) * 1024/2))
                    ymin = ET.SubElement(bndbox, 'ymin')
                    ymin.text = str(int(float(parts[2]) * 128 - float(parts[4]) * 128/2))
                    ymax = ET.SubElement(bndbox, 'ymax')
                    ymax.text = str(int(float(parts[2]) * 128 + float(parts[4]) * 128/2))

            # Write XML to file
            tree = ET.ElementTree(root)
            tree.write(xml_file_path)

def main():
    source_labels_dir = 'data/' + dataset_type + '/labels'
    destination_labels_dir = 'data/' + dataset_type + '/annotations'

    convert_labels_to_xml(source_labels_dir, destination_labels_dir)

if __name__ == "__main__":
    main()
