import cv2
import time
import mxnet as mx
import classSet as Cs
from img_transform import imgs_transform, imgs_fname_transform
from matplotlib import pyplot as plt


class detetor():
    def __init__(self, cap_Num, image, gps_data):
        if isinstance(image, str) : 
            self.tensors, self.image = imgs_fname_transform(image)
        else : 
            self.tensors, self.image = imgs_transform(image) # define in img_transform
        self.Bool_For_Detect = False
        self.CapNumber = cap_Num
        self.bbox = []
        self.class_name = Cs.getClass()
        self.class_color = Cs.getColor()
        self.gps = "25.0671544,121.521804"
        self.location = "KFFF+000" # Hundred-meter pile
        self.time = time.asctime(time.localtime(time.time()))
        #class_IDs, scores, bounding_boxes

    def get_tensors(self):
        return self.tensors
        
    def get_locations(self):
        return self.location
    
    def get_image(self):
        return self.image

    def get_cap_number(self):
        return self.CapNumber

    def get_break(self):
        return self.Bool_For_Detect
        
    def get_break_name(self):
        for i in range(len(self.bbox)):           
            if self.bbox[i][0]==1 or self.bbox[i][0]==3 or self.bbox[i][0]==7 or self.bbox[i][0]==8: return self.class_name[self.bbox[i][0]]

    def set_deteced_value(self, bboxes, class_IDs, scores):
        # if isinstance(class_IDs, mx.nd.NDArray) and isinstance(scores, mx.nd.NDArray): #check data type
        #     bboxes1 = bboxes.asnumpy()
        #     cls_id = class_IDs.asnumpy()
        #     scores1 = scores.asnumpy()
        bboxes1 = bboxes.asnumpy()
        cls_id = class_IDs.asnumpy()
        scores1 = scores.asnumpy()
        for r in range(len(cls_id)):
            if float(scores1[-1][r]) < 0.5 : break
            rectangle_detc = (int(cls_id[r])
                            , int(bboxes1[r][0])
                            , int(bboxes1[r][1])
                            , int(bboxes1[r][2])
                            , int(bboxes1[r][3]))
            self.bbox.append(rectangle_detc)
        #if len(self.bbox)>0 : self.Bool_For_Detect = True

    def draw_bbox(self):
        # print(len(self.bbox))
        for i in range(len(self.bbox)):
            # set rectangle value
            _min = (self.bbox[i][1], self.bbox[i][2])
            _max = (self.bbox[i][3], self.bbox[i][4])
            color = self.class_color[self.bbox[i][0]]
            # print(color)
            # set Text value
            Text = self.class_name[self.bbox[i][0]]
            if self.bbox[i][0]==1 or self.bbox[i][0]==3 or self.bbox[i][0]==7 or self.bbox[i][0]==8: self.Bool_For_Detect = True
            # draw picture
            cv2.rectangle(self.image, _min, _max, color, 2)
            cv2.putText(self.image, Text, _max, cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 2)# 圖片、添加的文字，左上角的坐標、字體、字體大小、顏色、字體粗細。
            # self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            
    def draw_shit(self, fps):
        Text = self.time + "  " + self.location  + "    fps: " + "{:.2f}". format(fps)
        cv2.putText(self.image, Text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (2, 232, 64), 2)# 圖片、添加的文字，左上角的坐標、字體、字體大小、顏色、字體粗細。


    def show_img(self):
        cv2.imshow('My_Image', self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()








