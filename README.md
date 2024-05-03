# Here are the steps to reproduce our training results for our final models:


# YOLOv8

-- Install YOLO in your environment using this command in terminal: pip install ultralytics

-- Navigate to YOLOV8_PROJECT-folder. Go to data.yaml-file, and change path from “/home/pederu/Documents/YOLOv8_project/dataset” to actual path for the dataset in this project, that now is on your computer. 
   Do the same for test_data.yaml.

-- Navigate then to the file YOLOv8.ipynb, which is the place for training and evaluating

-- To train with the hyperparameters used in our best model, be sure the trainings settings are like this: (The auto-settings of YOLOv8 decide the rest of the parameters)
   results = model.train(data='/home/pederu/Documents/YOLOv8_project/data.yaml', epochs=500, imgsz=(1080,128), batch=30, fliplr=0.0)

-- Find the next cell, and run to test the model on the test dataset.

-- If you want, use the next code cell to get two images of how the model inference and find objects with bounding boxes and certainty.

-- The last cell provide inference time, if of interest


# Faster R-CNN

-- Navigate to the folder Faster R-CNN

-- install the requirements listed in the requirements.txt file

-- within /data, create folders test, train, val, images, and labels

-- within /data/test, /data/train and /data/val, create folders annotation, images, and labels

-- put the images in the data/images folder

-- put the labels in the data/labels folder

-- run the data/datasort.py 

-- run the data/label_to_xml.py three times, changing the variable dataset_type so it is run once as test, train and val

-- If necessary, change the paths in the data_config/ntnu.yaml file


-- in terminal (in the Faster R-CNN folder) run this command to train:

python train.py --data data_configs/ntnu.yaml --epochs 100 --batch 16 --imgsz 1024 -ca -uta


-- run this command to eval

python eval.py --model fasterrcnn_resnet50_fpn_v2 --weights outputs/training/res_1/best_model.pth --data data_configs/ntnu.yaml --batch 4 --imgsz 1024


-- run these commands to run inference

python inference.py --input data/dataset_voc/archive/test/images/frame_000322.png --weights outputs/training/res_1/best_model.pth --imgsz 1024

python inference.py --input data/dataset_voc/archive/test/images/frame_000561.png --weights outputs/training/res_1/best_model.pth --imgsz 1024
