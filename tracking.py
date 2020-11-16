import cv2
import numpy as np
import math

cap = cv2.VideoCapture(0)

theta = 63*math.pi/180
dist = 26.5
bias = 13.25

cx = 0
cy = 0

ret, img = cap.read()
h, w, _ = img.shape

SCR_W = 380
SCR_H = 265


def track_dot(img, color=30, epsilon=10, thresh=128):
    bound_upper = img[:, :, 0] < (color+epsilon)
    bound_lower = img[:, :, 0] > (color-epsilon)
    bound_satur = img[:, :, 1] > thresh
    bound = bound_upper & bound_lower & bound_satur
    ys, xs = np.nonzero(bound)

    N = len(ys)

    if N > 0:
        xs = sorted(xs)
        ys = sorted(ys)
        return xs[N//2], ys[N//2]
    else:
        return 0, 0


def get_cam_pos(img_w, img_h, theta, dist, cx, cy, bias):
    # Calculate relative camera position
    # Range = [-1,1]
    crx = cx*2/img_w-1
    cry = (cy*2-img_h)/img_w

    # Get real camera position
    rx = -dist*math.tan(theta/2)*crx
    ry = bias-dist*math.tan(theta/2)*cry

    return rx, ry


def project(cx, cy, cz, ox, oy, oz):
    return [
        (cx*oz-ox*cz)/(oz-cz),
        (cy*oz-oy*cz)/(oz-cz)
    ]


def get_cube(x, y, z, d=1):
    return [
        [x+d, y+d, z+d],
        [x+d, y+d, z-d],
        [x+d, y-d, z+d],
        [x+d, y-d, z-d],
        [x-d, y+d, z+d],
        [x-d, y+d, z-d],
        [x-d, y-d, z+d],
        [x-d, y-d, z-d]
    ]


def get_screen_pos(x, y, scale, scr_w, scr_h):
    # Scale = screen pixel size / real monitor size (in unit of other data such as real position of camera)
    x = int(x*scale+scr_w/2)
    y = int(-y*scale+scr_h/2)
    return x, y


cube = get_cube(-5, 2, -10, 2)
back = cv2.resize(cv2.imread('./room.jpg'), (SCR_W, SCR_H))//2
cv2.namedWindow('Video', cv2.WINDOW_FREERATIO)
while True:
    ret, img = cap.read()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    cx, cy = track_dot(hsv)

    # Display
    img[cy, :] = [0, 0, 255]
    img[:, cx] = [255, 0, 0]
    cv2.imshow('img', img)

    rx, ry = get_cam_pos(w, h, theta, dist, cx, cy, bias)

    screen = np.copy(back)

    for dot in cube:
        x, y = project(rx, ry, -dist, dot[0], dot[1], dot[2])
        x, y = get_screen_pos(x, y, 10, SCR_W, SCR_H)
        screen[y-1:y+1, x-1:x+1] = 255

    cv2.imshow('Video', screen)
    cv2.waitKey(1)
