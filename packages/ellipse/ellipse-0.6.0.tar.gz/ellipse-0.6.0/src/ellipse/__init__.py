from skimage.draw import ellipse
from skimage.transform import resize_local_mean
import numpy as np
from typing import Tuple

def check_bounds(img_size:int=64,
                 row:int=32, col:int=32,
                 a:float=16, b:float=16,
                 theta:float=0.0, downsample_factor:int=4,
                 return_bounds=False):
    """ Check whether the specified ellipse is entirely within the image, without wrap-around.
    Same options as `get_ellipse`. Returns boolean.
    Additional option `return_bounds` will return the result as bounding-box too, as `bool, min_row, max_row, min_col, max_col`
    """

    # Expand a rotated ellipse. 
    A = (np.cos(theta)/a)**2 + (np.sin(theta)/b)**2
    B = -2*np.cos(theta)*np.sin(theta)*(1/a**2 - 1/b**2)
    C = (np.sin(theta)/a)**2 + (np.cos(theta)/b)**2
    # maximum row of centered ellipse. An exercise in the quadratic formula.
    r_shift = np.sqrt(np.abs(4*C/(B**2-4*A*C)))
    # maximum col point of centered ellipse. An exercise in the quadratic formula.
    c_shift = np.sqrt(np.abs(4*A/(B**2-4*A*C)))
    max_r = int(row + r_shift)
    min_r = int(row - r_shift)
    max_c = int(col + c_shift)
    min_c = int(col - c_shift)
    
    good = (0 <= min_r <= max_r < img_size and 0 <= min_c <= max_c < img_size)
    
    if return_bounds:
        return good, min_r % img_size, max_r % img_size, min_c % img_size, max_c % img_size
    else:
        return good




def get_ellipse(img_size:int=64,
                row:int=32, col:int=32,
                a:float=16, b:float=16,
                theta:float=0.0, downsample_factor:int=4,
                allow_wrap=True):
    """
    Make a single ellipse with the given geometry.
    NOTE! We use the "upper-left" origin convention, so that plt.imgshow( ) and print( )
    give the same orientation of the image/matrix.
    
    :param img_size: Output image resolution. For example, 64 gives a 64x64 image.
    :param r: row-position of ellipse center.  Relative to upper-left of image.
    :param c: col-position of ellipse center.  Relative to upper-left of image.
    :param a: Length of semi-major axis.
    :param b: Length of semi-minor axis.
    :param theta: Angle in radians of the semi-major axis versus the row-axis, in range [0,pi]
    :param downsample_factor: Oversampling factor for downscaling image. Default=4.
    :param allow_wrap: If False, raise an exception if the ellipse wraps around the image.
    :return: numpy array of shape (img_size,img_size) suitable for `matplotlib.pyplot.imshow`
    """

    rr,cc = ellipse(downsample_factor*row, downsample_factor*col,
                    downsample_factor*a, downsample_factor*b,
                    rotation=theta)
    img = np.zeros((img_size*downsample_factor,img_size*downsample_factor))
    img[rr%(img_size*downsample_factor),cc%(img_size*downsample_factor)] = 1
    
    if (not allow_wrap) and check_bounds(img_size,row,col,a,b,theta,downsample_factor):
        raise ValueError("Ellipse wraps around figure boundary. Fix parameters or set allow_wrap=True")

    # downsample the image by local averaging
    return resize_local_mean(img, (img_size, img_size))

def generate(img_size:int,
             row_range:Tuple[int,int],
             col_range:Tuple[int,int],
             area_range:Tuple[float,float],
             logar_range:Tuple[float,float],
             theta_range:Tuple[float,float],
             rng:np.random.Generator or int=None):
    """
    Randomly generate ellipse parameters in a dictionary `p`, to be fed into `get_ellipse(**p)`.
    Geometric values are sampled uniformly from the given ranges.
    
    :param img_size: Output image resolution. For example, 64 gives a 64x64 image.
    :param row_range: Allowable row-positions of ellipse center. low <= row < high. Wraps around. 
    :param col_range: Allowable col-positions of ellipse center. low <= col < high. Wraps around.
    :param area_range: Allowable range of area `a*b*pi`. 0 < low <= area < high.
    :param logar_range: Allowable range of `log(a/b)`.  1 <= low <= logar < high.
    :param theta_range: Allowable range of angles, in radians. low <= theta < high.
    :param random_state: Set the random state, np.random.RandomState
    :return: output the randomly chosen parameters as a dictionary, suitable for `get_ellipse`.
    """
    if not row_range[0] < row_range[1]:
        raise ValueError("row_range must be increasing")
    if not col_range[0] < col_range[1]:
        raise ValueError("col_range must be increasing")
    if not (0 < area_range[0] < area_range[1]):
        raise ValueError("area_range must be increasing, and positive.")
    if not (1 <= logar_range[0] < logar_range[1]):
        raise ValueError("logar_range must be increasing, and >= 1")
    if not theta_range[0] < theta_range[1]:
        raise ValueError("theta_range must be increasing")

    if rng is None:
        rng = np.random.default_rng()
    elif type(rng) is int:
        rng = np.random.default_rng(rng)

    row = int(rng.uniform(row_range[0],row_range[1]))
    col = int(rng.uniform(col_range[0],col_range[1]))
    size = rng.uniform(area_range[0],area_range[1])/np.pi
    logar = rng.uniform(logar_range[0],logar_range[1])
    a = np.sqrt(size*np.exp(logar))
    b = np.sqrt(size/np.exp(logar))
    theta = rng.uniform(theta_range[0],theta_range[1])
    return {'img_size': img_size, 'row':row, 'col':col, 'a':a, 'b':b, 'theta':theta} 

