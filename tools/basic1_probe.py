"""Basic1 修复现场记录；不改变业务数据。"""
import argparse
import importlib
from pathlib import Path
import sys
import time
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from aw_new import SeaOfStarsAW

ROOT = Path('Result/basic1_repair_20261019')


def snapshot(label):
    d = SeaOfStarsAW.ut_device
    folder = ROOT / 'probes'
    folder.mkdir(parents=True, exist_ok=True)
    xml = d.dump_hierarchy()
    (folder / (label + '.xml')).write_text(xml, encoding='utf-8')
    d.screenshot(str(folder / (label + '.png')), display_id=0)
    print('SNAPSHOT', label, flush=True)
    for n in ET.fromstring(xml).iter('node'):
        if n.get('display-id', '0') != '0' or n.get('visible-to-user') == 'false':
            continue
        if n.get('text') or n.get('content-desc') or n.get('class') == 'android.widget.EditText':
            print({k: n.get(k) for k in ('text', 'content-desc', 'resource-id', 'bounds', 'selected', 'class')})


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('label')
    p.add_argument('--case')
    p.add_argument('--actions', nargs='*', default=[])
    args = p.parse_args()
    ROOT.mkdir(parents=True, exist_ok=True)
    if args.case:
        name = 'PerformanceDynamic_' + args.case
        case = getattr(importlib.import_module('Cases.Top48.' + name), name)(str(ROOT))
        case.set_up()
        try:
            for action in args.actions:
                print('ACTION', action, flush=True)
                getattr(case, action)()
                time.sleep(1)
        finally:
            snapshot(args.label)
            if hasattr(case, 'restore_ime'):
                case.restore_ime()
            case.clean_up()
    else:
        snapshot(args.label)
