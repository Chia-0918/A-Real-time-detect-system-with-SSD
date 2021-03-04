from PyQt5 import QtCore,QtGui,QtWidgets
import sys
import cv2
import time 
import mxnet as mx
import detector as dc
import classSet as cls
from cameraSet import video_load, video_load_1
from gluoncv.model_zoo import get_model
from multiprocessing import Process, Pool, Queue, Manager
#m = Manager()
q2 = Queue(10)
q1 = Queue(10)
massage=""
#q_step1 = m.Queue(120)
#q_step2 = m.Queue(60)
def weight(q_video_in, q_video_out):
    dataclass = cls.getClass()
    classcolor = cls.getColor()
    net = get_model('ssd_512_vgg16_atrous_custom', classes=dataclass, transfer='voc' , pretrained_base=False, pretrained=False, ctx=mx.gpu())#modify mx.cpu(), gpu()

    net.load_parameters('ssd_512_vgg16_atrous_voc_4220_0.8260.params')
    net.collect_params().reset_ctx([mx.gpu()])
    net.hybridize()

    print('[OK] weight')
    while not q_video_in.empty() :
        # waiting
        while q_video_in.empty() : time.sleep(0.5)
        # get
        imgA = q_video_in.get()

        x = imgA.get_tensors()
        x = x.as_in_context(mx.gpu())

        class_IDs, scores, bounding_boxes = net(x)

        imgA.set_deteced_value(bounding_boxes[0], class_IDs[0], scores)

        while q_video_out.full() : time.sleep(0.05) # if q_video_out(funtion : show)is busy wait
        q_video_out.put(imgA) # else put imgA in Queue
    

def show(q_video_show):
    global q1,q2
    while q_video_show.empty() : time.sleep(0.5) # wait for detect

    while not q_video_show.empty():
        imgA = q_video_show.get() # get and draw
        imgA.draw_bbox()
        img = imgA.get_image()
        #q1.put(imgA)
        img = imgA.get_image()
        
        if imgA.get_cap_number() == 0 : q1.put(img)
        else : q2.put(img)
        #cv2.waitKey(63)

    #cv2.destroyAllWindows()


class Ui_MainWindow(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
 
        self.timer_camera = QtCore.QTimer()
        self.cap = cv2.VideoCapture(0)
        self.cap1 = cv2.VideoCapture(1)
        self.CAM_NUM = 0
 
        self.set_ui()
        self.slot_init()
    def set_ui(self):
        self.__layout_main = QtWidgets.QHBoxLayout()
        self.__layout_fun_button = QtWidgets.QVBoxLayout()
        self.__layout_data_show = QtWidgets.QVBoxLayout()
        self.button_open_camera = QtWidgets.QPushButton('打開相機')
        self.button_close = QtWidgets.QPushButton('退出')
        self.button_open_camera.setMinimumHeight(50)
        self.button_close.setMinimumHeight(50)
 
        self.button_close.move(10,100)
        self.label_show_camera = QtWidgets.QLabel()
        self.label_show_camera.setFixedSize(641,481)
        self.label_show_camera2 = QtWidgets.QLabel()
        self.label_show_camera2.setFixedSize(641,481)
        self.label_text = QtWidgets.QLabel()
        self.label_text.setFixedSize(200,481)
        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setWidget(self.label_text)
        #self.__layout_fun_button.addWidget(self.button_open_camera) 
        #self.__layout_fun_button.addWidget(self.button_close)
        #self.__layout_main.addLayout(self.__layout_fun_button)
        self.__layout_main.addWidget(self.scroll)
        self.__layout_main.addWidget(self.label_show_camera)
        self.__layout_main.addWidget(self.label_show_camera2)
        #layout.addWidget(scroll)
        self.setLayout(self.__layout_main)

    def consumer(self):
        global massage,q1,q2
        if q1.empty() or q2.empty(): return
        else: print("123")
        img1 = q1.get()
        img2 = q2.get()
        #img = imgA.get_image()
        show1 = cv2.resize(img1,(640,480))
        show2 = cv2.resize(img2,(640,480))
        show1 = cv2.cvtColor(show1,cv2.COLOR_BGR2RGB) 
        show2 = cv2.cvtColor(show2,cv2.COLOR_BGR2RGB) 
        showImage1 = QtGui.QImage(show1.data,show1.shape[1],show1.shape[0],QtGui.QImage.Format_RGB888)
        showImage2 = QtGui.QImage(show2.data,show2.shape[1],show2.shape[0],QtGui.QImage.Format_RGB888)
        self.label_show_camera.setPixmap(QtGui.QPixmap.fromImage(showImage1))
        self.label_show_camera2.setPixmap(QtGui.QPixmap.fromImage(showImage2))
        
        massage=massage+"test\n"
        self.label_text.setText(massage)

    def slot_init(self):
        self.button_open_camera_clicked()
        self.timer_camera.timeout.connect(self.consumer)#按下開啟後執行
        self.button_close.clicked.connect(self.close)

    def button_click(self):
        flag,self.image = self.cap.read()
        for i in range(10000):
            flag,self.image = self.cap.read()
            #q.put(self.image)
            #img=q.get()
            show = cv2.resize(self.image,(640,480))   
            show = cv2.cvtColor(show,cv2.COLOR_BGR2RGB) 
            showImage = QtGui.QImage(show.data,show.shape[1],show.shape[0],QtGui.QImage.Format_RGB888) 
            self.label_show_camera.setPixmap(QtGui.QPixmap.fromImage(showImage))
            time.sleep(10)
    def button_open_camera_clicked(self):
        if self.timer_camera.isActive() == False:
            flag = self.cap.open(self.CAM_NUM)
            if flag == False:       
                msg = QtWidgets.QMessageBox.warning(self,'warning',"無連接相機",buttons=QtWidgets.QMessageBox.Ok)
            else:
                self.timer_camera.start(1)#幾MS取一次圖
                self.button_open_camera.setText('關閉相機')
        else:
            self.timer_camera.stop()
            self.cap.release()
            self.label_show_camera.clear()
            self.button_open_camera.setText('打開相機')
    def read_cam(self):

        flag,self.image = self.cap.read()
        q.put(self.image)
        img=q.get()
        show = cv2.resize(img,(640,480))   
        show = cv2.cvtColor(show,cv2.COLOR_BGR2RGB) 
        showImage = QtGui.QImage(show.data,show.shape[1],show.shape[0],QtGui.QImage.Format_RGB888) 
        self.label_show_camera.setPixmap(QtGui.QPixmap.fromImage(showImage))
        #p.terminate()
    def show_camera(self):
        flag,self.image1 = self.cap1.read()
        q1.put(self.image1)
        img=q1.get()
        show = cv2.resize(img,(640,480))   
        show = cv2.cvtColor(show,cv2.COLOR_BGR2RGB) 
        showImage = QtGui.QImage(show.data,show.shape[1],show.shape[0],QtGui.QImage.Format_RGB888)
        self.label_show_camera2.setPixmap(QtGui.QPixmap.fromImage(showImage))
        #p1.terminate()
    def multishow(self):
            self.show_camera()
            self.read_cam()
            #p = Process(target=self.read_cam)
            #p.start()
            #p1 = Process(target=self.show_camera)
            #p1.start()
def producer(q):
    cap = cv2.VideoCapture(0)
    while True:
        print('producer execuation')
        if cap.isOpened():
            ret, img = cap.read()
            q.put(img)
def producer2():

    cap = cv2.VideoCapture(0)

    while True:
        print('producer execuation')
        if cap.isOpened():
            ret, img = cap.read()
            q.put(img)

    
if __name__ =='__main__':
    m = Manager()

    q_step1 = m.Queue(120)
    q_step2 = m.Queue(60)
    # a = [q_step1, q_step1]
    # b = ["GH050039_1.MP4", "GH050039_2.MP4"]
    # c = [0, 1]
    w = Process(target=weight, args=(q_step1, q_step2))
    w.start()
    # video_pool = Pool(2)
    # video_pool.starmap(video_load, zip(a, b, c))

    s = Process(target=show, args=(q_step2, ))
    v = Process(target=video_load, args=(q_step1, 'GH050039_1.MP4', 0))

    v1 = Process(target=video_load_1, args=(q_step1, 'GH050039_2.MP4', 1))
    print('ddone')

    s.start()
    v.start()
    v1.start()


    #p1 = Process(target=producer, args=(q,))

    #p1.start()

    app = QtWidgets.QApplication(sys.argv) 
    ui = Ui_MainWindow()                    
    ui.show()                               
    sys.exit(app.exec_())
    v.join()
    v1.join()
    w.join()
    s.join()