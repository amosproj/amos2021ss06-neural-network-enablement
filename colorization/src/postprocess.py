import cv2
import numpy as np

def postprocess(origImageFile,modelOutput):

     # reading the inference_image

     inference_result = cv2.imread(modelOutput)
     inference_result = cv2.resize(inference_result,(300,300))
     cv2.imshow('Inference_result', inference_result)
     cv2.waitKey(0)
     cv2.destroyAllWindows()

    # get ab channels from the model output
     a,b = cv2.split(inference_result)

     # pull out L channel in original/source image

     input_image = cv2.imread(origImageFile,cv2.IMREAD_COLOR)  # reading input image
     input_image = cv2.resize(input_image,(300,300))
     input_image = np.float32(input_image)
     input_image = 1.0 * input_image/255     # Normalizing the input image values
     bgrtolab = cv2.cvtColor(input_image, cv2.COLOR_BGR2LAB)
     cv2.imshow("Lab_channel", bgrtolab)
     (L,A,B) = cv2.split(bgrtolab)
     cv2.imshow("L_channel", L)
     cv2.imshow("A_channel", A)
     cv2.imshow("B_channel", B)
     cv2.waitKey(0)
     cv2.destroyAllWindows()

     # resize to match the size of original image L

     height = input_image[0]
     width = input_image[1]
     a_channel = cv2.resize(a,(height,width))
     b_channel = cv2.resize(b,(height,width))


     # result Lab image

     result_image = cv2.merge(L,a_channel,b_channel)
     cv2.imshow('result_image',result_image)

     # convert back to rgb

     output_image = cv2.cvtColor(result_image,cv2.COLOR_Lab2BGR)
     output_image = output_image*255
     cv2.imshow('output_image',output_image)

     return output_image