import bpy
import math
import mathutils
import os
import sys
import functools
import collections
import random
from mathutils import Vector, Matrix, Euler
try:
    import numpy as np
except:
    np = None

import sys
sys.path.insert(1, '/content/Swirski_Eye')

from set_Swirski_config import *



##enable cuda computation
def enable_gpus(device_type, use_cpus=False):
    preferences = bpy.context.preferences
    cycles_preferences = preferences.addons["cycles"].preferences
    cuda_devices, opencl_devices = cycles_preferences.get_devices()

    if device_type == "CUDA":
        devices = cuda_devices
    elif device_type == "OPENCL":
        devices = opencl_devices
    else:
        raise RuntimeError("Unsupported device type")

    activated_gpus = []

    for device in devices:
        if device.type == "CPU":
            device.use = use_cpus
        else:
            device.use = True
            activated_gpus.append(device.name)

    cycles_preferences.compute_device_type = device_type
    bpy.context.scene.cycles.device = "GPU"

    return activated_gpus


gpus = enable_gpus("CUDA")
print(gpus)

engines = ('BLENDER_EEVEE', 'CYCLES')
engine_chosen = engines[1]
bpy.context.scene.render.engine = engine_chosen


frame_num = 1
dim = 100
# std = np.pi/2 * 15/90 #15 degs

#initialize normal distribution with std = 15 deg
rand_seed = 42
np.random.seed(rand_seed)
angles = np.random.normal(0, 15, dim)
print(angles)
elev, azim = np.meshgrid(angles, angles)

np.random.seed(40)
closedness = np.abs(np.random.normal(0, 0.25, dim* dim))

for i in range(1):
    for j in range(1):
        input_eye_closedness = 0
        pattern_path =  "/content/Swirski_Eye/496-free-hdri-skies-com.jpg"
        set_Swirski_config(elev[i][j], azim[i][j], input_eye_closedness, pattern_path)
        bpy.context.scene.render.filepath = "/content/test.png"
        bpy.ops.render.render(write_still=True)


