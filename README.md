# RegStudioBackend部署文档
```text
依赖环境
python版本：v3.6
nginx:任意版本
vue:v3
mysql:任意版本
```
## 一.nginx安装
### nginx需要的依赖包括：gcc、g++、ssl、pcre、zlib；
#### 安装步骤
```text
1、安装依赖：gcc、gcc-c++、ssl、pcre、zlib。注意：一定要先安装gcc，再安装gcc-c++。然后再安装其他，其他的没有先后顺序。
2、安装Nginx；
3、启动Nginx（直接用默认配置启动测试即可）。
```
##### 详细步骤
```shell
#1、在CentOS服务器上解压源码包，并进入解压后的目录，如下所示：
tar -zxvf nginx-1.20.0.tar.gz
cd nginx-1.20.0
#2、为了使NGINX支持HTTPS协议，需要安装OpenSSL库。可以使用以下命令来安装：
yum install -y openssl openssl-devel
#3/为了确保编译过程中的依赖项已安装，可以使用以下命令：
yum groupinstall -y "Development Tools"
yum install -y zlib-devel
#4 配置NGINX的编译选项。可以使用以下命令来配置：
./configure --prefix=/usr/local/nginx --with-http_ssl_module
#5 编译并安装NGINX。可以使用以下命令来编译和安装：
make
make install
#6 启动NGINX。可以使用以下命令来启动：
/usr/local/nginx/sbin/nginx
#7 如果需要停止NGINX，可以使用以下命令：
/usr/local/nginx/sbin/nginx -s stop
#8 如果需要重新加载配置文件，可以使用以下命令：
/usr/local/nginx/sbin/nginx -s reload 
```

## 二.安装项目依赖包
### 安装步骤
```shell
#1、进入项目中的packagesDir目录
cd packagesDir
#2、执行批量安装命令
pip3 install *.whl
```

### 三.安装uwsgi
### 安装步骤
```shell
#1、进入项目中的RegStudioBackendPackages目录
cd RegStudioBackendPackages
#2、解压源码包，可以使用以下命令：
tar -zxvf uwsgi-2.0.21.tar.gz
#3、进入 uwsgi 源码包的目录，如下所示：
cd uwsgi-2.0.21
#4、安装编译 uwsgi 所需的依赖项，可以使用以下命令：
yum install gcc make automake autoconf libtool python-devel
#5、编译 uwsgi，可以使用以下命令：
python uwsgiconfig.py --build
#6、将 uwsgi 目录复制到某个系统路径中，例如 /usr/local/bin：
cp uwsgi /usr/local/bin/
#7、确认 uwsgi 安装成功，可以使用以下命令：
uwsgi --version
#8、需要注意的是，在执行编译 uwsgi 命令时，需要在具有管理员权限的用户下运行。
```
### 四、后端项目部署，启动
#### 后端部署
```shell
#1、将项目拷贝到目录下面并解压，例
cp RegStudioBackend.tar /home
tar -xvf RegStudioBackend.tar
#2、在setting中找到DataBases修改数据库连接串
cd RegStudioBackend/RegStudioBackend
vim settings.py
#3、修改uwsgi配置文件(只用修改前三项即可)
cd /RegStudioBackend/uwsgiConfig/
vim uwsgiConfig.ini
```
#### 创建数据库

```shell
#以 root 用户登录 MySQL:
mysql -u root -p
```

```mysql
/*1.创建一个新的数据库：*/
CREATE DATABASE reg;

/*2.创建一个新的用户并为其设置密码：*/
CREATE USER 'reg'@'localhost' IDENTIFIED BY '!QAZ2wsx';

/*3.为新用户授予访问权限：*/
GRANT ALL PRIVILEGES ON reg.* TO 'reg'@'localhost';

/*4.刷新权限：*/
FLUSH PRIVILEGES;
```
#### 数据库连接串内容如下，例
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'reg',#数据库名
        'USER': 'root',#登陆数据库用户名
        'PASSWORD': '!QAZ2wsx',#数据库密码
        'HOST': "172.16.38.11",#数据所在ip
        'POST': '3306',#数据库端口
    }
}
```
#### 配置文件内容如下，例
```ini
# path:/RegStudioBackend/uwsgiConfig/uwsgiConfig.ini
# 内容
[uwsgi]
# 使用nginx链接时使用
#socket=/tmp/uwsgi.sock
#chmod-socket=666
#socket=172.16.38.11:8080
# 直接做web服务器使用 python manage.py runserver ip:port
http=172.16.38.11:8000
# 项目目录 [pwd查看 直接填，不需要引号]
chdir=/home/RegStudioBackend
# 项目中wsgi.py文件的目录，相对于项目目录
wsgi-file=/home/RegStudioBackend/RegStudioBackend/wsgi.py
# 指定启动的工作进程数
processes=4
# 指定工作进程中的线程数
threads=2
# 进程中，有一个主进程
master=True
# 保存启动之后主进程的pid
pidfile=uwsgi.pid
# 设置uwsgi后台运行, uwsgi.log 保存日志信息
daemonize=uwsgi.log
# 设置虚拟环境的路径 [cd .virtualenvs]
#virtualenv=true
buffer-size = 32768
```
#### 创建数据库表
```shell
#1、进入RegStudioBackend根目录，以次执行以下语句
python manage.py makemigrations IP
python manage.py makemigrations User 
python manage.py migrate
```

#### 启动后端
```shell
#1、进入uwsgiConfig.ini目录
cd /RegStudioBackend/uwsgiConfig
#2、执行启动命令
uwsgi --ini uwsgiConfig.ini
#3、检查启动日志看是否启动成功
vim uwsgi.log
```

### 五、前端项目部署启动
#### 前端部署
```shell
#1、在文件夹中新建www/vue目录,例如在/home路径下
mkdir www
cd www
mkdir vue
#2、将前端项目拷贝到目录中并解压
cp RegStudioVue.tar /home/www/vue
tar -xvf RegStudioVue.tar
#3、配置nginx.conf(默认路径如下，如找不到以nginx安装的路径为准，配置详情见nginx配置内容)
vim /etc/nginx/nginx.conf
#4、修改完成配置之后启动nginx
systemctl start nginx
#5、检查nginx状态
systemctl status nginx
```
#### nginx配置文件
```shell
#在server语句块中修改，添加以下内容
server{
        listen       8080;#为前端访问接口
        listen       [::]:80;
        server_name  172.16.38.11;# 为当前服务器ip或者hostname
        root         /home/www/vue/dist;# 前端静态页面路径
        location / {
           # root         /home/www/vue/dist;
            try_files $uri $uri/ /index.html   #解决post请求出现404问题
            index  index.html index.htm;
         }
}
```

```mysql
/*链接mysql时:Host 'gateway' is not allowed to connect to this MySQL server;*/
mysql> use mysql;
Database changed
mysql> select 'host' from user where user='root'
    -> ;
+------+
| host |
+------+
| host |
+------+
1 row in set (0.00 sec)
 
mysql> update user set host = '%' where user ='root';
Query OK, 1 row affected (0.00 sec)
Rows matched: 1  Changed: 1  Warnings: 0
 
mysql> flush privileges;
Query OK, 0 rows affected (0.01 sec)
 
mysql> select 'host'   from user where user='root';
+------+
| host |
+------+
| host |
+------+
1 row in set (0.00 sec)
 
mysql> select 'host'  from user where user='root';
+------+
| host |
+------+
| host |
+------+
1 row in set (0.00 sec)
```