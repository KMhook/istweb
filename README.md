# 部署方法

1. pip install -r requirements.txt 安装依赖的包。
<<<<<<< HEAD
2. 配置数据库（步骤略）
3. python manage.py syncdb
4. python manage.py migrate
5. python manage.py collectstatic
6. 配置 nginx + gunicorn （步骤略）
7. 用celery来做定时任务，依赖的包已写进requirements.txt,之后syncdb，migrate
8. ./manage.py celeryd -s celerybeat-schedule -v 2 -B -l INFO
=======
2. 安装 vender 目录内的 douban-python 与 gdata (python setup.py install)
3. 配置数据库（步骤略）
4. python manage.py syncdb
5. python manage.py migrate
6. python manage.py collectstatic
7. 配置 nginx + gunicorn （步骤略）
>>>>>>> b1c8816ac8ea98d36c60779864c3b00117e60127

## 补充说明

1. 本项目的 css 文件全部由 sass 源文件编译生成，如需修改，建议修改 sass 文件后重新编译。
2. Guardfile 文件主要用于 guard-livereload（开发期间使用），部署时不需要用到这个文件。
3. 请保证当前目录以及 uploads/ 目录可写，因为文件上传时会上传到 uploads/。
