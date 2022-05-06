<h1>Antillia Realistic AutoAnnotation Tool (Updated: 2022/05/05)</h1>
This is an experimental project to develop <b>Antillia Realistic AutoAnnotation Tool(ARAAT)</b> for Object Detection.<br>

It generates a realistic image dataset for training and validation, which is artificially made from a small 
real or realistic images, and annotate those images automatically for object detection.<br>
For example, imagine to take a lot of real roadsigns pictures in US in a real world for 
training of object detection task.Probably, it is difficult to gather enough pictures, because the classes of roadsigns in US is more than 100.<br>
One of other approaches to alleviate the difficulties is to generate a lot of realistic and artificial images from some real or realistic object images including illustration
 by using any image augumentation methods.<br>
In this project, we try to design and implement a Realistic AutoAnnotation Tool, which genenetes a 
realistc images dataset,and annotation files to those images automatically,without any manual mouse operations 
of a GUI-based annotation tool.
 
<br>
<a href="#1">1 Antillia Realistic AutoAnnotation Tool</a><br>
<a href="#2">2 Generate enhanced images</a><br>
<a href="#3">3 Create YOLO dataset</a><br>
<a href="#4">4 Create TFRecord dataset </a><br>
<a href="#5">5 Create COCO dataset</a><br>
<a href="#6">6 Create realistic test dataset </a><br>
<a href="#7">7 Create your own dataset</a><br>

<br>
<h2><a name="1">1 Antillia Realistic AutoAnnotation Tool</a> </h2>
We have been using tensorflow 2.4.0 and Python 3.8 environment on Windows11.<br>
Please clone this repository to your local machine.<br>
git clone https://github.com/sarah-antillia/Realistic-AutoAnnotation-Tool.git<br>
You can see the following tree structure by tree command, and the projects folder contains a sample project 
<b>Japanese-RoadSigns-90classes</b>.<br> 
<h3>1.1 Folder tree structure</h3>
<pre>
├─btemplate
└─projects
    ├─template
    └─Japanese-RoadSigns-90classes
        ├─background_test
        ├─background_train
        ├─background_valid
        ├─COCO_Japanese_RoadSigns_90classes
        │  ├─train
        │  └─valid
        ├─Enhanced_images_test
        ├─Enhanced_images_train
        ├─Enhanced_images_valid
        ├─PNG_RoadSigns_Japan_90classes_small
        ├─PNG_RoadSigns_Japan_90classes_tiny
        ├─realistic_test_dataset
        ├─TFRecord_Japanese_RoadSigns_90classes
        │  ├─train
        │  └─valid
        └─YOLO_Japanese_RoadSigns_90classes
            ├─train
            └─valid

</pre>
 
<b>PNG_RoadSigns_Japan_90classes_small</b> and <b>PNG_RoadSigns_Japan_90classes_tiny</b> folders contain a set of 
90 classes Japanese RoadSigns PNG files. Those PNG files have been take from the following websites:<br>
<a href="https://en.wikipedia.org/wiki/Road_signs_in_Japan">en.wikipedia.org:Road signs in Japan</a>
<br>
<a href="https://commons.wikimedia.org/wiki/Road_signs_in_Japan">commons.wikimedia.org: Road signs in Japan</a>
<br>
See also:
<a href="https://github.com/sarah-antillia/PNG_Japanese_RoadSigns_90classes">PNG_Japanese_RoadSigns_90classes</a><br>
<br>
The following folders contain annotated train and valid dataset which have been generated byt this tool.<br> 
<b><a href="./projects/Japanese_RoadSigns_90classes/COCO_Japanese_RoadSigns_90classes">COCO_Japanese_RoadSigns_90classes</a></b><br>
<b><a href="./projects/Japanese_RoadSigns_90classes/TFRecord_Japanese_RoadSigns_90classes">TFRecord_Japanese_RoadSigns_90classes</a></b><br>
<b><a href="./projects/Japanese_RoadSigns_90classes/YOLO_Japanese_RoadSigns_90classes ">YOLO_Japanese_RoadSigns_90classes</a></b><br>
<br>
The following folder contains test dataset which has been generate by this tool.<br>
<b><a href="./projects/Japanese-RoadSigns-90classes/realistic_test_dataset">realistic_test_dataset</a></b><br>
<br>
 
<br>
<h2><a name="2">2 Generate enhanced images</a> </h2>
For our sample project <b>Japanese-RoadSigns-90classes</b>, we have created the following bat(sh) file 
<b>jp_roadsigns_image_enhancer.bat</b>, which will create enhanced images from base object images.<br>
<pre>
python ImageEnhancer.py ./projects/Japanese-RoadSigns-90classes/image_enhancer.conf train
python ImageEnhancer.py ./projects/Japanese-RoadSigns-90classes/image_enhancer.conf valid
python ImageEnhancer.py ./projects/Japanese-RoadSigns-90classes/image_enhancer.conf test
</pre>

For example, the first line of this bat file will generate Enhancesd_train images dataset
from base images dataset, based on <b>image_enhancer.conf</b>.
<pre>
;image_enhander.conf
[configs]
warp_rotator_config_small     = "./projects/Japanese-RoadSigns-90classes/warp_rotator_small.conf"
warp_rotator_config_tiny      = "./projects/Japanese-RoadSigns-90classes/warp_rotator_tiny.conf"
warp_trapezoider_config_small = "./projects/Japanese-RoadSigns-90classes/warp_trapezoider_small.conf"
warp_trapezoider_config_tiny  = "./projects/Japanese-RoadSigns-90classes/warp_trapezoider_tiny.conf"
enhanced_images_dir           = "./projects/Japanese-RoadSigns-90classes/Enhanced_images"
</pre>

For example, warp_rotator_small.conf is the following, which can be used in ImageWarpRotator.py<br>
<pre>
; warp_rotator_small.conf
[train]
input_dir   = "./projects/Japanese-RoadSigns-90classes/PNG_RoadSigns_Japan_90classes_small"
;output_dir = "./projects/Japanese-RoadSigns-90classes/train_rotated"
angles      = [ -4, -2, 3, 4,] 

[valid]
input_dir   = "./projects/Japanese-RoadSigns-90classes/PNG_RoadSigns_Japan_90classes_small"
;output_dir = "./projects/Japanese-RoadSigns-90classes/train_valid"
angles      = [-3, 1, 2,] 

[test]
input_dir   = "./projects/Japanese-RoadSigns-90classes/PNG_RoadSigns_Japan_90classes_small"
;output_dir = "./projects/Japanese-RoadSigns-90classes/test_valid"
angles      = [ -1, 1,] 
</pre>

Similarly, warp_trapezoider_small.conf is the following, which can be used in ImageWarpTrapezoider.py<br>
<pre>

[train]
input_dir   = "./projects/Japanese-RoadSigns-90classes/PNG_RoadSigns_Japan_90classes_small"
;output_dir = "./projects/Japanese-RoadSigns-90classes/train_trapezoided"
policy      = 2
ws_list     = [0.01, 0.02, 0.04]
hs_list     = [0.01, 0.02, 0.04]

[valid]
input_dir   = "./projects/Japanese-RoadSigns-90classes/PNG_RoadSigns_Japan_90classes_small"
;output_dir = "./projects/Japanese-RoadSigns-90classes/valid_trapezoided"
policy      = 2
ws_list     = [0.02, 0.03]
hs_list     = [0.02, 0.03]

[test]
input_dir   = "./projects/Japanese-RoadSigns-90classes/PNG_RoadSigns_Japan_90classes_small"
;output_dir = "./projects/Japanese-RoadSigns-90classes/test_trapezoided"
policy      = 2
ws_list     = [0.01]
hs_list     = [0.02]
</pre>

<h2><a name="3">3 Create YOLO dataset</a></h2>
For our sample project <b>Japanese-RoadSigns-90classes</b>, we have created the following bat(sh) file.<br>
jp_roadsigns_yolo_train_dataset_creator.bat<br>, which will create train and valid dataset with YOLO annotation format.
<pre>
python YOLOTrainDatasetCreator.py ./projects/Japanese-RoadSigns-90classes/train_dataset_creator.conf train
python YOLOTrainDatasetCreator.py ./projects/Japanese-RoadSigns-90classes/train_dataset_creator.conf valid
</pre>
train_dataset_creator.conf<br>
<pre>
; train_dataset_creator.conf
[dataset]
name            = "jp_roadsigns_90"
copyright       = "antillia.com"
version         = "1.0"
background_size = [512,512]
max_image_size  = [240,240]
classes         = "./projects/Japanese-RoadSigns-90classes/classes.txt"

[train]
backgrounds_dir = "./projects/Japanese-RoadSigns-90classes/background_train"
images_dir      = "./projects/Japanese-RoadSigns-90classes/Enhanced_images_train"
output_dir      = "./projects/Japanese-RoadSigns-90classes/YOLO_Japanese_RoadSigns_90classes/train"

[valid]
backgrounds_dir = "./projects/Japanese-RoadSigns-90classes/background_valid"
images_dir      = "./projects/Japanese-RoadSigns-90classes/Enhanced_images_valid"
output_dir      = "./projects/Japanese-RoadSigns-90classes/YOLO_Japanese_RoadSigns_90classes/valid"
</pre>

Sample images of train dataset<br>
<table>
<tr><td>
<img src="./projects/Japanese-RoadSigns-90classes/YOLO_Japanese_RoadSigns_90classes/train/jp_roadsigns_90_1000.jpg" width="400" height="auto">
</td></tr>
<tr><td>
<img src="./projects/Japanese-RoadSigns-90classes/YOLO_Japanese_RoadSigns_90classes/train/jp_roadsigns_90_1101.jpg" width="400" height="auto">
</td></tr>
<tr><td>
<img src="./projects/Japanese-RoadSigns-90classes/YOLO_Japanese_RoadSigns_90classes/train/jp_roadsigns_90_1202.jpg" width="400" height="auto">
</td></tr>
<tr><td>
<img src="./projects/Japanese-RoadSigns-90classes/YOLO_Japanese_RoadSigns_90classes/train/jp_roadsigns_90_1303.jpg" width="400" height="auto">
</td></tr>
<tr><td>
<img src="./projects/Japanese-RoadSigns-90classes/YOLO_Japanese_RoadSigns_90classes/train/jp_roadsigns_90_1404.jpg" width="400" height="auto">
</td></tr>
<tr><td>
<img src="./projects/Japanese-RoadSigns-90classes/YOLO_Japanese_RoadSigns_90classes/train/jp_roadsigns_90_1505.jpg" width="400" height="auto">
</td></tr>
<tr><td>
<img src="./projects/Japanese-RoadSigns-90classes/YOLO_Japanese_RoadSigns_90classes/train/jp_roadsigns_90_1606.jpg" width="400" height="auto">
</td></tr>

</table>
<br>
YOLO annotation inspection(LabelImg)<br>
<img src="./assets/YOLOAnnotationInspection.png" width="640" height="auto"><br>

<br>
<h2><a name="4">4 Create TFRecord dataset</a> </h2>
For our sample project <b>Japanese-RoadSigns-90classes</b>, we have created the following bat file <b>
jp_roadsigns_tfrecord_creator.bat</b>, which will create train and valid TFRecord from YOLO annotated dataset.
<pre>
python YOLO2TFRecordCreator.py ./projects/Japanese-RoadSigns-90classes/yolo2tfrecord_creator.conf
</pre>

yolo2tfrecord_creator.conf<br>
<pre>
; yolo2tfrecord_creator.conf

[dataset]
name         = "jp_roadsigns"
copyright    = "antillia.com"
version      = "1.0"
classes      = "./projects/Japanese-RoadSigns-90classes/classes.txt"
tfrecord_dir = "./projects/Japanese-RoadSigns-90classes/TFRecord_Japanese_RoadSigns_90classes"
label_map_pbtxt  = "./projects/Japanese-RoadSigns-90classes/TFRecord_Japanese_RoadSigns_90classes/label_map.pbtxt"
label_map_yaml   = "./projects/Japanese-RoadSigns-90classes/TFRecord_Japanese_RoadSigns_90classes/label_map.yaml"

[train]
images_dir  = "./projects/Japanese-RoadSigns-90classes/YOLO_Japanese_RoadSigns_90classes/train"
anno_dir    = "./projects/Japanese-RoadSigns-90classes/YOLO_Japanese_RoadSigns_90classes/train"

[valid]
images_dir  = "./projects/Japanese-RoadSigns-90classes/YOLO_Japanese_RoadSigns_90classes/valid"
anno_dir    = "./projects/Japanese-RoadSigns-90classes/YOLO_Japanese_RoadSigns_90classes/valid"

</pre>

<br>
Please run the following bat file to inspect the generated tfrecord.<br>
tfrecord_inspect.bat<br>
<pre>
python TFRecordInspector.py  ^
  ./projects/Japanese-RoadSigns-90classes/TFRecord_Japanese_RoadSigns_90classes/train/train.tfrecord ^
  ./projects/Japanese-RoadSigns-90classes/TFRecord_Japanese_RoadSigns_90classes/label_map.pbtxt ^
  ./Inspector/train
</pre>
<br>
Objects count in tfrecord:<br>
<img src="./assets/TFRecordInspector_objects_count.png" width="640" height="auto"><br>
<br>
Sample images in tfrecord:<br>
<img src="./assets/TFRecordInspector_train.png"  width="640" height="auto"><br>

Label map
<a href="./projects/Japanese-RoadSigns-90classes/TFRecord_Japanese_RoadSigns_90classes/label_map.pbtxt">label_map.pbtxt</a>
<br>
See also:<br>
<a href="https://github.com/atlan-antillia/EfficientDet-Slightly-Realistic-Japanese-RoadSigns">EfficientDet-Slightly-Realistic-Japanese-RoadSigns</a>
<br>
<a href="https://github.com/atlan-antillia/EfficientDet-Slightly-Realistic-USA-RoadSigns-160classes">EfficientDet-Slightly-Realistic-USA-RoadSigns-160classes</a>

<br>
<h2><a name="5">5 Create COCO dataset</a> </h2>
For our sample project <b>Japanese-RoadSigns-90classes</b>, we have created the following bat file <b>
jp_roadsigns_coco_creator.bat</b>, which will create train and valid coco annotation json files 
from YOLO annotated dataset.
<pre>
python YOLO2TFCOCOCreator.py ./projects/Japanese-RoadSigns-90classes/yolo2coco_creator.conf
</pre>

yolo2coco_creator.conf<br>

<pre>
 yolo2coco_creator.conf

[dataset]
name         = "jp_roadsigns_90"
copyright    = "antillia.com"
version      = "1.0"
classes      = "./projects/Japanese-RoadSigns-90classes/classes.txt"

[train]
images_dir  = "./projects/Japanese-RoadSigns-90classes/YOLO_Japanese_RoadSigns_90classes/train"
output_dir  = "./projects/Japanese-RoadSigns-90classes/COCO_Japanese_RoadSigns_90classes/train"

[valid]
images_dir  = "./projects/Japanese-RoadSigns-90classes/YOLO_Japanese_RoadSigns_90classes/valid"
output_dir  = "./projects/Japanese-RoadSigns-90classes/COCO_Japanese_RoadSigns_90classes/valid"

</pre>
<br>
COCO annotation files:<br>
<br>
<a href="./projects/Japanese-RoadSigns-90classes/COCO_Japanese_RoadSigns_90classes/train/annotation.json">train annotation</a><br>
<a href="./projects/Japanese-RoadSigns-90classes/COCO_Japanese_RoadSigns_90classes/valid/annotation.json">valid annotation</a><br>

<br>

<h2><a name="6">6 Create realistic test dataset</a> </h2>
For our sample project <b>Japanese-RoadSigns-90classes</b>, we have created the following bat file
<b>jp_roadsigns_yolo_test_dataset_creator.bat</b>, which will create realistic test dataset with YOLO annotation.
<pre>
python YOLOTestDatasetCreator.py ./projects/Japanese-RoadSigns-90classes/test_dataset_creator.conf
</pre>

<pre>
; test_dataset_creator.conf
[dataset]
name            = "jp_test_roadsigns_90"
copyright       = "antillia.com"
version         = "1.0"
background_size = [1280,720]
max_image_size  = [240, 240]
classes         = "./projects/Japanese-RoadSigns-90classes/classes.txt"

[test]
backgrounds_dir = "./projects/Japanese-RoadSigns-90classes/background_test/"
images_dir      = "./projects/Japanese-RoadSigns-90classes/Enhanced_images_test"
output_dir      = "./projects/Japanese-RoadSigns-90classes/realistic_test_dataset"
num_test_dataset= 100

</pre>


Sample images of realist_test_dataset<br>
<table>
<tr><td>
<img src="./projects/Japanese-RoadSigns-90classes/realistic_test_dataset/jp_test_roadsigns_90_1000.jpg" width="640" height="auto">
</td></tr>
<tr><td>
<img src="./projects/Japanese-RoadSigns-90classes/realistic_test_dataset/jp_test_roadsigns_90_1001.jpg" width="640" height="auto">
</td></tr>
<tr><td>
<img src="./projects/Japanese-RoadSigns-90classes/realistic_test_dataset/jp_test_roadsigns_90_1002.jpg" width="640" height="auto">
</td></tr>
<tr><td>
<img src="./projects/Japanese-RoadSigns-90classes/realistic_test_dataset/jp_test_roadsigns_90_1003.jpg" width="640" height="auto">
</td></tr>
<tr><td>
<img src="./projects/Japanese-RoadSigns-90classes/realistic_test_dataset/jp_test_roadsigns_90_1004.jpg" width="640" height="auto">
</td></tr>
<tr><td>
<img src="./projects/Japanese-RoadSigns-90classes/realistic_test_dataset/jp_test_roadsigns_90_1005.jpg" width="640" height="auto">
</td></tr>
<tr><td>
<img src="./projects/Japanese-RoadSigns-90classes/realistic_test_dataset/jp_test_roadsigns_90_1006.jpg" width="640" height="auto">
</td></tr>

</table>
<h2><a name="7">7 Create your own dataset</a></h2>
<h3>7.1 Prepare a set of object and background images  </h3>
If you would like to get started your own project, you have to do:<br>
1. Create your own project under the <b>projects</b> folder.<br>
2. Prepare a minimum set of object images of some classes.<br>
  Those images must be PNG format, and image size less than 240x240.<br>  
3. Prepare a set of background images to create train and valid image dataset.<br>
  Those backgrounds must have same image size 512x512. <br>
4. Prepare a set of background images to create test image dataset.<br>
  Those backgrounds must have same image size 1280x720. <br>
  <br>
The minimum image set will be augumented by our augumentation tool(python scripts), and the augumented images 
will be pasted on train, valid, test bacground images to generate realistic dataset for object detection.<br>
<br>

<h3>7.2 Create config files</h3>
Please run the following command to create conf files for your project.<br>
<pre>
python ProjectCreator.py dataset_name project_name
</pre>
This command creates conf files for the project_name from conf files in "./projects/template" folder.
<br>
Example: <b>Japanese_Signals</b> project<br>

<pre>
python ProjectCreator.py jp_signals Japanese_Signals
</pre>

This generates the following conf files under "./projects/Japanese_Signals"<br>
<pre>
./projects/Japanese_Signals/color_enhancer.conf
./projects/Japanese_Signals/image_enhancer.conf
./projects/Japanese_Signals/test_dataset_creator.conf
./projects/Japanese_Signals/train_dataset_creator.conf
./projects/Japanese_Signals/warp_rotator_small.conf
./projects/Japanese_Signals/warp_rotator_tiny.conf
./projects/Japanese_Signals/warp_trapezoider_small.conf
./projects/Japanese_Signals/warp_trapezoider_tiny.conf
./projects/Japanese_Signals/yolo2coco_creator.conf
./projects/Japanese_Signals/yolo2tfrecord_creator.conf
</pre>
, and bat files under "./" <br>
<pre>
./jp_signals_coco_creator.bat
./jp_signals_image_enhancer.bat
./jp_signals_tfrecord_creator.bat
./jp_signals_yolo_test_dataset_creator.bat
./jp_signals_yolo_train_dataset_creator.bat

</pre>

For example, <b>train_dataset_creator.conf</b> is the following.<br>
<pre>
; train_dataset_creator.conf
[dataset]
name            = "jp_signals"
copyright       = "antillia.com"
version         = "1.0"
background_size = [512,512]
max_image_size  = [240,240]
classes         = "./projects/Japanese_Signals/classes.txt"

[train]
backgrounds_dir = "./projects/Japanese_Signals/background_train"
images_dir      = "./projects/Japanese_Signals/Enhanced_images_train"
output_dir      = "./projects/Japanese_Signals/YOLO_Japanese_Signals/train"

[valid]
backgrounds_dir = "./projects/Japanese_Signals/background_valid"
images_dir      = "./projects/Japanese_Signals/Enhanced_images_valid"
output_dir      = "./projects/Japanese_Signals/YOLO_Japanese_Signals/valid"
</pre>
<br>
<h3>7.3 Create classes file</h3>
Please create <b>classes.txt</b> file containing all classes under your project folder.<br>
<pre>
./projects/Japanese_Signals/classes.txt
</pre>
This can be used to create YOLO annotation files.<br>
In this case, it will be the following.<br>
<pre>
Pedestrian_Signal_Blue
Pedestrian_Signal_Red
Traffic_Signal_Blue
Traffic_Signal_Red
Traffic_Signal_Yellow
</pre>

<h3>7.4 Copy objects and backgrounds image files</h3>
1. Copy the PNG signals files to your project folders.<br>
<pre>
./projects/Japanese_Signals/PNG_Japanese_Signals_small
./projects/Japanese_Signals/PNG_Japanese_Signals_tiny
</pre>
2. Copy the JPG background files to your project folders.<br>
<pre>
./projects/Japanese_Signals/background_train
./projects/Japanese_Signals/background_valid
./projects/Japanese_Signals/background_test
</pre>

<br>
<h3>7.5 Run dataset creation commands</h3>
<pre>
jp_signals_image_enhancer.bat
jp_signals_yolo_train_dataset_creator.bat
jp_signals_yolo_test_dataset_creator.bat
</pre>

If you need COCO and TFRecord annotated dataset, please run the following commands.<br>
<pre>
jp_signals_coco_creator.bat
jp_signals_tfrecord_creator.bat
</pre>

See also;<br>
<a href="https://github.com/atlan-antillia/EfficientDet-Japanese-Signals">EfficientDet-Japanese-Signals</a>


