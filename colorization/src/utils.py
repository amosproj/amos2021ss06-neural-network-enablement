import os
import acl

def IsDirectory(inputpath):
    return os.path.isfile(inputpath)

def IsPathExist(inputpath):
    return os.path.exists(inputpath)

# has never been referenced
# def SplitPath(inputpath):
# def GetPathFiles(inputpath):

def GetAllFiles(inputpath):
    return os.listdir(inputpath)


def CopyDataDeviceToHost(deviceData,dataSize):
    # malloc for memory on host
    host_ptr, malret = acl.rt.malloc_host(dataSize)
    # check malloc success
    if malret == 0:
        # copy from device to host
        cpyret = acl.rt.memcpy(host_ptr, dataSize, deviceData, dataSize, ACL_MEMCPY_DEVICE_TO_HOST)
        if cpyret == 0:
            freehostret = acl.rt.free_host(host_ptr)
            return host_ptr
        else:
            #copy fails
            return 1
    else:
        #malloc fails
        return 1