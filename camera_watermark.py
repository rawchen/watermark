'''
注意
本地编译运行修改为   proDir = os.path.split(os.path.realpath(__file__))[0]
打包exe运行修改为   proDir = os.path.dirname(os.path.realpath(sys.executable))
'''
try:
    import os
    import sys
    import exifread
    from PIL import ImageFont, ImageDraw, Image, ImageOps


    def find(path):
        path += '\\原图'
        files = os.listdir(path)
        jpg = []
        for file in files:
            if (os.path.splitext(file)[-1]) == '.jpg' or (os.path.splitext(file)[-1]) == '.JPG':
                jpg.append(file)
        if len(jpg) == 0:
            n = input("没有在[原图]文件夹检测到.JPG格式的文件,按回车键关闭程序")
        else:
            return jpg


    def easy(x):
        s = str(x)
        if '/' in s:
            s = s.split('/')
            a = int(s[0])
            b = int(s[1])
            if a != 1:
                b = b // a
                a = 1
                return str(a) + '/' + str(b)
            else:
                return str(x)
        else:
            return str(x)


    def exif(name):
        photo = name
        proDir = os.path.split(os.path.realpath(__file__))[0]

        def tonum(x):
            x = str(x)
            if '/' in x:
                x = x.split('/')
                a = x[0]
                b = x[1]
                x = int(a) / int(b)
                return float(round(x, 1))
            else:
                return float((x))

        img = Image.open(proDir + '\\原图\\' + photo)
        img = ImageOps.exif_transpose(img)
        imgSize = img.size  # 大小/尺寸
        wight = imgSize[0]
        hight = imgSize[1]
        px = int((wight * hight) / 10000)

        f = open(proDir + '\\原图\\' + photo, "rb")
        tags = exifread.process_file(f)

        #这个for是debug的
        for i in tags:
            print(i, ':', tags[i])

        id = tags.get('Image Model', '0')
        lens = tags.get('EXIF LensModel', '0')
        if lens == '0':
            lens = ' '
        mm = tags.get('EXIF FocalLength', '0')
        mm35 = tags.get('EXIF FocalLengthIn35mmFilm', '0')
        s = tags.get('EXIF ExposureTime', '0')
        f = tags.get('EXIF FNumber', '0')
        f = tonum(f)
        iso = tags.get('EXIF ISOSpeedRatings', '0')
        ev = tags.get('EXIF ExposureBiasValue', '0')
        ev = tonum(ev)
        daytime = tags.get('EXIF DateTimeOriginal', '0')

        types = [id, wight, hight, px, lens, mm, mm35, s, f, iso, ev, daytime]
        print(
            "机身型号：{}\n照片尺寸：{}X{}\n照片像素：{}万\n镜头规格：{}\n拍摄焦距：{}mm\n等效全幅：{}mm\n快门速度：{}s\n拍摄光圈：f{}\n感光度值：iso{}\n曝光补偿：{}Ev\n拍摄时间 ：{}".format(
                id, wight, hight, px, lens, mm, mm35, s, f, iso, ev, daytime))
        print("\n")
        color = [255, 255, 255]
        bg = Image.new('RGB', (wight, int(hight + hight / 10)), (color[0], color[1], color[2]))
        sy = Image.new('RGB', (wight, int(hight / 10)), (color[0], color[1], color[2]))

        bgSize = sy.size  # 大小/尺寸d
        bgwight = bgSize[0]
        bghight = bgSize[1]
        try:
            logo = Image.open(proDir + '\\logo配置\\' + 'logo.png')
        except:
            n = input('没有在[logo配置]文件夹找到名为[logo.png]的文件！\n请重新确认要使用的logo,推荐尺寸500x500z,按回车键关闭程序')

        newlogo = logo
        newlogo = newlogo.resize((bghight, bghight))
        sy.paste(newlogo, (0, 0))
        draw = ImageDraw.Draw(sy)
        path_to_ttf = 'msyh.ttc'

        font = ImageFont.truetype(path_to_ttf, size=int(bghight / 5))

        id = str(id)

        size = str(wight) + 'x' + str(hight)
        oldpx = (wight * hight) * 0.000001
        px = str(round(oldpx, 2)) + 'MP'
        lens = str(lens)

        s = easy(s)
        s = str(s) + 's'
        f = tonum(f)
        f = 'F' + str(f)
        iso = 'iso' + str(iso)

        mm = tonum(mm)
        mm = 'DX' + str(mm) + 'mm'
        mm35 = tonum(mm35)
        mm35 = 'FX' + str(mm35) + 'mm'
        ev = str(ev) + 'EV'

        daytime = str(daytime)

        path_to_ttf = 'ariblk.ttf'
        font = ImageFont.truetype(path_to_ttf, size=int(bghight * 0.25))
        draw.text(xy=(bghight + bghight * 0.1, bghight * 0.03), text=id, font=font, fill=(0, 0, 0))

        path_to_ttf = 'msyh.ttc'
        font = ImageFont.truetype(path_to_ttf, size=int(bghight * 0.20))
        draw.text(xy=(bghight + bghight * 0.1, bghight * 0.3), text=size, font=font, fill=(0, 0, 0))
        draw.text(xy=(bghight + bghight * 0.1, bghight * 0.5), text=px, font=font, fill=(0, 0, 0))
        draw.text(xy=(bghight + bghight * 0.1, bghight * 0.7), text=lens, font=font, fill=(0, 0, 0))

        path_to_ttf = 'ariblk.ttf'
        font = ImageFont.truetype(path_to_ttf, size=int(bghight * 0.25))
        draw.text(xy=(wight * 0.99, bghight * 0.3), text=s, font=font, fill=(102, 100, 100), anchor='rs')
        draw.text(xy=(wight * 0.81, bghight * 0.3), text=f, font=font, fill=(102, 100, 100), anchor='rs')
        draw.text(xy=(wight * 0.66, bghight * 0.3), text=iso, font=font, fill=(102, 100, 100), anchor='rs')

        path_to_ttf = 'msyh.ttc'
        font = ImageFont.truetype(path_to_ttf, size=int(bghight * 0.20))
        draw.text(xy=(wight * 0.7, bghight * 0.6), text=mm, font=font, fill=(102, 100, 100), anchor='rs')
        draw.text(xy=(wight * 0.88, bghight * 0.6), text=mm35, font=font, fill=(102, 100, 100), anchor='rs')
        draw.text(xy=(wight * 0.99, bghight * 0.6), text=ev, font=font, fill=(102, 100, 100), anchor='rs')

        font = ImageFont.truetype(path_to_ttf, size=int(bghight * 0.20))
        draw.text(xy=(wight * 0.99, bghight * 0.9), text=daytime, font=font, fill=(255, 100, 100), anchor='rs')

        sy.save(proDir + '\\logo配置\\' + '水印配置' + photo, quality=100)
        bg.paste(img, (0, 0))
        bg.paste(sy, (0, hight))
        bg.save(proDir + '\\水印图\\' + '水印' + photo, quality=100)


    print("欢迎使用，本软件完全免费")
    n = input("请将要处理的照片放至[原图]文件夹，默认只处理jpg格式文件\n可以在[logo配置]文件夹替换原本的logo.jpg文件，推荐尺寸500x500，按回车键继续：")

    proDir = os.path.split(os.path.realpath(__file__))[0]
    for i in find(proDir):
        exif(i)

    n = input("照片全部处理完成，请在[水印图片]文件夹查看处理后的照片，单独的水印图片保存在[logo配置]文件夹，按回车键关闭程序")
except Exception as e:
    print('程序出错')
    print('错误类型是', e.__class__.__name__)
    print('错误明细是', e)
n = input('error')
