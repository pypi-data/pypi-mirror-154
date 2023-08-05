# pylint: disable=invalid-name,line-too-long,too-many-lines
# pylint: disable=too-many-arguments,redefined-builtin,redefined-outer-name
# pylint: disable=missing-class-docstring,missing-function-docstring
# pylint: disable=protected-access, too-many-lines
"""Auto generated. Do not touch."""
import raf._ffi.op.imp as ffi
from raf._core.core_utils import set_module
from . import imp_utils

__all__ = [
    "_allgather", "_allreduce", "_broadcast", "_contrib_dropout", "_contrib_dropout_dx",
    "_group_allgather", "_group_reduce_scatter", "_recv", "_reduce", "_reduce_scatter",
    "_send", "abs", "adaptive_avg_pool2d", "adaptive_avg_pool2d_dx", "adaptive_max_pool2d",
    "adaptive_max_pool2d_dx", "add", "add_event", "adv_index", "adv_index_dx",
    "all", "any", "arange", "argmax", "argmin",
    "argsort", "argwhere", "atan", "avg_pool2d", "avg_pool2d_dx",
    "batch_flatten", "batch_matmul", "batch_matmul_nt", "batch_matmul_tn", "batch_matmul_tt",
    "batch_norm_infer", "batch_norm_train", "batch_norm_train_dxwb", "bias_add", "broadcast_to",
    "broadcast_to_like", "cast", "cast_like", "ceil", "clip",
    "clip_dx", "collapse_sum_like", "compiler_begin", "compiler_end", "concatenate",
    "concatenate_dx", "conv2d", "conv2d_dw", "conv2d_dx", "conv2d_transpose",
    "conv2d_transpose_dw", "conv2d_transpose_dx", "copy", "cos", "cross_entropy",
    "cross_entropy_dpred", "cross_entropy_dtrue", "cumsum", "defuse_tensor", "dense",
    "device_copy", "divide", "embedding", "embedding_dx", "equal",
    "erf", "erf_dx", "exp", "expand_dims", "floor",
    "floor_divide", "full", "full_like", "fuse_tensor", "gather",
    "gather_dx", "gather_nd", "gather_nd_dx", "gelu", "gelu_dx",
    "get_kept_dims", "get_reduce_axis", "get_valid_counts", "greater", "greater_equal",
    "group_cast", "l2norm", "lans", "layer_norm", "layer_norm_dx",
    "layer_norm_train", "layer_norm_train_dx", "left_shift", "less", "less_equal",
    "log", "log2", "log_softmax", "log_softmax_dx", "logical_and",
    "logical_not", "matmul", "matmul_nt", "matmul_tn", "matmul_tt",
    "max", "max_pool2d", "max_pool2d_dx", "maximum", "mean",
    "mean_dx", "mesh_grid", "min", "minimum", "mod",
    "multiply", "ndarray_size", "negative", "nll_loss", "nll_loss_dpred",
    "nll_loss_dtrue", "non_max_suppression", "not_equal", "numel", "one_hot",
    "ones", "ones_like", "pad", "power", "prod",
    "prod_dx", "relu", "relu_dx", "repeat", "repeat_dx",
    "reshape", "reshape_like", "resize2d", "resize2d_dx", "reverse",
    "reverse_sequence", "right_shift", "roi_align", "roi_align_dx", "round",
    "rsqrt", "scatter", "scatter_dx", "sequence_mask", "set_stream",
    "sgd", "shape", "shape_as_tensor", "sigmoid", "sigmoid_dx",
    "sign", "sin", "size", "smooth_l1_loss", "smooth_l1_loss_dpred",
    "smooth_l1_loss_dtrue", "softmax", "softmax_dx", "sort", "split",
    "sqrt", "sqrt_dx", "squeeze", "stack", "stream_barrier",
    "stream_sync", "strided_set", "strided_slice", "strided_slice_dx", "subtract",
    "sum", "sum_dx", "swap_axis", "take", "take_dx",
    "tanh", "tanh_dx", "threefry_generate", "threefry_split", "threshold",
    "threshold_dx", "topk", "transpose", "transpose_dx", "trunc",
    "upper_bound_argwhere", "vm_alloc_storage", "vm_alloc_tensor", "vm_free", "vm_infer_type",
    "vm_invoke_op", "vm_set_shape", "wait_event", "where", "zeros",
    "zeros_like",
]

@set_module("raf")
def _allgather(x, axis, rank_list=None):
    x = imp_utils.to_tensor(x)
    axis = imp_utils.to_int(axis)
    rank_list = imp_utils.to_any(rank_list)
    return imp_utils.ret(ffi._allgather(x, axis, rank_list))

@set_module("raf")
def _allreduce(x, computation="sum", rank_list=None):
    x = imp_utils.to_tensor_tuple(x)
    computation = imp_utils.to_string(computation)
    rank_list = imp_utils.to_any(rank_list)
    return imp_utils.ret(ffi._allreduce(x, computation, rank_list))

@set_module("raf")
def _broadcast(x, root):
    x = imp_utils.to_tensor_tuple(x)
    root = imp_utils.to_int(root)
    return imp_utils.ret(ffi._broadcast(x, root))

@set_module("raf")
def _contrib_dropout(x, p=0.5, in_states=None):
    x = imp_utils.to_tensor(x)
    p = imp_utils.to_double(p)
    in_states = imp_utils.to_tensor(in_states)
    return imp_utils.ret(ffi._contrib_dropout(x, p, in_states))

@set_module("raf")
def _contrib_dropout_dx(dy, mask, reserve_space, p=0.5):
    dy = imp_utils.to_tensor(dy)
    mask = imp_utils.to_tensor(mask)
    reserve_space = imp_utils.to_tensor(reserve_space)
    p = imp_utils.to_double(p)
    return imp_utils.ret(ffi._contrib_dropout_dx(dy, mask, reserve_space, p))

@set_module("raf")
def _group_allgather(tensor_list, axis, out):
    tensor_list = imp_utils.to_tensor_tuple(tensor_list)
    axis = imp_utils.to_int(axis)
    out = imp_utils.to_tensor_tuple(out)
    return imp_utils.ret(ffi._group_allgather(tensor_list, axis, out))

@set_module("raf")
def _group_reduce_scatter(tensor_list, computation="sum"):
    tensor_list = imp_utils.to_tensor_tuple(tensor_list)
    computation = imp_utils.to_string(computation)
    return imp_utils.ret(ffi._group_reduce_scatter(tensor_list, computation))

@set_module("raf")
def _recv(peer, shape, dtype="float32", token=None):
    peer = imp_utils.to_int(peer)
    shape = imp_utils.to_int_tuple(shape)
    dtype = imp_utils.to_string(dtype)
    token = imp_utils.to_tensor(token)
    return imp_utils.ret(ffi._recv(peer, shape, dtype, token))

@set_module("raf")
def _reduce(x, root, computation="sum"):
    x = imp_utils.to_tensor_tuple(x)
    root = imp_utils.to_int(root)
    computation = imp_utils.to_string(computation)
    return imp_utils.ret(ffi._reduce(x, root, computation))

@set_module("raf")
def _reduce_scatter(x, computation="sum", rank_list=None):
    x = imp_utils.to_tensor_tuple(x)
    computation = imp_utils.to_string(computation)
    rank_list = imp_utils.to_any(rank_list)
    return imp_utils.ret(ffi._reduce_scatter(x, computation, rank_list))

@set_module("raf")
def _send(x, peer, token=None):
    x = imp_utils.to_tensor(x)
    peer = imp_utils.to_int(peer)
    token = imp_utils.to_tensor(token)
    return imp_utils.ret(ffi._send(x, peer, token))

@set_module("raf")
def abs(x):
    x = imp_utils.to_any(x)
    return imp_utils.ret(ffi.abs(x))

@set_module("raf")
def adaptive_avg_pool2d(x, shape, layout="NCHW"):
    x = imp_utils.to_tensor(x)
    shape = imp_utils.to_int_tuple(shape)
    layout = imp_utils.to_string(layout)
    return imp_utils.ret(ffi.adaptive_avg_pool2d(x, shape, layout))

@set_module("raf")
def adaptive_avg_pool2d_dx(x, y, dy, shape):
    x = imp_utils.to_tensor(x)
    y = imp_utils.to_tensor(y)
    dy = imp_utils.to_tensor(dy)
    shape = imp_utils.to_int_tuple(shape)
    return imp_utils.ret(ffi.adaptive_avg_pool2d_dx(x, y, dy, shape))

@set_module("raf")
def adaptive_max_pool2d(x, shape, layout="NCHW"):
    x = imp_utils.to_tensor(x)
    shape = imp_utils.to_int_tuple(shape)
    layout = imp_utils.to_string(layout)
    return imp_utils.ret(ffi.adaptive_max_pool2d(x, shape, layout))

@set_module("raf")
def adaptive_max_pool2d_dx(x, y, dy, shape):
    x = imp_utils.to_tensor(x)
    y = imp_utils.to_tensor(y)
    dy = imp_utils.to_tensor(dy)
    shape = imp_utils.to_int_tuple(shape)
    return imp_utils.ret(ffi.adaptive_max_pool2d_dx(x, y, dy, shape))

@set_module("raf")
def add(x1, x2, out=None, where=None):
    x1 = imp_utils.to_any(x1)
    x2 = imp_utils.to_any(x2)
    out = imp_utils.to_any(out)
    where = imp_utils.to_any(where)
    return imp_utils.ret(ffi.add(x1, x2, out, where))

@set_module("raf")
def add_event(event_id, stream_id=-1):
    event_id = imp_utils.to_int(event_id)
    stream_id = imp_utils.to_int(stream_id)
    return imp_utils.ret(ffi.add_event(event_id, stream_id))

@set_module("raf")
def adv_index(inputs):
    inputs = imp_utils.to_tensor_tuple(inputs)
    return imp_utils.ret(ffi.adv_index(inputs))

@set_module("raf")
def adv_index_dx(dy, inputs):
    dy = imp_utils.to_tensor(dy)
    inputs = imp_utils.to_tensor_tuple(inputs)
    return imp_utils.ret(ffi.adv_index_dx(dy, inputs))

@set_module("raf")
def all(x, axis=(), keepdims=False, exclude=False):
    x = imp_utils.to_tensor(x)
    axis = imp_utils.to_int_tuple(axis)
    keepdims = imp_utils.to_bool(keepdims)
    exclude = imp_utils.to_bool(exclude)
    return imp_utils.ret(ffi.all(x, axis, keepdims, exclude))

@set_module("raf")
def any(x, axis=(), keepdims=False, exclude=False):
    x = imp_utils.to_tensor(x)
    axis = imp_utils.to_int_tuple(axis)
    keepdims = imp_utils.to_bool(keepdims)
    exclude = imp_utils.to_bool(exclude)
    return imp_utils.ret(ffi.any(x, axis, keepdims, exclude))

@set_module("raf")
def arange(start, stop, step, dtype="float32", device="cpu"):
    start = imp_utils.to_tensor(start)
    stop = imp_utils.to_tensor(stop)
    step = imp_utils.to_tensor(step)
    dtype = imp_utils.to_string(dtype)
    device = imp_utils.to_string(device)
    return imp_utils.ret(ffi.arange(start, stop, step, dtype, device))

@set_module("raf")
def argmax(x, axis=(), keepdims=False, exclude=False):
    x = imp_utils.to_tensor(x)
    axis = imp_utils.to_int_tuple(axis)
    keepdims = imp_utils.to_bool(keepdims)
    exclude = imp_utils.to_bool(exclude)
    return imp_utils.ret(ffi.argmax(x, axis, keepdims, exclude))

@set_module("raf")
def argmin(x, axis=(), keepdims=False, exclude=False):
    x = imp_utils.to_tensor(x)
    axis = imp_utils.to_int_tuple(axis)
    keepdims = imp_utils.to_bool(keepdims)
    exclude = imp_utils.to_bool(exclude)
    return imp_utils.ret(ffi.argmin(x, axis, keepdims, exclude))

@set_module("raf")
def argsort(data, axis=-1, is_ascend=True, dtype="int32"):
    data = imp_utils.to_tensor(data)
    axis = imp_utils.to_int(axis)
    is_ascend = imp_utils.to_bool(is_ascend)
    dtype = imp_utils.to_string(dtype)
    return imp_utils.ret(ffi.argsort(data, axis, is_ascend, dtype))

@set_module("raf")
def argwhere(condition):
    condition = imp_utils.to_tensor(condition)
    return imp_utils.ret(ffi.argwhere(condition))

@set_module("raf")
def atan(x):
    x = imp_utils.to_any(x)
    return imp_utils.ret(ffi.atan(x))

@set_module("raf")
def avg_pool2d(x, kernel, stride, padding=0, dilation=1, ceil_mode=False, include_pad=True, layout="NCHW"):
    x = imp_utils.to_tensor(x)
    kernel = imp_utils.to_int_tuple(kernel)
    stride = imp_utils.to_int_tuple(stride)
    padding = imp_utils.to_int_tuple(padding)
    dilation = imp_utils.to_int_tuple(dilation)
    ceil_mode = imp_utils.to_bool(ceil_mode)
    include_pad = imp_utils.to_bool(include_pad)
    layout = imp_utils.to_string(layout)
    return imp_utils.ret(ffi.avg_pool2d(x, kernel, stride, padding, dilation, ceil_mode, include_pad, layout))

@set_module("raf")
def avg_pool2d_dx(x, y, dy, kernel, stride, padding, dilation, ceil_mode, include_pad):
    x = imp_utils.to_tensor(x)
    y = imp_utils.to_tensor(y)
    dy = imp_utils.to_tensor(dy)
    kernel = imp_utils.to_int_tuple(kernel)
    stride = imp_utils.to_int_tuple(stride)
    padding = imp_utils.to_int_tuple(padding)
    dilation = imp_utils.to_int_tuple(dilation)
    ceil_mode = imp_utils.to_bool(ceil_mode)
    include_pad = imp_utils.to_bool(include_pad)
    return imp_utils.ret(ffi.avg_pool2d_dx(x, y, dy, kernel, stride, padding, dilation, ceil_mode, include_pad))

@set_module("raf")
def batch_flatten(x):
    x = imp_utils.to_any(x)
    return imp_utils.ret(ffi.batch_flatten(x))

@set_module("raf")
def batch_matmul(x1, x2):
    x1 = imp_utils.to_any(x1)
    x2 = imp_utils.to_any(x2)
    return imp_utils.ret(ffi.batch_matmul(x1, x2))

@set_module("raf")
def batch_matmul_nt(x1, x2):
    x1 = imp_utils.to_any(x1)
    x2 = imp_utils.to_any(x2)
    return imp_utils.ret(ffi.batch_matmul_nt(x1, x2))

@set_module("raf")
def batch_matmul_tn(x1, x2):
    x1 = imp_utils.to_any(x1)
    x2 = imp_utils.to_any(x2)
    return imp_utils.ret(ffi.batch_matmul_tn(x1, x2))

@set_module("raf")
def batch_matmul_tt(x1, x2):
    x1 = imp_utils.to_any(x1)
    x2 = imp_utils.to_any(x2)
    return imp_utils.ret(ffi.batch_matmul_tt(x1, x2))

@set_module("raf")
def batch_norm_infer(x, running_mean, running_var, w=None, b=None, momentum=0.1, eps=1e-05):
    x = imp_utils.to_tensor(x)
    running_mean = imp_utils.to_tensor(running_mean)
    running_var = imp_utils.to_tensor(running_var)
    w = imp_utils.to_tensor(w)
    b = imp_utils.to_tensor(b)
    momentum = imp_utils.to_double(momentum)
    eps = imp_utils.to_double(eps)
    return imp_utils.ret(ffi.batch_norm_infer(x, running_mean, running_var, w, b, momentum, eps))

@set_module("raf")
def batch_norm_train(x, running_mean, running_var, w=None, b=None, momentum=0.1, eps=1e-05):
    x = imp_utils.to_tensor(x)
    running_mean = imp_utils.to_tensor(running_mean)
    running_var = imp_utils.to_tensor(running_var)
    w = imp_utils.to_tensor(w)
    b = imp_utils.to_tensor(b)
    momentum = imp_utils.to_double(momentum)
    eps = imp_utils.to_double(eps)
    return imp_utils.ret(ffi.batch_norm_train(x, running_mean, running_var, w, b, momentum, eps))

@set_module("raf")
def batch_norm_train_dxwb(dy, x, w, b, eps):
    dy = imp_utils.to_tensor(dy)
    x = imp_utils.to_tensor(x)
    w = imp_utils.to_tensor(w)
    b = imp_utils.to_tensor(b)
    eps = imp_utils.to_double(eps)
    return imp_utils.ret(ffi.batch_norm_train_dxwb(dy, x, w, b, eps))

@set_module("raf")
def bias_add(x, bias, axis=1):
    x = imp_utils.to_tensor(x)
    bias = imp_utils.to_tensor(bias)
    axis = imp_utils.to_int(axis)
    return imp_utils.ret(ffi.bias_add(x, bias, axis))

@set_module("raf")
def broadcast_to(x, shape):
    x = imp_utils.to_tensor(x)
    shape = imp_utils.to_int_tuple(shape)
    return imp_utils.ret(ffi.broadcast_to(x, shape))

@set_module("raf")
def broadcast_to_like(x, like_type):
    x = imp_utils.to_tensor(x)
    like_type = imp_utils.to_tensor(like_type)
    return imp_utils.ret(ffi.broadcast_to_like(x, like_type))

@set_module("raf")
def cast(data, dtype):
    data = imp_utils.to_tensor(data)
    dtype = imp_utils.to_string(dtype)
    return imp_utils.ret(ffi.cast(data, dtype))

@set_module("raf")
def cast_like(x, like_type):
    x = imp_utils.to_tensor(x)
    like_type = imp_utils.to_tensor(like_type)
    return imp_utils.ret(ffi.cast_like(x, like_type))

@set_module("raf")
def ceil(x):
    x = imp_utils.to_any(x)
    return imp_utils.ret(ffi.ceil(x))

@set_module("raf")
def clip(x, a_min, a_max):
    x = imp_utils.to_tensor(x)
    a_min = imp_utils.to_double(a_min)
    a_max = imp_utils.to_double(a_max)
    return imp_utils.ret(ffi.clip(x, a_min, a_max))

@set_module("raf")
def clip_dx(x, dy, a_min, a_max):
    x = imp_utils.to_tensor(x)
    dy = imp_utils.to_tensor(dy)
    a_min = imp_utils.to_double(a_min)
    a_max = imp_utils.to_double(a_max)
    return imp_utils.ret(ffi.clip_dx(x, dy, a_min, a_max))

@set_module("raf")
def collapse_sum_like(x, like_type):
    x = imp_utils.to_tensor(x)
    like_type = imp_utils.to_tensor(like_type)
    return imp_utils.ret(ffi.collapse_sum_like(x, like_type))

@set_module("raf")
def compiler_begin(x):
    x = imp_utils.to_any(x)
    return imp_utils.ret(ffi.compiler_begin(x))

@set_module("raf")
def compiler_end(x):
    x = imp_utils.to_any(x)
    return imp_utils.ret(ffi.compiler_end(x))

@set_module("raf")
def concatenate(x, axis=0):
    x = imp_utils.to_tensor_tuple(x)
    axis = imp_utils.to_int(axis)
    return imp_utils.ret(ffi.concatenate(x, axis))

@set_module("raf")
def concatenate_dx(x, axis=0):
    x = imp_utils.to_tensor_tuple(x)
    axis = imp_utils.to_int(axis)
    return imp_utils.ret(ffi.concatenate_dx(x, axis))

@set_module("raf")
def conv2d(x, w, stride=1, padding=0, dilation=1, groups=1, layout="NCHW", kernel_layout="OIHW", out_layout="NCHW"):
    x = imp_utils.to_tensor(x)
    w = imp_utils.to_tensor(w)
    stride = imp_utils.to_int_tuple(stride)
    padding = imp_utils.to_int_tuple(padding)
    dilation = imp_utils.to_int_tuple(dilation)
    groups = imp_utils.to_int(groups)
    layout = imp_utils.to_string(layout)
    kernel_layout = imp_utils.to_string(kernel_layout)
    out_layout = imp_utils.to_string(out_layout)
    return imp_utils.ret(ffi.conv2d(x, w, stride, padding, dilation, groups, layout, kernel_layout, out_layout))

@set_module("raf")
def conv2d_dw(x_or_w, y, dy, shape, stride, padding, dilation, groups):
    x_or_w = imp_utils.to_tensor(x_or_w)
    y = imp_utils.to_tensor(y)
    dy = imp_utils.to_tensor(dy)
    shape = imp_utils.to_any(shape)
    stride = imp_utils.to_int_tuple(stride)
    padding = imp_utils.to_int_tuple(padding)
    dilation = imp_utils.to_int_tuple(dilation)
    groups = imp_utils.to_int(groups)
    return imp_utils.ret(ffi.conv2d_dw(x_or_w, y, dy, shape, stride, padding, dilation, groups))

@set_module("raf")
def conv2d_dx(x_or_w, y, dy, shape, stride, padding, dilation, groups):
    x_or_w = imp_utils.to_tensor(x_or_w)
    y = imp_utils.to_tensor(y)
    dy = imp_utils.to_tensor(dy)
    shape = imp_utils.to_any(shape)
    stride = imp_utils.to_int_tuple(stride)
    padding = imp_utils.to_int_tuple(padding)
    dilation = imp_utils.to_int_tuple(dilation)
    groups = imp_utils.to_int(groups)
    return imp_utils.ret(ffi.conv2d_dx(x_or_w, y, dy, shape, stride, padding, dilation, groups))

@set_module("raf")
def conv2d_transpose(x, w, stride=1, padding=0, output_padding=0, dilation=1, groups=1, layout="NCHW", kernel_layout="IOHW", out_layout="NCHW"):
    x = imp_utils.to_tensor(x)
    w = imp_utils.to_tensor(w)
    stride = imp_utils.to_int_tuple(stride)
    padding = imp_utils.to_int_tuple(padding)
    output_padding = imp_utils.to_int_tuple(output_padding)
    dilation = imp_utils.to_int_tuple(dilation)
    groups = imp_utils.to_int(groups)
    layout = imp_utils.to_string(layout)
    kernel_layout = imp_utils.to_string(kernel_layout)
    out_layout = imp_utils.to_string(out_layout)
    return imp_utils.ret(ffi.conv2d_transpose(x, w, stride, padding, output_padding, dilation, groups, layout, kernel_layout, out_layout))

@set_module("raf")
def conv2d_transpose_dw(x_or_w, y, dy, shape, stride, padding, output_padding, dilation, groups):
    x_or_w = imp_utils.to_tensor(x_or_w)
    y = imp_utils.to_tensor(y)
    dy = imp_utils.to_tensor(dy)
    shape = imp_utils.to_any(shape)
    stride = imp_utils.to_int_tuple(stride)
    padding = imp_utils.to_int_tuple(padding)
    output_padding = imp_utils.to_int_tuple(output_padding)
    dilation = imp_utils.to_int_tuple(dilation)
    groups = imp_utils.to_int(groups)
    return imp_utils.ret(ffi.conv2d_transpose_dw(x_or_w, y, dy, shape, stride, padding, output_padding, dilation, groups))

@set_module("raf")
def conv2d_transpose_dx(x_or_w, y, dy, shape, stride, padding, output_padding, dilation, groups):
    x_or_w = imp_utils.to_tensor(x_or_w)
    y = imp_utils.to_tensor(y)
    dy = imp_utils.to_tensor(dy)
    shape = imp_utils.to_any(shape)
    stride = imp_utils.to_int_tuple(stride)
    padding = imp_utils.to_int_tuple(padding)
    output_padding = imp_utils.to_int_tuple(output_padding)
    dilation = imp_utils.to_int_tuple(dilation)
    groups = imp_utils.to_int(groups)
    return imp_utils.ret(ffi.conv2d_transpose_dx(x_or_w, y, dy, shape, stride, padding, output_padding, dilation, groups))

@set_module("raf")
def copy(x):
    x = imp_utils.to_any(x)
    return imp_utils.ret(ffi.copy(x))

@set_module("raf")
def cos(x):
    x = imp_utils.to_any(x)
    return imp_utils.ret(ffi.cos(x))

@set_module("raf")
def cross_entropy(y_true, y_pred):
    y_true = imp_utils.to_tensor(y_true)
    y_pred = imp_utils.to_tensor(y_pred)
    return imp_utils.ret(ffi.cross_entropy(y_true, y_pred))

@set_module("raf")
def cross_entropy_dpred(dy, y_true, y_pred):
    dy = imp_utils.to_tensor(dy)
    y_true = imp_utils.to_tensor(y_true)
    y_pred = imp_utils.to_tensor(y_pred)
    return imp_utils.ret(ffi.cross_entropy_dpred(dy, y_true, y_pred))

@set_module("raf")
def cross_entropy_dtrue(dy, y_true, y_pred):
    dy = imp_utils.to_tensor(dy)
    y_true = imp_utils.to_tensor(y_true)
    y_pred = imp_utils.to_tensor(y_pred)
    return imp_utils.ret(ffi.cross_entropy_dtrue(dy, y_true, y_pred))

@set_module("raf")
def cumsum(x, axis, dtype="float32", exclusive=False):
    x = imp_utils.to_tensor(x)
    axis = imp_utils.to_int(axis)
    dtype = imp_utils.to_string(dtype)
    exclusive = imp_utils.to_bool(exclusive)
    return imp_utils.ret(ffi.cumsum(x, axis, dtype, exclusive))

@set_module("raf")
def defuse_tensor(data, sizes, shapes, shape_indices):
    data = imp_utils.to_tensor(data)
    sizes = imp_utils.to_int_tuple(sizes)
    shapes = imp_utils.to_int_tuple(shapes)
    shape_indices = imp_utils.to_int_tuple(shape_indices)
    return imp_utils.ret(ffi.defuse_tensor(data, sizes, shapes, shape_indices))

@set_module("raf")
def dense(x1, x2):
    x1 = imp_utils.to_any(x1)
    x2 = imp_utils.to_any(x2)
    return imp_utils.ret(ffi.dense(x1, x2))

@set_module("raf")
def device_copy(data, src_device="cpu", dst_device="cpu"):
    data = imp_utils.to_tensor(data)
    src_device = imp_utils.to_string(src_device)
    dst_device = imp_utils.to_string(dst_device)
    return imp_utils.ret(ffi.device_copy(data, src_device, dst_device))

@set_module("raf")
def divide(x1, x2):
    x1 = imp_utils.to_any(x1)
    x2 = imp_utils.to_any(x2)
    return imp_utils.ret(ffi.divide(x1, x2))

@set_module("raf")
def embedding(x, indices):
    x = imp_utils.to_tensor(x)
    indices = imp_utils.to_tensor(indices)
    return imp_utils.ret(ffi.embedding(x, indices))

@set_module("raf")
def embedding_dx(dy, indices, num_weight):
    dy = imp_utils.to_tensor(dy)
    indices = imp_utils.to_tensor(indices)
    num_weight = imp_utils.to_any(num_weight)
    return imp_utils.ret(ffi.embedding_dx(dy, indices, num_weight))

@set_module("raf")
def equal(x1, x2):
    x1 = imp_utils.to_any(x1)
    x2 = imp_utils.to_any(x2)
    return imp_utils.ret(ffi.equal(x1, x2))

@set_module("raf")
def erf(x):
    x = imp_utils.to_any(x)
    return imp_utils.ret(ffi.erf(x))

@set_module("raf")
def erf_dx(x, y, dy):
    x = imp_utils.to_any(x)
    y = imp_utils.to_tensor(y)
    dy = imp_utils.to_tensor(dy)
    return imp_utils.ret(ffi.erf_dx(x, y, dy))

@set_module("raf")
def exp(x):
    x = imp_utils.to_any(x)
    return imp_utils.ret(ffi.exp(x))

@set_module("raf")
def expand_dims(x, axis, num_newaxis=1):
    x = imp_utils.to_tensor(x)
    axis = imp_utils.to_int(axis)
    num_newaxis = imp_utils.to_int(num_newaxis)
    return imp_utils.ret(ffi.expand_dims(x, axis, num_newaxis))

@set_module("raf")
def floor(x):
    x = imp_utils.to_any(x)
    return imp_utils.ret(ffi.floor(x))

@set_module("raf")
def floor_divide(x1, x2):
    x1 = imp_utils.to_any(x1)
    x2 = imp_utils.to_any(x2)
    return imp_utils.ret(ffi.floor_divide(x1, x2))

@set_module("raf")
def full(fill_value, shape, dtype="int32", device="cpu"):
    fill_value = imp_utils.to_double(fill_value)
    shape = imp_utils.to_any(shape)
    dtype = imp_utils.to_string(dtype)
    device = imp_utils.to_string(device)
    return imp_utils.ret(ffi.full(fill_value, shape, dtype, device))

@set_module("raf")
def full_like(data, fill_value):
    data = imp_utils.to_tensor(data)
    fill_value = imp_utils.to_double(fill_value)
    return imp_utils.ret(ffi.full_like(data, fill_value))

@set_module("raf")
def fuse_tensor(data):
    data = imp_utils.to_tensor_tuple(data)
    return imp_utils.ret(ffi.fuse_tensor(data))

@set_module("raf")
def gather(data, axis, indices):
    data = imp_utils.to_tensor(data)
    axis = imp_utils.to_int(axis)
    indices = imp_utils.to_tensor(indices)
    return imp_utils.ret(ffi.gather(data, axis, indices))

@set_module("raf")
def gather_dx(data, axis, indices, dy):
    data = imp_utils.to_tensor(data)
    axis = imp_utils.to_int(axis)
    indices = imp_utils.to_tensor(indices)
    dy = imp_utils.to_tensor(dy)
    return imp_utils.ret(ffi.gather_dx(data, axis, indices, dy))

@set_module("raf")
def gather_nd(data, indices):
    data = imp_utils.to_tensor(data)
    indices = imp_utils.to_tensor(indices)
    return imp_utils.ret(ffi.gather_nd(data, indices))

@set_module("raf")
def gather_nd_dx(data, indices, dy):
    data = imp_utils.to_tensor(data)
    indices = imp_utils.to_tensor(indices)
    dy = imp_utils.to_tensor(dy)
    return imp_utils.ret(ffi.gather_nd_dx(data, indices, dy))

@set_module("raf")
def gelu(x):
    x = imp_utils.to_any(x)
    return imp_utils.ret(ffi.gelu(x))

@set_module("raf")
def gelu_dx(x, y, dy):
    x = imp_utils.to_any(x)
    y = imp_utils.to_tensor(y)
    dy = imp_utils.to_tensor(dy)
    return imp_utils.ret(ffi.gelu_dx(x, y, dy))

@set_module("raf")
def get_kept_dims(x1, x2):
    x1 = imp_utils.to_any(x1)
    x2 = imp_utils.to_any(x2)
    return imp_utils.ret(ffi.get_kept_dims(x1, x2))

@set_module("raf")
def get_reduce_axis(x1, x2):
    x1 = imp_utils.to_any(x1)
    x2 = imp_utils.to_any(x2)
    return imp_utils.ret(ffi.get_reduce_axis(x1, x2))

@set_module("raf")
def get_valid_counts(data, score_threshold, id_index=0, score_index=1):
    data = imp_utils.to_tensor(data)
    score_threshold = imp_utils.to_tensor(score_threshold)
    id_index = imp_utils.to_int(id_index)
    score_index = imp_utils.to_int(score_index)
    return imp_utils.ret(ffi.get_valid_counts(data, score_threshold, id_index, score_index))

@set_module("raf")
def greater(x1, x2):
    x1 = imp_utils.to_any(x1)
    x2 = imp_utils.to_any(x2)
    return imp_utils.ret(ffi.greater(x1, x2))

@set_module("raf")
def greater_equal(x1, x2):
    x1 = imp_utils.to_any(x1)
    x2 = imp_utils.to_any(x2)
    return imp_utils.ret(ffi.greater_equal(x1, x2))

@set_module("raf")
def group_cast(tensor_list, dtype):
    tensor_list = imp_utils.to_tensor_tuple(tensor_list)
    dtype = imp_utils.to_string(dtype)
    return imp_utils.ret(ffi.group_cast(tensor_list, dtype))

@set_module("raf")
def l2norm(x):
    x = imp_utils.to_tensor(x)
    return imp_utils.ret(ffi.l2norm(x))

@set_module("raf")
def lans(tensor_list, step, learning_rate, beta1, beta2, eps, bias_correction, weight_decay, grad_averaging, mode, normalize_grad):
    tensor_list = imp_utils.to_tensor_tuple(tensor_list)
    step = imp_utils.to_tensor(step)
    learning_rate = imp_utils.to_double(learning_rate)
    beta1 = imp_utils.to_double(beta1)
    beta2 = imp_utils.to_double(beta2)
    eps = imp_utils.to_double(eps)
    bias_correction = imp_utils.to_int(bias_correction)
    weight_decay = imp_utils.to_double(weight_decay)
    grad_averaging = imp_utils.to_int(grad_averaging)
    mode = imp_utils.to_int(mode)
    normalize_grad = imp_utils.to_bool(normalize_grad)
    return imp_utils.ret(ffi.lans(tensor_list, step, learning_rate, beta1, beta2, eps, bias_correction, weight_decay, grad_averaging, mode, normalize_grad))

@set_module("raf")
def layer_norm(x, scale=None, bias=None, axis=-1, eps=1e-05):
    x = imp_utils.to_tensor(x)
    scale = imp_utils.to_tensor(scale)
    bias = imp_utils.to_tensor(bias)
    axis = imp_utils.to_int(axis)
    eps = imp_utils.to_double(eps)
    return imp_utils.ret(ffi.layer_norm(x, scale, bias, axis, eps))

@set_module("raf")
def layer_norm_dx(x, scale, dy, axis=-1, eps=1e-05):
    x = imp_utils.to_tensor(x)
    scale = imp_utils.to_tensor(scale)
    dy = imp_utils.to_tensor(dy)
    axis = imp_utils.to_int(axis)
    eps = imp_utils.to_double(eps)
    return imp_utils.ret(ffi.layer_norm_dx(x, scale, dy, axis, eps))

@set_module("raf")
def layer_norm_train(x, scale=None, bias=None, axis=-1, eps=1e-05):
    x = imp_utils.to_tensor(x)
    scale = imp_utils.to_tensor(scale)
    bias = imp_utils.to_tensor(bias)
    axis = imp_utils.to_int(axis)
    eps = imp_utils.to_double(eps)
    return imp_utils.ret(ffi.layer_norm_train(x, scale, bias, axis, eps))

@set_module("raf")
def layer_norm_train_dx(x, scale, dy, mean, invvar, axis=-1, eps=1e-05):
    x = imp_utils.to_tensor(x)
    scale = imp_utils.to_tensor(scale)
    dy = imp_utils.to_tensor(dy)
    mean = imp_utils.to_tensor(mean)
    invvar = imp_utils.to_tensor(invvar)
    axis = imp_utils.to_int(axis)
    eps = imp_utils.to_double(eps)
    return imp_utils.ret(ffi.layer_norm_train_dx(x, scale, dy, mean, invvar, axis, eps))

@set_module("raf")
def left_shift(x1, x2):
    x1 = imp_utils.to_any(x1)
    x2 = imp_utils.to_any(x2)
    return imp_utils.ret(ffi.left_shift(x1, x2))

@set_module("raf")
def less(x1, x2):
    x1 = imp_utils.to_any(x1)
    x2 = imp_utils.to_any(x2)
    return imp_utils.ret(ffi.less(x1, x2))

@set_module("raf")
def less_equal(x1, x2):
    x1 = imp_utils.to_any(x1)
    x2 = imp_utils.to_any(x2)
    return imp_utils.ret(ffi.less_equal(x1, x2))

@set_module("raf")
def log(x):
    x = imp_utils.to_any(x)
    return imp_utils.ret(ffi.log(x))

@set_module("raf")
def log2(x):
    x = imp_utils.to_any(x)
    return imp_utils.ret(ffi.log2(x))

@set_module("raf")
def log_softmax(x, axis=-1):
    x = imp_utils.to_tensor(x)
    axis = imp_utils.to_int(axis)
    return imp_utils.ret(ffi.log_softmax(x, axis))

@set_module("raf")
def log_softmax_dx(y, dy, axis=-1):
    y = imp_utils.to_tensor(y)
    dy = imp_utils.to_tensor(dy)
    axis = imp_utils.to_int(axis)
    return imp_utils.ret(ffi.log_softmax_dx(y, dy, axis))

@set_module("raf")
def logical_and(x1, x2):
    x1 = imp_utils.to_any(x1)
    x2 = imp_utils.to_any(x2)
    return imp_utils.ret(ffi.logical_and(x1, x2))

@set_module("raf")
def logical_not(x):
    x = imp_utils.to_any(x)
    return imp_utils.ret(ffi.logical_not(x))

@set_module("raf")
def matmul(x1, x2):
    x1 = imp_utils.to_any(x1)
    x2 = imp_utils.to_any(x2)
    return imp_utils.ret(ffi.matmul(x1, x2))

@set_module("raf")
def matmul_nt(x1, x2):
    x1 = imp_utils.to_any(x1)
    x2 = imp_utils.to_any(x2)
    return imp_utils.ret(ffi.matmul_nt(x1, x2))

@set_module("raf")
def matmul_tn(x1, x2):
    x1 = imp_utils.to_any(x1)
    x2 = imp_utils.to_any(x2)
    return imp_utils.ret(ffi.matmul_tn(x1, x2))

@set_module("raf")
def matmul_tt(x1, x2):
    x1 = imp_utils.to_any(x1)
    x2 = imp_utils.to_any(x2)
    return imp_utils.ret(ffi.matmul_tt(x1, x2))

@set_module("raf")
def max(x, axis=(), keepdims=False, exclude=False):
    x = imp_utils.to_tensor(x)
    axis = imp_utils.to_int_tuple(axis)
    keepdims = imp_utils.to_bool(keepdims)
    exclude = imp_utils.to_bool(exclude)
    return imp_utils.ret(ffi.max(x, axis, keepdims, exclude))

@set_module("raf")
def max_pool2d(x, kernel, stride, padding=0, dilation=1, ceil_mode=False, include_pad=True, layout="NCHW"):
    x = imp_utils.to_tensor(x)
    kernel = imp_utils.to_int_tuple(kernel)
    stride = imp_utils.to_int_tuple(stride)
    padding = imp_utils.to_int_tuple(padding)
    dilation = imp_utils.to_int_tuple(dilation)
    ceil_mode = imp_utils.to_bool(ceil_mode)
    include_pad = imp_utils.to_bool(include_pad)
    layout = imp_utils.to_string(layout)
    return imp_utils.ret(ffi.max_pool2d(x, kernel, stride, padding, dilation, ceil_mode, include_pad, layout))

@set_module("raf")
def max_pool2d_dx(x, y, dy, kernel, stride, padding, dilation, ceil_mode, include_pad):
    x = imp_utils.to_tensor(x)
    y = imp_utils.to_tensor(y)
    dy = imp_utils.to_tensor(dy)
    kernel = imp_utils.to_int_tuple(kernel)
    stride = imp_utils.to_int_tuple(stride)
    padding = imp_utils.to_int_tuple(padding)
    dilation = imp_utils.to_int_tuple(dilation)
    ceil_mode = imp_utils.to_bool(ceil_mode)
    include_pad = imp_utils.to_bool(include_pad)
    return imp_utils.ret(ffi.max_pool2d_dx(x, y, dy, kernel, stride, padding, dilation, ceil_mode, include_pad))

@set_module("raf")
def maximum(x1, x2):
    x1 = imp_utils.to_any(x1)
    x2 = imp_utils.to_any(x2)
    return imp_utils.ret(ffi.maximum(x1, x2))

@set_module("raf")
def mean(x, axis=(), keepdims=False, exclude=False):
    x = imp_utils.to_tensor(x)
    axis = imp_utils.to_int_tuple(axis)
    keepdims = imp_utils.to_bool(keepdims)
    exclude = imp_utils.to_bool(exclude)
    return imp_utils.ret(ffi.mean(x, axis, keepdims, exclude))

@set_module("raf")
def mean_dx(dy, shape, axis=(), keepdims=False, exclude=False):
    dy = imp_utils.to_tensor(dy)
    shape = imp_utils.to_any(shape)
    axis = imp_utils.to_int_tuple(axis)
    keepdims = imp_utils.to_bool(keepdims)
    exclude = imp_utils.to_bool(exclude)
    return imp_utils.ret(ffi.mean_dx(dy, shape, axis, keepdims, exclude))

@set_module("raf")
def mesh_grid(x):
    x = imp_utils.to_tensor_tuple(x)
    return imp_utils.ret(ffi.mesh_grid(x))

@set_module("raf")
def min(x, axis=(), keepdims=False, exclude=False):
    x = imp_utils.to_tensor(x)
    axis = imp_utils.to_int_tuple(axis)
    keepdims = imp_utils.to_bool(keepdims)
    exclude = imp_utils.to_bool(exclude)
    return imp_utils.ret(ffi.min(x, axis, keepdims, exclude))

@set_module("raf")
def minimum(x1, x2):
    x1 = imp_utils.to_any(x1)
    x2 = imp_utils.to_any(x2)
    return imp_utils.ret(ffi.minimum(x1, x2))

@set_module("raf")
def mod(x1, x2):
    x1 = imp_utils.to_any(x1)
    x2 = imp_utils.to_any(x2)
    return imp_utils.ret(ffi.mod(x1, x2))

@set_module("raf")
def multiply(x1, x2):
    x1 = imp_utils.to_any(x1)
    x2 = imp_utils.to_any(x2)
    return imp_utils.ret(ffi.multiply(x1, x2))

@set_module("raf")
def ndarray_size(x):
    x = imp_utils.to_any(x)
    return imp_utils.ret(ffi.ndarray_size(x))

@set_module("raf")
def negative(x):
    x = imp_utils.to_any(x)
    return imp_utils.ret(ffi.negative(x))

@set_module("raf")
def nll_loss(y_true, y_pred):
    y_true = imp_utils.to_tensor(y_true)
    y_pred = imp_utils.to_tensor(y_pred)
    return imp_utils.ret(ffi.nll_loss(y_true, y_pred))

@set_module("raf")
def nll_loss_dpred(dy, y_true, y_pred):
    dy = imp_utils.to_tensor(dy)
    y_true = imp_utils.to_tensor(y_true)
    y_pred = imp_utils.to_tensor(y_pred)
    return imp_utils.ret(ffi.nll_loss_dpred(dy, y_true, y_pred))

@set_module("raf")
def nll_loss_dtrue(dy, y_true, y_pred):
    dy = imp_utils.to_tensor(dy)
    y_true = imp_utils.to_tensor(y_true)
    y_pred = imp_utils.to_tensor(y_pred)
    return imp_utils.ret(ffi.nll_loss_dtrue(dy, y_true, y_pred))

@set_module("raf")
def non_max_suppression(data, valid_count, indices, max_output_size, iou_threshold, force_suppress=False, top_k=-1, coord_start=2, score_index=1, id_index=0, return_indices=True, invalid_to_bottom=False):
    data = imp_utils.to_tensor(data)
    valid_count = imp_utils.to_tensor(valid_count)
    indices = imp_utils.to_tensor(indices)
    max_output_size = imp_utils.to_tensor(max_output_size)
    iou_threshold = imp_utils.to_tensor(iou_threshold)
    force_suppress = imp_utils.to_bool(force_suppress)
    top_k = imp_utils.to_int(top_k)
    coord_start = imp_utils.to_int(coord_start)
    score_index = imp_utils.to_int(score_index)
    id_index = imp_utils.to_int(id_index)
    return_indices = imp_utils.to_bool(return_indices)
    invalid_to_bottom = imp_utils.to_bool(invalid_to_bottom)
    return imp_utils.ret(ffi.non_max_suppression(data, valid_count, indices, max_output_size, iou_threshold, force_suppress, top_k, coord_start, score_index, id_index, return_indices, invalid_to_bottom))

@set_module("raf")
def not_equal(x1, x2):
    x1 = imp_utils.to_any(x1)
    x2 = imp_utils.to_any(x2)
    return imp_utils.ret(ffi.not_equal(x1, x2))

@set_module("raf")
def numel(x):
    x = imp_utils.to_any(x)
    return imp_utils.ret(ffi.numel(x))

@set_module("raf")
def one_hot(indices, on_value, off_value, depth, axis=-1, dtype="int32", device="cpu"):
    indices = imp_utils.to_tensor(indices)
    on_value = imp_utils.to_tensor(on_value)
    off_value = imp_utils.to_tensor(off_value)
    depth = imp_utils.to_int(depth)
    axis = imp_utils.to_int(axis)
    dtype = imp_utils.to_string(dtype)
    device = imp_utils.to_string(device)
    return imp_utils.ret(ffi.one_hot(indices, on_value, off_value, depth, axis, dtype, device))

@set_module("raf")
def ones(shape, dtype="int32", device="cpu"):
    shape = imp_utils.to_any(shape)
    dtype = imp_utils.to_string(dtype)
    device = imp_utils.to_string(device)
    return imp_utils.ret(ffi.ones(shape, dtype, device))

@set_module("raf")
def ones_like(x):
    x = imp_utils.to_any(x)
    return imp_utils.ret(ffi.ones_like(x))

@set_module("raf")
def pad(x, pad_width, pad_value=0.0, pad_mode="constant"):
    x = imp_utils.to_tensor(x)
    pad_width = imp_utils.to_int_tuple(pad_width)
    pad_value = imp_utils.to_double(pad_value)
    pad_mode = imp_utils.to_string(pad_mode)
    return imp_utils.ret(ffi.pad(x, pad_width, pad_value, pad_mode))

@set_module("raf")
def power(x1, x2):
    x1 = imp_utils.to_any(x1)
    x2 = imp_utils.to_any(x2)
    return imp_utils.ret(ffi.power(x1, x2))

@set_module("raf")
def prod(x, axis=(), keepdims=False, exclude=False):
    x = imp_utils.to_tensor(x)
    axis = imp_utils.to_int_tuple(axis)
    keepdims = imp_utils.to_bool(keepdims)
    exclude = imp_utils.to_bool(exclude)
    return imp_utils.ret(ffi.prod(x, axis, keepdims, exclude))

@set_module("raf")
def prod_dx(x, dy, axis=(), keepdims=False, exclude=False):
    x = imp_utils.to_tensor(x)
    dy = imp_utils.to_tensor(dy)
    axis = imp_utils.to_int_tuple(axis)
    keepdims = imp_utils.to_bool(keepdims)
    exclude = imp_utils.to_bool(exclude)
    return imp_utils.ret(ffi.prod_dx(x, dy, axis, keepdims, exclude))

@set_module("raf")
def relu(x):
    x = imp_utils.to_any(x)
    return imp_utils.ret(ffi.relu(x))

@set_module("raf")
def relu_dx(x, y, dy):
    x = imp_utils.to_any(x)
    y = imp_utils.to_tensor(y)
    dy = imp_utils.to_tensor(dy)
    return imp_utils.ret(ffi.relu_dx(x, y, dy))

@set_module("raf")
def repeat(x, repeats, axis=None):
    x = imp_utils.to_tensor(x)
    repeats = imp_utils.to_int(repeats)
    axis = imp_utils.to_any(axis)
    return imp_utils.ret(ffi.repeat(x, repeats, axis))

@set_module("raf")
def repeat_dx(x, dy, repeats, axis=None):
    x = imp_utils.to_tensor(x)
    dy = imp_utils.to_tensor(dy)
    repeats = imp_utils.to_int(repeats)
    axis = imp_utils.to_any(axis)
    return imp_utils.ret(ffi.repeat_dx(x, dy, repeats, axis))

@set_module("raf")
def reshape(x, shape, reverse=False):
    x = imp_utils.to_tensor(x)
    shape = imp_utils.to_any(shape)
    reverse = imp_utils.to_bool(reverse)
    return imp_utils.ret(ffi.reshape(x, shape, reverse))

@set_module("raf")
def reshape_like(x, like_type):
    x = imp_utils.to_tensor(x)
    like_type = imp_utils.to_tensor(like_type)
    return imp_utils.ret(ffi.reshape_like(x, like_type))

@set_module("raf")
def resize2d(x, size, layout="NCHW", method="linear", coordinate_transformation_mode="half_pixel", rounding_method="", cubic_alpha=-0.5, cubic_exclude=0, out_dtype=""):
    x = imp_utils.to_tensor(x)
    size = imp_utils.to_any(size)
    layout = imp_utils.to_string(layout)
    method = imp_utils.to_string(method)
    coordinate_transformation_mode = imp_utils.to_string(coordinate_transformation_mode)
    rounding_method = imp_utils.to_string(rounding_method)
    cubic_alpha = imp_utils.to_double(cubic_alpha)
    cubic_exclude = imp_utils.to_int(cubic_exclude)
    out_dtype = imp_utils.to_string(out_dtype)
    return imp_utils.ret(ffi.resize2d(x, size, layout, method, coordinate_transformation_mode, rounding_method, cubic_alpha, cubic_exclude, out_dtype))

@set_module("raf")
def resize2d_dx(x, dy, size, layout="NCHW", method="linear", coordinate_transformation_mode="half_pixel", rounding_method="", cubic_alpha=-0.5, cubic_exclude=0, out_dtype=""):
    x = imp_utils.to_tensor(x)
    dy = imp_utils.to_tensor(dy)
    size = imp_utils.to_int_tuple(size)
    layout = imp_utils.to_string(layout)
    method = imp_utils.to_string(method)
    coordinate_transformation_mode = imp_utils.to_string(coordinate_transformation_mode)
    rounding_method = imp_utils.to_string(rounding_method)
    cubic_alpha = imp_utils.to_double(cubic_alpha)
    cubic_exclude = imp_utils.to_int(cubic_exclude)
    out_dtype = imp_utils.to_string(out_dtype)
    return imp_utils.ret(ffi.resize2d_dx(x, dy, size, layout, method, coordinate_transformation_mode, rounding_method, cubic_alpha, cubic_exclude, out_dtype))

@set_module("raf")
def reverse(x, axis=0):
    x = imp_utils.to_tensor(x)
    axis = imp_utils.to_int(axis)
    return imp_utils.ret(ffi.reverse(x, axis))

@set_module("raf")
def reverse_sequence(x, sequence_length, seq_axis=1, batch_axis=0):
    x = imp_utils.to_tensor(x)
    sequence_length = imp_utils.to_tensor(sequence_length)
    seq_axis = imp_utils.to_int(seq_axis)
    batch_axis = imp_utils.to_int(batch_axis)
    return imp_utils.ret(ffi.reverse_sequence(x, sequence_length, seq_axis, batch_axis))

@set_module("raf")
def right_shift(x1, x2):
    x1 = imp_utils.to_any(x1)
    x2 = imp_utils.to_any(x2)
    return imp_utils.ret(ffi.right_shift(x1, x2))

@set_module("raf")
def roi_align(data, rois, pooled_size, spatial_scale, sample_ratio=-1, layout="NCHW", mode="avg"):
    data = imp_utils.to_tensor(data)
    rois = imp_utils.to_tensor(rois)
    pooled_size = imp_utils.to_int_tuple(pooled_size)
    spatial_scale = imp_utils.to_double(spatial_scale)
    sample_ratio = imp_utils.to_int(sample_ratio)
    layout = imp_utils.to_string(layout)
    mode = imp_utils.to_string(mode)
    return imp_utils.ret(ffi.roi_align(data, rois, pooled_size, spatial_scale, sample_ratio, layout, mode))

@set_module("raf")
def roi_align_dx(data, rois, dy, pooled_size, spatial_scale, sample_ratio=-1, layout="NCHW", mode="avg"):
    data = imp_utils.to_tensor(data)
    rois = imp_utils.to_tensor(rois)
    dy = imp_utils.to_tensor(dy)
    pooled_size = imp_utils.to_int_tuple(pooled_size)
    spatial_scale = imp_utils.to_double(spatial_scale)
    sample_ratio = imp_utils.to_int(sample_ratio)
    layout = imp_utils.to_string(layout)
    mode = imp_utils.to_string(mode)
    return imp_utils.ret(ffi.roi_align_dx(data, rois, dy, pooled_size, spatial_scale, sample_ratio, layout, mode))

@set_module("raf")
def round(x):
    x = imp_utils.to_any(x)
    return imp_utils.ret(ffi.round(x))

@set_module("raf")
def rsqrt(x):
    x = imp_utils.to_any(x)
    return imp_utils.ret(ffi.rsqrt(x))

@set_module("raf")
def scatter(x, index, src, axis):
    x = imp_utils.to_tensor(x)
    index = imp_utils.to_tensor(index)
    src = imp_utils.to_tensor(src)
    axis = imp_utils.to_any(axis)
    return imp_utils.ret(ffi.scatter(x, index, src, axis))

@set_module("raf")
def scatter_dx(x, y, dy, index, src, axis):
    x = imp_utils.to_tensor(x)
    y = imp_utils.to_tensor(y)
    dy = imp_utils.to_tensor(dy)
    index = imp_utils.to_tensor(index)
    src = imp_utils.to_tensor(src)
    axis = imp_utils.to_any(axis)
    return imp_utils.ret(ffi.scatter_dx(x, y, dy, index, src, axis))

@set_module("raf")
def sequence_mask(x, sequence_length, mask_value=0.0, axis=0):
    x = imp_utils.to_tensor(x)
    sequence_length = imp_utils.to_tensor(sequence_length)
    mask_value = imp_utils.to_double(mask_value)
    axis = imp_utils.to_int(axis)
    return imp_utils.ret(ffi.sequence_mask(x, sequence_length, mask_value, axis))

@set_module("raf")
def set_stream(device_id, stream_id):
    device_id = imp_utils.to_int(device_id)
    stream_id = imp_utils.to_int(stream_id)
    return imp_utils.ret(ffi.set_stream(device_id, stream_id))

@set_module("raf")
def sgd(x, dx, v, learning_rate, mu):
    x = imp_utils.to_tensor(x)
    dx = imp_utils.to_tensor(dx)
    v = imp_utils.to_tensor(v)
    learning_rate = imp_utils.to_double(learning_rate)
    mu = imp_utils.to_double(mu)
    return imp_utils.ret(ffi.sgd(x, dx, v, learning_rate, mu))

@set_module("raf")
def shape(x):
    x = imp_utils.to_any(x)
    return imp_utils.ret(ffi.shape(x))

@set_module("raf")
def shape_as_tensor(x):
    x = imp_utils.to_any(x)
    return imp_utils.ret(ffi.shape_as_tensor(x))

@set_module("raf")
def sigmoid(x):
    x = imp_utils.to_any(x)
    return imp_utils.ret(ffi.sigmoid(x))

@set_module("raf")
def sigmoid_dx(x, y, dy):
    x = imp_utils.to_any(x)
    y = imp_utils.to_tensor(y)
    dy = imp_utils.to_tensor(dy)
    return imp_utils.ret(ffi.sigmoid_dx(x, y, dy))

@set_module("raf")
def sign(x):
    x = imp_utils.to_any(x)
    return imp_utils.ret(ffi.sign(x))

@set_module("raf")
def sin(x):
    x = imp_utils.to_any(x)
    return imp_utils.ret(ffi.sin(x))

@set_module("raf")
def size(x, axis=None):
    x = imp_utils.to_tensor(x)
    axis = imp_utils.to_any(axis)
    return imp_utils.ret(ffi.size(x, axis))

@set_module("raf")
def smooth_l1_loss(y_true, y_pred):
    y_true = imp_utils.to_tensor(y_true)
    y_pred = imp_utils.to_tensor(y_pred)
    return imp_utils.ret(ffi.smooth_l1_loss(y_true, y_pred))

@set_module("raf")
def smooth_l1_loss_dpred(y_true, y_pred):
    y_true = imp_utils.to_tensor(y_true)
    y_pred = imp_utils.to_tensor(y_pred)
    return imp_utils.ret(ffi.smooth_l1_loss_dpred(y_true, y_pred))

@set_module("raf")
def smooth_l1_loss_dtrue(y_true, y_pred):
    y_true = imp_utils.to_tensor(y_true)
    y_pred = imp_utils.to_tensor(y_pred)
    return imp_utils.ret(ffi.smooth_l1_loss_dtrue(y_true, y_pred))

@set_module("raf")
def softmax(x, axis=-1):
    x = imp_utils.to_tensor(x)
    axis = imp_utils.to_int(axis)
    return imp_utils.ret(ffi.softmax(x, axis))

@set_module("raf")
def softmax_dx(y, dy, axis=-1):
    y = imp_utils.to_tensor(y)
    dy = imp_utils.to_tensor(dy)
    axis = imp_utils.to_int(axis)
    return imp_utils.ret(ffi.softmax_dx(y, dy, axis))

@set_module("raf")
def sort(data, axis=-1, is_ascend=True):
    data = imp_utils.to_tensor(data)
    axis = imp_utils.to_int(axis)
    is_ascend = imp_utils.to_bool(is_ascend)
    return imp_utils.ret(ffi.sort(data, axis, is_ascend))

@set_module("raf")
def split(x, indices_or_sections=None, axis=0):
    x = imp_utils.to_tensor(x)
    indices_or_sections = imp_utils.to_any(indices_or_sections)
    axis = imp_utils.to_int(axis)
    return imp_utils.ret(ffi.split(x, indices_or_sections, axis))

@set_module("raf")
def sqrt(x):
    x = imp_utils.to_any(x)
    return imp_utils.ret(ffi.sqrt(x))

@set_module("raf")
def sqrt_dx(x, y, dy):
    x = imp_utils.to_any(x)
    y = imp_utils.to_tensor(y)
    dy = imp_utils.to_tensor(dy)
    return imp_utils.ret(ffi.sqrt_dx(x, y, dy))

@set_module("raf")
def squeeze(x, axis=None):
    x = imp_utils.to_tensor(x)
    axis = imp_utils.to_int_tuple(axis)
    return imp_utils.ret(ffi.squeeze(x, axis))

@set_module("raf")
def stack(x, axis=0):
    x = imp_utils.to_tensor_tuple(x)
    axis = imp_utils.to_int(axis)
    return imp_utils.ret(ffi.stack(x, axis))

@set_module("raf")
def stream_barrier():

    return imp_utils.ret(ffi.stream_barrier())

@set_module("raf")
def stream_sync(x, stream_tag=0):
    x = imp_utils.to_tensor(x)
    stream_tag = imp_utils.to_int(stream_tag)
    return imp_utils.ret(ffi.stream_sync(x, stream_tag))

@set_module("raf")
def strided_set(data, v, begin, end, strides=None):
    data = imp_utils.to_tensor(data)
    v = imp_utils.to_tensor(v)
    begin = imp_utils.to_int_tuple(begin)
    end = imp_utils.to_int_tuple(end)
    strides = imp_utils.to_int_tuple(strides)
    return imp_utils.ret(ffi.strided_set(data, v, begin, end, strides))

@set_module("raf")
def strided_slice(x, begin, end, strides=None, slice_mode="end"):
    x = imp_utils.to_tensor(x)
    begin = imp_utils.to_any(begin)
    end = imp_utils.to_any(end)
    strides = imp_utils.to_int_tuple(strides)
    slice_mode = imp_utils.to_string(slice_mode)
    return imp_utils.ret(ffi.strided_slice(x, begin, end, strides, slice_mode))

@set_module("raf")
def strided_slice_dx(dy, shape, begin, end, strides=None, slice_mode="end"):
    dy = imp_utils.to_tensor(dy)
    shape = imp_utils.to_any(shape)
    begin = imp_utils.to_int_tuple(begin)
    end = imp_utils.to_int_tuple(end)
    strides = imp_utils.to_int_tuple(strides)
    slice_mode = imp_utils.to_string(slice_mode)
    return imp_utils.ret(ffi.strided_slice_dx(dy, shape, begin, end, strides, slice_mode))

@set_module("raf")
def subtract(x1, x2, out=None, where=None):
    x1 = imp_utils.to_any(x1)
    x2 = imp_utils.to_any(x2)
    out = imp_utils.to_any(out)
    where = imp_utils.to_any(where)
    return imp_utils.ret(ffi.subtract(x1, x2, out, where))

@set_module("raf")
def sum(x, axis=(), keepdims=0, exclude=False):
    x = imp_utils.to_tensor(x)
    axis = imp_utils.to_int_tuple(axis)
    keepdims = imp_utils.to_int_tuple(keepdims)
    exclude = imp_utils.to_bool(exclude)
    return imp_utils.ret(ffi.sum(x, axis, keepdims, exclude))

@set_module("raf")
def sum_dx(x, dy, axis=(), keepdims=0, exclude=False):
    x = imp_utils.to_tensor(x)
    dy = imp_utils.to_tensor(dy)
    axis = imp_utils.to_int_tuple(axis)
    keepdims = imp_utils.to_int_tuple(keepdims)
    exclude = imp_utils.to_bool(exclude)
    return imp_utils.ret(ffi.sum_dx(x, dy, axis, keepdims, exclude))

@set_module("raf")
def swap_axis(x, axis1, axis2):
    x = imp_utils.to_tensor(x)
    axis1 = imp_utils.to_int(axis1)
    axis2 = imp_utils.to_int(axis2)
    return imp_utils.ret(ffi.swap_axis(x, axis1, axis2))

@set_module("raf")
def take(x, indices, axis=None, mode="clip"):
    x = imp_utils.to_tensor(x)
    indices = imp_utils.to_tensor(indices)
    axis = imp_utils.to_any(axis)
    mode = imp_utils.to_string(mode)
    return imp_utils.ret(ffi.take(x, indices, axis, mode))

@set_module("raf")
def take_dx(x, dy, indices, axis=None, mode="clip"):
    x = imp_utils.to_tensor(x)
    dy = imp_utils.to_tensor(dy)
    indices = imp_utils.to_tensor(indices)
    axis = imp_utils.to_any(axis)
    mode = imp_utils.to_string(mode)
    return imp_utils.ret(ffi.take_dx(x, dy, indices, axis, mode))

@set_module("raf")
def tanh(x):
    x = imp_utils.to_any(x)
    return imp_utils.ret(ffi.tanh(x))

@set_module("raf")
def tanh_dx(x, y, dy):
    x = imp_utils.to_any(x)
    y = imp_utils.to_tensor(y)
    dy = imp_utils.to_tensor(dy)
    return imp_utils.ret(ffi.tanh_dx(x, y, dy))

@set_module("raf")
def threefry_generate(key, shape):
    key = imp_utils.to_tensor(key)
    shape = imp_utils.to_int_tuple(shape)
    return imp_utils.ret(ffi.threefry_generate(key, shape))

@set_module("raf")
def threefry_split(key):
    key = imp_utils.to_tensor(key)
    return imp_utils.ret(ffi.threefry_split(key))

@set_module("raf")
def threshold(x, threshold=0.0, value=0.0):
    x = imp_utils.to_any(x)
    threshold = imp_utils.to_double(threshold)
    value = imp_utils.to_double(value)
    return imp_utils.ret(ffi.threshold(x, threshold, value))

@set_module("raf")
def threshold_dx(x, dy, threshold=0.0):
    x = imp_utils.to_any(x)
    dy = imp_utils.to_tensor(dy)
    threshold = imp_utils.to_double(threshold)
    return imp_utils.ret(ffi.threshold_dx(x, dy, threshold))

@set_module("raf")
def topk(data, k, axis=-1, ret_type="both", is_ascend=False, dtype="int64"):
    data = imp_utils.to_tensor(data)
    k = imp_utils.to_any(k)
    axis = imp_utils.to_int(axis)
    ret_type = imp_utils.to_string(ret_type)
    is_ascend = imp_utils.to_bool(is_ascend)
    dtype = imp_utils.to_string(dtype)
    return imp_utils.ret(ffi.topk(data, k, axis, ret_type, is_ascend, dtype))

@set_module("raf")
def transpose(x, axes=None):
    x = imp_utils.to_tensor(x)
    axes = imp_utils.to_int_tuple(axes)
    return imp_utils.ret(ffi.transpose(x, axes))

@set_module("raf")
def transpose_dx(x, axes=None):
    x = imp_utils.to_tensor(x)
    axes = imp_utils.to_int_tuple(axes)
    return imp_utils.ret(ffi.transpose_dx(x, axes))

@set_module("raf")
def trunc(x):
    x = imp_utils.to_any(x)
    return imp_utils.ret(ffi.trunc(x))

@set_module("raf")
def upper_bound_argwhere(condition):
    condition = imp_utils.to_tensor(condition)
    return imp_utils.ret(ffi.upper_bound.argwhere(condition))

@set_module("raf")
def vm_alloc_storage(size, alignment, device_type, device_id, dtype="float32", alloc_async=True):
    size = imp_utils.to_any(size)
    alignment = imp_utils.to_any(alignment)
    device_type = imp_utils.to_int(device_type)
    device_id = imp_utils.to_int(device_id)
    dtype = imp_utils.to_string(dtype)
    alloc_async = imp_utils.to_bool(alloc_async)
    return imp_utils.ret(ffi.vm.alloc_storage(size, alignment, device_type, device_id, dtype, alloc_async))

@set_module("raf")
def vm_alloc_tensor(storage, shape, dtype="float32", assert_shape=None, own=True):
    storage = imp_utils.to_tensor(storage)
    shape = imp_utils.to_any(shape)
    dtype = imp_utils.to_string(dtype)
    assert_shape = imp_utils.to_int_tuple(assert_shape)
    own = imp_utils.to_bool(own)
    return imp_utils.ret(ffi.vm.alloc_tensor(storage, shape, dtype, assert_shape, own))

@set_module("raf")
def vm_free(memory):
    memory = imp_utils.to_tensor(memory)
    return imp_utils.ret(ffi.vm.free(memory))

@set_module("raf")
def vm_infer_type(func, inputs):
    func = imp_utils.to_any(func)
    inputs = imp_utils.to_any(inputs)
    return imp_utils.ret(ffi.vm.infer_type(func, inputs))

@set_module("raf")
def vm_invoke_op(func, inputs, outputs):
    func = imp_utils.to_any(func)
    inputs = imp_utils.to_any(inputs)
    outputs = imp_utils.to_any(outputs)
    return imp_utils.ret(ffi.vm.invoke_op(func, inputs, outputs))

@set_module("raf")
def vm_set_shape(data, shape):
    data = imp_utils.to_tensor(data)
    shape = imp_utils.to_any(shape)
    return imp_utils.ret(ffi.vm.set_shape(data, shape))

@set_module("raf")
def wait_event(event_id, stream_id=-1):
    event_id = imp_utils.to_int(event_id)
    stream_id = imp_utils.to_int(stream_id)
    return imp_utils.ret(ffi.wait_event(event_id, stream_id))

@set_module("raf")
def where(condition, x, y):
    condition = imp_utils.to_tensor(condition)
    x = imp_utils.to_tensor(x)
    y = imp_utils.to_tensor(y)
    return imp_utils.ret(ffi.where(condition, x, y))

@set_module("raf")
def zeros(shape, dtype="int32", device="cpu"):
    shape = imp_utils.to_any(shape)
    dtype = imp_utils.to_string(dtype)
    device = imp_utils.to_string(device)
    return imp_utils.ret(ffi.zeros(shape, dtype, device))

@set_module("raf")
def zeros_like(x):
    x = imp_utils.to_any(x)
    return imp_utils.ret(ffi.zeros_like(x))
