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
#
# BatScriptCreator.py

import os
import sys
import glob
import traceback

class BatScriptCreator:

  def __init__(self, btemplate = "./btemplate"):
    self.BTEMPLATE    = btemplate
    self.DATASET_NAME = "{DATASET_NAME}"
    self.PROJECT_NAME = "{PROJECT_NAME}"

  def run(self, dataset_name, project_name, output_dir="./"):
    print("=== BatScriptCreator run")
    pattern = self.BTEMPLATE + "/*.bat"

    files   = glob.glob(pattern)
    for file in files:
       basename = os.path.basename(file)
       tf = open(file, "r")
       if tf ==None:
         raise Exception("Failed to open bat file: {}".format(file))
       all_lines = tf.readlines()
       tf.close()
       new_lines = []
       for line in all_lines:
         line = line.replace(self.DATASET_NAME, dataset_name)
         line = line.replace(self.PROJECT_NAME, project_name)
         new_lines.append(line)
       output_file = os.path.join(output_dir, dataset_name + "_" + basename)

       with open(output_file, "w") as bf:
         bf.writelines(new_lines)
       print("=== Created {}".format(output_file))

# python BatFileCreator dataset_name project_name
    
if __name__ == "__main__":
  btemplate    = "./btemplate"
  dataset_name = ""
  project_name  = ""
  boutput_dir  = "./"
  try:
    if len(sys.argv) == 4:
      dataset_name = sys.argv[1]
      project_name = sys.argv[2]
      boutput_dir  = sys.argv[3]
    else:
      raise Exception("Invalid argument")
    creator = BatScriptCreator()
    creator.run(dataset_name, project_name, boutput_dir=boutput_dir)
         
  except:
    traceback.print_exc()
