#
# YOLOTrainDatasetSplitter.py
# 2022/05/10 to-arai


import os
import sys
import glob
import shutil

import numpy as np
from sklearn.model_selection import train_test_split
import traceback

# yolo_train_dir: includes image and annotation files.
# splitted_train_dir
# splitted_valid_dir


class YOLOMasterDatasetSplitter:

  def __init__(self):
    pass


  def run(self, yolo_master_dir, splitted_train_dir, splitted_valid_dir, classes_file):
    if not os.path.exists(yolo_master_dir):
      raise Exception("Not found " + yolo_master_dir)

    if os.path.exists(splitted_train_dir):
       shutil.rmtree(splitted_train_dir) 

    if not os.path.exists(splitted_train_dir):
      os.makedirs(splitted_train_dir)

    if os.path.exists(splitted_valid_dir):
       shutil.rmtree(splitted_valid_dir) 

    if not os.path.exists(splitted_valid_dir):
      os.makedirs(splitted_valid_dir)


    image_files = glob.glob(yolo_master_dir + "/*.jpg")
    print("--- files {}".format(len(image_files)))

    train_image_files, test_image_files = train_test_split(image_files)
    print("---train len {}".format(len(train_image_files)))
    print("---valid len {}".format(len(test_image_files)))

    for image_file in train_image_files:
      self.copy_image_and_text_file_to(image_file, splitted_train_dir)

    for image_file in test_image_files:
      self.copy_image_and_text_file_to(image_file, splitted_valid_dir)

    train_classes_file = os.path.join(splitted_train_dir, "classes.txt")
    shutil.copy2(classes_file, train_classes_file)

    valid_classes_file = os.path.join(splitted_valid_dir, "classes.txt")
    shutil.copy2(classes_file, valid_classes_file)


  def  copy_image_and_text_file_to(self, image_file, dest_dir):
    basename = os.path.basename(image_file)
    outfile  = os.path.join(dest_dir, basename)
    shutil.copy2(image_file, outfile)
    print("Copied {} to {}".format(image_file, outfile))  
       
    txtfile = image_file.replace(".jpg", ".txt")
    txtbasename = os.path.basename(txtfile)
    out_txtfile = os.path.join(dest_dir, txtbasename)

    shutil.copy2(txtfile, out_txtfile)


# python YOLOMasterDatasetSplitter.py ./projects/Japanese_Signals/YOLO_Signals/master ^
#  ./projects/Japanese_Signals/YOLO_Signals/train ^
#  ./projects/Japanese_Signals/YOLO_Signals/valid

if __name__ == "__main__":
  yolo_master_dir     = ""
  splitted_train_dir  = ""
  splitted_valid_dir  = ""

  try:
    if len(sys.argv) == 4:
      yolo_master_dir    = sys.argv[1]
      splitted_train_dir = sys.argv[2]
      splitted_valid_dir = sys.argv[3]
    else:
      raise Exception("Invalid argment!")

    splitter = YOLOMasterDatasetSplitter()

    splitter.run(yolo_master_dir, splitted_train_dir, splitted_valid_dir)

  except:
    traceback.print_exc()
  