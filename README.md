# Django Task Scheduler

## 包及组件安装
- Python包安装见requirements.txt
- Docker
----------
## 项目搭建
### 将终端进入到项目目录下
```
    cd your_path/django_task_schedule/
```
### 执行 migration
```
    python manage.py migrate
```
### 启动项目
```
    python manage.py runserver
```
### 启动 redis

```
    docker run -p 6379:6379 -d redis:5
```

### 启动 Celery Worker

    celery -A django_task_schedule worker -l info

### 启动 Celery beat

    celery -A django_task_schedule beat -l info
----------
## 项目访问

- 主界面: http://127.0.0.1:8000/dashboard
  
- 可通过访问 http://127.0.0.1:8000/ 自动跳转

----------
## 主要功能

- 任务的创建
   1. 任务名称以及描述
   2. 指定任务开始时间
   3. 指定任务多久执行一次：每天/每周/每月/仅执行一次
    

- 任务列表
    1. 展示所有任务以及任务状
    2. 停止正在执行的定时任务
    

- 消息列表
    1. 展示任务执行过程中的输出（测试为生成随机数）
    