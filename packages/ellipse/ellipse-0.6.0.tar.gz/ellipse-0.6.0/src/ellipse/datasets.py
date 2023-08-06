from re import I
import numpy as np
from . import generate, get_ellipse, check_bounds

def circle(n=10000, img_size=64, downsample_factor=4, return_arrays=False):
    """ A circle of circles """
    center = img_size/2
    r = img_size/3
    a = img_size/6
    b = img_size/6
    out_lst = []
    for i in range(n):
        alpha = 2*np.pi*i/n
        row = center + r*np.cos(alpha)
        col = center + r*np.sin(alpha)
        p = {'img_size':img_size, 'row':row, 'col':col, 'a':a, 'b':b, 'theta':0, 'downsample_factor':downsample_factor}
        assert check_bounds(**p), f"Produced an out-of-bounds image! {p}"
        if return_arrays:
            out_lst.append(get_ellipse(**p))
        else:
            out_lst.append(p)
    return out_lst

def spin(n=10000, img_size=64, a=16, b=8, row=32, col=32, downsample_factor=4, return_arrays=False):
    """ Varying angles at a fixed position. """
    out_lst = []
    for i in range(n):
        theta = np.pi*i/n
        p = {'img_size':img_size, 'row':row, 'col':col, 'a':a, 'b':b, 'theta':theta, 'downsample_factor':downsample_factor}
        assert check_bounds(**p), f"Produced an out-of-bounds image! {p}"
        if return_arrays:
            out_lst.append(get_ellipse(**p))
        else:
            out_lst.append(p)
    return out_lst


def line(n=10000, img_size=64, a=8, b=8, theta=0, row_range=(16,48), col_range=(32,32), downsample_factor=4, return_arrays=False):
    """ Generate a dataset of a line in parameter space.
    """
    out_lst = []
    for row,col in zip(np.linspace(row_range[0], row_range[1],n),
                       np.linspace(col_range[0], col_range[1],n)):
        p = {'img_size':img_size, 'row':row, 'col':col, 'a':a, 'b':b, 'theta':theta, 'downsample_factor':downsample_factor}
        assert check_bounds(**p), f"Produced an out-of-bounds image! {p}"
        if return_arrays:
            out_lst.append(get_ellipse(**p))
        else:
            out_lst.append(p)
    return out_lst



def torus(n=10000, img_size=64, downsample_factor=4, return_arrays=False):
    """ Generate a dataset of a topolgical torus in parameter space.
    :param: n = approximate number to produce (default 10000). Sampling is by sqrt(n)
    :param: img_size, default 64
    :param: downsample_factor, default 4
    :param: return_arrays, bool. If `output_arrays` is False [default], return the parameter dictionaries, and user must apply `[ get_ellipse(**p) for p in torus() ]` to generate the arrays. If `output_arrays` is True, returns the numpy arrays.
    :return: list of dictionaries or images.
    """
    gran = int(np.sqrt(n))
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