from PIL import Image
import webcolors
import sys

def xy_to_frame_buffer(x,y):
    return (y*128 + x)*4

def main():
    im = Image.open(sys.argv[1])
    im = im.convert('RGB')
    sx, sy = im.size
    
    f = open("output.txt", "w")

    count = 0
    # Create a list of colors excluding black
    coloursList = []

    # loop through pixels of the image and find the colours
    for j in range(sy):
        for i in range(sx):
            count += 1
            px = im.getpixel((i,j))
            px = (px[0],px[1],px[2])
            if px != (0,0,0) and (px not in coloursList):
                coloursList.append(px)
            #print(f"The pixel value at ({i},{j}) is {px}")
    # f.write("        la $t6, FRAME_ADR\n\n")
    # print the colours to the registers
    for i in range(len(coloursList)):
        stuff = webcolors.rgb_to_hex(coloursList[i]).replace("#", "0x")
        f.write(f"        li $t1, {stuff}\n")

        # print the location to the images
        for j in range(sy):
            for i in range(sx):
                px = im.getpixel((i,j))
                px = (px[0],px[1],px[2])
                colour = webcolors.rgb_to_hex(px).replace("#", "0x")
                if (colour != stuff):
                    continue

                if px != (0,0,0):
                    f.write(f"        sw $t1, {xy_to_frame_buffer(i,j)}($t0)\n")
        f.write("\n")
    f.write("        jr $ra")

if __name__ == "__main__":
    main()