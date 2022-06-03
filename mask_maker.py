#!/usr/bin/env python3

from cv2 import cv2

DOWN = "down"
UP = "up"


class MaskMaker:
    def __init__(self, path_in, path_out):
        self._path_out = path_out
        self.source_image = cv2.imread(path_in)
        self.mask_image = 0 * self.source_image
        self.display_image = self.source_image

        self._windowName = "image"
        self._default_brush_size = 20
        self._default_opacity_value = 20
        cv2.imshow(self._windowName, self.mask_image)
        cv2.createTrackbar(
            "Brush Size",
            self._windowName,
            self._default_brush_size,
            100,
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

        self.updateable = False
        self._mouse_state = UP
        self._mouse_x = 0
        self._mouse_y = 0
        self._brush_value = self._default_brush_size
        self._opacity_value = self._default_opacity_value / 100

        while cv2.waitKey(1) & 0xFF != 27:
            self.update_image()
            cv2.imshow(self._windowName, self.display_image)

        self.shutdown()

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
        cv2.imwrite(self._path_out, self.mask_image)
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
    MaskMaker("./ghprofile.jpeg","./ghprofile_out.jpg")


if __name__ == "__main__":
    main()
