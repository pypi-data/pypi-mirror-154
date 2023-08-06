import torch

from .constants import (
    PYTORCH_EXT
)

# Makes filename for .pt file using provided prefix filename
def generate_pt_filename(filename_prefix: str) -> str:
  """Returns proper filename for PyTorch file containing model weights, 
     i.e. filename.pt

  Args:
    filename_prefix: part of PyTorch filename that comes before PyTorch file extension
     i.e. '{filename_prefix}.pt'

  Returns:
    pt_filename: PyTorch filename of the form '{filename_prefix}.pt'
  """
  pt_filename = f'{filename_prefix}{PYTORCH_EXT}'
  return pt_filename

# Determine PyTorch settings
def determine_device(no_cuda: bool = False) -> torch.device:
  """Determines device based on CUDA availability on host and no_cuda parameter

  Args:
    no_cuda: boolean indicates if CUDA should not be used. Default is False.

  Returns:
    device: PyTorch device, i.e. cuda or cpu
    use_cuda: boolean indicating if CUDA should be used for task
  """
  use_cuda = not no_cuda and torch.cuda.is_available()
  device = torch.device('cuda' if use_cuda else 'cpu')
  return device, use_cuda