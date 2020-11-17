import cv2
import numpy as np
import math

cap = cv2.VideoCapture(0)

theta = 71*math.pi/180
dist = 26.5
bias = 125

cx = 0
cy = 0

ret, img = cap.read()
h, w, _ = img.shape

SCR_W = 380
SCR_H = 265

# 화면 세로 폭 22.9cm
# 화면 가로 폭 36.65cm
# 화면 위쪽 경계에서 카메라 중심까지 0.65cm


def track_dot(img, color=30, epsilon=10, thresh=160):
    '''
    Get the position of color dot from hsv type imge
    '''

    bound_upper = img[:, :, 0] < (color+epsilon)  # Upper hue bound
    bound_lower = img[:, :, 0] > (color-epsilon)  # Lower hue bound
    bound_satur = img[:, :, 1] > thresh  # Saturation threshold
    bound = bound_upper & bound_lower & bound_satur

    # Get detected points
    ys, xs = np.nonzero(bound)

    N = len(ys)

    # Calculate median point
    if N > 0:
        xs = sorted(xs)
        ys = sorted(ys)
        return xs[N//2], ys[N//2]
    else:
        return 0, 0


def get_cam_pos(img_w, img_h, theta, dist, cx, cy, bias):
    '''
    Calculate relative camera position
    Range = [-1,1]
    '''
    crx = cx*2/img_w-1
    cry = (cy*2-img_h)/img_w

    # Get real camera position
    rx = -dist*math.tan(theta/2)*crx
    ry = bias-dist*math.tan(theta/2)*cry

    return rx, ry


def project(cx, cy, cz, ox, oy, oz):
    '''
    Project given point to screen
    [cx,cy,cz] is the position of the camera.
    [ox,oy,oz] is the position of the point.
    '''
    return [
        (cx*oz-ox*cz)/(oz-cz),
        (cy*oz-oy*cz)/(oz-cz)
    ]


def get_cube(x, y, z, d=2):
    '''
    Get the points and edges of cube
    '''
    d /= 2
    return [
        [x+d, y+d, z+d],
        [x+d, y+d, z-d],
        [x+d, y-d, z+d],
        [x+d, y-d, z-d],
        [x-d, y+d, z+d],
        [x-d, y+d, z-d],
        [x-d, y-d, z+d],
        [x-d, y-d, z-d]
    ], [
        [0, 1],
        [2, 3],
        [4, 5],
        [6, 7],
        [0, 2],
        [1, 3],
        [4, 6],
        [5, 7],
        [0, 4],
        [1, 5],
        [2, 6],
        [3, 7]
    ]


def get_screen_pos(x, y, scale, scr_w, scr_h):
    # Scale = screen pixel size / real monitor size (in unit of other data such as real position of camera)
    x = int(x*scale+scr_w/2)
    y = int(-y*scale+scr_h/2)
    return x, y


points, edges = get_cube(0, 0, -10, 4)
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

    for edge in edges:
        x1, y1 = get_screen_pos(
            *project(rx, ry, -dist, *points[edge[0]]), 10, SCR_W, SCR_H)
        x2, y2 = get_screen_pos(
            *project(rx, ry, -dist, *points[edge[1]]), 10, SCR_W, SCR_H)
        screen = cv2.line(screen, (x1, y1), (x2, y2), (255, 255, 255), 1)

    cv2.imshow('Video', screen)
    cv2.waitKey(1)
