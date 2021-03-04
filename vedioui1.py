import os
import cv2
import sys
import time
import mxnet as mx
import detector as dc
import classSet as cls
from cameraSet import video_load, video_load_1
from gluoncv.model_zoo import get_model
from PyQt5 import QtCore, QtGui, QtWidgets
from multiprocessing import Process, Pool, Queue, Manager
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import xlsxwriter
import pyglet

workbook = xlsxwriter.Workbook('demo.xlsx')
worksheet = workbook.add_worksheet()
worksheet.set_column('A:A', 30)
worksheet.set_column('B:B', 30)
worksheet.set_column('C:C', 30)
worksheet.set_column('D:D', 30)
worksheet.set_column('E:E', 30)
bold = workbook.add_format({'bold': True})
worksheet.write('A1', '類別')
worksheet.write('B1', '經緯度')
worksheet.write('C1', '百公尺樁')
worksheet.write('D1', '時間')
worksheet.write('E1', '圖片')
# worksheet.write(2, 0, 123)
# worksheet.write(3, 1, 123.456)

massage=""
massage2=""
bindex = 0
bkindex=0
writeindex=1;
bname = "./image/break"
array_of_img = []
class Ui_MainWindow(QtWidgets.QWidget):
    def __init__(self, q_for_show, q_for_v, parent=None):
        super().__init__(parent)
        self.timer_camera = QtCore.QTimer()
        self.q_for_show = q_for_show
        self.q_for_video = q_for_v
        # self.cap = cv2.VideoCapture(0)
        # self.cap1 = cv2.VideoCapture(1)
        self.CAM_NUM = 0
 
        self.set_ui()
        self.slot_init()
    def set_ui(self):
        self.__layout_main = QtWidgets.QVBoxLayout()
        self.__layout_vedio = QtWidgets.QHBoxLayout()
        self.__layout_text = QtWidgets.QHBoxLayout()
        self.label_show_camera = QtWidgets.QLabel()
        self.label_show_camera.setFixedSize(641,481)
        self.label_show_camera2 = QtWidgets.QLabel()
        self.label_show_camera2.setFixedSize(641,481)
        self.label_show_camera3 = QtWidgets.QLabel()
        self.label_show_camera3.setFixedSize(641,481)
        self.label_title = QtWidgets.QLabel(self)
        self.label_title.resize(1923,100)
        self.label_title.setAlignment(Qt.AlignCenter)
        self.label_title.setFont(QFont("Roman times",30,QFont.Bold))
        # self.label_title.setStyleSheet()
        self.label_text = QtWidgets.QTextBrowser(self)
        self.label_text.resize(962,200)
        self.label_text.setFont(QFont("Roman times",14,QFont.Bold))
        self.label_text2 = QtWidgets.QTextBrowser(self)
        self.label_text2.resize(962,200)
        self.label_text2.setFont(QFont("Roman times",14,QFont.Bold))
        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setWidget(self.label_text)
        self.scroll2 = QtWidgets.QScrollArea()
        self.scroll2.setWidget(self.label_text2)
        self.__layout_vedio.addWidget(self.label_show_camera)
        self.__layout_vedio.addWidget(self.label_show_camera2)
        self.__layout_vedio.addWidget(self.label_show_camera3)
        self.__layout_text.addWidget(self.scroll)
        self.__layout_text.addWidget(self.scroll2)
        self.__layout_main.addWidget(self.label_title)
        self.__layout_main.addLayout(self.__layout_vedio)
        self.__layout_main.addLayout(self.__layout_text)
        self.setLayout(self.__layout_main)
        

    def consumer(self):
        if self.q_for_show.empty(): return
        imgA = self.q_for_show.get() 
        global massage,massage2
        img = imgA.get_image()
        
        show = cv2.resize(img,(640,480))   
        show = cv2.cvtColor(show,cv2.COLOR_BGR2RGB) 
        showImage = QtGui.QImage(show.data,show.shape[1],show.shape[0],QtGui.QImage.Format_RGB888)             
        if(imgA.get_cap_number() == 0): 
            self.label_show_camera.setPixmap(QtGui.QPixmap.fromImage(showImage))
        else : 
            self.label_show_camera2.setPixmap(QtGui.QPixmap.fromImage(showImage))

        global bindex,bkindex,array_of_img,writeindex    
        if(imgA.get_break() == True):
            music = pyglet.resource.media('1.mp3', streaming=False)
            music.play()
            bkindex = bindex
            savename = bname+str(bindex)+".jpg"
            bindex = bindex+1
            cv2.imwrite(savename, img)
            array_of_img.append(img)
            self.label_show_camera3.setPixmap(QtGui.QPixmap.fromImage(showImage))
            if(imgA.get_cap_number() == 0):
                massage = "時間:"+imgA.time+" 類別:"+imgA.get_break_name()+"經緯度:"+imgA.gps+" 百公尺樁:"+imgA.location+"\n"
                self.label_text.append(massage)
                self.label_text.moveCursor(self.label_text.textCursor().End)
                # self.cursor = self.label_text.textCursor()
                # self.label_text.moveCursor(self.cursor.End)
                worksheet.write(writeindex, 0, imgA.get_break_name())
                worksheet.write(writeindex, 1, imgA.gps)
                worksheet.write(writeindex, 2, imgA.location)
                worksheet.write(writeindex, 3, imgA.time)
                worksheet.write_url(writeindex,4,savename)
                writeindex = writeindex+1
            else:
                massage2 = "時間:"+imgA.time+" 類別:"+imgA.get_break_name()+"經緯度:"+imgA.gps+" 百公尺樁:"+imgA.location+"\n"
                self.label_text2.append(massage2)
                self.label_text2.moveCursor(self.label_text2.textCursor().End)
                # self.cursor = self.label_text2.textCursor()
                # self.label_text2.moveCursor(self.cursor.End)
                worksheet.write(writeindex, 0, imgA.get_break_name())
                worksheet.write(writeindex, 1, imgA.gps)
                worksheet.write(writeindex, 2, imgA.location)
                worksheet.write(writeindex, 3, imgA.time)
                # worksheet.insert_image(writeindex,4,'H:\\20201204\\image\\'+savename,{'url':'http://www.python.org'})
                worksheet.write_url(writeindex,4,savename)
                writeindex = writeindex+1
            #self.getbimg()           
        del imgA

    def keyPressEvent(self, event):
        global bkindex
        if  event.key() == Qt.Key_K:
            bkindex = bkindex - 1
            if bkindex<0:
                bkindex=0
            img=array_of_img[bkindex]
            # show = cv2.cvtColor(array_of_img[bkindex],cv2.COLOR_BGR2RGB)
            show = cv2.resize(img,(640,480))   
            show = cv2.cvtColor(show,cv2.COLOR_BGR2RGB) 
            showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888) 
            self.label_show_camera3.setPixmap(QtGui.QPixmap.fromImage(showImage))
            # self.label_text.append('you press Shift+A !')
        
        elif event.key() == Qt.Key_L:
            bkindex = bkindex + 1
            if bkindex>=bindex:
                bkindex=bindex-1
            img=array_of_img[bkindex]
            show = cv2.resize(img, (640, 480))   
            show = cv2.cvtColor(show,cv2.COLOR_BGR2RGB) 
            showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888) 
            self.label_show_camera3.setPixmap(QtGui.QPixmap.fromImage(showImage))
        # elif event.key() == Qt.Key_Return:
        #     self.label_text.append('you press enter !')

        # else:
        #     #使用該按鍵的預設動作
        #     QWidget.keyPressEvent(self, event)

    def getbimg(self):
        print("get")
        global array_of_img
        for filename in os.listdir(r"./image"):
            print(filename)
            img = cv2.imread("./image/" + filename)
            array_of_img.append(img)
        print(array_of_img)
        
    def closeEvent(self, event):
        ok = QtWidgets.QPushButton()
        cancel = QtWidgets.QPushButton()
        msg = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, u'關閉', u'是否關閉！')
        msg.addButton(ok, QtWidgets.QMessageBox.ActionRole)
        msg.addButton(cancel, QtWidgets.QMessageBox.RejectRole)
        ok.setText(u'確定')
        cancel.setText(u'取消')
        if msg.exec_() == QtWidgets.QMessageBox.RejectRole:
            event.ignore()
        else:
            workbook.close()
            p1.terminate()
            c.terminate()
            c1.terminate()
            if not self.q_for_show.empty():
                self.q_for_show.close()
            if not self.q_for_video.empty():
                self.q_for_video.close()
            event.accept()



    def slot_init(self):
        self.button_open_camera_clicked()
        self.timer_camera.timeout.connect(self.consumer)#按下開啟後執行

            
    def button_open_camera_clicked(self):
        self.label_title.setText("軌道扣件即時辨識系統")
        img = cv2.imread('load.jpg')
        show = cv2.resize(img,(640,480))   
        show = cv2.cvtColor(show,cv2.COLOR_BGR2RGB) 
        showImage = QtGui.QImage(show.data,show.shape[1],show.shape[0],QtGui.QImage.Format_RGB888) 
        self.label_show_camera.setPixmap(QtGui.QPixmap.fromImage(showImage))
        self.label_show_camera2.setPixmap(QtGui.QPixmap.fromImage(showImage))
        if self.timer_camera.isActive() == False:    
            self.timer_camera.start(22)#幾MS取一次圖


def producer(q, q_for_v):
    dataclass = cls.getClass()
    classcolor = cls.getColor()

    net = get_model('ssd_300_vgg16_atrous_custom', classes=dataclass, transfer='voc' , pretrained_base=False, pretrained=False, ctx=mx.gpu())#modify mx.cpu(), gpu()
    net.load_parameters(r'./weight/ssd_300_ssd_512_vgg16_atrous_voc_1000_0.8837.params')
    net.collect_params().reset_ctx([mx.gpu()])
    net.hybridize()
    print('[OK] detector is ready.')

    while q_for_v.empty() : time.sleep(0.01)
    
    while not q_for_v.empty() :
        start = time.time()
        imgA = q_for_v.get()
        x = imgA.get_tensors()
        x = x.as_in_context(mx.gpu())

        class_IDs, scores, bounding_boxes = net(x)

        imgA.set_deteced_value(bounding_boxes[0], class_IDs[0], scores)
        
        # if q.empty() : print("q is empty")
        # if q.full() : print("q is full")
        imgA.draw_bbox()
        imgA.draw_shit(1/(time.time()-start))
        while q.full() : time.sleep(0.01) # if q_video_out(funtion : show)is busy wait
        q.put(imgA) # else put imgA in Queue
    


if __name__ =='__main__':
    try : 
        os.mkdir("image")
    except : 
        pass

    q = Queue(100)
    q_for_v = Queue(50)
    app = QtWidgets.QApplication(sys.argv) 
    ui = Ui_MainWindow(q, q_for_v)
    p1 = Process(target=producer, args=(q, q_for_v))
    c = Process(target=video_load, args=(q_for_v, r'./gopro8(1)_best.mp4', 0))
    c1 = Process(target=video_load_1, args=(q_for_v, r'./gopro8(2)_best.mp4', 1))

    ui.show()                    
    p1.start()
    c.start()
    c1.start()
    
    sys.exit(app.exec_())
    p1.join()
    c.join()
    c1.join()
    q_for_v.join()
    q.join()
    # q_for_v.close()
    # q.close()
