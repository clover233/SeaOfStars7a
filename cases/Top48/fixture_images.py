"""采集前准备专用纯色图片，避免自动化选取相册中的个人照片。"""
from pathlib import Path
import struct
import tempfile
import zlib


def prepare_images(device, album, count=5):
    remote = '/sdcard/Pictures/' + album
    device.shell(['mkdir', '-p', remote])

    def chunk(kind, data):
        return (struct.pack('!I', len(data)) + kind + data
                + struct.pack('!I', zlib.crc32(kind + data)))

    with tempfile.TemporaryDirectory(prefix='performance-images-') as folder:
        for index in range(count):
            destination = remote + '/SeaOfStars_{:02d}.png'.format(index + 1)
            if device.shell(['test', '-f', destination]).exit_code == 0:
                continue
            rgb = (40 + index * 35, 180 - index * 20, 70 + index * 25)
            raw = b''.join(b'\x00' + bytes(rgb) * 320 for _ in range(320))
            png = (b'\x89PNG\r\n\x1a\n'
                   + chunk(b'IHDR', struct.pack('!2I5B', 320, 320, 8, 2, 0, 0, 0))
                   + chunk(b'IDAT', zlib.compress(raw)) + chunk(b'IEND', b''))
            local = Path(folder) / Path(destination).name
            local.write_bytes(png)
            device.push(str(local), destination)
            device.shell(['am', 'broadcast', '-a', 'android.intent.action.MEDIA_SCANNER_SCAN_FILE',
                          '-d', 'file://' + destination])
