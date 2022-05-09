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

# ImageEnhancer.py
# 2022/05/10 

import os
import sys
import glob
import traceback
import shutil

sys.path.append('../../')

from ConfigParser import ConfigParser
from ImageColorEnhancer import ImageColorEnhancer
from ImageWarpRotator import ImageWarpRotator
from ImageWarpTrapezoider import ImageWarpTrapezoider

class ImageEnhancer:
  pass
  def __init__(self):
    pass

  def run(self, config_ini, target):
    parser  = ConfigParser(config_ini)
    CONFIGS = "configs"
    #config1 = parser.get(CONFIGS, "color_enhancer_config")

    small_rconfig = parser.get(CONFIGS, "warp_rotator_config_small")
    tiny_rconfig  = parser.get(CONFIGS, "warp_rotator_config_tiny")

    small_tconfig = parser.get(CONFIGS, "warp_trapezoider_config_small")
    tiny_tconfig  = parser.get(CONFIGS, "warp_trapezoider_config_tiny")

    enhanced_images_dir = parser.get(CONFIGS, "enhanced_images_dir")
    enhanced_images_dir = enhanced_images_dir + "_" + target
    print("=== enhanced_images_dir {}".format(enhanced_images_dir))
    if os.path.exists(enhanced_images_dir):
      shutil.rmtree(enhanced_images_dir, ignore_errors=False, onerror=None)
    else:
      print("=== Create enhanced_images_dir {}".format(enhanced_images_dir))
      os.makedirs(enhanced_images_dir)

    if small_rconfig != None:
      parser = ConfigParser(small_rconfig)
      input_dir  = parser.get(target, "input_dir")
      angles     = parser.get(target, "angles") 
      rotator    = ImageWarpRotator()
      rotator.rotate(input_dir, angles, enhanced_images_dir)
    if tiny_rconfig != None:
      parser = ConfigParser(tiny_rconfig)
      input_dir  = parser.get(target, "input_dir")
      angles     = parser.get(target, "angles") 
      rotator    = ImageWarpRotator()
      rotator.rotate(input_dir, angles, enhanced_images_dir)

    if small_tconfig != None:
      parser = ConfigParser(small_tconfig)
      input_dir  = parser.get(target,     "input_dir")
      policy     = int(parser.get(target, "policy"))
      ws_list    = parser.get(target,     "ws_list")
      hs_list    = parser.get(target,     "hs_list") 
      trapezoider = ImageWarpTrapezoider()
      trapezoider.generate(input_dir, enhanced_images_dir, ws_list, hs_list, policy=policy)
    if tiny_tconfig != None:
      parser = ConfigParser(tiny_tconfig)
      input_dir  = parser.get(target,     "input_dir")
      policy     = int(parser.get(target, "policy"))
      ws_list    = parser.get(target,     "ws_list")
      hs_list    = parser.get(target,     "hs_list") 
      trapezoider = ImageWarpTrapezoider()
      trapezoider.generate(input_dir, enhanced_images_dir, ws_list, hs_list, policy=policy)


# python ImageEnhancer ./projects/Something/image_enhance.conf train/valid/test
# python ImageEnhancer.py ./projects/Japanese-RoadSigns-90classes/image_enhancer.conf train

if __name__ == "__main__":
  configs = None
  config_in = ""
  target    = ""  # train, valid, test
  targets   = ["train", "valid", "test"]
  try:
    if len(sys.argv) == 3:
      config_ini = sys.argv[1]
      target     = sys.argv[2]
      if not target in targets:
        raise Exception("Invalid argment " + target)
    else:
      raise Exception("Invalid argment")

    enhancer = ImageEnhancer()
    enhancer.run(config_ini, target)
  except:
    traceback.print_exc()

