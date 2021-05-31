import os
import acl
import acl_constants


def IsDirectory(inputpath):
    """This function checks whether a given path is a file.
             Parameters:
            -----------
            inputpath : str
            return value :
                Return True if path is an existing regular file
                Otherwise Return False
            """
    return os.path.isfile(inputpath)


def IsPathExist(inputpath):
    """This function checks whether a given path exists.
             Parameters:
            -----------
            inputpath : str
            return value :
                Return True if path refers to an existing path or an open file descriptor
                Returns False for broken symbolic links.
            """
    return os.path.exists(inputpath)


# has never been referenced
# def SplitPath(inputpath):
# def GetPathFiles(inputpath):


def GetAllFiles(inputpath):
    """This function is used to get all file names under a certain path.
             Parameters:
            -----------
            inputpath : str
            return value :
                Return a list containing the names of the entries in the directory
                given by path
            """
    return os.listdir(inputpath)


def CopyDataDeviceToHost(deviceData, dataSize):
    # malloc for memory on host
    host_ptr, malret = acl.rt.malloc_host(dataSize)
    # check malloc success
    if malret == 0:
        # copy from device to host
        cpyret = acl.rt.memcpy(host_ptr, dataSize, deviceData, dataSize,
                               acl_constants.ACL_MEMCPY_DEVICE_TO_HOST)
        if cpyret == 0:
            freehostret = acl.rt.free_host(host_ptr)
            return host_ptr
        else:
            #copy fails
            return 1
    else:
        #malloc fails
        return 1
