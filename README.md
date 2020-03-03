# StockPriceMonitor
监控股票达到制定价格后触发事件，使用QQmail推送到手机。基于aiohttp

## 安装说明
0、不用编译也可以直接运行

1、下载项目仓库

    https://github.com/GoodManWEN/StockPriceMonitor.git && \
    cd StockPriceMonitor
    
2、安装指定版本的nodejs

    curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash - && \
    sudo apt-get install -y nodejs
    
3、安装vue脚手架

    npm install -g @vue/cli

4、初始化一个vue项目

    vue create stockm 

5、添加axios插件

    cd stockm && \
    vue add axios && \
    cd ..

6、覆盖前端src

    rm -rf src/components && \
    rm -rf src/plugins && \
    rm src/App.vue && \
    cp -r ../src/components src/ && \
    cp -r ../src/plugins src/ && \
    cp ../src/App.vue src/App.vue
    
7、编译并挂载

    npm run build && \
    cd .. && \
    bash loading.sh

8、安装Python依赖

    pip3 install -r requirements.txt

9、修改`aiomonitorstock.py`配置信息

10、run serve

    python3 aiomonitorstock.py

11、持久化运行，解析域名，并配置反向代理
    
    # app 挂载于 127.0.0.1:7923

## 避坑指南

 - linux Python 版本默认配置 ./configure 不包含 sqlite 插件。需要执行`sudo apt-get install libsqlite3-dev`并按照配置`./configure --enable-optimozations --enable-loadable-sqlite-extensions`重新编译安装 Python
 - 程序在测试期间产生的临时文件，如果使用 root 账号测试则 root 拥有其归属，持久化运行使用非 root 账号会出现权限错误。
 - 基于 Python3.7 + 
    
    
    
