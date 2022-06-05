#!/usr/bin/env python3

from cv2 import cv2
import numpy as np
import argparse
import os

DOWN = "down"
UP = "up"


class MaskMaker:
    def __init__(self, path_in, path_out, types):
        isdir = False
        paths_in = []
        if os.path.isfile(path_in):
            paths_in.append(path_in)
        if os.path.isdir(path_in):
            dirlist = os.listdir(path_in)
            paths_in += dirlist
            isdir = True

        self._windowName = "image"
        self._default_brush_size = 20
        self._default_opacity_value = 20
        cv2.namedWindow(self._windowName, cv2.WINDOW_KEEPRATIO)
        cv2.imshow(self._windowName, np.zeros(20))
        cv2.resizeWindow(self._windowName, 1000, 1000)

        self.updateable = False
        self._mouse_state = UP
        self._mouse_x = 0
        self._mouse_y = 0
        self._brush_value = self._default_brush_size
        self._opacity_value = self._default_opacity_value / 100

        cv2.createTrackbar(
            "Brush Size",
            self._windowName,
            self._default_brush_size,
            1000,
            self._brush_slider_cb,
        )
        cv2.createTrackbar(
            "Display Opacity",
            self._windowName,
            self._default_opacity_value,
            100,
            self._opacity_cb,
        )
        cv2.setMouseCallback(self._windowName, self._mouse_cb)

        for f in paths_in:
            f: str
            for type_ in types:
                split = f.split(".")
                ext = split[-1]
                root = ".".join(split[:-1])
                outfile = path_out
                infile = f
                if isdir:
                    outfile = os.path.join(path_out, root, type_ + "mask." + ext)
                    infile = os.path.join(path_in, f)
                self.run_masking(infile, outfile, type_)
        self.shutdown()

    def run_masking(self, path_in, path_out, type_):
        print("Mask out this type: " + str(type_))

        self.source_image = cv2.imread(path_in)
        self.mask_image = 0 * self.source_image
        self.display_image = self.source_image

        while True:
            if cv2.waitKey(1) & 0xFF == 27:
                break
            self.update_image()
            cv2.imshow(self._windowName, self.display_image)

        output_root = os.sep.join(path_out.split(os.sep)[:-1])
        if not os.path.exists(path_in):
            os.makedirs(output_root)
        print("writing mask to " + str(path_out))
        cv2.imwrite(path_out, self.mask_image)

    def _brush_slider_cb(self, value):
        self._brush_value = value
        self.updateable = True

    def _opacity_cb(self, value):
        self._opacity_value = value / 100 if value != 0 else 0
        self.updateable = True

    def _mouse_cb(self, event, x, y, _, __):
        self._mouse_x = x
        self._mouse_y = y

        if event == 4:
            self._mouse_state = UP
        if event == 1:
            self._mouse_state = DOWN

        self.updateable = True

    def shutdown(self):
        cv2.destroyAllWindows()
        # todo: save output image, etc.

    def update_image(self):
        if not self.updateable:
            return

        if self._mouse_state == DOWN:
            self.mask_image = cv2.circle(
                self.mask_image,
                (self._mouse_x, self._mouse_y),
                self._brush_value,
                (255, 255, 255),
                -1,
            )

        self.display_image = cv2.addWeighted(
            self.source_image, 1.0, self.mask_image, self._opacity_value, 0.0
        )
        self.display_image = cv2.circle(
            self.display_image,
            (self._mouse_x, self._mouse_y),
            self._brush_value,
            (255, 255, 255),
            int(self._brush_value * 0.2) + 1,
        )

        self.updateable = False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, required=True)
    parser.add_argument("-o", "--output", type=str, required=True)
    parser.add_argument("-t", "--types", type=str, nargs="+", required=True)
    args = parser.parse_args()

    MaskMaker(args.input, args.output, args.types)


if __name__ == "__main__":
    main()
