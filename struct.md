wcplusPro 项目架构清晰，且已经跑通了完整的商业闭环。如果你是一个 Python 开发者，计划推出自己的产品，wcplusPro 能多诸多方面提供参考价值。

./wcplusPro7 19 directories, 96 files
├── cmp 组件根目录
│   ├── __init__.py
│   ├── auth.py 订阅版授权
│   ├── database 数据库通用接口
│   │   ├── __init__.py
│   │   └── utils.py
│   ├── mongo mongodb数据库API
│   │   ├── __init__.py
│   │   └── data_schema.py
│   ├── proxy_server 代理服务器
│   │   ├── __init__.py
│   │   └── addons.py
│   ├── req_data 请求参数
│   │   └── __init__.py
│   ├── spider 爬虫
│   │   ├── __init__.py
│   │   ├── article.py 文章内容爬虫
│   │   ├── article_list.py 文章列表爬虫
│   │   ├── comment.py 评论爬虫
│   │   ├── reading_data.py 阅读数据爬虫
│   │   └── request.py 网络请求API
│   └── update_note 更新日志
│       └── __init__.py
├── controller MVC控制器 一般一张数据库搭配一个控制器
│   ├── __init__.py
│   ├── article.py 文章控制器
│   ├── gzh.py 公众号控制器
│   ├── req_data.py 请求参数控制器
│   ├── settings.py 用户设置控制器
│   ├── task.py 任务控制器
│   └── wcplus_export.py 数据导出控制器
├── macos_install_package.command macos一键安装脚本
├── macos_run_wcplusPro.command macos一键运行脚本
├── main.py 项目入口脚本
├── model MVC数据库model
│   ├── __init__.py
│   ├── article.py 文章
│   ├── gzh.py 公众号
│   ├── req_data.py 请求参数
│   ├── settings.py 设置
│   └── task.py 任务
├── requirement.txt python依赖文件
├── settings.py 全局设置
├── utils 小工具
│   ├── __init__.py
│   ├── dev.py 开发相关
│   └── network.py 网络相关
├── view MVC视图
│   ├── __init__.py
│   ├── article.py 文章
│   ├── category.py 分类
│   ├── gzh.py 公众号
│   ├── report.py 报告
│   ├── req_data.py 请求参数
│   ├── task.py 任务
│   └── wcplus_export.py 数据导出
├── webserver web服务器
│   ├── __init__.py
│   ├── handler url请求处理
│   │   ├── __init__.py
│   │   ├── article.py
│   │   ├── gzh.py
│   │   ├── help.py
│   │   ├── report.py
│   │   ├── req_data.py
│   │   ├── task.py
│   │   ├── test.py
│   │   └── user.py
│   ├── instance.py
│   ├── sio socketio通信
│   │   ├── __init__.py
│   │   └── events.py
│   └── static 前端静态文件 通过webpack打生成
│       ├── css
│       │   ├── app.30dd1d84.css
│       │   ├── chunk-1dd67c7e.4e2ab945.css
│       │   ├── chunk-36db224a.6d14bd25.css
│       │   ├── chunk-41a04990.e034db36.css
│       │   ├── chunk-4ba7a1a6.43521034.css
│       │   ├── chunk-552cb800.9d4179c7.css
│       │   ├── chunk-6b9eb7a4.79f4ad54.css
│       │   ├── chunk-76cea4de.3c7f5ad9.css
│       │   ├── chunk-9d0b7412.61337cac.css
│       │   ├── chunk-d53fc788.15da535a.css
│       │   ├── chunk-elementUI.68c70ad5.css
│       │   └── chunk-libs.417a0e7c.css
│       ├── favicon.ico
│       ├── fonts
│       │   ├── element-icons.535877f5.woff
│       │   ├── element-icons.732389de.ttf
│       │   ├── fontawesome-webfont.674f50d2.eot
│       │   ├── fontawesome-webfont.af7ae505.woff2
│       │   ├── fontawesome-webfont.b06871f2.ttf
│       │   └── fontawesome-webfont.fee66e71.woff
│       ├── img
│       │   ├── 404.a57b6f31.png
│       │   ├── 404_cloud.0f4bc32b.png
│       │   └── fontawesome-webfont.912ec66d.svg
│       ├── index.html
│       └── js
│           ├── app.0535d10d.js
│           ├── chunk-1dd67c7e.9e2b092a.js
│           ├── chunk-36db224a.551d2de1.js
│           ├── chunk-40b58352.ba6cc64e.js
│           ├── chunk-41a04990.aa0987f6.js
│           ├── chunk-4ba7a1a6.174db71a.js
│           ├── chunk-552cb800.1cc7d77e.js
│           ├── chunk-6b9eb7a4.d0229c05.js
│           ├── chunk-76cea4de.2ad6beee.js
│           ├── chunk-9d0b7412.804c049c.js
│           ├── chunk-d53fc788.5eb90fb8.js
│           ├── chunk-elementUI.6b366487.js
│           └── chunk-libs.dad75063.js
├── windows_install_package.bat windows一键安装脚本
└── windows_run_wcplusPro.bat windows一键运行脚本