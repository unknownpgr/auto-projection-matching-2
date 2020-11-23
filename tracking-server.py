import cv2
import numpy as np
import math
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

hostName = "localhost"
serverPort = 8080

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

'''

Let the width of screen be 1.
Then height = 1*36.65/22.9 = 0.6248.

:. Screen width             = 1
:. Screen height            = 0.6248
:. Screen top ~ cam center  = 0.3301

'''


cap = cv2.VideoCapture(0)

CAM_ANGLE = 61*math.pi/180
DIST = 0.5      # Distance from screen to the observer
BIAS = 0.3301   # Distance from the center of the screen to the center of the camera

IMG_H, IMG_W, _ = cap.read()[1].shape


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


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        _, img = cap.read()
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        cx, cy = track_dot(hsv)
        cam_x, cam_y = get_cam_pos(IMG_W, IMG_H, CAM_ANGLE, DIST, cx, cy, BIAS)
        self.send_response(200)
        self.send_header("Content-type", "text/json")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(bytes(f'[{cam_x},{cam_y}]', "utf-8"))


def thread_server():
    tracking_server = HTTPServer((hostName, serverPort), MyServer)
    try:
        tracking_server.serve_forever()
    except KeyboardInterrupt:
        pass

    tracking_server.server_close()
    print("Server stopped.")


thread = threading.Thread(target=thread_server)
thread.start()
input(0)
exit()
