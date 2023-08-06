from ._interface cimport *
from .camera cimport Camera


cdef class CameraNodes:

    cdef Camera _camera
    cdef dict _nodes

    cdef public list bool_nodes
    cdef public list int_nodes
    cdef public list float_nodes
    cdef public list str_nodes
    cdef public list enum_nodes
    cdef public list command_nodes
    cdef public list register_nodes


cdef class TLDevNodes:

    cdef Camera _camera
    cdef dict _nodes

    cdef public list bool_nodes
    cdef public list int_nodes
    cdef public list float_nodes
    cdef public list str_nodes
    cdef public list enum_nodes
    cdef public list command_nodes
    cdef public list register_nodes


cdef class TLStreamNodes:

    cdef Camera _camera
    cdef dict _nodes

    cdef public list bool_nodes
    cdef public list int_nodes
    cdef public list float_nodes
    cdef public list str_nodes
    cdef public list enum_nodes
    cdef public list command_nodes
    cdef public list register_nodes
