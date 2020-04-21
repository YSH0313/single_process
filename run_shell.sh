#!/bin/bash
. /etc/profile
. ~/.bash_profile
export PYENV_VIRTUALENV_DISABLE_PROMPT=1
eval "$(pyenv init -)"
pyenv deactivate
pyenv activate env356
ps -ef | grep beizhixing_new_api.py | grep -v grep | awk '{print $2}' | xargs kill -9
cd /root/shaohang/single_process/spider/
rm -rf new_api.log
nohup python -u beizhixing_new_api.py > new_api.log 2>&1 &
