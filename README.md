# XLWeb Manager

用于管理XLWeb的在线交互式管理工具。  
Online interactive management tool for managing XLWeb.  
同时提供部分XLWeb接口的简单可视化。  
Simple visualisation of parts of the XLWeb interface is also provided.

## 配置安装

参考appsettings.json.demo文件。  
Refer to the appsettings.json.demo file.   
请复制并重命名为appsettings.json。  
Please copy and rename it to appsettings.json.  
然后选择一个你喜欢的部署方式启动app.py。  
Then select a deployment mode to start app.py.

## Management side

利用HTTPBasicAuth进行鉴权。  
Authenticate using HTTPBasicAuth.

### /

XlWeb状态查看、日志查看、开启服务、关闭服务、重启服务。  
View XlWeb status, log, start, stop, restart services.

### /config

XlWeb配置查看、配置修改。  
View XlWeb configuration, modify configuration.

### /flush

刷新CDN缓存、预热CDN。（仅限天翼云CDN）  
Flush CDN cache, preheat CDN. (Only for TianYi Cloud CDN)

### /analytics

打开grafana的监控页面。（功能存在问题，暂不可用）  
Open Grafana's monitoring page. (Function not available)

## User side

无鉴权，可以直接访问。  
No authentication, can be accessed directly.

### /plugin_status

显示插件状态。按照main/testing/all三个标签进行分类。   
Display plugin status. Grouped by main/testing/all.

## RESTAPI

RESTAPI使用headers中的`api-secret`进行鉴权。  
RESTAPI uses the `api-secret` in the headers to authenticate.

### /api/v1/plugin_master_site

[Post] 刷新插件状态json缓存。   
[Post] Refresh plugin status json cache.