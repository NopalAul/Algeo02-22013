def rgbToHSV(r,g,b):
    # normalisasi
    r = r/255
    g = g/255
    b = b/255

    # nilai ekstrim
    cmax = max(r,g,b)
    cmin = min(r,g,b)
    delta = cmax - cmin

    # nilai HSV
    ## H
    if cmax == cmin :
        h = 0
    elif cmax == r :
        h = 60*(((g-b)/delta) % 6)
    elif cmax == g :
        h = 60*(((b-r)/delta) + 2)
    else :
        h = 60*(((r-g)/delta) + 4)
    ## S
    if cmax != 0 :
        s = (delta/cmax)*100
    else :
        s = 0
    ## V
    v = cmax*100

    return h,s,v


r = 142
g = 244
b = 85
print(f"{r}, {g}, {b}")
print(f"{rgbToHSV(r,g,b)[0]}, ", end="")
print(f"{rgbToHSV(r,g,b)[1]}, ", end="")
print(f"{rgbToHSV(r,g,b)[2]}\n")

