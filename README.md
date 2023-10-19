# PyTorch ROCm gfx803

build pytorch 1.x with ROCm support for stable-diffusion-webui

```
Ubuntu 22.04.2 LTS
Radeon RX 580 8GB
RoCm 5.4.3
Gcc 11.2.0
Linux 5.19

Python 3.10.6
- pytorch 1.13.1
- torchvision 0.14.1
```

## Install ROCm

Ubuntu and other Debian-based distros:

```bash
sudo echo ROC_ENABLE_PRE_VEGA=1 >> /etc/environment
sudo echo HSA_OVERRIDE_GFX_VERSION=8.0.3 >> /etc/environment
# reboot

wget https://repo.radeon.com/amdgpu-install/22.40.3/ubuntu/focal/amdgpu-install_5.4.50403-1_all.deb
sudo apt install ./amdgpu-install_5.4.50403-1_all.deb
sudo amdgpu-install -y --usecase=rocm,hiplibsdk,mlsdk

sudo usermod -aG video $LOGNAME
sudo usermod -aG render $LOGNAME

# verify
rocminfo
clinfo
```

Fedora & possibly other RH-based distros:

```bash
sudo echo ROC_ENABLE_PRE_VEGA=1 >> /etc/environment
sudo echo HSA_OVERRIDE_GFX_VERSION=8.0.3 >> /etc/environment
# reboot

curl -LO https://repo.radeon.com/amdgpu-install/5.5/rhel/9.1/amdgpu-install-5.5.50500-1.el9.noarch.rpm
sudo dnf install ./amdgpu-install-5.5.50500-1.el9.noarch.rpm
sudo sed -i 's/\$amdgpudistro/9.1/gi' /etc/yum.repos.d/amdgpu.repo # on fedora, renders an error otherwise
sudo sed -i 's/\$amdgpudistro/9.1/gi' /etc/yum.repos.d/amdgpu-proprietary.repo # on fedora, renders an error otherwise
sudo amdgpu-install -y --usecase=rocm,hiplibsdk,mlsdk

sudo usermod -aG video $LOGNAME
sudo usermod -aG render $LOGNAME

# verify
rocminfo
clinfo
```

## Build

You may need to install additional dependencies, and the build will take a long time.

**TL;DR:** use the prebuilt [binaries](https://github.com/tsl0922/pytorch-gfx803/releases) if you want to make your life easier.

> Quick note for Fedora users trying to use prebuilt binaries:
>
> Sometimes this error shows up even if `openmpi` and `openmpi-devel` packages were already installed:
> 
> `OSError: libmpi_cxx.so.40: cannot open shared object file: No such file or directory while import torch`
> 
> To fix that, you should add the path to OpenMPI libraries to LD_LIBRARY_PATH:
> 
> 1. Open the config file: `sudo nano /etc/ld.so.conf.d/openmpi-x86_64.conf`.
> 2. Paste `/usr/lib64/openmpi/lib`, then save and quit.
> 3. Run `sudo ldconfig` to refresh dynamic library cache.

### Build pytorch

```bash
git clone https://github.com/pytorch/pytorch.git -b v1.13.1
cd pytorch
export PATH=/opt/rocm/bin:$PATH ROCM_PATH=/opt/rocm HIP_PATH=/opt/rocm/hip
export PYTORCH_ROCM_ARCH=gfx803
export PYTORCH_BUILD_VERSION=1.13.1 PYTORCH_BUILD_NUMBER=1
python3 tools/amd_build/build_amd.py
USE_ROCM=1 USE_NINJA=1 python3 setup.py bdist_wheel
pip3 install dist/torch-1.13.1-cp310-cp310-linux_x86_64.whl
```

### Build torchvision

```bash
git clone https://github.com/pytorch/vision.git -b v0.14.1
cd vision
export BUILD_VERSION=0.14.1
FORCE_CUDA=1 ROCM_HOME=/opt/rocm/ python3 setup.py bdist_wheel
pip3 install dist/torchvision-0.14.1-cp310-cp310-linux_x86_64.whl
```

## Test

```python
import torch
torch.cuda.is_available()
```

## Reference

- https://github.com/RadeonOpenCompute/ROCm/issues/1659
- https://github.com/xuhuisheng/rocm-gfx803
