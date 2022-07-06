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

# PNGImageResizer.py
# 2022/06/22


import os
import sys
import glob
from uuid import uuid4

from random import *
import numpy as np
import shutil

from PIL import Image, ImageOps, ImageFilter
import traceback

sys.path.append('../../')

from ConfigParser import ConfigParser

class PNGImageResizer:

  ##
  # Constructor
  def __init__(self, source_folder, medium_dir, small_dir):
    self.source_folder = source_folder
    self.medium_dir    = medium_dir
    self.small_dir     = small_dir

    self.MAX_SIZE      = 500
    self.SMALL_SIZE    = 240

    self.background    = None
    self.save_format   = "png"    

  def generate(self, expand=1.3):
    print("=== source_folder {}".format(self.source_folder))
    pattern = self.source_folder + "/*.png"
    files = glob.glob(pattern)
    i = 1
    for filepath in files:
        filename = os.path.basename(filepath)        
        pos = filename.find(".png")
        name = filename[0:pos]
        source_image = Image.open(filepath).convert("RGBA")
        
        width   = float(source_image.width)  * expand 
        height  = float(source_image.height) * expand 
        width   = int(width)
        height  = int(height)
        if width >self.MAX_SIZE or height >self.MAX_SIZE:
          print("==== Skipping: Invalid resized image size w:{} h:{}  file:{} expand:{}".format(width, height, filepath, expand))
          continue
        id = uuid4()
        resized_image = source_image.resize((int(width), int(height)))
        if width >self.SMALL_SIZE or height > self.SMALL_SIZE:
          save_pathname = os.path.join(self.medium_dir, name + "___" + str(id) + ".png")
        else:
          save_pathname = os.path.join(self.small_dir, name + "___" + str(id) + ".png")
        print("----- saved file {}".format(save_pathname))
        resized_image.save(save_pathname)
        i += 1      
    
"""

rem 0_image_resizer.bat
python ../../PNGImageResizer.py ^
  ./PNG_Japanese-RoadSigns-90classes_Master ^
  ./PNG_Japanese-RoadSigns-90classes_Medium_Mixed ^
  ./PNG_Japanese-RoadSigns-90classes_Small_Mixed ^

python ../../PNGImageResizer.py ./configs/image_resizer.conf

"""

if __name__ == "__main__":
  try:
    master_dir = ""
    medium_dir = ""
    small_dir  = ""
    config_ini = ""

    ratios     = [0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0,]

    if len(sys.argv) == 2:
      config_ini = sys.argv[1]

      parser  = ConfigParser(config_ini)
      CONFIGS = "configs"
      master_dir = parser.get(CONFIGS,  "master_dir")
      medium_dir = parser.get(CONFIGS,  "medium_dir")
      small_dir  = parser.get(CONFIGS,  "small_dir")
      ratios     = parser.get(CONFIGS,  "ratios")
    if len(sys.argv) == 4:
      master_dir = sys.argv[1]
      medium_dir = sys.argv[2]
      small_dir  = sys.argv[3]

    if not os.path.exists(master_dir):
      raise Exception("Not found source {}".format(master_dir))
    if master_dir == medium_dir or master_dir == small_dir:
      raise Exception("Error source  {} is idential with mediumu {} or small {}".format(master_dir, medium_dir, small_dir))

    if os.path.exists(medium_dir):
      shutil.rmtree(medium_dir)

    if not os.path.exists(medium_dir):
      os.makedirs(medium_dir)

    if os.path.exists(small_dir):
      shutil.rmtree(small_dir)

    if not os.path.exists(small_dir):
      os.makedirs(small_dir)

    expander = PNGImageResizer(master_dir, medium_dir, small_dir)
  
    for ratio in ratios:
      expander.generate(expand=ratio)
    
  except:
    traceback.print_exc()
      
