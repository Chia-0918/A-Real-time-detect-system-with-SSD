print("loading...")

import time
import cla
import bbox
import classSet as cls
from gluoncv.model_zoo import get_model
from gluoncv import model_zoo, utils
from ownGluoncv import data
from matplotlib import pyplot as plt
import mxnet as mx


if __name__ == '__main__':
    print("Done. Start execute!")
    time.sleep(2)
    dataclass = cls.getClass()
    classcolor = cls.getColor()
    print(dataclass)

    net = model_zoo.get_model('ssd_512_vgg16_atrous_custom', classes=dataclass, transfer='voc' , pretrained_base=False, pretrained=False, ctx=mx.gpu())#modify mx.cpu(), gpu()

    print("Loading model ssd_512_vgg16_atrous_voc_0066_0.9462.params....")
    MODEL_Load_time_Start = time.time()
    net.load_parameters('ssd_512_vgg16_atrous_voc_0066_0.9462.params')
    MODEL_Load_time_End = time.time()
    print("Loading model use {:.3f} sec".format(MODEL_Load_time_End - MODEL_Load_time_Start))

    im_fname = 'wood_crossties_break_18.jpg'
    
    imgA = cla.dect(0, im_fname)

    x, img = data.transforms.presets.ssd.transform_test(imgA.getImage(), 512, 1024, (0.485, 0.456, 0.406),
              (0.229, 0.224, 0.225))
    yy = x.as_in_context(mx.gpu())


    MODEL_Detect_time_Start = time .time()
    class_IDs, scores, bounding_boxes = net(yy)
    MODEL_Detect_time_End = time.time()
    print("{:.3f}sec".format((MODEL_Detect_time_End - MODEL_Detect_time_Start)))

    imgA.ID_Score(bounding_boxes[0], class_IDs[0], scores)
    print("imgA.getBBox() : ", imgA.getBBox())

    ax = utils.viz.plot_bbox(img, bounding_boxes[0], scores[0],
                        class_IDs[0], class_names=net.classes, colors=classcolor)

    plt.show()
    """
    x.as_in_context(mx.gpu())

    class_IDs, scores, bounding_boxes = net(x)
    img.ID_Score(bounding_boxes[0], class_IDs[0], scores)
    ax = cv_plot_bbox(img, bounding_boxes[0], scores[0],
                        class_IDs[0], class_names=net.classes, colors=classcolor)

    plt.show()

    
    x, img = data.transforms.presets.ssd.load_test(im_fname, short=512, max_size=1920)
    x = x.as_in_context(mx.gpu())

    print('Shape of pre-processed image:', x.shape)

    class_IDs, scores, bounding_boxes = net(x)
    ID_Score(bounding_boxes[0], class_IDs[0], scores)

    ax = utils.viz.plot_bbox(img, bounding_boxes[0], scores[0],
                            class_IDs[0], class_names=net.classes, colors=classcolor)

    plt.show()
    """
    
    