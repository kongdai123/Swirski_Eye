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

outer_eye = bpy.data.collections["Collection 1"].objects['eye-outer']

def rotate_eye(obj, x_angle, z_angle):
    obj.rotation_mode = 'XYZ'
    deg_to_rad = np.pi * 2/360
    x_rot = -x_angle * deg_to_rad
    z_rot = z_angle * deg_to_rad
    euler_rotation =  Euler((x_rot, 0, z_rot) , 'XYZ')
    obj.rotation_euler = euler_rotation
    outer_eye.rotation_euler = Euler((-x_rot - np.pi/2, 0, z_rot) , 'XYZ')
    obj_rot_mat = euler_rotation.to_matrix()
    
    #obj_rot_mat = initPoseMat

    if obj.parent:
        P = obj.parent.matrix.decompose()[1].to_matrix()
        obj_rot_mat = P * obj_rot_mat * P.inverted()



def set_Swirski_config(elev, azim, clo, pattern_path):
    print("hello")
    z_angle = -azim
    x_angle = -elev
    outer_eye = bpy.data.collections["Collection 1"].objects['eye-outer']

    scene = bpy.context.scene
    armature = bpy.data.objects['Armature Head']
    camera_obj = bpy.data.objects['Camera']
    camera = bpy.data.cameras['Camera']


    eyeLbone = armature.pose.bones['def_eye.L']
    eyeLblinkbone = armature.pose.bones['eyeblink.L']
    eyeRbone = armature.pose.bones['def_eye.R']
    eyeRblinkbone = armature.pose.bones['eyeblink.R']

    input_eye_closedness = 0

    plane  = bpy.data.objects['Plane']

    texture = plane.active_material.node_tree.nodes['Image Texture'].image
    texture.filepath =  pattern_path

    for c in list(eyeLbone.constraints.values()):
        eyeLbone.constraints.remove(c)
    for c in list(eyeRbone.constraints.values()):
        eyeRbone.constraints.remove(c)

    rotate_eye(eyeLbone, x_angle, z_angle)

    eyeLblinkbone.location[2] = input_eye_closedness * eyeLblinkbone.constraints['Limit Location'].max_z   
    eyeRblinkbone.location[2] = input_eye_closedness * eyeRblinkbone.constraints['Limit Location'].max_z 

