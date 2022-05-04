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
# ProjectCreator.py

import os
import sys
import glob
import traceback
import shutil

class ProjectCreator:

  def __init__(self, tempate_dir):
    self.template_dir = template_dir

  def run(self, dataset_name, project_name, output_dir):
    pattern = self.template_dir + "/*.conf"
    configs = glob.glob(pattern)
    # 1: copy *.conf files in template_dir to output_dir
    for conf in configs:
      basename    = os.path.basename(conf)
      output_conf = os.path.join(output_dir, basename)
      shutil.copy2(conf, output_conf)

    # 2 Replace {DATASET_NAME} in *.conf in output_dir to dataset_name
    #  {PROJECT_NAME} to project_name
    pattern = output_dir + "/*.conf"
    configs = glob.glob(pattern)
    for conf in configs:
       tf = open(conf, "r")
       lines = tf.readlines()
       tf.close()
       new_lines = []
       for line in lines:
         line = line.replace("{DATASET_NAME}", dataset_name)
         line = line.replace("{PROJECT_NAME}", project_name)
         new_lines.append(line)
       with open(conf, "w") as cf:
         cf.writelines(new_lines)


# python ProjectCreator.py jp_signals Japanese_Signals

usage = "python ProjectCreator.py jp_signals Japanese_Signals"

if __name__ == "__main__":
  template_dir = "./projects/template/"
  dataset_name = ""  
  project_name = ""  # project_folder_name
  output_dir   = "./projects"
  try:
    if len(sys.argv) == 3:
      dataset_name = sys.argv[1]
      project_name = sys.argv[2]
    else:
      raise Exception(usage)
    if not os.path.exists(template_dir):
      raise Exception("Not found template_dir " + template_dir)

    output_dir = os.path.join("./projects", project_name)
    if not os.path.exists(output_dir):
      os.makedirs(output_dir)

    creator = ProjectCreator(template_dir)
    creator.run(dataset_name, project_name, output_dir)

  except:
    traceback.print_exc()
