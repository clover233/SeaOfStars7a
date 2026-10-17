# SeaOfStars



> 我的uiautomator2现在已经启动了。我现在已经运行起来了自动化用例，帮我写一下
>
> 
>
> 这几个用例。
>
> 步骤有之前写的，如果不符合要求就删掉重新。尽量让weditor定位去写（weditor已经打开），但是如果用weditor的坐标定位，分辨率差异会比较大，工程点击尽量不要用绝对坐标值，最好是按比例换算出来的值。
>
> 具体步骤可以在动态性能模型测试用例7.xlsx中查到，另外可以仿照之前的代码来。
>
> 如果有需要开启的权限（如定位、扫码等）帮我开启一下。



## 第 2–6 页 App Android 包名

Excel表中黄色为需要注意的地方。

以下 Android 包名于 2026-10-12 通过 ADB 在当前连接的小米 M154FF（Android 17）上核实，81 个应用均已安装。保留原第 2–6 页的分组、顺序与 App 名称，包名大小写以实机为准。

- 系统应用按本机对应功能填写：钱包为小米钱包，备忘录对应「笔记」，照片对应「相册」，信息对应「短信」；电话桌面入口属于「通讯录与拨号」（`com.android.contacts`）。这些包名可能随手机品牌或系统版本变化。
- 掼蛋、途游斗地主（比赛版）、多乐够级使用本机已安装的小米渠道版包名。
- WPS Office 对应 `cn.wps.moffice_eng`；本机另装有「小米文档查看器（WPS定制）」`cn.wps.moffice_eng.xiaomi.lite`，表中使用 WPS Office 的包名。

### 第 2 页（16 个）

| App | Android 包名 |
| --- | --- |
| 天天象棋 | `com.tencent.qqgame.xq` |
| 掼蛋 | `com.guandan.mi` |
| 途游斗地主（比赛版） | `com.tuyoo.doudizhu.android3d.mi` |
| 多乐够级 | `com.k7k7.goujihd.mi` |
| 钱包 | `com.mipay.wallet` |
| 起点读书 | `com.qidian.QDReader` |
| 央广网 | `news.cnr.cn` |
| 酷狗音乐 | `com.kugou.android` |
| 新浪新闻 | `com.sina.news` |
| 天天爱消除 | `com.tencent.peng` |
| 凤凰新闻 | `com.ifeng.news2` |
| 搜狐新闻 | `com.sohu.newsclient` |
| 蜻蜓FM | `fm.qingting.qtradio` |
| 懒人听书 | `bubei.tingshu` |
| YY | `com.duowan.mobile` |
| 地铁跑酷 | `com.kiloo.subwaysurf` |

### 第 3 页（20 个）

| App | Android 包名 |
| --- | --- |
| 支付宝 | `com.eg.android.AlipayGphone` |
| 高德地图 | `com.autonavi.minimap` |
| 百度 | `com.baidu.searchbox` |
| 百度地图 | `com.baidu.BaiduMap` |
| 备忘录 | `com.miui.notes` |
| 哔哩哔哩 | `tv.danmaku.bili` |
| 电话 | `com.android.contacts` |
| 相机 | `com.android.camera` |
| 云闪付 | `com.unionpay` |
| 网易云音乐 | `com.netease.cloudmusic` |
| 大众点评 | `com.dianping.v1` |
| DeepSeek | `com.deepseek.chat` |
| 抖音极速版 | `com.ss.android.ugc.aweme.lite` |
| 蛋仔派对 | `com.netease.party` |
| 米家 | `com.xiaomi.smarthome` |
| MOMO陌陌 | `com.immomo.momo` |
| TapTap | `com.taptap` |
| 元宝 | `com.tencent.hunyuan.app.chat` |
| 滴滴 | `com.sdu.didi.psnger` |
| 钉钉 | `com.alibaba.android.rimet` |

### 第 4 页（20 个）

| App | Android 包名 |
| --- | --- |
| 懂车帝 | `com.ss.android.auto` |
| 豆包 | `com.larus.nova` |
| 抖音 | `com.ss.android.ugc.aweme` |
| 番茄小说 | `com.dragon.read` |
| 番茄畅听 | `com.xs.fm` |
| 开心消消乐 | `com.happyelements.AndroidAnimal` |
| 和平精英 | `com.tencent.tmgp.pubgmhd` |
| 红果短剧 | `com.phoenix.read` |
| 华为运动健康 | `com.huawei.health` |
| 华为商城 | `com.vmall.client` |
| 京东 | `com.jingdong.app.mall` |
| 今日头条 | `com.ss.android.article.news` |
| 快手 | `com.smile.gifmaker` |
| 美团 | `com.sankuai.meituan` |
| 美图秀秀 | `com.mt.mtxx.mtxx` |
| 信息 | `com.android.mms` |
| 照片 | `com.miui.gallery` |
| 拼多多 | `com.xunmeng.pinduoduo` |
| 千问 | `com.aliyun.tongyi` |
| 七猫小说 | `com.kmxs.reader` |

### 第 5 页（20 个）

| App | Android 包名 |
| --- | --- |
| 爱奇艺 | `com.qiyi.video` |
| QQ | `com.tencent.mobileqq` |
| QQ浏览器 | `com.tencent.mtt` |
| QQ音乐 | `com.tencent.qqmusic` |
| 去哪儿旅行 | `com.Qunar` |
| 设置 | `com.android.settings` |
| 汽水音乐 | `com.luna.music` |
| 淘宝 | `com.taobao.taobao` |
| 腾讯新闻 | `com.tencent.news` |
| 腾讯视频 | `com.tencent.qqlive` |
| 同花顺 | `com.hexin.plat.android` |
| 铁路12306 | `com.MobileTicket` |
| UC浏览器 | `com.UCMobile` |
| 王者荣耀 | `com.tencent.tmgp.sgame` |
| 天气 | `com.miui.weather2` |
| 微博 | `com.sina.weibo` |
| 唯品会 | `com.achievo.vipshop` |
| 微信 | `com.tencent.mm` |
| WPS Office | `cn.wps.moffice_eng` |
| 小红书 | `com.xingin.xhs` |

### 第 6 页（5 个）

| App | Android 包名 |
| --- | --- |
| 闲鱼 | `com.taobao.idlefish` |
| 携程旅行 | `ctrip.android.view` |
| 优酷 | `com.youku.phone` |
| 知乎 | `com.zhihu.android` |
| 作业帮 | `com.baidu.homework` |


## Basic1 支付宝与高德地图

Basic1 涉及支付宝 `0010、0020`，高德 `0060、0070、0080`。这两组公共操作使用主显示屏（display 0）的焦点和 resumed activity 判断前台；页面切换时短暂缺失焦点会继续等待，实际离开目标应用仍会报错。

- 高德 `0070` 建立导航并留在后台，`0080` 接续退出。两者之间保留高德后台；单独运行 `0080` 时需要先运行 `0070`。`0060` 自行建立导航并在小红书、抖音切换后恢复退出。
- 导航用例在采集前开启前台/后台定位和录音权限；首次“驾车导航使用提示”按用户已确认的授权处理。可关闭的一键登录引导只返回关闭，不进行登录。
- 支付宝 `0010` 还会准备扫码、相册、定位及附近设备权限；`0020` 继续使用 `ALIPAY_TEST_CONTACT` 和 `ALIPAY_TEST_PHOTOS` 指定测试联系人及五张素材，发送前核实收件人。
- 支付宝 Canvas 控件优先读取可访问节点；缺少节点时按本地截图文字定位，再使用已核实的比例坐标。macOS 使用系统 Vision，Swift OCR 程序在环境准备阶段编译并缓存。其他系统需配置 `ANDROID_OCR_COMMAND`：命令接收截图路径，向标准输出返回 JSON 数组，元素包含 `text` 和归一化的 `x/y/w/h`。稳健理财活动遮罩需截图核实，无法识别时明确报错。

主屏识别回归测试：`.venv/bin/python -m unittest discover -s tests -v`。
