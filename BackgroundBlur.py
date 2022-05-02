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
# 2022/05/10 copyright (c) antillia.com


import os
import sys

import cv2
#import numpy as np

import traceback

import glob

def image_blur(source_dir, output_dir):
  files = glob.glob(source_dir + "/*.jpg")
  if len(files) == 0:
    raise Exception("Not found jpg files in " + source_dir)
    
  for file in files:
    
    image = cv2.imread(file)
    base_name = os.path.basename(file)

    blur = cv2.blur(image,(5,5))
    output_file = os.path.join(output_dir, base_name)
    print("--- saved {}".format(output_file))

    cv2.imwrite(output_file, blur)

# python BackgroundBlur.py source_dir dest_dir
if __name__ == "__main__":
  source_dir = "./source"
  dest_dir   = "./blurred"
  try:
    if len(sys.argv) == 3:
      source_dir = sys.argv[1]
      dest_dir   = sys.argv[2]
    else:
      raise Exception("Invalid argment")

    if not os.path.exists(source_dir):
      raise Exception("Not found " + source_dir)
    if not os.path.exists(dest_dir):
      os.makedirs(dest_dir)

    image_blur(source_dir, dest_dir)
  except:
    traceback.print_exc()

