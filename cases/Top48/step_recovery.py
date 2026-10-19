"""指定用例的分支跳过，以及始终执行的“应用主页 → 桌面”收尾。"""
import json
import logging
from pathlib import Path
import time

from aw_new import SeaOfStarsAW


def run_recoverable_case(case):
    # 启用此执行器的用例必须以返回应用主页、返回桌面两个步骤结束。
    steps = list(case.steps())
    records = []
    errors = []

    def save():
        (Path(case.result_dir_path) / 'step_results.json').write_text(
            json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')

    def execute(run, number, step, action=None, cleanup=False):
        name, original, stay = step
        row = dict(run=run, step=number, name=name, status='PASS')
        case._adaptations = []
        case._locators = set()
        started = False
        logging.info('%s、%s', number, name)
        try:
            # 收尾不依赖采集服务可用，采集异常也必须执行导航。
            try:
                SeaOfStarsAW.start_perfetto_trace()
                started = True
            except Exception as error:
                if not cleanup:
                    raise
                row.update(status='FAIL', reason='trace 启动失败：' + str(error))
                errors.append(row['reason'])
            try:
                (action or original)()
                time.sleep(stay)
            except Exception as error:
                if cleanup:
                    raise
                row.update(status='SKIP', reason=str(error))
                logging.warning('SKIP %s：%s', name, error, exc_info=True)
                return False
            if case._adaptations and row['status'] == 'PASS':
                row.update(status='ADAPTED', reason='；'.join(case._adaptations))
            return True
        except Exception as error:
            row.update(status='FAIL', reason=str(error))
            raise
        finally:
            row['locators'] = sorted(case._locators)
            records.append(row)
            if started:
                try:
                    SeaOfStarsAW.stop_and_get_perfetto_trace(
                        case.trace_dir_path, case.__class__.__name__,
                        'step_{}、{}_{}'.format(number, name, row['status']), '', case.screenshot_dir_path)
                    row['trace_exported'] = True
                except Exception as error:
                    row.update(status='FAIL', trace_exported=False, trace_error=str(error))
                    errors.append('trace 导出失败：' + str(error))
                    logging.exception('trace 导出失败')
            save()

    def main_page():
        last_error = None
        for attempt in range(2):
            try:
                if attempt or case.current_app()['package'] != case.PACKAGE:
                    case.start()
                invalidate = getattr(case, 'invalidate', None)
                if invalidate:
                    invalidate()
                steps[-2][1]()
                case.foreground()
                return
            except Exception as error:
                last_error = error
                logging.warning('返回应用主页第 %s 次失败：%s', attempt + 1, error)
        raise RuntimeError('返回应用主页失败：{}'.format(last_error))

    def home():
        try:
            if 'launcher' in case.current_app()['activity'].lower():
                return
            steps[-1][1]()
        except Exception:
            logging.exception('Home 手势失败，使用 Home 键兜底')
            case.d.press('home')
        case.wait_for(lambda: 'launcher' in case.current_app()['activity'].lower(),
                      '收尾未返回 Home 页', timeout=10)

    for run in range(1, case.TEST_TIME + 1):
        try:
            if not getattr(case, '_prepared', False):
                case.set_up()
            blocked = None
            for number, step in enumerate(steps[:-2], 1):
                name, action, _ = step
                checkpoint = getattr(action, '__name__', '') in case.RECOVERY_CHECKPOINTS
                if blocked and not checkpoint:
                    records.append(dict(run=run, step=number, name=name, status='SKIP',
                                        reason='前置步骤不可用：' + blocked, trace_exported=False))
                    save()
                    continue
                if execute(run, number, step):
                    blocked = None
                else:
                    blocked = name
        finally:
            # 不论业务、准备或采集哪里失败，严格按顺序尝试两项收尾。
            for number, step, action in ((len(steps)-1, steps[-2], main_page),
                                         (len(steps), steps[-1], home)):
                try:
                    execute(run, number, step, action=action, cleanup=True)
                except Exception as error:
                    errors.append('{}：{}'.format(step[0], error))
                    logging.exception('收尾步骤失败：%s', step[0])
    if errors:
        raise RuntimeError('；'.join(errors))
