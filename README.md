# StockPriceMonitor
监控股票达到制定价格后触发事件，使用QQmail推送到手机。基于aiohttp

## 安装说明
-1、不用编译也可以直接运行

0、下载项目仓库

    https://github.com/GoodManWEN/StockPriceMonitor.git && \
    cd StockPriceMonitor
    
1、安装指定版本的nodejs

    curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash - && \
    sudo apt-get install -y nodejs
    
2、安装vue脚手架

    npm install -g @vue/cli

3、初始化一个vue项目

    vue create stockm 

4、添加axios插件

    cd stockm && \
    vue add axios && \
    cd ..

5、覆盖前端src

    rm -rf src/components && \
    rm -rf src/plugins && \
    rm src/App.vue && \
    cp -r ../src/components src/ && \
    cp -r ../src/plugins src/ && \
    cp ../src/App.vue src/App.vue
    
6、编译

    npm run build
 
7、装载目录

    cd .. && \
    bash loading.sh

8、安装Python依赖

    pip3 install -r requirements.txt
    
9、run serve

    python3 aiomonitorstock.py

10、持久化运行，解析域名，并配置反向代理
    
    # app 挂载于 127.0.0.1:7923

## 避坑指南

 - linux Python版本默认配置./configure不包含sqlite插件。需要执行`sudo apt-get install libsqlite3-dev`并按照配置`./configure --enable-optimozations --enable-loadable-sqlite-extensions`重新编译安装Python
 - 程序在测试期间产生的临时文件，如果使用root账号测试则root拥有其归属，持久化运行使用非root账号会出现权限错误。
    
    
    
