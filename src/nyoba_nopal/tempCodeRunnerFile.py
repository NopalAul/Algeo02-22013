for i in range(0,height,3):
        for j in range(0,width,3):
            h = rgbToHSV(img[i][j][0],img[i][j][1],img[i][j][2])
            print(h)