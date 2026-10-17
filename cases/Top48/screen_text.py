"""Canvas 页面文字定位：macOS 本地 Vision OCR，也支持外部命令。"""
import hashlib
import json
import os
from pathlib import Path
import platform
import shlex
import subprocess
import tempfile


SOURCE = r'''
import Foundation
import Vision
let request = VNRecognizeTextRequest()
request.recognitionLevel = .accurate
request.recognitionLanguages = ["zh-Hans", "en-US"]
request.usesLanguageCorrection = false
try VNImageRequestHandler(url: URL(fileURLWithPath: CommandLine.arguments[1])).perform([request])
let rows = (request.results ?? []).compactMap { item -> [String: Any]? in
    guard let candidate = item.topCandidates(1).first else { return nil }
    let box = item.boundingBox
    return ["text": candidate.string, "x": box.minX, "y": 1-box.maxY,
            "w": box.width, "h": box.height]
}
let json = try JSONSerialization.data(withJSONObject: rows)
print(String(data: json, encoding: .utf8)!)
'''


class ScreenshotText:
    def __init__(self):
        command = os.environ.get('ANDROID_OCR_COMMAND')
        self.command = shlex.split(command) if command else None
        if not self.command and platform.system() == 'Darwin':
            digest = hashlib.sha256(SOURCE.encode()).hexdigest()[:12]
            binary = Path(tempfile.gettempdir()) / ('seaofstars-screen-text-' + digest)
            if not binary.exists():
                with tempfile.TemporaryDirectory(prefix='screen-text-source-') as directory:
                    source = Path(directory) / 'main.swift'
                    source.write_text(SOURCE)
                    subprocess.run(['/usr/bin/swiftc', str(source), '-o', str(binary)],
                                   check=True, capture_output=True, timeout=120)
            self.command = [str(binary)]

    def read(self, device):
        if not self.command:
            raise RuntimeError('当前页面需要截图文字定位，请配置 ANDROID_OCR_COMMAND')
        with tempfile.TemporaryDirectory(prefix='screen-text-') as directory:
            path = str(Path(directory) / 'screen.png')
            device.screenshot(path)
            result = subprocess.run(self.command + [path], check=True,
                                    capture_output=True, text=True, timeout=30)
            return json.loads(result.stdout)
