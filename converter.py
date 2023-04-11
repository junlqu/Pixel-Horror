from PIL import Image
import webcolors
import sys

def xy_to_frame_buffer(x, y):
    return (y * 128 + x) * 4

def main():
    im = Image.open(sys.argv[1])
    im = im.convert('RGB')
    sx, sy = im.size
    
    f = open("output.txt", "w")

    # loop through pixels of the image and find the colours

    f.write("        la $t0, FRAME_ADR\n")
    
    # print the location to the images
    for j in range(sy):
        for i in range(sx):
            px = im.getpixel((i, j))
            px = (px[0], px[1], px[2])

            #if px != (0, 0, 0):
            frame = xy_to_frame_buffer(i,j)
            colour = webcolors.rgb_to_hex(px).replace("#", "0x")
            #f.write(f"        li $t1, {colour}\n")
            f.write(f"        lw $t1, {frame}($t7)\n")
            f.write(f"        sw $t1, {frame}($t6)\n")
    f.write("\n        jr $ra")

if __name__ == "__main__":
    main()