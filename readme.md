
BMC服务器故障预测与诊断平台网址:http://59.110.144.74/，
# 代码结构
BMCBack文件夹为后端，包含故障等级判定和硬盘寿命预测，BMCFronted为前端，BMCDiskWarning为硬盘故障预测代码，splitbmc_type为故障类型判定代码

# 前置需要

请使用apt-get安装Python3，MySQL和Nginx

# 数据库配置

在MySQL中创建名为bmc的数据库和用户，并授权。

# Nginx配置

将在/etc/nginx/下的nginx.conf更名或移除，然后将Frontend包中的nginx.conf-Linux复制到这里，并改名为nginx.conf

使用vim打开nginx.conf，将里面的ip地址更改为本机地址。

在/root/下创建BMCNginx文件夹，并在里面创建logs文件夹

# 前端配置

将Frontend包中的build文件夹移至BMCNginx

输入nginx命令执行前端

# 后端配置

在/root/下创建BMCBackend文件夹

将Backend包解压到/BMCBackend文件夹

使用vim打开BMCBackend/BMCBackend/settings.py文件，将里面database部分改为MySQL的设定，特别是密码。

在/root/BMCBackend/下执行python3 -m venv .venv命令创建虚拟环境（如果服务器不在意环境的话，虚拟环境步骤可跳过）

source .venv/bin/activate运行虚拟环境。

pip install -r requirements.txt安装全部依赖

python3 manage.py runserver [本机IP]:8000执行后端

# 模拟数据导入

如果需要导入模拟数据，请依次执行【注意该类命令耗时较久，请耐心等待服务器反馈status:ok】

本机IP:8000/api/logquery/server_log_data_receiver/

本机IP:8000/api/logquery/memory_log_data_receiver/

本机IP:8000/api/logquery/pcie_log_data_receiver/

本机IP:8000/api/logquery/disk_log_data_receiver/

如果完全不需要模拟数据，请移除BMCBackend中data文件夹以节省服务器空间。
