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

-- 