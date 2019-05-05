from util import check_chinese_char


def test_check_chinese_char_has_chinese():
    t_str = "aaaaaaaaa 在 中 一"
    assert check_chinese_char(t_str) is True


def test_check_chinese_char_no_chinese():
    t_str = "fdavwavaafq"
    assert check_chinese_char(t_str) is False


def test_filter_argss():
    import re
    args_pattern = re.compile(u"(Arguments)|(Args)|(:param)")

    str1 = """Functional interface for the densely-connected layer.
  This layer implements the operation:
  `outputs = activation(inputs * kernel + bias)`
  where `activation` is the activation function passed as the `activation`
  argument (if not `None`), `kernel` is a weights matrix created by the layer,
  and `bias` is a bias vector created by the layer
  (only if `use_bias` is `True`).
  Arguments:
    inputs: Tensor input.
    units: Integer or Long, dimensionality of the output space.
    activation: Activation function (callable). Set it to None to maintain a
      linear activation.
    use_bias: Boolean, whether the layer uses a bias.
    kernel_initializer: Initializer function for the weight matrix.
      If `None` (default), weights are initialized using the default
      initializer used by `tf.compat.v1.get_variable`.
    bias_initializer: Initializer function for the bias.
    kernel_regularizer: Regularizer function for the weight matrix.
    bias_regularizer: Regularizer function for the bias.
    activity_regularizer: Regularizer function for the output.
    kernel_constraint: An optional projection function to be applied to the
        kernel after being updated by an `Optimizer` (e.g. used to implement
        norm constraints or value constraints for layer weights). The function
        must take as input the unprojected variable and must return the
        projected variable (which must have the same shape). Constraints are
        not safe to use when doing asynchronous distributed training.
    bias_constraint: An optional projection function to be applied to the
        bias after being updated by an `Optimizer`.
    trainable: Boolean, if `True` also add variables to the graph collection
      `GraphKeys.TRAINABLE_VARIABLES` (see `tf.Variable`).
    name: String, the name of the layer.
    reuse: Boolean, whether to reuse the weights of a previous layer
      by the same name.
  Returns:
    Output tensor the same shape as `inputs` except the last dimension is of
    size `units`.
  Raises:
    ValueError: if eager execution is enabled."""

    str2 = """提取函数节点中的函数定义，函数描述（docstring），函数体

    :param node: 函数节点
    :param out_func_decl_fd: 输出函数定义的流
    :param out_description_fd: 输出函数描述的流
    :param out_bodies_fd: 输出函数体的流
    :return:
    """

    str3 = """Computes the gradient of conv1d with respect to the weight of the convolution.
    Args:
        input: input tensor of shape (minibatch x in_channels x iW)
        weight_size : Shape of the weight gradient tensor
        grad_output : output gradient tensor (minibatch x out_channels x oW)
        stride (int or tuple, optional): Stride of the convolution. Default: 1
        padding (int or tuple, optional): Zero-padding added to both sides of the input. Default: 0
        dilation (int or tuple, optional): Spacing between kernel elements. Default: 1
        groups (int, optional): Number of blocked connections from input channels to output channels. Default: 1
    Examples::
        >>> input = torch.randn(1,1,3, requires_grad=True)
        >>> weight = torch.randn(1,1,1, requires_grad=True)
        >>> output = F.conv1d(input, weight)
        >>> grad_output = torch.randn(output.shape)
        >>> grad_weight = torch.autograd.grad(output, filter, grad_output)
        >>> F.grad.conv1d_weight(input, weight.shape, grad_output)"""

    assert args_pattern.search(str1)
    assert args_pattern.search(str2)
    assert args_pattern.search(str3)
