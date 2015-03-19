import fileinput
import os.path
import cv2
from larson_filters_png import larsonSekanina
from larson_filters_png import larsonSlaughter

def main():
    for file in fileinput.input():
        filename = fileinput.filename()

        #dr = 1
        #dtheta = 5
        #lars_sek_img = larsonSekanina(filename, dr, dtheta)
        lars_sla_img = larsonSlaughter(filename,5,5,5,10)

        # Split filename and extension.
        spl = os.path.splitext(filename)
        #lars_sek_name = spl[0] + '_lars-sek' + spl[1]
        lars_sla_name = spl[0] + '_lars-sla' + spl[1]

        # Write new image.
        #cv2.imwrite(lars_sek_name, lars_sek_img)
        cv2.imwrite(lars_sla_name, lars_sla_img)

        fileinput.nextfile()

    fileinput.close()

if __name__ == '__main__':
    main()
