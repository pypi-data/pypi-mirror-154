# Copyright (c) 2022 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
from six import text_type as _text_type
from .download import download

import argparse

# Since the source code is now fully open sourced
# currently we will provide the prebuilt library 
# and demo codes
import os

__version__ = "0.0.2"

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=_text_type, default=None, help='Name of model, which can be listed by --list_models')
    parser.add_argument('--platform', type=_text_type, default=None, help='Define platform, supports windows/linux/android/ios.')
    parser.add_argument('--soc', type=_text_type, default=None, help='Define soc for the platform, supports x86/x86-nvidia-gpu/arm/jetson.')
    parser.add_argument('--list_models', required=False, action="store_true", default=False, help='List all the supported models.')
    return parser.parse_args()

def read_sources():
    source_cfgs = "https://bj.bcebos.com/paddlehub/fastdeploy/fastdeploy_newest_sources.cfg"
    user_dir = os.environ["HOME"]
    download(source_cfgs, user_dir)
    res = dict()
    with open(os.path.join(user_dir, "fastdeploy_newest_sources.cfg")) as f:
        for line in f:
            if line.strip().startswith("#"):
                continue
            if line.strip() == "":
                continue
            model, plat, soc, url = line.strip().split()
            if model not in res:
                res[model] = dict()
            if plat not in res[model]:
                res[model][plat] = dict()
            if soc not in res[model][plat]:
                res[model][plat][soc] = dict()
            res[model][plat][soc] = url
    return res

def main():
    args = parse_arguments()


    if args.list_models:
        print("Currently, FastDeploy supports {} models:".format(len(all_models)), all_models)
        return

    if args.model is None or args.model == "":
        print("Please define --model to choose which kind of model to deploy, use --list_models to show all the supported models.")
        return

    all_sources = read_sources()

    all_models = list(all_sources.keys())
    all_models.sort()

    if args.model not in all_sources:
        print("{} is not supported, use --list_models to list all the models FastDeploy supported.".format(args.model))
        return

    if args.platform is None or args.platform == "":
        print("Please define --platform to choose which platform to deploy, supports windows/linux/android/ios.")
        return

    if args.platform not in ["windows", "linux", "android", "ios"]:
        print("The flag --platform only can be windows/linux/android/ios.")
        return

    if args.platform not in all_sources[args.model]:
        print("The model:{} only supports platform of {}, {} is not supported now.".format(args.model, list(all_sources[args.model].keys()), args.platform))
        return

    if args.soc is None or args.soc == "":
        print("Please define --soc to choose which hardware to deploy, for model:{} and platform:{}, the available socs are {}.".format(args.model, args.platform, list(all_sources[args.model][args.platform].keys())))
        return

    if args.soc not in all_sources[args.model][args.platform]:
        print("The model:{} in platform:{} only supports soc of {}, {} is not supported now.".format(args.model, args.platform, list(all_sources[args.model][args.platform].keys()), args.soc))
        return
        
    print("\nDownload SDK:", all_sources[args.model][args.platform][args.soc]) 

if __name__ == "__main__":
    main()
