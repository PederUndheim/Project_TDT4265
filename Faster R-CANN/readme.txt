One must install the requirements listed in requirements.txt in order to run the program. 
List of requirements is therefore found in requirements.txt.

Here are the terminal commands used to train and validate the data. One must be in the Faster_R-CNN folder to run:

python train.py --data data_configs/ntnu.yaml --epochs 25 --batch 16 --imgsz 1024 -ca -uta

python eval.py --model fasterrcnn_resnet50_fpn_v2 --weights outputs/training/res_1/best_model.pth --data data_configs/ntnu.yaml --batch 4 --imgsz 1024

python inference.py --input data/dataset_voc/archive/test/images/frame_000322.png --weights outputs/training/res_1/best_model.pth --imgsz 1024
python inference.py --input data/dataset_voc/archive/test/images/frame_000561.png --weights outputs/training/res_1/best_model.pth --imgsz 1024