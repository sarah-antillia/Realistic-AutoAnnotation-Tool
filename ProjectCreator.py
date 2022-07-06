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
# 2022/07/05 Modified  the command parameter:
#  python ProjectCreator.py category dataset_name project_name
# Example1: 
#  python ProjectCreator.py roadsigns us_roadsigns  US_RoadSigns_86classes  
#
# ProjectCreator.py

import os
import sys
import glob
import traceback
from BatScriptCreator import BatScriptCreator
from ConfigCreator import ConfigCreator

"""
python ProjectCreator.py roadsigns jp_roadsigns  JP_RoadSigns_90classes
python ProjectCreator.py roadsigns us_roadsigns  US_RoadSigns_86classes
python ProjectCreator.py roadsigns us_roadsigns  US_RoadSigns_160classes
python ProjectCreator.py roadsigns fr_roadsigns  FR_RoadSigns_152classes
python ProjectCreator.py roadsigns uk_roadsigns  UK_RoadSigns_94classes
"""

usage = "python ProjectCreator.py category dataset_name project_name"

if __name__ == "__main__":
  #config template dir
  template_dir  = "./config_templates/"
  # 2022/07/04 Added category parameter

  category      = ""
  dataset_name  = ""  
  project_name  = ""  # project_folder_name
  output_dir    = "./projects"
  #bat template dir 
  btemplate_dir = "./batch_templates"
  boutput_dir   = "./"
  try:
    if len(sys.argv) == 4:
      category     = sys.argv[1]
      dataset_name = sys.argv[2]
      project_name = sys.argv[3]
    else:
      raise Exception(usage)
    if not os.path.exists(template_dir):
      raise Exception("Not found template_dir " + template_dir)


    output_dir = os.path.join("./projects", project_name)
    configs_output_dir = os.path.join(output_dir + "/configs")
    if not os.path.exists(configs_output_dir):
      os.makedirs(configs_output_dir)

    if not os.path.exists(output_dir):
      os.makedirs(output_dir)
    
    config_creator = ConfigCreator(template_dir)
    config_creator.run(category, dataset_name, project_name, configs_output_dir)
 
    #2022/05/10 Moodified bat_output_dir to be output_dir of project_name
    bat_output_dir = output_dir
    if not os.path.exists(bat_output_dir):
      os.makedirs(bat_output_dir)

    bat_creator = BatScriptCreator(btemplate_dir)
    bat_creator.run(dataset_name, project_name, bat_output_dir)
  
  except:
    traceback.print_exc()
