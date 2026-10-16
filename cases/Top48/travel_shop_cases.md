# 去哪儿、汽水音乐、淘宝动态性能用例

依据 `动态性能模型测试用例7.xlsx` 第一张表1315～1347、1384～1395、1410～1441行，保留19/14/12/17/15共77个独立步骤。

| 用例 | 场景 | 步数 |
| --- | --- | ---: |
| PerformanceDynamic_qunaer_0010 | 机票查询、明天航班、酒店西安、酒店订单和图片 | 19 |
| PerformanceDynamic_qunaer_0020 | 机票方案、预订填写页、值机选座、火车高铁查询 | 14 |
| PerformanceDynamic_sodamusic_0010 | 搜索国歌、播放15秒后暂停、我喜欢和播放列表 | 12 |
| PerformanceDynamic_taobao_0010 | 清风卫生纸搜索、销量排序、评价、客服、店铺和加购 | 17 |
| PerformanceDynamic_taobao_0020 | 首页频道、关注、逛逛/视频、我的订单 | 15 |

实现集中在 `travel_shop_common.py`，复用现有正式逐步Perfetto采集、截图、结果JSON和输入法恢复。未修改主程序的运行队列。

weditor连接报Unsupported deviceId后已尝试Dump Hierarchy，定位改用uiautomator2控件树与截图OCR交叉核对。优先resource-id、content-desc和文本，点击由运行时控件边界计算；截图补充定位使用窗口比例。手势实时读取窗口尺寸，注入display 0，不写死绝对像素位置。

`PASS`表示动作及对应页面/状态已核验，`ADAPTED`记录当前版本的替代或空态，`SKIP`记录功能、账号、内容或前置不可用；异常为`FAIL`。缺失的前置功能阻止依赖步骤操作，独立步骤继续。

去哪儿仅查询与浏览，不填写乘机人、提交订单或支付。酒店目的地按西安选择；遇登录页保留限制说明。广告按已确认的关闭控件或弹层特征关闭，不领取优惠或进入广告详情。

汽水音乐只读取本应用MediaSession，连续播放15秒后暂停。返回首页不点击底部中央播放按钮。未登录的收藏列表和版本中缺失的播放列表按实际记录跳过。

淘宝0010仅在本次清风商品详情直接进入、并核对客服页面与会话标题后才允许实发。日常批跑默认跳过实发；本次已获用户授权，校验时设置 `TAOBAO_ALLOW_CUSTOMER_MESSAGES=1`。文字严格为“你好”，图片只从本用例创建的 `Pictures/SeaOfStars_Taobao_Test` 专用相册选择；发送不自动重试。加购只操作当前核对的商品，不下单或付款。第三个首页频道及“逛逛”随版本变化按实际入口适配并记录。

无设备保护测试：`tests/test_travel_shop_guards.py`，覆盖客服授权/身份改变、重复发送、前置状态、缺失输入框和播放暂停。

实机证据和执行范围见 `Result/qunar_soda_taobao_validation/验证说明.md`。
