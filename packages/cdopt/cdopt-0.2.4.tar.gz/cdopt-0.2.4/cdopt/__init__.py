__all__ = ["core", "manifold", "manifold_np", "manifold_torch"]
__author__ = 'Nachuan Xiao, Xiaoyin Hu, Xin Liu, and Kim-Chuan Toh'

from . import manifold_np,  manifold
from .core import problem, backbone_autograd

try:
    import torch
    from .core import backbone_torch
    from . import manifold_torch
    from . import nn
except ImportError:
    print('Warning: Cannot import PyTorch-related components, including `cdopt.manifold_torch` and `cdopt.nn`. Please check whether PyTorch is correctly installed.')


try:
    import jax 
    from .core  import backbone_jax
except ImportError:
    print('Warning: Cannot import JAX-related components. Please check whether JAX is correctly installed.')
