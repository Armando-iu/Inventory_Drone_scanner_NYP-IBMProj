from keyboard._keyboard_event import KEY_DOWN, KEY_UP
import keyboard
from djitellopy import tello
import cv2
import numpy as np
from pyzbar.pyzbar import decode
import threading
import time

def get_hsv_values(val):
    pass

def keyboard_debugging(drone):
    def on_action(event):
        if event.name == 'w':
            drone.send_rc_control(0 ,10 ,0 ,0)
            print("moving foward")
        if event.name == 's':
            drone.send_rc_control(0 ,-10 ,0 ,0)
            print("moving back")
        if event.name == 'd':
            drone.send_rc_control(10 ,0 ,0 ,0)
            print("moving back")
        if event.name == 'a':
            drone.send_rc_control(-10 ,0 ,0 ,0)
            print("moving back")

        if event.name == 'u':
            drone.send_rc_control(0 ,0 ,15 ,0)
            print("moving back")
        if event.name == 'j':
            drone.send_rc_control(0 ,0 ,-10 ,0)
            print("moving back")
        if event.event_type == KEY_UP:
            on_release(event.name)

    def on_release(key):
        print(f"Released: {key}")
        print("stop moving")
        drone.send_rc_control(0 ,0 ,0 ,0)

    keyboard.hook(lambda e: on_action(e))


def run_video(drone):
    while True:
        # changes the HSV values
        h_min = cv2.getTrackbarPos('H min', 'image')
        h_max = cv2.getTrackbarPos('H max', 'image')
        s_min = cv2.getTrackbarPos('S min', 'image')
        s_max = cv2.getTrackbarPos('S max', 'image')
        v_min = cv2.getTrackbarPos('V min', 'image')
        v_max = cv2.getTrackbarPos('V max', 'image')


        frame = drone.get_frame_read().frame #getting the drone cam feed
        print(f"type {type(frame)}")
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV) #hell looking ass
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        img = rgb_frame.copy()

        # Set the lower and upper HSV limits
        # move_lower_limit = np.array([86 , 50 , 11])
        # move_upper_limit = np.array([103 , 197 , 255])
        red_move_lower_limit = np.array([140 , 139 , 143]) 
        red_move_upper_limit = np.array([179 , 255 , 255])
                # Set the lower and upper HSV limits
        blue_move_lower_limit = np.array([114 , 92 , 133])
        blue_move_upper_limit = np.array([125 , 132 , 255])

        edit_lower_limit = np.array([h_min , s_min , v_min])
        edit_upper_limit = np.array([h_max , s_max , v_max])
        # create a mask for the specified color range
        blue_mask = cv2.inRange(hsv_frame, blue_move_lower_limit, blue_move_upper_limit)

        green_edit_mask = cv2.inRange(hsv_frame, edit_lower_limit, edit_upper_limit)

        green_move_lower_limit = np.array([42 , 150 , 125])
        green_move_upper_limit = np.array([64 , 255 , 255])

        red_mask = cv2.inRange(hsv_frame, red_move_lower_limit, red_move_upper_limit)

        # create a mask for the specified color range
        green_mask = cv2.inRange(hsv_frame, green_move_lower_limit, green_move_upper_limit)
        # get the bounding box from the mask image
        bound_box_red = cv2.boundingRect(green_mask)

        # get the bounding box from the mask image
        bound_box_blue = cv2.boundingRect(blue_mask)

        if bound_box_blue is not None:
            x, y, w, h = bound_box_blue
            print(f"(x: {x} , y: {y}) of Width: {w} and Height: {h}") 
            cv2.putText(rgb_frame , f"(x: {x} , y: {y}) of Width: {w} and Height: {h}" , (0,200) , cv2.FONT_HERSHEY_COMPLEX , 0.5 , (0,255,255), 2 , cv2.LINE_4 ) #giving info of bodunding box
            cv2.rectangle(rgb_frame, (x, y), (x + w, y + h), (0, 255, 0), 2) #making the bounding box


        if bound_box_red is not None:
            x, y, w, h = bound_box_red
            print(f"(x: {x} , y: {y}) of Width: {w} and Height: {h}") 
            cv2.putText(rgb_frame , f"(x: {x} , y: {y}) of Width: {w} and Height: {h}" , (0,400) , cv2.FONT_HERSHEY_COMPLEX , 0.5 , (255,0,255), 2 , cv2.LINE_4 ) #giving info of bodunding box
            cv2.rectangle(rgb_frame, (x, y), (x + w, y + h), (255, 0, 0), 2) #making the bounding box

        # # create a mask for the specified color range
        # mask = cv2.inRange(hsv_frame, move_lower_limit, move_upper_limit)

        # # get the bounding box from the mask image
        # bound_box = cv2.boundingRect(mask)

        # if bound_box is not None:
        #     x, y, w, h = bound_box
        #     print(f"(x: {x} , y: {y}) of Width: {w} and Height: {h}") 
        #     cv2.putText(rgb_frame , f"(x: {x} , y: {y}) of Width: {w} and Height: {h}" , (0,200) , cv2.FONT_HERSHEY_COMPLEX , 0.5 , (0,255,255), 2 , cv2.LINE_4 ) #giving info of bodunding box
        #     cv2.rectangle(rgb_frame, (x, y), (x + w, y + h), (0, 255, 0), 2) #making the bounding box

        qrcodes = decode(rgb_frame)
        for qrcode in qrcodes:
            if qrcode != []: #if qr code is seen
                x , y , w, h = qrcode.rect
                cropped_img = img[y:y+h, x:x+w]  # Crop the image to the QR code area
                if np.sum(cropped_img) != 0: #to check if empty
                    cv2.putText(rgb_frame , f"can see QR" , (0,275) , cv2.FONT_HERSHEY_COMPLEX , 0.5 , (0,255,255), 2 , cv2.LINE_4 ) 

        # frame_stuff = frame.copy()
        # qr_codes = decode(frame_stuff)
        # print(qr_codes)
        
        cv2.imshow("green mask frame" , green_mask)
        cv2.imshow("blue Frame" , blue_mask)
        cv2.imshow("red Frame" , red_mask)
        cv2.imshow("editable Frame" , green_edit_mask)
        cv2.imshow("RGB Frame" , rgb_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.imwrite("green line.jpg" , rgb_frame)
            drone.land()
            break

def Trackbar_Makers():
    # Create a trackbar for Hue
    cv2.createTrackbar('H min', 'image', 0, 179, get_hsv_values)
    cv2.createTrackbar('H max', 'image', 179, 179, get_hsv_values)

    # Create a trackbar for Saturation
    cv2.createTrackbar('S min', 'image', 0, 255, get_hsv_values)
    cv2.createTrackbar('S max', 'image', 255, 255, get_hsv_values)

    # Create a trackbar for Value
    cv2.createTrackbar('V min', 'image', 0, 255, get_hsv_values)
    cv2.createTrackbar('V max', 'image', 255, 255, get_hsv_values)

def fly_to(height , me):
    # fly to around 90
    while True:
        curr_height = me.get_height()
        if height - curr_height > 5:
            me.send_rc_control(0,0,10,0)
        elif height - curr_height < -5:
            me.send_rc_control(0,0,-10,0)
        else:
            print(f"curr height {me.get_height()}")
            me.send_rc_control(0,0,0,0)
            break

def main():
    drone = tello.Tello()
    drone.connect()
    drone.streamon()
    drone.takeoff()
    drone.set_video_direction(drone.CAMERA_FORWARD)
    fly_to(70 , drone)

    drone.send_rc_control(0,0,0,0)
    # drone.send_rc_control(0,0,10 , 0)
    # time.sleep(2.5)
    # drone.send_rc_control(0,0,0,0)
    keyboard_debugging(drone)
    # Create a window to display the image
    cv2.namedWindow('image')
    Trackbar_Makers()
    print(f"bat {drone.get_battery()}")
    
    run_video(drone)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

# Experiment 1 
# hypothesis:
# as Drone gets closer the blue height gets larger
# as Drone gets further the blue gets smaller in height
# there is a range of perfect height to scan qr code
# Results:

# normal lighting conditions
    # 140 px on 40 cm away from cabinet
    # 100 px on 60 cm away from cabinet
    # HSV min  = [86 , 43 , 11]
    # HSV max  = [103 , 197 , 255]
# dark lighting conditions
    # 140 px on 30-40 cm away from cabinet
    # 100 px on 60-70 cm away from cabinet
    # HSV min  = [86 , 50-60 , 11]
    # HSV max  = [103 , 197 , 255]
    # The video gets more noisy the darker it is -> to solve this increase saturation by a shit ton