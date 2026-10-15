# 华为商城与京东动态性能用例

按 `动态性能模型测试用例7.xlsx` 的「新-7.0.2模型测试步骤」实现，逐步沿用 `aw_new.SeaOfStarsAW` 的 Perfetto 和截图采集。

| 用例 | Excel 行 | 步骤数 |
| --- | --- | --- |
| PerformanceDynamic_hwvmall_0010 | 818–831 | 14 |
| PerformanceDynamic_hwvmall_0020 | 832–846 | 15 |
| PerformanceDynamic_jingdong_0010 | 847–858 | 12 |
| PerformanceDynamic_jingdong_0020 | 859–881 | 23 |
| PerformanceDynamic_jingdong_0030 | 882–913 | 32 |
| PerformanceDynamic_jingdong_0040 | 914–928 | 15 |

2026-10-14 在设备 `cff0cbff`（M154FF，主屏 1208×2624）核对，应用版本为华为商城 1.26.8.301、京东 16.1.0。weditor 的 Connect 报 `Unsupported deviceId`，Dump Hierarchy 可用；结合 uiautomator2 控件树与截图确认入口。

## 定位和版本适配

优先使用文字、描述、resource-id 和当前控件 bounds。常规点击、滑动和返回明确指定主屏 `display 0`，点击维持 250ms，避免本机过滤过短触摸。京东 Taro 结算按钮使用框架已有的 uiautomator2 200ms 短按，并限定购物车 Activity 或根节点。华为商城首页搜索框、轮播图、京东无文字控件的 Taro 订单页、购物车结算按钮，以及有明确根节点但无按钮文字的加购规格弹窗，使用实机截图确认的屏幕比例，每次按实时宽高计算坐标。

华为商城分类页无可定位商品卡片时，以搜索 `p60` 进入商品详情。京东分类入口使用新版首页右上角入口；电脑分类不暴露文字时，以搜索 `电脑` 替代。粮油频道不能进入时，以搜索 `食用油` 替代。京东评价页兼容「大家评」「买家评价」；我的页面的「全部」是全部订单入口。

AI 直播间没有输入框、外卖小程序没有可定位加购按钮、空购物车没有结算入口、当前地区秒送搜索不到药店等情况，记为 `SKIP`，并跳过相应依赖步骤。秒送弹出「非常火爆，请稍后再试」时先关闭；若外卖页反复出现该提示，也记录为 `SKIP`。药店搜索为空时，不把下方推荐餐厅当成药店。真实导航失败、应用切到非目标前台、安全验证以及 trace 导出失败会报错，不作为功能缺失吞掉。

购买流程只打开商品规格或订单确认页，不点击支付或提交订单。若版本直接打开订单确认页，则跳过独立的「确认」步骤。新建地址只打开编辑页，不填写或保存。清空外卖购物袋只允许在能确认原本为空且本用例加购成功时执行。

## 运行和结果

6 个用例已被 `main.py` 导入。当前工程 `case_list` 仍为原来的 `PerformanceDynamic_fuzai`；运行这组用例时，可将列表设置为：

```python
case_list = [
    PerformanceDynamic_hwvmall_0010,
    PerformanceDynamic_hwvmall_0020,
    PerformanceDynamic_jingdong_0010,
    PerformanceDynamic_jingdong_0020,
    PerformanceDynamic_jingdong_0030,
    PerformanceDynamic_jingdong_0040,
]
```

`run_case()` 会在尚未准备时调用 `set_up()`。正式用例保留 Excel 的滑动次数，每次滑动后停留 2 秒，普通操作后停留 2 秒，启动后停留 3 秒。运行前按工程原有方式准备性能采集环境、登录账号并处理验证。

每个用例结果目录内包含 `shopping_steps.json`，记录步骤编号、名称、`PASS / SKIP / FAIL` 和原因。跳过或失败步骤的 trace、截图名称分别带 `_SKIP` 或 `_FAIL`，可与正常性能结果区分。结束后保留应用后台。

本次实机核对使用缩短的导航测试，不采集正式性能数据，也不发布直播评论；完整性能采集需通过工程正常入口运行。
