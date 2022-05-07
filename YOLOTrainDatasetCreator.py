# Copyright 2022 antillia.com Toshiyuki Arai
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# 
# 2022/05/10 copyright (c) antillia.com

# YOLOTrainDatasetCreator.py

import os
import sys
import shutil

from PIL import Image, ImageDraw, ImageFilter

import cv2
import numpy as np
import glob
import traceback
import random
import pprint
from ConfigParser import ConfigParser
from YOLOMasterDatasetSplitter import YOLOMasterDatasetSplitter

#from LabelMapReader import LabelMapReader
#import LabelMapReader

# Generate realistc train images and yolo annotation files from background imaes and object images a 
# 
# All background image size should be 512x512, and all object image size less than 250
#  
class YOLOTrainDatasetCreator:
  # Constructor
  def __init__(self, dataset_name, background_size, max_image_size, classes_file):
    self.dataset_prefix = dataset_name + "_"
    self.labelmap = None
    self.classes = []
    self.classes_file = classes_file
    with open(classes_file, "r") as f:
      lines = f.readlines()
      for line in lines:
        classname = line.rstrip('\r\n')
        
        if classname in self.classes:
          print("=== Error duplicate class name {}".format(classname))
          raise Exception("Duplicate class " + classname) 
        self.classes.append(classname)

    print("=== len {} classes {}".format(len(self.classes), self.classes))
    
    self.BACKGROUND_IMAGE_WIDTH  = background_size[0] #[512, 512]
    self.BACKGROUND_IMAGE_HEIGHT = background_size[1] #[512, 512]

    self.MAX_IMAGE_SIZE        = max_image_size[0]

  def getClassIndex(self, sname):
    index = -1
    for i, name in enumerate(self.classes):
      if sname == name:
         print("----- Found {} {} {}".format(sname, name, i))
         index = i
         break
    return index

  def getClassName(self, sname):
    cname = None

    pos = sname.find("___")
    if pos >0:
      sname = sname[0:pos]
    pos = sname.find("__")
    if pos >0:
     cname = sname[0:pos]
     return cname
    pos = sname.find(".png")
    if pos >0:
      cname = sname[0:pos]
    return cname


  def  validatePasteArea(self, bg_img, fg_img, px, py):
    w, h = fg_img.size
    MARGIN = 2
    bw, bh = bg_img.size

    if w > bw:
      w = bw
    if h > bh:
      h = bh

    if (px + w) > bw:
       px = bw - w - MARGIN
    if (py + h) > bh:
       py = bh - h - MARGIN
    return (px, py, w, h)

  
  def  paste(self, bg_img, fg_img, px, py):
    rc = True
    w, h = fg_img.size
    print("----- px     {} py     {}".format(px, py))
    print("----- px_max {} py_max {}".format(px+w, py+h))

    for x in range(w):
      for y in range(h):
        (r, g, b, a) = fg_img.getpixel((x, y))
        if a != 0:
          try:
            bg_img.putpixel([px+x, py+y], (r, g, b))
          except Exception as ex:
            #print("------ Exception {}".format(ex))
            rc = False
            break
    return rc


  def run(self, backgrounds_dir, images_dir, output_dir):
    if os.path.exists(backgrounds_dir) == False:
       raise Exception("Not found backgrounds_dir {}".format(backgrounds_dir))
    if os.path.exists(images_dir) == False:
       raise Exception("Not found images_dir {}".format(images_dir))
    
    if os.path.exists(output_dir):
       shutil.rmtree(output_dir) 

    if os.path.exists(output_dir) == False:
       os.makedirs(output_dir)  
  
    #Background 
    background_pattern   = backgrounds_dir  + "/*.jpg"
    background_files     = glob.glob(background_pattern)
    background_files     = background_files*100
    images_pattern  = images_dir + "/*.png"
    images_files    = glob.glob(images_pattern)
    
    num_images      = len(images_files)
    num_backgroundfiles  = len(background_files)
    print("=== Num backgroundFiles  {}".format(num_backgroundfiles))
    print("=== Num imagesFiles {}".format(num_images))
    background_files     = background_files * (int(num_images/num_backgroundfiles) + 1)

    slen   = int(len(images_files)/4)
    print("--- all_imagele len {}".format(num_images))
    print("--- slen           {}".format(slen))

    classes_file = os.path.join(output_dir, "classes.txt")
    shutil.copy2(self.classes_file, classes_file)

    index = 0
  
    print("=== background_files len {}".format(len(background_files)))

    max = 0

    length = len(background_files)
    
    print("--- length background_files {}".format(length) )

    #Layout policy 1
    # Paste 4 png images onto background images
    #      
    for n in range(slen):
        background_file = background_files[n]
        
        try:
          image1  = images_files[n]
          image2  = images_files[n+slen]
          image3  = images_files[n+slen*2]
          image4  = images_files[n+slen*3]

        except Exception as ex:
          traceback.print_exc()
          break
         
        #background = Image.open(background).convert("RGBA")
        background = Image.open(background_file)
        BW, BH = background.size
        if BW != self.BACKGROUND_IMAGE_WIDTH and BH != self.BACKGROUND_IMAGE_HEIGHT:
          print("Invalid background image size {} {}".format(BW, BH))
          break
        
        sample = [image1, image2, image3, image4]
        try:      
          print("--- {} background {}".format(index, background))
          fname = self.dataset_prefix + str(1000+n) + ".jpg"
          aname = self.dataset_prefix + str(1000+n) + ".txt"
          outputfile   = os.path.join(output_dir, fname)
          annotation   = os.path.join(output_dir, aname) 
          print("=== output {}".format(outputfile))
          i = 0
        
          #g = int((self.BACKGROUND_IMAGE_SIZE - self.MAX_IMAGE_SIZE)/2)
          g = 10
          SPACE = " "
          NL    = "\n"
          bgwidth  = self.BACKGROUND_IMAGE_SIZE #512 
          bgheight = self.BACKGROUND_IMAGE_SIZE #512

          with open(annotation, "w") as f:
            for i, image_file in enumerate(sample):
              print(" === i {} image {}".format(i, image_file))
              image = Image.open(image_file).convert("RGBA")
              W, H = image.size
              print("--- W: {} H: {}".format(W,H))
              # Relayout of each pastable image on the background image to (2x2) 
              if i == 0 or i == 1:
                n = i
                m = 0
              elif i == 2 or i ==3:
                n = i-2
                m = 1
              px   = g  + self.MAX_IMAGE_SIZE * n
              py   = 30 + self.MAX_IMAGE_SIZE * m

              (px, py, W, H) = self.validatePasteArea(background, image, px, py)
     
              sname = os.path.basename(image_file)
              print("--- getClassName--------sname {}".format(sname))
              sname = self.getClassName(sname)
              classIndex = self.getClassIndex(sname)
              if classIndex == -1:
                raise Exception("FATAL ERROR: Not found clsss " + sname)

              centerx = (px + (W)/2 ) / float(bgwidth)
              centery = (py + (H)/2 ) / float(bgheight)
              width   = (W ) / float(bgwidth)
              height  = (H ) / float(bgheight)

              centerx = round(centerx, 4)
              centery = round(centery, 4)
              width   = round(width,   4)
              height  = round(height,  4)

              ann     =  str(classIndex) + SPACE + str(centerx) + SPACE + str(centery) + SPACE + str(width) + SPACE + str(height) + NL
              f.write(ann)
              rc = self.paste(background, image, px, py)
              if rc == False:
                raise Exception("Failed to paste {}".format(image_file))
                
              print("--- pasted {}".format(image_file))
            
          print("=== save outputfile {}".format(outputfile))
          background.save(outputfile, quality=95)
          #
          image.close()
          max += 1
        except:
          traceback.print_exc()
          break

# python YOLOTrainDatasetCreator.py ./projects/Something/dataset_creator.conf master

# python YOLOTrainDatasetCreator.py ./projects/Japanese-RoadSigns-90classes/train_dataset_creator.conf master

# 
if __name__ == "__main__":
  config_ini = ""
  target     = ""
  targets    = ["master", "train", "valid", "test"]
  try:  
    if len(sys.argv) == 3:
       config_ini = sys.argv[1]   # ./projects/Something/dataset_creator.conf
       target     = sys.argv[2]   # master|train|valid|test
    else:
       raise Exception("Invalid parameters")
    # target should be master
    if target not in targets:
      raise Exception("Invalid target " + target)

    print("--- config_ini {}".format(config_ini))
    parser = ConfigParser(config_ini)
    DATASET = "dataset"
    dataset_name    = parser.get(DATASET, "name")
    background_size = parser.get(DATASET, "background_size")
    max_image_size  = parser.get(DATASET, "max_image_size")
    classes_file    = parser.get(DATASET, "classes")
    auto_splitter   = parser.get(DATASET, "auto_splitter")

    backgrounds_dir = parser.get(target,  "backgrounds_dir")
    images_dir      = parser.get(target,  "images_dir")
    output_dir      = parser.get(target,  "output_dir")

    creator = YOLOTrainDatasetCreator(dataset_name, background_size, max_image_size, classes_file)
    creator.run(backgrounds_dir, images_dir, output_dir)

    if target == "master":
       splitted_train_dir = parser.get("train", "output_dir")
       splitted_valid_dir = parser.get("valid", "output_dir")
       splitter = YOLOMasterDatasetSplitter()
       splitter.run(output_dir, splitted_train_dir, splitted_valid_dir, classes_file)
 


  except:
    traceback.print_exc()
