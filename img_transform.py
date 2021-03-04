import numpy as np
import mxnet as mx
from mxnet.image.image import _get_interp_method as get_interp

def imgs_fname_transform(filenames, short=300, max_size=1024, mean=(0.485, 0.456, 0.406),
               std=(0.229, 0.224, 0.225)):
    filenames = [filenames]
    imgs = [mx.image.imread(f) for f in filenames]
    return imgs_transform(imgs, short, max_size, mean, std)

def imgs_transform(imgs, short=300, max_size=1024, mean=(0.485, 0.456, 0.406),
                   std=(0.229, 0.224, 0.225)):
    if isinstance(imgs, mx.ndarray.ndarray.NDArray) : imgs = [imgs]
    tensors = []
    origs = []
    for img in imgs:
        img = resize_short_within(img, short, max_size)
        orig_img = img.asnumpy().astype('uint8')
        img = mx.nd.image.to_tensor(img)
        img = mx.nd.image.normalize(img, mean=mean, std=std)
        tensors.append(img.expand_dims(0))
        origs.append(orig_img)
    if len(tensors) == 1:
        return tensors[0], origs[0]
    return tensors, origs

def resize_short_within(src, short, max_size, mult_base=1, interp=2):
    h, w, _ = src.shape # _ = len
    im_size_min, im_size_max = (h, w) if w > h else (w, h)
    scale = float(short) / float(im_size_min)
    if np.round(scale * im_size_max / mult_base) * mult_base > max_size:
        # fit in max_size
        scale = float(np.floor(max_size / mult_base) * mult_base) / float(im_size_max)
    new_w, new_h = (int(np.round(w * scale / mult_base) * mult_base),
                    int(np.round(h * scale / mult_base) * mult_base))
    return imresize(src, new_w, new_h, interp=get_interp(interp, (h, w, new_h, new_w)))

def imresize(src, w, h, interp=1):
    oh, ow, _ = src.shape # len
    return mx.image.imresize(src, w, h, interp=get_interp(interp, (oh, ow, h, w)))
