# wallhaven_tools
功能：实现从wallhaven网站将别人的收藏夹的美图、自己搜索的，一键增加到自己的收藏夹、图片搜索、下载等、

使用说明：
0、请先修改config.test.ini文件，配置好自己的各种隐私数据

1、直接去https://wallhaven.cc/settings/account 生成一个API

2、然后放到config.ini即可，手动将config.test.ini改成config.ini即可

3、把token和cookie放到config.ini文件中去

4、想运行什么功能，直接运行对应的py文件即可，添加到自己的收藏和下载时请自己选择好存图片url的文件

5、添加到自己的收藏夹默认需要把收藏夹id放到config.ini的coll中

6、已经在自己其他收藏夹内的图片不会添加到新的收藏夹内去

7、下载图片时忽略报错,搜索图片可以自己设置观看等级，解释：三个1分别代表了SFW、Sketchy、NSFW，如001将会查找不宜展示的图片

8、注意在每个request添加了proxy

9、不考虑性能优化，毕竟这个网站这么好，不要搞别人

