#!/bin/bash
. /etc/profile
. ~/.bash_profile
export PYENV_VIRTUALENV_DISABLE_PROMPT=1
eval "$(pyenv init -)"
pyenv deactivate
pyenv activate env372
ps -ef | grep fumian_hunan.py | grep -v grep | awk '{print $2}' | xargs kill -9
cd /root/shaohang/single_process/spider/fumian
rm -rf /data/ysh/fumian_zhengcai_xingfa.log
nohup python -u fumian_hunan.py >> /data/ysh/fumian_hunan.log 2>&1 &