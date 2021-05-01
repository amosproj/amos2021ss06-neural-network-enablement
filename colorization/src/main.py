import cv2
import numpy as np
import numpy.linalg as la
import pyACL
import utils

# #include <iostream> #//是C++中用于数据的流式输入与输出的头文件，C++标准程式库的一部分.「流」是一連串從I/O設備讀寫的字符。
# #include <stdlib.h> #//C的标准库,定义了C的常用函数
# #include <dirent.h> #//POSIX.1标准定义的unix类目录操作的头文件,包含了许多UNIX系统服务的函数原型,例如opendir函数、readdir函数。 opendir函数
#
# #include "colorize_process.h" #//另一个已定义的头文件
# #include "utils.h" #//另一个已定义的头文件

# using namespace std; #//namespace:指标识符的各种可见范围。C++标准程序库中的所有标识符都被定义于一个名为std的namespace中。
# //当使用<iostream>时，该头文件没有定义全局命名空间，必须使用namespace std，这样才能使用类似于cout这样的C++标识符。
# namespace {
# uint32_t kModelWidth = 224;
# uint32_t kModelHeight = 224;
# const char* kModelPath = "../model/colorization.om";
# }

# // python 中不需要main，可以拆分main的每一步单独写functions，并且无需检验输入项
# int main(int argc, char *argv[]) {
#     //检查应用程序执行时的输入,程序执行要求输入图片目录参数
#     if((argc < 2) || (argv[1] == nullptr)){
#         ERROR_LOG("Please input: ./main <image_dir>");
#         return FAILED;
#     }

# // 第一步：程序执行要求输入图片目录参数, 已知input为一张黑白图片，用灰阶图读取函数，尝试返回无效值
def inputcheck (path): # example path = "./bear_left.jpg"
    # 如果图片unvalid，main 为失败
    if inputImageDir == None:
        print("Oops!  That was no valid number.  Try again...")
        return 0
    else:
        inputImageDir = cv2.imread(path, # parameter：" "中input图片路径，cv2.IMREAD_GRAYSCALE为灰阶读取参数
                                   cv2.IMREAD_GRAYSCALE)
    return 1


#     //实例化分类推理对象,参数为分类模型路径,模型输入要求的宽和高
#     ColorizeProcess colorize(kModelPath, kModelWidth, kModelHeight);
#     //初始化分类推理的acl资源, 模型和内存
#     Result ret = colorize.Init();
#     if (ret != SUCCESS) {
#         ERROR_LOG("Classification Init resource failed");
#         return FAILED;
#     }



#     //获取图片目录下所有的图片文件名
#     string inputImageDir = string(argv[1]);
#     vector<string> fileVec;
#     Utils::GetAllFiles(inputImageDir, fileVec);
#     if (fileVec.empty()) {
#         ERROR_LOG("Failed to deal all empty path=%s.", inputImageDir.c_str());
#         return FAILED;
#     }
#     //逐张图片推理
#     for (string imageFile : fileVec) {
#         //预处理图片:读取图片,讲图片缩放到模型输入要求的尺寸
#         Result ret = colorize.Preprocess(imageFile);
#         if (ret != SUCCESS) {
#             ERROR_LOG("Read file %s failed, continue to read next",
#                       imageFile.c_str());
#             continue;
#         }
#         //将预处理的图片送入模型推理,并获取推理结果
#         aclmdlDataset* inferenceOutput = nullptr;
#         ret = colorize.Inference(inferenceOutput);
#         if ((ret != SUCCESS) || (inferenceOutput == nullptr)) {
#             ERROR_LOG("Inference model inference output data failed");
#             return FAILED;
#         }
#         //解析推理输出,并将推理得到的物体类别标记到图片上
#         ret = colorize.Postprocess(imageFile, inferenceOutput);
#         if (ret != SUCCESS) {
#             ERROR_LOG("Process model inference output data failed");
#             return FAILED;
#         }
#     }
#
#     INFO_LOG("Execute sample success");
#     return SUCCESS;
# }
