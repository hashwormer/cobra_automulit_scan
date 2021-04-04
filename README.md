# cobra_automulit_scan

### 功能说明

cobra_automulit_scan 是利用开源白盒代码扫描工具cobra 的api接口，结合git的api接口实现批量代码仓库的自动化扫描的脚本。
因为cobra的报告内容查看仅能通过sid一个project 一个project的去查看，不太适合对git仓库中的海量项目进行扫描。我们通过git的api接口先查出全部git仓库中的项目地址
如 https://git.com/xxxxx.git ,然后再通过cobra的api接口逐条添加到cobra的扫描任务中。然后通过每3s请求cobra查询扫描状态的接口确认扫描是否完成，当扫描完成时会再查询扫描结果是否为0。
如果扫描结果为0则添加下一个project地址进行扫描，如果扫描结果不为0则记录下此条扫描任务的sid，再添加下一个任务。
最后我们查看所有扫描任务记录下的sid，即可逐一通过cobra的报告地址进行查看 ，如：http://127.0.0.1:8888/?sid=xxxxxx
