def assert_cuda_availability():
    import torch

    assert torch.cuda.is_available(), "CUDA is not available"
