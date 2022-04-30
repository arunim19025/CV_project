#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import cv2
import numpy as np
from skimage import transform
from IPython.display import display
from skimage import transform, exposure
from PIL import Image, ImageOps,ImageEnhance
import thinplate.hybrid as tps
import blend_modes
from PIL import ImageEnhance, Image
import matplotlib.pyplot as plt
import blend_modes
pil_imshow = lambda x: display(Image.fromarray(x.astype(np.uint8)))


# In[ ]:


def importFabric(path):
    fabric = cv2.imread(path)
    fabric_img = cv2.cvtColor(fabric, cv2.COLOR_BGR2RGB)
    pil_imshow(fabric_img)
    
    return fabric_img


# In[ ]:


def importBase(path):
    base = cv2.imread(path)
    base_img = cv2.cvtColor(base, cv2.COLOR_BGR2RGB)
    pil_imshow(base_img)
    
    return base_img, base_img.shape


# In[ ]:


def create_pts_for_tps(cords,res):
    # Ignore (Used in Bedsheets)
    slcs = {40:(0,None)}
    snew, dnew = [], []
    
    for idx,i in enumerate(cords):
        if len(i) > 2:
            s,e = slcs[idx] if idx in slcs else (0,None)
            snew.append(np.linspace(i[0], i[1], i[2])[s:e]) # generates new pts between the 2 end points
            dnew.append(np.linspace(i[3], i[4], i[2])[s:e])
        else:
            snew.append(np.array([i[0]]))
            dnew.append(np.array([i[1]]))

    c_src = np.vstack(snew).astype(np.float32)
    c_dst = np.vstack(dnew).astype(np.float32)
    
    assert len(c_src) == len(c_dst), f"{len(c_src)}, {len(c_dst)}"

    _, idxs = np.unique(c_dst.astype(int), return_index=True, axis=0)
    c_src = c_src[idxs]/1.
    c_dst = c_dst[idxs]/np.array(res).astype(np.float32)

    return c_src,c_dst


# In[ ]:


def Thin_plate_splines(c_src,c_dst,output_size, fabric):

    # We first calculate theta for our grid generation
    theta = tps.tps_theta_from_points(c_src, c_dst, reduced=False)
    
    # Genertaes grid x,y, values  where to map
    grid = tps.tps_grid(theta, c_dst, out_size)
    
    # Extract x and y values from grid to map it to org img
    mapx, mapy = tps.tps_grid_to_remap(grid, fabric.shape)

    # We create the fabric 
    tpw = cv2.remap(fabric, mapx, mapy, cv2.INTER_CUBIC)
    cv2.imwrite('fabric_after_tps.jpg', tpw)
    
    print("Generated Fabric Segment Image")
    pil_imshow(tpw)
    
    return tpw


# In[ ]:


fabric = importFabric('dataset/fabric2.jpg')
base, out_size= importBase('dataset/base1.jpg')
res = [out_size[1], out_size[0]]


# In[ ]:


# Cordinates stucture : [[Top Left of Fabric], [Top Right of Fabric], 
#(Number of Points to be Generated between these endpoints), [Top Left of Base Img], [Top Right of Base Img]
cords =[[[0.0, 0.0], [1.0, 0.0], 4, [56, 40], [463, 40]], 
        [[0.0, 0.4], [1.0, 0.4], 4, [50, 500], [480,500]],    
        [[0.0, 1.0], [1.0, 1.0], 4, [2, 1412], [460,1412]],]

c_src ,c_dst = create_pts_for_tps(cords,res)
left_mask = Thin_plate_splines(c_src,c_dst,out_size, fabric)


# In[ ]:


base_left = cv2.addWeighted(base, 0.9,left_mask, 0.3, 0)
pil_imshow(base_left)


# In[ ]:


cords = [[[0.0, 0.0], [1.0, 0.0], 4, [640, 40], [1020, 40]],
        #[[0.0, 0.2], [1.0, 0.2], 4, [635, 289], [1200,289]],
        [[0.0, 0.4], [1.0, 0.4], 8, [628, 639], [1036,639]],    
        [[0.0, 1.0], [1.0, 1.0], 4, [637, 1420], [1073,1420]],         
    ]

c_src ,c_dst = create_pts_for_tps(cords,res)
right_mask = Thin_plate_splines(c_src,c_dst,out_size, fabric)


# In[ ]:


back_im = cv2.addWeighted(base_left, 1,right_mask, 0.3, 0)
pil_imshow(back_im)


# In[ ]:


disp_im = cv2.addWeighted(back_im, 0.9,back_im, 0.1, 0)
pil_imshow(disp_im)


# In[ ]:





# In[ ]:




