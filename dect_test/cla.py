import cv2
import mxnet as mx
from matplotlib import pyplot as plt
from gluoncv import model_zoo, data, utils
from gluoncv.model_zoo import get_model
from gluoncv import model_zoo, utils
from ownGluoncv import data


class dect():

    def __init__(self, num, im_fname):
        self.img = im_fname
        self.Bool_For_Detect = False
        self.CapNumber = num
        self.bbox = []

    def ID_Score(self, bboxes, class_IDs, scores): #, txt_fname 加在要求傳入參數最後一項
        #轉換ndarray到一般array
        if isinstance(class_IDs, mx.nd.NDArray) and isinstance(scores, mx.nd.NDArray):
            bboxes1 = bboxes.asnumpy()
            cls_id = class_IDs.asnumpy()
            scores1 = scores.asnumpy()
        flage = 2
        for r in range(len(cls_id)):
            if float(scores1[-1][r])<0.5:break
            if int(cls_id[r])==0:flage=0
            elif int(cls_id[r])==1:flage=1
            elif int(cls_id[r])==2:flage=2
            elif int(cls_id[r])==3:flage=3
            elif int(cls_id[r])==4:flage=4
        if flage!=2:
            #f = open(aft_txt+txt_fname, 'w')
            pass
        else:return 0
        #比較class, score
        for r in range(len(cls_id)):
            if float(scores1[-1][r])<0.5:break
            self.bbox.append(list())

            self.bbox[r].append(round(scores1[-1][r][0], 2)) #加入分數
            for i in range(4) : self.bbox[r].append(int(bboxes1[r][i])) #加入bbox
            #print(self.getBBox())
            #print(tmpArr)
            #xmin = int(bboxes1[0][0])
            #ymin = int(bboxes1[0][1])
            #xmax = int(bboxes1[0][2])
            #ymax = int(bboxes1[0][3])
            #f.write(dataclass[int(cls_id[r])]+' '+str(xmin)+' '+str(ymin)+' '+str(xmax)+' '+str(ymax)+'\n')
            #print(dataclass[int(cls_id[r])], str(scores1[-1][r]), str(bboxes1[0][0]), str(bboxes1[0][1]))
        #f.close()
        return 1

    def setBBox(self, tmpArr):
        self.bbox.append(tmpArr)

    def getBBox(self):
        return self.bbox


    def getImage(self):
        return self.img

    def getX(self):
        return data.transforms.presets.ssd.transform_test(self.img, 768, 1024, (0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
        #(filenames, short, max_size=1024, mean=(0.485, 0.456, 0.406),std=(0.229, 0.224, 0.225))
    
    def startDetec(self, net):
        return
