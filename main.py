import time
import cv2
import mxnet as mx
import detector as dc
import classSet as cls
from cameraSet import video_load, video_load_1
from gluoncv.model_zoo import get_model
from multiprocessing import Process, Pool, Queue, Manager


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
    while q_video_show.empty() : time.sleep(0.5) # wait for detect

    while not q_video_show.empty():
        imgA = q_video_show.get() # get and draw
        imgA.draw_bbox()
        img = imgA.get_image()

        if imgA.get_cap_number() == 0 : cv2.imshow('My_Image_0', img)
        else : cv2.imshow('My_Image_1', img)
        cv2.waitKey(63)

    cv2.destroyAllWindows()





# if __name__ == '__main__':
#     m = Manager()
#     q_step1 = m.Queue(120)
#     q_step2 = m.Queue(60)

#     # a = [q_step1, q_step1]
#     # b = ["GH050039_1.MP4", "GH050039_2.MP4"]
#     # c = [0, 1]

#     w = Process(target=weight, args=(q_step1, q_step2))
#     w.start()
#     # video_pool = Pool(2)
#     # video_pool.starmap(video_load, zip(a, b, c))

#     s = Process(target=show, args=(q_step2, ))
#     v = Process(target=video_load, args=(q_step1, 'GH050039_1.MP4', 0))

#     v1 = Process(target=video_load_1, args=(q_step1, 'GH050039_2.MP4', 1))
#     print('ddone')

#     s.start()
#     v.start()
#     v1.start()
#     v.join()
#     v1.join()
#     w.join()
#     s.join()



if __name__ == '__main__':
    dataclass = cls.getClass()
    classcolor = cls.getColor()
    print(dataclass)

    net = get_model('ssd_512_vgg16_atrous_custom', classes=dataclass, transfer='voc' , pretrained_base=False, pretrained=False, ctx=mx.gpu())#modify mx.cpu(), gpu()

    net.load_parameters('ssd_512_vgg16_atrous_voc_4220_0.8260.params')
    net.collect_params().reset_ctx([mx.gpu()])
    net.hybridize()

    im_fname = '10005000607.985.jpg'
    
    imgA = dc.detetor(0, im_fname)

    x = imgA.get_tensors()
    x = x.as_in_context(mx.gpu())

    class_IDs, scores, bounding_boxes = net(x)

    imgA.set_deteced_value(bounding_boxes[0], class_IDs[0], scores)

    imgA.draw_bbox()
    imgA.show_img()

