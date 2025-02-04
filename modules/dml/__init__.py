# pylint: disable=no-member,no-self-argument
import torch
import torch_directml # pylint: disable=import-error

import modules.dml.hijack

from .optimizer.unknown import UnknownOptimizer

class DirectML():
    def get_optimizer(device: torch.device):
        assert device.type == 'privateuseone'
        try:
            device_name = torch_directml.device_name(device.index)
            if 'NVIDIA' in device_name or 'GeForce' in device_name:
                from .optimizer.nvidia import nVidiaOptimizer as optimizer
            elif 'AMD' in device_name or 'Radeon' in device_name:
                from .optimizer.amd import AMDOptimizer as optimizer
            elif 'Intel' in device_name:
                from .optimizer.intel import IntelOptimizer as optimizer
            else:
                return UnknownOptimizer
            return optimizer
        except:
            return UnknownOptimizer

    def memory_stats(device: torch.device):
        optimizer = DirectML.get_optimizer(device)
        return optimizer.memory_stats(device.index)

# Alternative of torch.cuda for DirectML.
torch.dml = DirectML
