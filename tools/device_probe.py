"""保存当前主屏控件树和截图，输出有语义的可见节点供实机定位。"""
import argparse
from pathlib import Path
import sys
import time
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from aw_new import SeaOfStarsAW
from Cases.Top48.main_display import MainDisplayMixin


def capture(label, package=None, folder='Result/repair_20261019/probes'):
    d = SeaOfStarsAW.ut_device
    if package:
        activity = d.shell(['cmd', 'package', 'resolve-activity', '--brief',
                            '-a', 'android.intent.action.MAIN',
                            '-c', 'android.intent.category.LAUNCHER', package]).output
        component = next(x.strip() for x in activity.splitlines() if x.startswith(package+'/'))
        print(d.shell(['am', 'start', '-W', '--display', '0', '-n', component]).output)
        time.sleep(3)
    root = Path(folder)
    root.mkdir(parents=True, exist_ok=True)
    xml = d.dump_hierarchy()
    (root / (label+'.xml')).write_text(xml, encoding='utf-8')
    d.screenshot(str(root / (label+'.png')))
    context = type('Context', (), {'d': d})()
    print(MainDisplayMixin.current_app(context))
    for n in ET.fromstring(xml).iter('node'):
        if n.get('display-id', '0') != '0' or n.get('visible-to-user') == 'false':
            continue
        if n.get('text') or n.get('content-desc') or n.get('class') == 'android.widget.EditText':
            print({k:n.get(k) for k in ('text','content-desc','resource-id','bounds','selected','class')})


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('label')
    parser.add_argument('--package')
    args = parser.parse_args()
    capture(args.label, args.package)
