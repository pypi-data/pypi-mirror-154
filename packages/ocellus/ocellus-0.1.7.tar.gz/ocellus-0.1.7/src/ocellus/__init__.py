# Copyright © 2022 Byte Motion AB
import sys
from os import path
  
# Adding the cwd to the path is needed since
# scripts generated from protos do not take the
# module name into consideration when importing.
sys.path.insert(0, path.abspath(path.dirname(__file__)))

from ocellus.ocellus_types_pb2 import *
from ocellus.ocellus_module_service_pb2 import *
from ocellus.ocellus_module_service_pb2_grpc import *
