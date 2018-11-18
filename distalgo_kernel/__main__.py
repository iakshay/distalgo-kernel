from ipykernel.kernelapp import IPKernelApp
from .kernel import DistAlgoKernel

IPKernelApp.launch_instance(kernel_class=DistAlgoKernel)
