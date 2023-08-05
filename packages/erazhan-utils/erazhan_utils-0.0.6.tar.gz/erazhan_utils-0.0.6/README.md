```angular2html

1、在PyPi官网注册账号
2、创建pypi文件夹作为根目录,创建toolsbyerazhan文件夹作为创建项目的名称(最后就是pip install toolsbyerazhan)
3、在toolsbyerazhan文件夹中创建__init__.py(可以为空)表示这是一个package,并创建其它自定义文件,例如timetools.py
4、在根目录下编写setup.py文件(参考网址或者自己之前做的)
5、然后执行python setup.py sdist
6、重新手动(不要复制)创建.pypirc文件(参考网址或者自己之前做的)
7、最后执行python setup.py sdist upload 更新为 twine upload dist/erazhan_utils-0.0.1.tar.gz(通过pip install twine安装twine)

注意:在win10上操作时,要用管理员启动cmd,然后进入到根目录文件夹下

阿里云项目地址(阿里云镜像一般要隔一天才会更新)
http://mirrors.aliyun.com/pypi/simple/erazhan-utils/

使用和更新
pip install erazhan_utils
pip install --upgrade erazhan_utils
pip install --U erazhan_utils

用官网镜像(http -> https)
-i https://pypi.python.org/simple ## 不需要后面的 --trusted-host pypi.python.org
http://e.pypi.python.org/simple?

用国内镜像
-i http://pypi.douban.com/simple --trusted-host pypi.douban.com

阿里云镜像？
http://mirrors.aliyun.com/pypi/simple/

官网:
https://pypi.org/
参考网址:
https://blog.csdn.net/fengmm521/article/details/79144407
https://www.cnblogs.com/Barrybl/p/12090534.html
https://www.cnblogs.com/smileyes/p/7657591.html
```

### __version__ = 0.0.6改动

#### time_utils.py

1. 更改backto_Ndays, 增加参数data_format(默认='%Y-%m-%d')
2. 增加backto_Ntoday, 可自定义data_format(默认='%Y%m%d')
3. 增加trans_timestamp2str, 时间戳转字符串

####  json_utils.py
   
1. 更改save_json_file, 增加参数mode(默认='indent'), 保存时是否展开
   
#### logging_utils.py
1. 更改update_logger, 将参数名"app_version"改为"app_version_name", 增加参数"update_type"(默认='day')
