# 项目说明  

一个Django app用于注册nacos

### 依赖库清单  
- python >= 3.6
- django >= 2.0
- requests anyversion

### 安装环境方式

在对应的python环境中: python setup.py install

### 功能及作用
1、适用于Django服务程序注册微服务实例至nacos服务中心，实现服务集群健康检测，服务弹性伸缩，压力负载均衡;  
2、实现了服务与注册中心的登录授权，服务注册，心跳检测;  

### 引入方式
以下两点同时满足后方可启动服务注册

1、在django对应settings中INSTALLED_APPS添加nacos_app
```
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'nacos_app.apps.NacosRegisterConfig'
]
```
2、django程序需要在settings环境配置中写入服务注册的信息  
```
NACOS_SERVER_DISCOVERY = {  
    "server_addr": "",  # nacos服务中心地址,多个英文逗号隔开  
    "namespace": "",                   # 命名空间  
    "group_name": "",                # 分组
    "ip": "",                # 本机ip, 优先级低于socket请求包获取的ip
    "port": "",                       # 本机服务端口
    "service_name": "",           # 本机服务名称
    "ephemeral": ,                   # 是否临时实例，true为临时实例
    "username": "",                    # 拥有对应命名空间权限的账户
    "password": "",               # 密码
    "heartbeat_interval": 5               # 心跳检测间隔，单位秒，nacos默认5s
}
```

### gunicorn web服务启动
gunicorn多个worker模式下启动需要添加--preload参数，由管理进程预加载非函数式编程中的代码块，从而避免多个worker同时加载register  
gunicorn backend.wsgi -w 8 -b 0.0.0.0:port -t 600 --preload  

### 1.1.1版本构想
✓ 实现项目功能结构分离  
✓ 增加查询服务列表接口功能  
✓ 二次封装requests，增加支持LoadBalance的请求发送工具, 可以根据服务名名称自动查找服务ip:port   
✓ 定义实体类接收数据类型  
