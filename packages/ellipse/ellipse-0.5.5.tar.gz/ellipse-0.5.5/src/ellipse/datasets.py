import numpy as np
from . import generate, get_ellipse, check_bounds

def torus(n=10000, img_size=64, downsample_factor=4, return_arrays=False):
    r""" Generate a dataset of a topolgical torus in parameter space.
    :param: n = approximate number to produce (default 10000). Sampling is by sqrt(n)
    :param: img_size, default 64
    :param: downsample_factor, default 4
    :param: return_arrays, bool. If `output_arrays` is False [default], return the parameter dictionaries, and user must apply `[ get_ellipse(**p) for p in torus() ]` to generate the arrays. If `output_arrays` is True, returns the numpy arrays.
    :return: list of dictionaries or images.
    """
    gran = int(np.sqrt(n))
    img_size = 64
    center = img_size/2
    r = img_size/3
    logar = 0.5
    size = (img_size/10)**2
    a = np.sqrt(size*np.exp(logar))
    b = np.sqrt(size/np.exp(logar))
    
    out_lst = []
    for i in range(gran):
        alpha = 2*np.pi*i/gran
        row = center+np.cos(alpha)*r
        col = center+np.sin(alpha)*r
        for j in range(gran):
            theta = np.pi/gran*j
            p = {'img_size':img_size, 'row':row, 'col':col, 'a':a, 'b':b, 'theta':theta, 'downsample_factor':downsample_factor}
            assert check_bounds(**p), f"Produced an out-of-bounds image! {p}"
            if return_arrays:
                out_lst.append(get_ellipse(**p))
            else:
                out_lst.append(p)
    
    return out_lst