# Copyright 2024 Magicum Sidus
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


import os
import re


from bladoxy.utils.kill_process import kill_possible_sslocal_processes
from bladoxy.utils.nodes import change_node
from bladoxy.utils.configure_port import configure_port
from bladoxy.utils.start_process import start_sslocal
from bladoxy.utils.check_availability import check_availability
from bladoxy.utils.logger import logger




def check_marker_in_bashrc(bashrc_path, start_marker):
    """检查 .bashrc 中是否包含指定的标记"""
    try:
        with open(bashrc_path, 'r') as file:
            content = file.read()
        return re.search(re.escape(start_marker), content) is not None
    except FileNotFoundError:
        logger.warning(f"未找到文件: {bashrc_path}")
        return False



def update_node():
    bashrc_path = os.path.expanduser("~/.bashrc")
    START_MARKER_BLADOXY = "######## START MY_BLADOXY ########"
    if check_marker_in_bashrc(bashrc_path, START_MARKER_BLADOXY):

        # 停止 sslocal 进程
        kill_possible_sslocal_processes()
        change_node()
        configure_port(is_init=False, onlyss=True)
        start_sslocal()
        check_availability()

    else:
        logger.error("请先执行 bladoxy init 进行初始化！")



    
