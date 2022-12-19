
"""

"""# Copyright 2022 Huawei Technologies Co., Ltd
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

import sys
import os
from configparser import ConfigParser
from check_env_remote import CheckDemoEnvironment


def check_control_server(ip,usermae, port,flag):
    """
    Verifying the Controller Node Environment
    1.Ensure that the operating system version.
    2.Ensure that the firewall is disabled.
    3.Ensure that The hinic3 driver has been installed.
    4.Ensure that The VF device has been loaded.
    5.Ensure that the network bridge and port are configured.
    6.Ensure that the OVS is running.
    """
    control = CheckDemoEnvironment(ip,usermae, port,flag)
    check_list = {
        control.check_os:(),
        control.check_status_firewalld:(),
        control.check_status_hinic3:(),
        control.check_vf_status:(),
        control.ovs_vsctl_show:(),
        control.check_openv_switch_status:()
    }
    for function, args in check_list.items():
        status, result = function(*args)
        if not status:
            break
    return status, result


if __name__ == "__main__":
    flag = sys.argv[1]
    cfg = ConfigParser()
    cfg.read(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), 
                          "conf/demo_conf.cfg"))
    ip_compute = None
    username_compute = None
    port_compute = None
    if flag == "remote":
        port_compute = cfg['server_host_second'].get('port_host_second')
        username_compute = cfg['server_host_second'].get('username_host_first')
        ip_compute = cfg['server_host_second'].get('ip_host_first')
    status, result = check_control_server(ip_compute,username_compute,port_compute,flag)
    if status:
        sys.exit(0)
    sys.exit(1)
