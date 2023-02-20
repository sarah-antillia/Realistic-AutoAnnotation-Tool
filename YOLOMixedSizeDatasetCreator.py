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
# 


# YOLOMixedSizeDatasetCreator.py

# importing libraries
import os
import sys
from PIL import Image, ImageDraw, ImageFilter
import shutil
import uuid

import numpy as np
import glob
import traceback
import random
sys.path.append('../../')

from ConfigParser import ConfigParser
# 2022/05/31
from YOLO2COCOConverter import YOLO2COCOConverter

class YOLOMixedSizeDatasetCreator:
  # Constructor
  def __init__(self, dataset_name, background_size, max_image_size, classes_file, debug):
  
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
    
    self.BACKGROUND_IMAGE_WIDTH = background_size[0]
    self.BACKGROUND_IMAGE_HEIGHT= background_size[1]

    self.MAX_IMAGE_WIDTH        = max_image_size[0]
    self.MAX_IMAGE_HEIGHT       = max_image_size[1]

    self.debug = debug
    
  def getClassIndex(self, sname):
    index = -1
    for i, name in enumerate(self.classes):
      #print("------------- '{}' '{}' {} ".format(sname, name, i))
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
      else:
        return sname
    pos = sname.find(".png")
    if pos >0:
      cname = sname[0:pos]
    return cname

  def __getClassName(self, sname):
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
            rc = False
            break
    return rc

  def create(self, backgrounds_dir, images_dir, output_dir, scalings):
    if os.path.exists(backgrounds_dir) == False:
       raise Exception("Not found backgrounds_dir {}".format(backgrounds_dir))
    if os.path.exists(images_dir) == False:
       raise Exception("Not found images_dir {}".format(images_dir))
    
    if os.path.exists(output_dir):
       shutil.rmtree(output_dir) 

    if os.path.exists(output_dir) == False:
       os.makedirs(output_dir)  
    
    background_pattern  = backgrounds_dir  + "/*.jpg"
    background_files    = glob.glob(background_pattern)
    images_pattern      = images_dir + "/*.png"
    image_files         = glob.glob(images_pattern)

    for image_file in image_files:

      for scaling in scalings:

        [background_file] = random.sample(background_files, 1)

        background = Image.open(background_file)
        
        try:      
          uuid4= uuid.uuid4()

          fname = str(uuid4) + ".jpg"
          aname = str(uuid4) + ".txt"
          outputfile = os.path.join(output_dir, fname)
          annotation = os.path.join(output_dir, aname) 
          print("=== output {}".format(outputfile))
          i = 0
          WIDTH = self.MAX_IMAGE_WIDTH #240
 
          X_POS = 10  
          Y_POS = 10  

          SPACE = " "
          NL    = "\n"
          bgwidth  = self.BACKGROUND_IMAGE_WIDTH
          bgheight = self.BACKGROUND_IMAGE_HEIGHT
          with open(annotation, "w") as f:
              image = Image.open(image_file).convert("RGBA")
              if image == None:
                raise Exception("Failed to open an image file " + image_file)

              ow, oh = image.size
              rw = int(ow * scaling)
              rh = int(oh * scaling)
              image = image.resize((rw, rh))
              W, H = image.size
              print("--- W: {} H: {}".format(W,H))

              if W> self.MAX_IMAGE_WIDTH or H > self.MAX_IMAGE_HEIGHT:
                print("--------------skipping image file {} scaling {}".format(image_file, scaling))
                
                continue

              print("--- W: {} H: {}".format(W,H))
              px   = X_POS
              py   = Y_POS        
              sname = os.path.basename(image_file)
              sname = self.getClassName(sname)
              classIndex = self.getClassIndex(sname)
              if classIndex == -1:
                print("--- Not found class {}".format(sname))
                raise Exception("Invalid index----------")
            
              #YOLO annotation
              centerx = (px + W/2 ) / float(bgwidth)
              centery = (py + H/2 ) / float(bgheight)
              width   = W / float(bgwidth)
              height  = H / float(bgheight)

              centerx = round(centerx, 4)
              centery = round(centery, 4)
              width   = round(width,   4)
              height  = round(height,  4)

              line    =  str(classIndex) + SPACE + str(centerx) + SPACE + str(centery) + SPACE + str(width) + SPACE + str(height) + NL
              f.write(line)

              print("--- annotation file:{} annotation:{}".format(annotation, line))
  
              self.paste(background, image, px, py)
              if self.debug:
                draw = ImageDraw.Draw(background) 
                rectcolor = (255, 0, 0) 
                linewidth = 2 
                draw.rectangle([(px, py), (px+W, px+H)], \
                      outline=rectcolor, width=linewidth) 

  
          print("=== saved outputfile {}".format(outputfile))
          background.save(outputfile, quality=95)


        except:
          traceback.print_exc()

# python YOLOTestDatasetCreator.py  ./projects/IT-RoadSigns-120classes/configs/yolo_mixed_size_dataset_creator.conf

if __name__ == "__main__":
  config_ini  = ""

  try:
    if len(sys.argv) == 2:
      config_ini = sys.argv[1]
    else:
      raise Exception("Invalid parameters")

    print("--- config_ini {}".format(config_ini))
    parser = ConfigParser(config_ini)
    DATASET = "dataset"
    TRAIN   = "train"
    VALID   = "valid"
    dataset_name    = parser.get(DATASET, "name")
    background_size = parser.get(DATASET, "background_size")
    max_image_size  = parser.get(DATASET, "max_image_size")
    classes_file    = parser.get(DATASET, "classes")
    debug           = parser.get(DATASET, "debug")
  
    if os.path.exists(classes_file) == False:
       raise Exception("Not found classes_file {}".format(classes_file))
    targets = [TRAIN, VALID]
      
    creator = YOLOMixedSizeDatasetCreator(dataset_name, background_size, max_image_size, classes_file, debug)

    for target in targets:
      backgrounds_dir = parser.get(target,  "backgrounds_dir")
      images_dir      = parser.get(target,  "images_dir")
      output_dir      = parser.get(target,  "output_dir")
      scalings        = parser.get(target,  "scalings")
 
      creator.create(backgrounds_dir, images_dir, output_dir, scalings)
    

  except:
    traceback.print_exc()
