"""按旧日志重跑失败用例，逐步保存主屏截图、控件树、状态和可选 Perfetto。

示例：.venv/bin/python tools/rerun_failed.py --log Result/20261019_153938/all_log.txt
--no-trace 用于定位调试，不代表已经完成性能采集。
"""
import argparse
from datetime import datetime
import importlib
import json
import logging
import os
from pathlib import Path
import re
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from aw_new import SeaOfStarsAW


class ValidationSkipped(Exception):
    pass


def main_display_home(case):
    # 准备/收尾不依赖 UIAutomator 的短暂 HTTP 会话，并明确操作主显示屏。
    result = case.d.shell('input -d 0 keyevent 3')
    if result.exit_code:
        raise RuntimeError('返回主屏桌面失败：' + result.output)


def evidence(case, number):
    folder = Path(case.result_dir_path)/'Evidence'
    folder.mkdir(exist_ok=True)
    xml, shot = folder/f'{number:02d}.xml', folder/f'{number:02d}.png'
    xml.write_text(case.d.dump_hierarchy(), encoding='utf-8')
    case.d.screenshot(str(shot), display_id=0)
    return {'hierarchy': str(xml), 'screenshot': str(shot), 'foreground': case.current_app()}


def run_one(name, output, trace, allow_weixin_send=False):
    cls = getattr(importlib.import_module('Cases.Top48.'+name), name)
    case = cls(str(output))
    records = []
    summary = {'case': name, 'mode': 'performance' if trace else 'ui_validation',
               'directory': case.result_dir_path, 'steps': records}
    # 旧代码中“先前已授权”的注释不是当前用户的授权证据。
    # 默认不实发/拨号；显式参数只授权本轮指定的两条微信测试会话用例。
    external_actions = {'send_text', 'send_voice', 'send_emoji', 'send_image',
                        'send_chat_photos', 'video_call', 'voice_call', 'live_send'}
    failed = False
    blocked_reason = None
    original_ime = case.d.current_ime()
    try:
        main_display_home(case)
        case.set_up()
        # 商城原执行器会初始化分支依赖状态；直接逐步回归也必须保留这一前置。
        case._groups = {}
        steps = list(case.steps())
        numbers = getattr(case, 'STEP_NUMBERS', range(1, len(steps) + 1))
        for number, (label, action, stay) in zip(numbers, steps):
            row = {'step': number, 'name': label, 'status': 'PASS'}
            started = False
            case._adaptations, case._locators = [], set()
            case._adaptation = None
            case._last_skip_reason = None
            old_skips = len(getattr(case, 'skipped_steps', []))
            logging.info('%s %02d %s', name, number, label)
            try:
                if blocked_reason and action.__name__ not in ('home', 'launcher_gesture'):
                    raise ValidationSkipped('账号前置条件未满足：'+blocked_reason)
                sends = (action.__name__ in external_actions or '并发送' in label
                         or label.startswith('发送'))
                authorized = allow_weixin_send and name in (
                    'PerformanceDynamic_weixin_0040', 'PerformanceDynamic_weixin_0190')
                if sends and not authorized:
                    if (action.__name__ == 'send_text' and hasattr(case, 'keyboard_shown')
                            and case.keyboard_shown()):
                        case.back()
                    if action.__name__ in ('video_call', 'voice_call'):
                        if case.visible('取消'):
                            case.choose('取消')
                        case._last_call_warning = '本次定位验证未拨出通话，无需挂断'
                    raise ValidationSkipped('当前定位验证不对外实发消息或拨出通话')
                if trace:
                    SeaOfStarsAW.start_perfetto_trace()
                    started = True
                result = action()
                time.sleep(stay)
                if result is False or len(getattr(case, 'skipped_steps', [])) > old_skips:
                    row.update(status='SKIP', reason='；'.join(getattr(case, 'skipped_steps', [])[old_skips:])
                               or case._last_skip_reason or '该功能返回不可用，未计为通过')
                adaptations = case._adaptations + ([case._adaptation] if case._adaptation else [])
                if adaptations and row['status'] == 'PASS':
                    row.update(status='ADAPTED', reason='；'.join(adaptations))
            except Exception as error:
                if error.__class__.__name__ in (
                        'ValidationSkipped', 'WeixinStepSkipped', 'QQStepSkipped',
                        'MeituanStepSkipped', 'PhotoStepSkipped', 'StepUnavailable', 'AccountBlocked'):
                    row.update(status='SKIP', reason=str(error))
                    if getattr(error, 'blocks_case', False):
                        blocked_reason = str(error)
                else:
                    row.update(status='FAIL', reason=f'{type(error).__name__}: {error}')
                    logging.exception('步骤失败')
                    failed = True
            finally:
                if started:
                    try:
                        SeaOfStarsAW.stop_and_get_perfetto_trace(
                            case.trace_dir_path, name, f"step_{number}_{row['status']}",
                            '-LAST', case.screenshot_dir_path)
                        traces = sorted(Path(case.trace_dir_path).glob('*.trace'), key=lambda p:p.stat().st_mtime)
                        if not traces or traces[-1].stat().st_size == 0:
                            raise RuntimeError('Perfetto 导出为空')
                        row['trace'] = str(traces[-1])
                    except Exception as error:
                        row.update(status='FAIL', trace_error=str(error))
                        failed = True
                try:
                    row.update(evidence(case, number))
                except Exception as error:
                    row.update(status='FAIL', evidence_error=str(error))
                    failed = True
                row['locators'] = sorted(case._locators)
                records.append(row)
                (Path(case.result_dir_path)/'verified_steps.json').write_text(
                    json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')
                logging.info('RESULT %s %02d %s %s', name, number, row['status'], row.get('reason',''))
            if failed:
                break
    except Exception as error:
        summary['error'] = f'{type(error).__name__}: {error}'
        failed = True
        logging.exception('用例准备或收尾失败')
    finally:
        try:
            if getattr(case, '_call_active', False) and hasattr(case, 'hang_up'):
                case.hang_up()
            if getattr(case, '_own_recording', False) and case.has('alert_recording_time_view'):
                case.click('shutter_button')
            if hasattr(case, 'restore_ime'):
                case.restore_ime()
            if original_ime and case.d.current_ime() != original_ime:
                case.d.shell(['ime', 'set', original_ime])
            try:
                case.clean_up()
            finally:
                # 会议清理可能重新拉起应用；清理结束后仍应回到主屏桌面。
                main_display_home(case)
        except Exception as error:
            summary['cleanup_error'] = str(error)
            failed = True
        summary['status'] = 'FAIL' if failed else 'COMPLETED_WITH_SKIPS' if any(
            r['status'] == 'SKIP' for r in records) else 'PASS'
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--log', type=Path, default=ROOT/'Result/20261019_153938/all_log.txt')
    parser.add_argument('--case', action='append', dest='cases')
    parser.add_argument('--output', type=Path)
    parser.add_argument('--no-trace', action='store_true')
    parser.add_argument('--fail-fast', action='store_true', help='某用例失败后停止队列，便于保留现场排查')
    parser.add_argument('--allow-weixin-send', action='store_true',
                        help='仅在用户明确授权后使用：0040/0190 向已核验的置顶测试会话实发和拨号')
    args = parser.parse_args()
    names = args.cases or list(dict.fromkeys(re.findall(
        r'用例失败：(PerformanceDynamic_\w+)', args.log.read_text(encoding='utf-8'))))
    if not names or any(not re.fullmatch(r'PerformanceDynamic_\w+', name) for name in names):
        parser.error('未找到有效的失败用例名称')
    output = (args.output or ROOT/'Result'/('rerun_'+datetime.now().strftime('%Y%m%d_%H%M%S'))).resolve()
    os.chdir(ROOT)
    output.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s',
                        handlers=[logging.StreamHandler(), logging.FileHandler(output/'all_log.txt', encoding='utf-8')])
    results = []
    for name in names:
        result = run_one(name, output, not args.no_trace, args.allow_weixin_send)
        results.append(result)
        (output/'summary.json').write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
        logging.info('CASE_RESULT %s %s', name, result['status'])
        if args.fail_fast and result['status'] == 'FAIL':
            break
    print('结果目录：', output)
    return int(any(r['status'] == 'FAIL' for r in results))


if __name__ == '__main__':
    raise SystemExit(main())
