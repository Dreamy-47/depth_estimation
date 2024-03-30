from PIL import Image
import os
def main(path):
    dir_path = os.path.dirname(path)
    image = Image.open(path)
    pixel_list = []
    pixel_list.append(image.getpixel((1842,890)))
    pixel_list.append(image.getpixel((500,838)))
    pixel_list.append(image.getpixel((842,859)))
    pixel_list.append(image.getpixel((975,234)))
    pixel_list.append(image.getpixel((1274,852)))
    pixel_list.append(image.getpixel((1476,962)))
    pixel_list.append(image.getpixel((1663,970)))
    pixel_list.append(image.getpixel((2008,795)))
    pixel_list.append(image.getpixel((2150,622)))
    pixel_list.append(image.getpixel((1746,411)))
    pixel_list.append(image.getpixel((1207,127)))
    for p in pixel_list:
        print(p)

if __name__ == "__main__":
    fpath = r"record\dest\none_target\Left_depth.png"
    main(fpath)