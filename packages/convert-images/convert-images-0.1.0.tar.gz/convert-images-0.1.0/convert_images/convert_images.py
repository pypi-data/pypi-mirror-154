#!/usr/bin/env python
# coding: utf-8

import argparse
import sys
from pathlib import Path

from PIL import Image
from loguru import logger


class DegradingError(Exception):
    pass


class Convert:

    def __init__(self, overwrite=False):
        self.overwrite = overwrite

    @staticmethod
    def size(file):
        return round(Path(file).stat().st_size / 1000, 2)

    def to_jpeg(self, path, quality=70):
        im = Image.open(path).convert('RGB')
        out = Path(path).with_suffix('.jpg')
        if Path(out) == Path(path):
            if quality != 100 and not self.overwrite:
                out = f'{Path(path).name}_compressed.jpg'
            else:
                raise DegradingError(
                    'The image is already in JPEG format! '
                    'Processing it will only increase the size of the file. '
                    'If you want to compress the image, pass --quality with a '
                    'value lower than 100.')
        im.save(out, 'JPEG', quality=quality, subsampling=0)
        if self.overwrite:
            if Path(path) != Path(out):
                Path(path).unlink()
        return out, self.size(out)

    def to_png(self, path):
        im = Image.open(path)
        im = im.convert('RGBA')
        img = [(255, 255, 255, 0) if x[:3] == (0, 0, 0) else x
               for x in im.getdata()]
        im.putdata(img)
        out = Path(path).with_suffix('.png')
        im.save(out, 'PNG', quality=100, lossless=True)
        if self.overwrite:
            if Path(path) != Path(out):
                Path(path).unlink()
        return out, self.size(out)


def opts() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-j',
                        '--to-jpeg',
                        action='store_true',
                        help='Convert the image(s) to JPEG')
    parser.add_argument('-p',
                        '--to-png',
                        action='store_true',
                        help='Convert the image(s) to PNG')
    parser.add_argument('-q',
                        '--quality',
                        default=70,
                        type=int,
                        help='Output image quality (JPEG only; default: 70)')
    parser.add_argument('--overwrite',
                        action='store_true',
                        help='Overwrite the original image')
    parser.add_argument('path', nargs='+', help='Path(s) to the image file(s)')
    return parser.parse_args()


def main():
    args = opts()
    c = Convert(overwrite=args.overwrite)

    if not args.to_jpeg and not args.to_png:
        sys.exit(
            '\033[31mMust select at least one format to convert to!\033[39m')

    for file in args.path:
        size_before = c.size(file)
        if args.to_jpeg:
            out, size_after = c.to_jpeg(file, args.quality)
            logger.info(f'Output: {out}')
            logger.info(f'{size_before} kB ==> {size_after} kB')

        if args.to_png:
            if args.quality != 100:
                logger.warning('--quality has no effect on PNG files.')
            out, size_after = c.to_png(file)
            logger.info(f'Output: {out}')
            logger.info(f'{size_before} kB ==> {size_after} kB')


if __name__ == '__main__':
    logger.remove()
    logger.add(
        sys.stderr,
        level='INFO',
        format='<fg #99aab5>{time:YYYY-MM-DD HH:mm:ss.SSS}</fg #99aab5> | '
        '<level>{level: <6}</level> | <level>{message}</level>')
    main()
