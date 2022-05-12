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
# 2022/05/12 copyright (c) antillia.com
#
# class ImageWarpParallelogramer.py
# This is a very simple, primitive parallelogramer to convert a rectangle area of an image to a parallelogram.
#

import os
import sys
import uuid
import glob
import shutil
import numpy as np
import cv2
import traceback

sys.path.append('../../')

from ConfigParser import ConfigParser

class Parallelogramer:
  def __init__(self, ws_list):
    self.ws_list  = ws_list

  def to_pixel_shift(self, h, flist):
    pix_list = []
    for f in flist:
      s = float(h)*f
      pix_list.append(int(s))
    return pix_list

  def generate_from(self, rectangle):
    
    # rectangle may take a list something like [0, 0, w, h]
    parallelograms  = []   
    x, y, w, h = rectangle

    self.ws_list = self.to_pixel_shift(w, self.ws_list)

    for ws in self.ws_list:
        if ws>0:
          parallelogram = [(x,  y), (w,    y ), (w+ws, h   ),  (x+ws, h)]
        else:
          ws = ws * (-1)
          parallelogram = [(x+ws,  y), (w+ws,    y ), (w, h   ),  (x, h)]

        parallelograms.append(parallelogram)

    return parallelograms


class ImageWarpParallelogramer:

  def __init__(self):
    self.PNG = ".png"
    self.JPG = ".jpg"

  def getImageFiles(self, input_dir):
    #
    input_files = glob.glob(input_dir + "./*" + self.PNG)
    if len(input_files) > 0:
      return (input_files, self.PNG)
    else:
      input_files = glob.glob(input_dir + "./*" + self.JPG)
      return (input_files, self.JPG)


  def generate(self, input_dir, output_dir, ws_list):
    if ws_list == None:
      raise Exception("Invalid ws_list")

    #
    input_files, type = self.getImageFiles(input_dir)
  
    if len(input_files) == 0:
      msg = "Sorry, not found image files in:" + input_dir
      raise Exception(msg)

    for n, input_file in enumerate(input_files):
      image  = None
      h      = 0
      w      = 0
      if type == self.PNG:
        image   = cv2.imread(input_file, cv2.IMREAD_UNCHANGED)
        h, w, _ = image.shape
      elif type == self.JPG:
        image   = cv2.imread(input_file, cv2.IMREAD_COLOR)
        h, w,   = image.shape
      rectangle = [(0, 0), (w, 0),(w, h), (0, h)]

      parallelogramer = Parallelogramer(ws_list)
      rect  = [0, 0, w, h]
      parasllelograms = parallelogramer.generate_from(rect)

      print("---- len parasllelograms {}".format(len(parasllelograms)))
      for i,parasllelogram in enumerate(parasllelograms):
        warped   = self.generate_one(image, rectangle, parasllelogram)
        basename = os.path.basename(input_file)
        name     = basename
        pos      = basename.find(type)
        if pos>0:
          name = basename[0:pos]

        id = str(uuid.uuid4())
        output_filepath = os.path.join(output_dir, name + "___" + id + type)

        cv2.imwrite(output_filepath, warped)
        print("=== saved {}".format(output_filepath)) 
        

  def generate_one(self, image, rectangle, parallelogram):
    rectangle =  np.float32(rectangle)

    W_MAX     = max(parallelogram, key = lambda x:x[0])[0]
    H_MAX     = max(parallelogram, key = lambda x:x[1])[1]
    parallelogram =  np.float32(parallelogram)
    
    MATRIX = cv2.getPerspectiveTransform(rectangle, parallelogram)
    warped = cv2.warpPerspective(image, MATRIX, (W_MAX, H_MAX))
    return warped
# python ImageWarpParallelogramer.py
# python ImageWarpParallelogramer.py parasllelogramer.conf  all/train/valid/test

if __name__ == "__main__":
  input_file = ""
  input_dir  = ""
  target     = "train"
  config_ini = ""
  try:
    if len(sys.argv) == 3:
      config_ini = sys.argv[1]
      target     = sys.argv[2]
    else:
      raise Exception("Usage:python ImageWarpParallelogramer.py config.ini")
    
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
      input_dir  = parser.get(target,     "input_dir")
      output_dir = parser.get(target,     "output_dir") 

      ws_list    = parser.get(target,     "ws_list")

      if not os.path.exists(input_dir):
        msg = "Not found input_dir:" + input_dir
        raise Exception(msg)

      if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
      if not os.path.exists(output_dir):
        os.makedirs(output_dir)
      
      parasllelogramer = ImageWarpParallelogramer()

      print("-----ws_list {}".format(ws_list))

      parasllelogramer.generate(input_dir, output_dir, ws_list)
        
  except:
    traceback.print_exc()
