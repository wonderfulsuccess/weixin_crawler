Github主页 | [官网](https://www.wcplus.cn/?s=weixin_crawler) | [4K视频介绍](https://www.youtube.com/watch?v=mPALu1LZk3s) | [源代码结构](struct.md) 

![1](./img/wcplusPro7.5.svg) ![2](./img/build.svg) ![3](./img/Python.svg) ![4](./img/vue.svg) ![5](./img/tornado6.1.svg) <a href="http://www.wcplus.cn/?s=weixin_crawler">![6](./img/website.svg)</a>

<br>
<div align="center" style="margin: 100px 0px">
<img src="http://cdn2.wcplus.cn/wcplusProLogo.png"/>
</div>
<br>

![7](./img/7507.png)


weixin_crawler 已于2019年更名为 wcplusPro，不再免费提供源代码。更名之前的最新的源代码（最后更新于2019年3月），仍然开源，位于项目的 weixin_crawler/ 路径下，可能已经无法直接运行，仅供学习之用，使用方法见[文档](http://www.wcplus.cn/weixin_crawler?s=weixin_crawler)。本文仅介绍 wcplusPro 的技术和功能特性。

wcplusPro 提供了：
- 稳定的公众号数据采集服务
- 面向公众号的分析报告
- 公众号全文检索

你可以按照使用时长购买订阅版，也可以直接购买源代码。订阅版采集一个公众号的全部历史数据成本不到 10 块钱，更多内容请访问：

- [官网](https://www.wcplus.cn/?s=weixin_crawler)
- [详细功能介绍](https://www.wcplus.cn/intro?s=weixin_crawler)
- [产品形式](https://www.wcplus.cn/product?s=weixin_crawler)
- [在线演示](https://www.wcplus.cn/demo?s=weixin_crawler)
- [视频演示](https://www.youtube.com/watch?v=mPALu1LZk3s)

### 功能特性

1. 采集任意公众号的全部历史文章数据，这些数据包括：
   - 公众号的名称
   - 标题、封面链接、作者、摘要、发布时间（精确到秒）、版权标志、发文IP属地
   - 文章位置（头条、次1条等）
   - 永久文章链接
   - 图文内容（包括文章开头的原创标识和文末的原文链接，用户可进一步提取图文中的文字和图片）
   - 阅读数量、点赞数量、在看数量、评论数量、打赏数量 在内的数据。
2. 提供面向公众号的分析报告 
   - 阅读数据全景图，包括阅读量、点赞量、阅读量、赞赏量、在看量、评论量
   - 全部历史文章列表，可以筛选、排序
   - 数据报告卡片：文章数据报告卡片、时间数据报告卡片、影响力数据报告卡片、发文IP属地数据报告卡片
   - 发文周历统计报告
3. 公众号全文检索
   - 所有已经采集公众号的标题、作者、摘要全文检索
   - 单个公众号的标题、作者、摘要、正文全文检索

详细功能介绍请查看[官网文档](https://www.wcplus.cn/?s=weixin_crawler)

<img style="margin:0px auto;display:block;border:1px green solid;border-radius:5px;color:green;font-size:16px;" src="http://cdn2.wcplus.cn/7509.gif">

### 技术特性

- 自带安装脚本、运行脚本，点击鼠标就能完成所有的安装和运行工作，零技术要求。
- 提供详细在线使用文档、QA手册。
- 前后端分离，使用 socketio 做前后端实时通信

#### 前端
  
- 前端框架 vue2，打包 webpack
- 图表 ECharts
- 部分 UI 组件 Element
- http 请求 axios
- 图标 Font Awesome

#### 后端

- 经典 MVC 架构
- 纯 Python 编写，支持 Python3.7 及其更高版本
- web 框架 tornado
- 异步网络请求 tornado
- 数据库 sqlite
- 爬虫加速 Python 协程
- 前后端实时通信 socketio

### 申请试用
试用版，足够完成对1个公众号，全部历史文章的采集。无论是几十篇文，还是数万篇文章
[wcplusPro试用版 申请方法](https://www.wcplus.cn/intro/a/2.html)


### 联系购买

邮箱: <a href = "mailto:wonderfulsuccess@163.com">wonderfulsuccess@163.com</a> 点击邮箱地址可直接发送邮件

微信: wonderfulcorporation，也可以通过扫码添加客服（请备注 wcplusPro）

<div align="center" style="border:1px green solid; border-radius: 5px; color:green;">
<img style="margin:0px auto; display: block; width: 150px" src="http://cdn2.wcplus.cn/7515.jpg" >
</div>