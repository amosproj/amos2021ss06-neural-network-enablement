import acl

from .atlas_utils.utils import *


class AclResource(object):
    """
    This class is a singleton, init is called when creating the first object,
    for subsequent calls of the constructor init is not called.
    """

    _instance = None

    def __new__(cls, device_id=0):
        if cls._instance is None:
            cls._instance = super(AclResource, cls).__new__(cls)

            cls._instance.device_id = device_id
            cls._instance.context = None
            cls._instance.stream = None
            cls._instance.run_mode = None
            cls._instance.init()

        return cls._instance

    def init(self):
        print("init resource stage:")
        ret = acl.init()
        check_ret("acl.rt.set_device", ret)

        ret = acl.rt.set_device(self.device_id)
        check_ret("acl.rt.set_device", ret)

        self.context, ret = acl.rt.create_context(self.device_id)
        check_ret("acl.rt.create_context", ret)

        self.stream, ret = acl.rt.create_stream()
        check_ret("acl.rt.create_stream", ret)

        self.run_mode, ret = acl.rt.get_run_mode()
        check_ret("acl.rt.get_run_mode", ret)

        print("Init resource success")

    def __del__(self):
        if self.stream:
            acl.rt.destroy_stream(self.stream)
        if self.context:
            acl.rt.destroy_context(self.context)
        acl.rt.reset_device(self.device_id)
        acl.finalize()
        print("Release acl resource success")
