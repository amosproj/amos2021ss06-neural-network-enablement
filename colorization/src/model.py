import cv2

def model_process(modelPath):
    model_file = modelPath + 'colorization.prototxt'
    pretrained_network = modelPath + 'colorization.caffemodel'
    caffe_net = cv2.dnn.readNetFromCaffe(model_file,pretrained_network)
    caffe_net.set_mode_cpu()
    caffe_net.setInput(cv2.dnn.blobFromImage(l_channel))
    ab_channel = caffe_net.forward()[0,:,:,:].transpose((1,2,0))
