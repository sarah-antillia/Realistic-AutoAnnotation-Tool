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

# ImageColorEnhancer.py
# 2022/04/20
# antillia.com

import os
import sys
import uuid
import traceback
import glob
from PIL import Image
import random
import shutil

sys.path.append('../../')
from ConfigParser import ConfigParser

class ImageColorEnhancer:
  def __init__(self):
    self.PNG = ".png"
    self.JPG = ".jpg"
    self.PARAMETERS = [0.82, 0.86, 0.90, 0.94, 0.98, 1.02, 1.06, 1.10, 1.14, 1.18 ]
  
  def getImageFiles(self, input_dir):
    #
    input_files = glob.glob(input_dir + "./*" + self.PNG)
    if len(input_files) > 0:
      return (input_files, self.PNG)
    else:
      input_files = glob.glob(input_dir + "./*" + self.JPG)
      return (input_files, self.JPG)
          
  def enhance(self, input_dir, output_dir, color_params, max_enhancer, remove_output_dir=False):
    if not os.path.exists(input_dir):
      msg = "Not found input_dir:" + input_dir
      raise Exception(msg)
    if remove_output_dir:
      if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    if not os.path.exists(output_dir):
      os.makedirs(output_dir)

    self.PARAMETERS = color_params
    (files, type) = self.getImageFiles(input_dir)
    if len(files) == 0:
      raise Exception("No found image files in {}".format(input_dir))
    for n, file in enumerate(files):
      fname = os.path.basename(file)
      name  = fname
      pos   = fname.find(type)

      if pos>-1:
        name = fname[0:pos]
    
      for i in range(max_enhancer):   
        r_image = self.enhance_one(type, file)
        if r_image == None:
          raise Exception("Failed to enhace " + file)
        id = str(uuid.uuid4())
        output_filepath = os.path.join(output_dir, name + "___" + id + type)

        r_image.save(output_filepath)
        print("=== Saved {}".format(output_filepath))
 

  def enhance_one(self, type, filename):
    image = None
    if type == self.PNG:
      image = Image.open(filename).convert("RGBA")
    if type == self.JPG:
      image = Image.open(filename).convert("RGB")
    [xr, xg, xb] = random.sample(self.PARAMETERS, 3)
    r_image = None 
    split = image.split()
    if len(split) == 4:
      (r, g, b, a) = split
      r = r.point(lambda i: i * xr)
      g = g.point(lambda i: i * xg)
      b = b.point(lambda i: i * xb)
      r_image = Image.merge('RGBA',(r,g,b,a))

    elif len(split) == 3:
      (r, g, b)   = split
      r = r.point(lambda i: i * xr)
      g = g.point(lambda i: i * xg)
      b = b.point(lambda i: i * xb)
      r_image =  Image.merge('RGB', (r,g, b  ))
    else:
      r_image = None
    return r_image

# python ImageColorEnhancer.py colorenhancer.conf all/train/valid/test

if __name__ == "__main__":
  images_dir  = ""
  output_dir  = ""
  try:
    if len(sys.argv) == 3:
      config_ini    = sys.argv[1]
      target        = sys.argv[2]
    else:
      raise Exception("Usage: python ImageColorEnhander.py images_dir output_dir max")

    if target not in ["all", "train","valid", "test"]:
      raise Exception("Invalid parameter: target should be train or valid ")

    if not os.path.exists(config_ini):
      msg = "Not found config_ini:" + config_ini
      raise Exception(msg)

    parser     = ConfigParser(config_ini)
    dataset = []
    if target == "train" or target == "valid" or target == "test":
      dataset = [target]
    elif target == "all":
      dataset = ["train", "valid", "test"] #all
 
    for target in dataset:
      input_dir    = parser.get(target, "input_dir")
      output_dir   = parser.get(target, "output_dir") 
      max_enhancer = parser.get(target, "max_enhancer")      
      color_params = parser.get(target, "color_params")
     
      enhancer = ImageColorEnhancer()
      enhancer.enhance(input_dir, output_dir, color_params, max_enhancer)

  except:
    traceback.print_exc()
 