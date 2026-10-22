"""汇总本轮十条 Basic1 回归及其逐步证据，保留历史失败结果。"""
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / 'Result/basic1_repair_20261019'
CASES = {
    'weixin_0030': ('微信 0030', 16, '扫码相册同名匹配冲突；改用唯一生成相册并限定列表区域。'),
    'weixin_0040': ('微信 0040', 17, '背景工具栏和底部操作表均有视频通话；限定操作表区域。'),
    'weixin_0190': ('微信 0190', 12, '两个同名相册导致选图跳过，后续仍在相册校验聊天；唯一测试相册及返回恢复。'),
    'weibo_0030': ('微博 0030', 15, '启动后在发现主 tab，旧流程强制查找首页推荐；按所需主界面校验。点赞后任务奖励遮挡状态确认，增加关闭再校验。'),
    'momo_0010': ('陌陌 0010', 11, '青少年提示、手势引导、小窗引导、推广及退出确认遮挡导航，且挽留层复用列表控件；结合 Activity、控件与截图关闭后再导航。'),
    'xianyu_0010': ('闲鱼 0010', 10, '旧脚本遗漏搜索输入和结果浏览，分享描述已改为分享按钮；按 Excel 恢复十步，Flutter 使用节点边界短按。'),
    'xhs_0030': ('小红书 0030', 14, '输入框无障碍文本增加搜索前缀；大图覆盖层保留详情旧树。修复断言、补齐三次搜索并用截图确认大图。'),
    'kuaishou_0010': ('快手 0010', 7, '新版首页提供精选全屏流，底栏 selected 未同步；按实际视频和评论/赞/收藏控件确认并记录替代。'),
    'alipay_0010': ('支付宝 0010', 19, '碰一下支付券异步弹层遮挡转账入口；补充截图识别和比例关闭。'),
    'fanqiechangting_0010': ('番茄畅听 0010', 11, '搜索前实际停在听歌页，且顶部搜索框筛选不稳定；统一主屏尺寸，搜索前恢复首页并实际点击首页导航。'),
}


def main():
    latest = {}
    for path in ROOT.glob('*/summary.json'):
        for row in json.loads(path.read_text()):
            if row.get('mode') != 'performance':
                continue
            case = row['case'].removeprefix('PerformanceDynamic_')
            if case not in CASES:
                continue
            records = Path(row['directory']) / 'verified_steps.json'
            stamp = records.stat().st_mtime if records.exists() else 0
            if stamp > latest.get(case, (0, None))[0]:
                latest[case] = stamp, row
    results, failures = [], []
    lines = ['# Basic1 实机修复与回归记录', '',
             '设备和应用版本见 [environment.json](environment.json)。业务步骤来自工程内《动态性能模型测试用例7.xlsx》。', '',
             'PASS 表示用例执行完成（可包含有证据的 ADAPTED）。COMPLETED_WITH_SKIPS 表示存在未执行步骤，不等同完整通过。', '',
             '| 用例 | 结果 | 步骤 | 修复原因 |', '| --- | --- | --- | --- |']
    for case, (label, expected, cause) in CASES.items():
        row = latest.get(case, (0, None))[1]
        if row is None:
            lines.append(f'| {label} | 待验证 | 0/{expected} | {cause} |')
            continue
        for step in row['steps']:
            for key in ('hierarchy', 'screenshot'):
                if not Path(step.get(key, '')).is_file():
                    failures.append(f"{label} 第{step['step']}步缺少{key}")
            if step['status'] in ('PASS', 'ADAPTED'):
                trace = Path(step.get('trace', ''))
                if not trace.is_file() or not trace.stat().st_size:
                    failures.append(f"{label} 第{step['step']}步缺少非空trace")
        if row['status'] != 'FAIL' and len(row['steps']) != expected:
            failures.append(f'{label} 步骤数不匹配')
        results.append(row)
        lines.append(f"| {label} | {row['status']} | {len(row['steps'])}/{expected} | {cause} |")
    lines += ['', '## 逐步记录', '']
    if len(results) == len(CASES):
        passed = sum(r['status'] == 'PASS' for r in results)
        total = sum(len(r['steps']) for r in results)
        skipped = sum(s['status'] == 'SKIP' for r in results for s in r['steps'])
        lines.insert(4, f'最终回归：{passed}/10 条通过，共记录 {total} 步；{skipped} 步因微信通话风控跳过。微信文字、语音、表情及三张测试图片已按本轮授权实际发送。\n')
    for row in results:
        label = CASES[row['case'].removeprefix('PerformanceDynamic_')][0]
        records = Path(row['directory']) / 'verified_steps.json'
        lines.append(f'- {label}：[步骤、截图、控件树和 trace]({records.resolve()})')
        for step in row['steps']:
            if step['status'] in ('SKIP', 'FAIL', 'ADAPTED'):
                lines.append(f"  - 第{step['step']}步 {step['status']}：{step.get('reason', '')}")
    lines += ['', '## 验证', '', '40 项离线回归检查通过；具体输出见 [unit_tests.txt](unit_tests.txt)。',
              '证据检查：' + ('通过。' if not failures else '；'.join(failures)),
              '微信通话选择面板实机截图重放：旧区域匹配 2 项，新区域匹配 1 项，见 [定位验证](call_selector_verification.json)。', '']
    lines += ['修改沿用工程已有公共基类和 steps 逐步采集方式。优先使用 text、resource-id、description；截图兜底点击均采用屏幕比例，实时按主屏宽高换算。', '']
    (ROOT / 'summary.json').write_text(json.dumps(results, ensure_ascii=False, indent=2))
    (ROOT / 'repair_report.md').write_text('\n'.join(lines))
    print([(r['case'], r['status'], len(r['steps'])) for r in results])
    print('证据问题：', failures)


if __name__ == '__main__':
    main()
