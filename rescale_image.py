import argparse
import glob
import os

from PIL import Image, ImageChops


def trim(im):
  bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))
  diff = ImageChops.difference(im, bg)
  diff = ImageChops.add(diff, diff, 2.0, -100)
  bbox = diff.getbbox()
  if bbox:
    return im.crop(bbox)


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('wcard', help='wildcard for input images')
  parser.add_argument('-s', type=int, default=512)
  parser.add_argument('-t', type=int, default=0, help='Trim border or not')
  opts = parser.parse_args()

  exts = ['.png', '.jpg', '.jpeg', '.tif']

  for f in glob.glob(opts.wcard):
    folder = os.path.dirname(f)
    name, ext = os.path.splitext(os.path.basename(f))

    if ext in exts:
      inputf = f
      outputf = os.path.join(folder, '%s.jpg' % name)

      img = Image.open(inputf)

      # # crop image
      # img = img.crop((475, 1, 475 + 1072, 1072 + 1))

      if opts.t:
        img = trim(img)
      img = img.resize((opts.s, opts.s), Image.ANTIALIAS)

      try:
        img.save(outputf)
      except:
        new = Image.new("RGB", img.size, (255, 255, 255))
        new.paste(img, mask=img.split()[3])  # 3 is the alpha channel
        new.save(outputf, quality=100)

    #   if outputf != inputf:
    #     os.remove(inputf)
