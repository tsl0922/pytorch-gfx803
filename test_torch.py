import torch

print("Cuda available:", torch.cuda.is_available())
print("Number of devices:", torch.cuda.device_count())
print("Current device index:", torch.cuda.current_device())
print("Current device name:",
      torch.cuda.get_device_name(torch.cuda.current_device()))

tensor = torch.randn(2, 2)
res = tensor.to(0)
print(res)


print("----------------------------")
print("Torch successfully installed")
