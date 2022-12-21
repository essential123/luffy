# luffy

## 介绍
luffy前后台，一键docker-compose部署,安全方便

## 软件架构
前端Vue，后端django+drf


## 安装教程

### 1 新的centos机器，安装docker和docker-compost

```python
# 安装依赖
yum install -y yum-utils device-mapper-persistent-data lvm2

# 设置yum源
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# 安装docker
yum install -y docker-ce

# 设置开机启动
systemctl enable docker

# 启动 Docker
systemctl start docker

# 查看版本
docker version

## 安装docker-compose
# 下载
curl -L https://get.daocloud.io/docker/compose/releases/download/v2.5.0/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose

# 赋予执行权限
chmod +x /usr/local/bin/docker-compose

# 查看版本
docker-compose --version
```



### 2 下载代码并启动

```python
# 下载git
yum install git -y
# 下载代码
git clone https://gitee.com/liuqingzheng/luffy.git
# 进入目录
cd luffy
# 运行
docker-compose up
```



### 3 导入测试数据

```python
# 把luffy下luffy_api下的luffy.sql导入luffy库
```



## 使用说明

1.  xxxx
2.  xxxx
3.  xxxx

## 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request


## 特技

1.  使用 Readme\_XXX.md 来支持不同的语言，例如 Readme\_en.md, Readme\_zh.md
2.  Gitee 官方博客 [blog.gitee.com](https://blog.gitee.com)
3.  你可以 [https://gitee.com/explore](https://gitee.com/explore) 这个地址来了解 Gitee 上的优秀开源项目
4.  [GVP](https://gitee.com/gvp) 全称是 Gitee 最有价值开源项目，是综合评定出的优秀开源项目
5.  Gitee 官方提供的使用手册 [https://gitee.com/help](https://gitee.com/help)
6.  Gitee 封面人物是一档用来展示 Gitee 会员风采的栏目 [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)
