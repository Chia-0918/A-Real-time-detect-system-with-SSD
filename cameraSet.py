import cv2
import time
import mxnet as mx
import detector as dc
from gps_realTime import GPS
""" GPS 座標程式已導入 暫未開啟 """

def video_load(video_q, v_name, cap_num):
	cap = cv2.VideoCapture(v_name)
	# a = GPS.HandsomeHanWen() #宣告

	print('[OK] video_load')

	while cap.isOpened():
	    ret, frame = cap.read()
	    if not ret : break

	    # gps_data = a.HanWenIsRealyHandsome() # 獲取GPS資料/顯示

	    # read and set class
	    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	    frame = mx.nd.array(frame).astype('uint8') # frame[...,::-1]
	    # print(type(frame))
	    imgA = dc.detetor(cap_num, frame, 0)
	    # if not full put in to Queue else keep sleep
	    while video_q.full(): time.sleep(1)
	    video_q.put(imgA)

	    cv2.waitKey(1)
	# a.HanWenIsVeryHandsome() # 關閉serial port //this step is very important, must remember
	cap.release()

def video_load_1(video_q, v_name, cap_num):
	cap = cv2.VideoCapture(v_name)
	# a = GPS.HandsomeHanWen() #宣告

	print('[OK] video_load')

	while cap.isOpened():
	    ret, frame = cap.read()
	    if not ret : break

	    # gps_data = a.HanWenIsRealyHandsome() # 獲取GPS資料/顯示
	    
	    # read and set class
	    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	    frame = mx.nd.array(frame).astype('uint8') # frame[...,::-1]
	    # print(type(frame))
	    imgA = dc.detetor(cap_num, frame, 0)
	    # if not full put in to Queue else keep sleep
	    while video_q.full(): time.sleep(1)
	    video_q.put(imgA)

	    cv2.waitKey(1)
	# a.HanWenIsVeryHandsome() # 關閉serial port //this step is very important, must remember
	print("done")
	cap.release()