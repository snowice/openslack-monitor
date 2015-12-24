openslack管理平台，包含告警配置、管理、展示以及其他组件(定时任务分发)的管理
============

## Install dependency

    # yum install -y python-virtualenv

    $ cd /home/work/open-falcon/portal/
    $ virtualenv ./env

    # use douban pypi
    $ ./env/bin/pip install -r pip_requirements.txt -i http://pypi.douban.com/simple


## Init database and config

- database schema: scripts/schema.sql
- database config: frame/config.py

## Start

    $ ./env/bin/python wsgi.py

    --> goto http://127.0.0.1:5050


## Run with gunicorn

    $ . env/bin/activate
    $ bash run.sh
    
    --> goto http://127.0.0.1:5050

TODO：需要改成基于django框架开发

