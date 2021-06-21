import acl
import numpy as np
import datetime
from atlas_utils.utils import *
from atlas_utils.acl_image import AclImage


class Model(object):
    def __init__(self, acl_resource, model_path):
        self._run_mode = acl_resource.run_mode
        self.model_path = model_path    # string
        self.model_id = None            # pointer
        self.input_dataset = None
        self.output_dataset = None
        self._output_info = []
        self.model_desc = None          # pointer when using
        self._init_resource()
        

    def __del__(self):
        if self.input_dataset:
            self._release_dataset(self.input_dataset)        
        if self.output_dataset:
            self._release_dataset(self.output_dataset)
        if self.model_id:
            ret = acl.mdl.unload(self.model_id)
            if ret != ACL_ERROR_NONE:
                print("acl.mdl.unload error:", ret)
        if self.model_desc:
            ret = acl.mdl.destroy_desc(self.model_desc)
            if ret != ACL_ERROR_NONE:
                print("acl.mdl.destroy_desc error:", ret)
        print("Model release source success")

    def _init_resource(self):
        print("Init model resource")
        # loading model file
        self.model_id, ret = acl.mdl.load_from_file(self.model_path)
        check_ret("acl.mdl.load_from_file", ret)
        self.model_desc = acl.mdl.create_desc()
        ret = acl.mdl.get_desc(self.model_desc, self.model_id)
        check_ret("acl.mdl.get_desc", ret)
        # obtain model outputs number
        output_size = acl.mdl.get_num_outputs(self.model_desc)
        # create model output dataset structure
        self._gen_output_dataset(output_size)
        print("[Model] class Model init resource stage success")
        # obtain shape and type of each output of the model
        self._get_output_desc(output_size)
        # create a table to record memory for input data, which can be reused when allocating memory for the input
        self._init_input_buffer()

        return SUCCESS

    def _get_output_desc(self, output_size):
        for i in range(output_size):
            # obtain shape and type of each output
            dims = acl.mdl.get_output_dims(self.model_desc, i)
            shape = tuple(dims[0]["dims"])
            datatype = acl.mdl.get_output_data_type(self.model_desc, i)
            size = acl.mdl.get_output_size_by_index(self.model_desc, i)

            if datatype == ACL_FLOAT:
                np_type = np.float32            
            elif datatype == ACL_INT32:
                np_type = np.int32
            elif datatype == ACL_UINT32:
                np_type = np.uint32
            else:
                print("Unspport model output datatype ", datatype)
                return None
            # create a numpy array corresponding to outputs, with the same datatype and shape of outputs        
            output_tensor = np.zeros(size//4, dtype=np_type).reshape(shape)
            if not output_tensor.flags['C_CONTIGUOUS']:
                output_tensor = np.ascontiguousarray(output_tensor)

            tensor_ptr = acl.util.numpy_to_ptr(output_tensor)           
            self._output_info.append({"ptr": tensor_ptr,
                                      "tensor": output_tensor})            

    def _gen_output_dataset(self, size):
        print("[Model] create model output dataset:")
        dataset = acl.mdl.create_dataset()
        for i in range(size):
            # allocate device memory for each output
            size = acl.mdl.get_output_size_by_index(self.model_desc, i)
            buffer, ret = acl.rt.malloc(size, ACL_MEM_MALLOC_NORMAL_ONLY)
            check_ret("acl.rt.malloc", ret)
            # create output data buffer structure, fill allocated memory into the data buffer
            dataset_buffer = acl.create_data_buffer(buffer, size)
            #add data buffer to output dataset 
            _, ret = acl.mdl.add_dataset_buffer(dataset, dataset_buffer)
            print("malloc output %d, size %d"%(i, size))
            if ret:
                # release resource if failed 
                acl.rt.free(buffer)
                acl.destroy_data_buffer(dataset)
                check_ret("acl.destroy_data_buffer", ret)
        self.output_dataset = dataset
        print("[Model] create model output dataset success")

    def _init_input_buffer(self):
        # create a table recording the input data memory allocated for users
        # currently, the numpy data needs to be copied to device for memory allocation only when the input is numpy array
        self._input_num = acl.mdl.get_num_inputs(self.model_desc)
        self._input_buffer = []
        for i in range(self._input_num):
            # none of inputs is allocated memory initially 
            item = {"addr":None, "size":0}
            self._input_buffer.append(item)

    def _gen_input_dataset(self, input_list):
        # organize input dataset structure 
        ret = SUCCESS
        # return if the input number does not match model requirements
        if len(input_list) != self._input_num:
            print("Current input data num %d unequal to"
                  " model input num %d"%(len(input_list), self._input_num))
            return FAILED

        self.input_dataset = acl.mdl.create_dataset()
        for i in range(self._input_num):
            item = input_list[i]
            # parse input, currently supports AclImage type, Acl pointer and numpy array
            data, size = self._parse_input_data(item, i)            
            if (data is None) or (size == 0):
                # not parse the remaining data when parsing data fails
                ret = FAILED
                print("The %d input is invalid"%(i))
                break
            # create input dataset buffer structure, fill in input data
            dataset_buffer = acl.create_data_buffer(data, size)
            # add dataset buffer to dataset 
            _, ret = acl.mdl.add_dataset_buffer(self.input_dataset,
                                                dataset_buffer)
            if ret:
                print("Add input dataset buffer failed")
                acl.destroy_data_buffer(self.input_dataset)
                ret = FAILED
                break
        if ret == FAILED:
            # release dataset if fails 
            self._release_dataset(self.input_dataset)

        return ret

    def _parse_input_data(self, input, index):
        data = None
        size = 0
        if isinstance(input, AclImage):
            # if input data is AclImage, directly return memory pointer and sieze of image
            # defautly image memory is data on the device 
            size = input.size
            data = input.data()
        elif isinstance(input, np.ndarray):
            # if input is numpy data, allocate device memory for data and copy data to device
            # allocated memory can be reused, no need to apply for it everytime
            ptr = acl.util.numpy_to_ptr(input)
            size = input.size * input.itemsize
            data = self._copy_input_to_device(ptr, size, index)
            if data == None:
                size = 0
                print("Copy input to device failed")
        # if directly input memory pointer, structure should be dict like {"data":, "size":}, and default memory is on the device side
        elif (isinstance(input, dict) and
              input.has_key('data') and input.has_key('size')):
            size = input['size']
            data = input['data']
        else:
            print("Unsupport input")

        return data, size

    def _copy_input_to_device(self, input_ptr, size, index):
        # allocate device memory for input, and copy data to this memory
        buffer_item = self._input_buffer[index]
        data = None
        # according to the index of the data in the model input, check whether the input has already been allocated memory
        if buffer_item['addr'] is None:
            # if not, allocate memory, copy data and record memory for resue
            data = copy_data_device_to_device(input_ptr, size)
            if data is None:
                print("Malloc memory and copy model %dth "
                      "input to device failed"%(index))
                return None
            buffer_item['addr'] = data
            buffer_item['size'] = size
        elif size == buffer_item['size']:
            # if memory has already been allocated for the input, and memory size is consistent with current input data
            # copy data to this memory for inference 
            ret = acl.rt.memcpy(buffer_item['addr'], size,
                                input_ptr, size,
                                ACL_MEMCPY_DEVICE_TO_DEVICE)
            if ret != ACL_ERROR_NONE:
                print("Copy model %dth input to device failed"%(index))
                return None
            data = buffer_item['addr']
        else:
            # if memory has already been allocated for the input, but memory size is not consistent with current input data
            # it would be considered as exception. because size of each model input is fixed 
            print("The model %dth input size %d is change,"
                  " before is %d"%(index, size, buffer_item['size']))
            return None

        return data

    def execute(self, input_list):
        # create dataset object instance for offline model inference
        ret = self._gen_input_dataset(input_list)
        if ret == FAILED:
            print("Gen model input dataset failed")
            return None
        # call execute inference data of offline model
        start = datetime.datetime.now()
        ret = acl.mdl.execute(self.model_id,
                              self.input_dataset,
                              self.output_dataset)
        if ret != ACL_ERROR_NONE:
            print("Execute model failed for acl.mdl.execute error ", ret)
            return None
        end = datetime.datetime.now()        
        print("acl.mdl.execute exhaust ", end - start)
        # release input dataset object instance without releasing input data memory 
        #self._release_dataset(self.input_dataset)
        # decode the binary data stream output from inference to numpy array, shape and datatype of the array are consistent with model outputs
        return self._output_dataset_to_numpy()

    def _output_dataset_to_numpy(self):
        dataset = []
        num = acl.mdl.get_dataset_num_buffers(self.output_dataset)
        # iterative each output 
        for i in range(num):
            # obtain memory address from output buffer
            buffer = acl.mdl.get_dataset_buffer(self.output_dataset, i)
            data = acl.get_data_buffer_addr(buffer)
            size = int(acl.get_data_buffer_size(buffer))
            output_ptr = self._output_info[i]["ptr"]
            output_tensor = self._output_info[i]["tensor"]
            ret = acl.rt.memcpy(output_ptr, output_tensor.size*output_tensor.itemsize,                            
                                data, size, ACL_MEMCPY_DEVICE_TO_DEVICE)
            if ret != ACL_ERROR_NONE:
                print("Memcpy inference output to local failed")
                return None

            dataset.append(output_tensor)

        return dataset  

    def _release_dataset(self, dataset):
        if not dataset:
            return
        print("destroy dataset")
        num = acl.mdl.get_dataset_num_buffers(dataset)
        for i in range(num):
            data_buf = acl.mdl.get_dataset_buffer(dataset, i)
            if data_buf:
                ret = acl.destroy_data_buffer(data_buf)
                if ret != ACL_ERROR_NONE:
                    print("Destroy data buffer error ", ret)
        ret = acl.mdl.destroy_dataset(dataset)
        if ret != ACL_ERROR_NONE:
            print("Destroy data buffer error ", ret)

