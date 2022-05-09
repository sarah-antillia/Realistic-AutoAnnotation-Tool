<h1>Antillia Realistic AutoAnnotation Tool (Updated: 2022/05/10)</h1>
This is an experimental project to implement <b>Antillia Realistic AutoAnnotation Tool(ARAAT)</b> for Object Detection.<br>

It generates a realistic image dataset for training and validation, which is artificially made from a small 
real or realistic images, and annotate those images automatically for object detection.<br>
For example, imagine to take a lot of real roadsigns pictures in US in a real world for 
training of object detection task.
Probably, it is difficult to gather such a pictures, because the classes of roadsigns inUS is more than 160.
One of other approaches to alleviate the difficulties is  
to generate a lot of realistic and artificial images from some real or realistic object images including illustration
 by using any image augumentation methods.
In this project, we try to design and implement a Realistic AutoAnnotation Tool, which genenetes a 
realistc images dataset,and annotation files to those images automatically,without any manual mouse operations 
of a GUI-based annotation tool.
<br> 
<br>
<a href="#1">1 Antillia Realistic AutoAnnotation Tool</a><br>
<a href="#2">2 Generate Enhanced images</a><br>
<a href="#3">3 Create YOLO dataset</a><br>
<a href="#4">4 Create TFRecord dataset </a><br>
<a href="#5">5 Create COCO dataset</a><br>
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
    ├─Japanese-RoadSigns-90classes
    │  ├─background_test
    │  ├─background_train
    │  ├─background_valid
    │  ├─configs
    │  ├─PNG_Japanese-RoadSigns-90classes_small
    │  └─PNG_Japanese-RoadSigns-90classes_tiny
    └─template    
</pre>
<h3>1.2 Create a project</h3>
Please use ProjectCreator.py to create your own project.<br>
<pre>
python ProjectCreator.py dataset_name project_name
</pre>
Please run the following command to create <b>Japanese-RoadSigns-90classes</b> project:<br>
<pre>
python ProjectCreator.py jp_roadsigns Japanese-RoadSigns-90classes
</pre>
<li>
<b>PNG_Japanese-RoadSigns-90classes_small</b>: RoadSigns files of small size
</li>
<li>
<b>PNG_Japanese-RoadSigns-90classes_small_tiny</b>; RoadSigns files of tine size
</li>
 Those PNG files have been take from the following websites:<br>
<a href="https://en.wikipedia.org/wiki/Road_signs_in_Japan">en.wikipedia.org:Road signs in Japan</a>
<br>
<a href="https://commons.wikimedia.org/wiki/Road_signs_in_Japan">commons.wikimedia.org: Road signs in Japan</a>
<br>
See also:
<a href="https://github.com/sarah-antillia/PNG_Japanese_RoadSigns_90classes">PNG_Japanese_RoadSigns_90classes</a><br>
<br>
The following backgroud foloders contain background jpg images files, which will be used as the background images to generate
test, train and valid dataset.<br> 
<pre>
background_test
background_train
background_valid
</pre>

The ProjectCretator.py generates <b>configs</b> folder, which contain the following configuration files.<br>

<pre>
color_enhancer.conf
image_enhancer.conf
warp_rotator_small.conf
warp_rotator_tiny.conf
warp_trapezoider_small.conf
warp_trapezoider_tiny.conf
yolo2coco_converter.conf
yolo2pascalvoc_converter.conf
yolo2tfrecord_converter.conf
yolo_test_dataset_creator.conf
yolo_train_dataset_creator.conf
</pre>

,and the following bat files under your project folder.<br>
<pre>
image_enhancer.bat
yolo2coco_converter.bat
yolo2pascalvoc_converter.bat
yolo2tfrecord_converter.bat
yolo_test_dataset_creator.bat
yolo_train_dataset_creator.bat
</pre>

<h2><a name="2">2 Generate Enhanced images</a> </h2>

Please move to your project directory, and run the following <b>image_enhancer.bat</b> to augument original PNG roadsings images:<br>
<pre>
./image_enhancer.bat
</pre>
This bat file is the followng.<br>
<pre>
python ../../ImageEnhancer.py ./configs/image_enhancer.conf train
python ../../ImageEnhancer.py ./configs/image_enhancer.conf valid
python ../../ImageEnhancer.py ./configs/image_enhancer.conf test
</pre>
, and the image_enhancer.conf in configs folder.<br>
<pre>
;image_enhander.conf
[configs]
version                       = "2.0"
warp_rotator_config_small     = "./configs/warp_rotator_small.conf"
warp_rotator_config_tiny      = "./configs/warp_rotator_tiny.conf"
warp_trapezoider_config_small = "./configs/warp_trapezoider_small.conf"
warp_trapezoider_config_tiny  = "./configs/warp_trapezoider_tiny.conf"
enhanced_images_dir           = "./Enhanced_images"
</pre>

This will generate the following enhanced image folders:<br>
<pre>
├─Enhanced_images_test
├─Enhanced_images_train
└─Enhanced_images_valid
</pre>

<h2><a name="3">3 Create YOLO dataset</a></h2>

<h3>3.1 Create train and valid dataset</h3>
In your projecr folder, please run the following <b>yolo_train_dataset_creator.bat</b>.<br>
<pre>
./yolo_train_dataset_creator.bat
</pre>
<pre>
python ../../YOLOTrainDatasetCreator.py ./configs/yolo_train_dataset_creator.conf master
</pre>
yolo_train_dataset_creator.conf<br>
<pre>
; yolo_train_dataset_creator.conf
; 2022/05/10 Modified to use splitter to split yolo_master to train and valid when specified master specified
[configs]
version         = "2.0"

[dataset]
name            = "jp_roadsigns"
copyright       = "antillia.com"
version         = "1.1"
background_size = [512,512]
max_image_size  = [240,240]
classes         = "./classes.txt"
auto_splitter   = True

[master]
backgrounds_dir = "./background_train"
images_dir      = "./Enhanced_images_train"
output_dir      = "./YOLO_Japanese-RoadSigns-90classes/master"
  
[train]
backgrounds_dir = "./background_train"
images_dir      = "./Enhanced_images_train"
output_dir      = "./YOLO_Japanese-RoadSigns-90classes/train"

[valid]
backgrounds_dir = "./background_valid"
images_dir      = "./Enhanced_images_valid"
output_dir      = "./YOLO_Japanese-RoadSigns-90classes/valid"

</pre>

This bat file wll generate <b>YOLO_Japanese-RoadSigns-90classes</b> folder, which contain train and valid dataset(images and annotation files).
<pre>
└─YOLO_Japanese-RoadSigns-90classes
    ├─master
    ├─train
    └─valid
</pre>
Sample images of train dataset<br>
<table>
<tr><td>
<img src="./assets/train/jp_roadsigns_1000.jpg" width="400" height="auto">
</td></tr>
<tr><td>
<img src="./assets/train/jp_roadsigns_1101.jpg" width="320" height="auto">
</td></tr>
<tr><td>
<img src="./assets/train/jp_roadsigns_1202.jpg" width="320" height="auto">
</td></tr>
<tr><td>
<img src="./assets/train/jp_roadsigns_1303.jpg" width="320" height="auto">
</td></tr>
<tr><td>
<img src="./assets/train/jp_roadsigns_1405.jpg" width="320" height="auto">
</td></tr>
<tr><td>
<img src="./assets/train/jp_roadsigns_1505.jpg" width="320" height="auto">
</td></tr>
<tr><td>
<img src="./assets/train/jp_roadsigns_1606.jpg" width="320" height="auto">
</td></tr>

</table>

<h3>3.2 Create realist testdataset</h3>
In your projecr folder, please run the following yolo_test_dataset_creator.bat.<br>
<pre>
./yolo_test_dataset_creator.bat
</pre>
yolo_test_dataset_creator.bat is the following.<br>

<pre>
python ../../YOLOTestDatasetCreator.py ./configs/yolo_test_dataset_creator.conf

</pre>
,and yolo_test_dataset_creator.conf.<br>
<pre>
; test_dataset_creator.conf
[configs]
version         = "2.0"

[dataset]
name            = "jp_roadsigns"
copyright       = "antillia.com"
version         = "1.0"
background_size = [1280,720]
max_image_size  = [240, 240]
classes         = "./classes.txt"

[test]
backgrounds_dir = "./background_test/"
images_dir      = "./Enhanced_images_test"
output_dir      = "./realistic_test_dataset"
num_test_dataset= 100
</pre>

This wll generate realistc_test_dataset folder, which contain test dataset(images and annotation files).
<pre>
└─realistic_test_dataset
</pre>
<table>
Sample images of realist_test_dataset<br>
<table>
<tr><td>
<img src="./assets/realistic_test_dataset/jp_roadsigns_1000.jpg" width="640" height="auto">
</td></tr>
<tr><td>
<img src="./assets/realistic_test_dataset/jp_roadsigns_1001.jpg" width="640" height="auto">
</td></tr>
<tr><td>
<img src="./assets/realistic_test_dataset/jp_roadsigns_1002.jpg" width="640" height="auto">
</td></tr>
<tr><td>
<img src="./assets/realistic_test_dataset/jp_roadsigns_1003.jpg" width="640" height="auto">
</td></tr>
<tr><td>
<img src="./assets/realistic_test_dataset/jp_roadsigns_1004.jpg" width="640" height="auto">
</td></tr>
<tr><td>
<img src="./assets/realistic_test_dataset/jp_roadsigns_1005.jpg" width="640" height="auto">
</td></tr>
<tr><td>
<img src="./assets/realistic_test_dataset/jp_roadsigns_1006.jpg" width="640" height="auto">
</td></tr>

</table>

<h2><a name="4">4 Create TFRecord dataset</a> </h2>

In your projecr folder, please run the following <b> yolo2tfrecord_converter.bat</b>.<br>
<pre>
./yolo2tfrecord_converter.bat <br>
</pre>
The yolo2tfrecord_converter.bat is the following.<br>
<pre>
python ../../YOLO2TFRecordConverter.py ./configs/yolo2tfrecord_converter.conf 
</pre>
,and yolo2tfrecord_converter.conf<br>
<pre>
; yolo2tfrecord_converter.conf
[configs]
version      = "2.0"

[dataset]
name         = "jp_roadsigns"
copyright    = "antillia.com"
version      = "2.0"
classes      = "./classes.txt"
tfrecord_dir = "./TFRecord_Japanese-RoadSigns-90classes"
label_map_pbtxt = "./TFRecord_Japanese-RoadSigns-90classes/label_map.pbtxt"
label_map_yaml  = "./TFRecord_Japanese-RoadSigns-90classes/label_map.yaml"

[train]
images_dir   = "./YOLO_Japanese-RoadSigns-90classes/train"
anno_dir     = "./YOLO_Japanese-RoadSigns-90classes/train"

[valid]
images_dir   = "./YOLO_Japanese-RoadSigns-90classes/valid"
anno_dir     = "./YOLO_Japanese-RoadSigns-90classes/valid"
</pre>

This wll generate <b>TFRecord_Japanese-RoadSigns-90classes</b> folder, which contain train and valid tfrecords.
<pre>
└─TFRecord_Japanese-RoadSigns-90classes
    ├─train
    └─valid
</pre>

<br>
YOLO annotation inspection(LabelImg)<br>
<img src="./assets/YOLOAnnotationInspection.png" width="640" height="auto"><br>

Please run the following bat file to inspect the generated tfrecord.<br>
tfrecord_inspect.bat<br>
<pre>
python ../../TFRecordInspector.py ^
  ./TFRecord_Japanese-RoadSigns-90classes/train/train.tfrecord ^
  ./TFRecord_Japanese-RoadSigns-90classes/label_map.pbtxt ^
  ./Inspector/train
</pre>
<br>
Objects count in tfrecord:<br>
<img src="./assets/TFRecordInspector_objects_count.png" width="640" height="auto"><br>
<br>
Sample images in tfrecord:<br>
<img src="./assets/TFRecordInspector_train.png"  width="640" height="auto"><br>

Label map
<a href="./asset/label_map.pbtxt">label_map.pbtxt</a>
<br>
See also:<br>
<a href="https://github.com/atlan-antillia/EfficientDet-Slightly-Realistic-Japanese-RoadSigns">EfficientDet-Slightly-Realistic-Japanese-RoadSigns</a>
<br>
<a href="https://github.com/atlan-antillia/EfficientDet-Slightly-Realistic-USA-RoadSigns-160classes">EfficientDet-Slightly-Realistic-USA-RoadSigns-160classes</a>

<br>
<h2><a name="5">5 Create COCO dataset</a> </h2>
In your project directory, please run the following command to convert YOLO annotation dataset to COCO annotation dataset:<br>
<pre>
,/yolo2coco_converter.bat
</pre>
yolo2coco_converter.bat is the following:<br>
<pre>
python ../../YOLO2COCOConverter.py ./configs/yolo2coco_converter.conf 
</pre>
,and yolo2coco_converter.conf <br>
<pre>
; yolo2coco_converter.conf
[configs]
version      = "2.0"

[dataset]
name         = "jp_roadsigns"
copyright    = "antillia.com"
version      = "2.0"
classes      = "./classes.txt"

[train]
images_dir  = "./YOLO_Japanese-RoadSigns-90classes/train"
output_dir  = "./COCO_Japanese-RoadSigns-90classes/train"

[valid]
images_dir  = "./YOLO_Japanese-RoadSigns-90classes/valid"
output_dir  = "./COCO_Japanese-RoadSigns-90classes/valid"
</pre>


