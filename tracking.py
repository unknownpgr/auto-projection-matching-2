import cv2
import numpy as np
import math

'''

Dimensions (For my LG gram 17 inch laptop)

Screen height                   22.9cm
Screen width                    36.65cm
Screen top edge - camera center 0.65cm

Therefore

Screen center to camera center = 22.9/2+0.65 = 12.1

Distance to object = 38.7cm
Length of object = 45.4cm
Camera angle = 2*atan(45.4/2/38.7) = About 61 deg

'''


cap = cv2.VideoCapture(0)

CAM_ANGLE = 61*math.pi/180
DIST = 22.5  # Distance from screen to the observer
BIAS = 12.1  # Distance from the center of the screen to the center of the camera

IMG_H, IMG_W, _ = cap.read()[1].shape
SCR_W = 366*2
SCR_H = 229*2
SCR_SCALE = 20


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


def get_cam_pos(img_w, img_h, cam_angle, dist, cx, cy, bias):
    '''
    Calculate relative camera position
    Range = [-1,1]
    '''
    crx = cx*2/img_w-1
    cry = (cy*2-img_h)/img_w

    # Get real camera position
    cam_x = -dist*math.tan(cam_angle/2)*crx
    cam_y = bias-dist*math.tan(cam_angle/2)*cry

    return cam_x, cam_y


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
    Get the points and edges of a cube
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
    '''
    Convert projected posion (unit=cm,anchor=center) to screen position(unit=pixel,anchor=top lefft)
    Scale = screen pixel size / real monitor size (in unit of other data such as real position of camera)
    '''
    x = int(x*scale+scr_w/2)
    y = int(-y*scale+scr_h/2)
    return x, y


pointsA, edgesA = get_cube(0, 5, -4, 8)
background = cv2.resize(cv2.imread('./room.jpg'), (SCR_W, SCR_H))//2
cv2.namedWindow('Video', cv2.WINDOW_FREERATIO)

t = 0
while True:
    t += 0.1
    ret, img = cap.read()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    cx, cy = track_dot(hsv)

    # Display tracked position
    img[cy, :] = [0, 0, 255]
    img[:, cx] = [255, 0, 0]
    cv2.imshow('img', img)

    cam_x, cam_y = get_cam_pos(IMG_W, IMG_H, CAM_ANGLE, DIST, cx, cy, BIAS)

    screen = np.copy(background)

    for i in range(0, SCR_H, SCR_H//10):
        screen = cv2.line(screen, (0, i), (SCR_W, i), (128, 128, 128), 1)

    for j in range(0, SCR_W, SCR_H//10):
        screen = cv2.line(screen, (j, 0), (j, SCR_H), (128, 128, 128), 1)

    for edge in edgesA:
        x1, y1 = get_screen_pos(
            *project(cam_x, cam_y, -DIST, *pointsA[edge[0]]), SCR_SCALE, SCR_W, SCR_H)
        x2, y2 = get_screen_pos(
            *project(cam_x, cam_y, -DIST, *pointsA[edge[1]]), SCR_SCALE, SCR_W, SCR_H)
        screen = cv2.line(screen, (x1, y1), (x2, y2), (255, 255, 255), 1)

    pointsB, edgesB = get_cube(math.sin(t)*4, 5, -4, 4)

    for edge in edgesB:
        x1, y1 = get_screen_pos(
            *project(cam_x, cam_y, -DIST, *pointsB[edge[0]]), SCR_SCALE, SCR_W, SCR_H)
        x2, y2 = get_screen_pos(
            *project(cam_x, cam_y, -DIST, *pointsB[edge[1]]), SCR_SCALE, SCR_W, SCR_H)
        screen = cv2.line(screen, (x1, y1), (x2, y2), (255, 255, 255), 1)

    cv2.imshow('Video', screen)
    cv2.waitKey(1)
