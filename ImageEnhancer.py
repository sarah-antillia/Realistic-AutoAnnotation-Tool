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

# 2022/06/23 Modified to use medium and small section

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

  # 2022/06/23 Modified to use medium and small section
  def run(self, config_ini, target):
    parser  = ConfigParser(config_ini)
    CONFIGS = "configs"
    #config1 = parser.get(CONFIGS, "color_enhancer_config")
    MEDIUM  = "medium"
    SMALL   = "small"
    medium_rotator_config = parser.get(MEDIUM, "warp_rotator_config")
    small_rotator_config  = parser.get(SMALL,  "warp_rotator_config")

    medium_trapezoider_config = parser.get(MEDIUM, "warp_trapezoider_config")
    small_trapezoider_config  = parser.get(SMALL,  "warp_trapezoider_config")

    medium_enhanced_images_dir = parser.get(MEDIUM, "enhanced_images_dir")
    medium_enhanced_images_path = medium_enhanced_images_dir + "_" + target
    print("=== medium_enhanced_images_path {}".format(medium_enhanced_images_path))
    if os.path.exists(medium_enhanced_images_path):
      shutil.rmtree(medium_enhanced_images_path, ignore_errors=False, onerror=None)
    else:
      print("=== Create enhanced_images_dir {}".format(medium_enhanced_images_path))
      os.makedirs(medium_enhanced_images_path)

    small_enhanced_images_dir = parser.get(SMALL, "enhanced_images_dir")
    small_enhanced_images_path = small_enhanced_images_dir + "_" + target
    print("=== small_enhanced_images_path {}".format(small_enhanced_images_path))
    if os.path.exists(small_enhanced_images_path):
      shutil.rmtree(small_enhanced_images_path, ignore_errors=False, onerror=None)
    else:
      print("=== Create enhanced_images_dir {}".format(small_enhanced_images_path))
      os.makedirs(small_enhanced_images_path)

    if medium_rotator_config != None:
      parser = ConfigParser(medium_rotator_config)
      input_dir  = parser.get(target, "input_dir")
      angles     = parser.get(target, "angles") 
      rotator    = ImageWarpRotator()
      rotator.rotate(input_dir, angles, medium_enhanced_images_path)

    if small_rotator_config != None:
      parser = ConfigParser(small_rotator_config)
      input_dir  = parser.get(target, "input_dir")
      angles     = parser.get(target, "angles") 
      rotator    = ImageWarpRotator()
      rotator.rotate(input_dir, angles, small_enhanced_images_path)

    if medium_trapezoider_config != None:
      parser = ConfigParser(medium_trapezoider_config)
      input_dir  = parser.get(target,     "input_dir")
      policy     = int(parser.get(target, "policy"))
      ws_list    = parser.get(target,     "ws_list")
      hs_list    = parser.get(target,     "hs_list") 
      trapezoider = ImageWarpTrapezoider()
      trapezoider.generate(input_dir, medium_enhanced_images_path, ws_list, hs_list, policy=policy)

    if small_trapezoider_config != None:
      parser = ConfigParser(small_trapezoider_config)
      input_dir  = parser.get(target,     "input_dir")
      policy     = int(parser.get(target, "policy"))
      ws_list    = parser.get(target,     "ws_list")
      hs_list    = parser.get(target,     "hs_list") 
      trapezoider = ImageWarpTrapezoider()
      trapezoider.generate(input_dir, small_enhanced_images_path, ws_list, hs_list, policy=policy)


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

