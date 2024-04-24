#!/bin/bash
source your_env_path/bin/activate

pid=$(ps -ef | grep xxx.py | grep -v grep | awk '{print $2}')
echo "$pid"
if [[ $pid ]]; then
  echo "进程存活"

else
  echo "进程死亡，正在重启"
  rm -rf xxx.log
  cd your_path && nohup python -u xxx.py >> xxx.log 2>&1 &

fi
