import numpy as np
import cv2
import sys
#simport pafy

#img1 = plt.imread('eye.jpg')
# OpenCV Utility Class for Mouse Handling
class Sketcher:
    def __init__(self, windowname, dests, colors_func):
        self.prev_pt = None
        self.windowname = windowname
        self.dests = dests
        self.colors_func = colors_func
        self.dirty = False
        self.show()
        cv2.setMouseCallback(self.windowname, self.on_mouse)

    def show(self):
        cv2.imshow(self.windowname, self.dests[0])
        cv2.imshow(self.windowname + ": mask", self.dests[1])

    # onMouse function for Mouse Handling
    def on_mouse(self, event, x, y, flags, param):
        pt = (x, y)
        if event == cv2.EVENT_LBUTTONDOWN:
            self.prev_pt = pt
        elif event == cv2.EVENT_LBUTTONUP:
            self.prev_pt = None

        if self.prev_pt and flags & cv2.EVENT_FLAG_LBUTTON:
            for dst, color in zip(self.dests, self.colors_func()):
                cv2.line(dst, self.prev_pt, pt, color, 5)
            self.dirty = True
            self.prev_pt = pt
            self.show()

cap = cv2.VideoCapture(0)

#def main():

print("Usage: python inpaint <image_path>")
print("Keys: ")
print("t - inpaint using FMM")
print("n - inpaint using NS technique")
print("r - reset the inpainting mask")
print("ESC - exit")

    # Read image in color mode
img = cv2.imread('flower-garden.jpg', cv2.IMREAD_COLOR)
ret, frame1 = cap.read()
 
    # Create a copy of original image
img_mask = frame1.copy()
    # Create a black copy of original image
    # Acts as a mask
inpaintMask = np.zeros(frame1.shape[:2], np.uint8)
    # Create sketch using OpenCV Utility Class: Sketcher
sketch = Sketcher('image', [frame1, inpaintMask], lambda : ((255, 255, 255), 255))
res = cv2.inpaint(src=frame1, inpaintMask=inpaintMask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)

while True:
    ch = cv2.waitKey(1) & 0xFF
    ret, frame = cap.read()
    cv2.imshow('Input', frame)
    #cv2.imshow('Inpaint Output using FMM', res)
    res = cv2.inpaint(src=frame, inpaintMask=inpaintMask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)
    if ch == 27:
        break
        
    if ch == ord('r'):
        img_mask[:] = frame1
        inpaintMask[:] = 0
        sketch.show()
        sketch = Sketcher('image', [frame, inpaintMask], lambda : ((255, 255, 255), 255))

    cv2.imshow('Inpaint Output using FMM', res)
    print('Completed')


if __name__ == '__main__':
    main()
    cv.destroyAllWindows()
