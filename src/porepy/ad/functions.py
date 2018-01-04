import numpy as np

from porepy.ad.forward_mode import Ad_array


def exp(var):
    if isinstance(var, Ad_array):
        val = np.exp(var.val)
        der = var.l_jac_mul(np.exp(var.val))
        return Ad_array(val, der)
    else:
        return np.exp(var)

def log(var):
    if not isinstance(var, Ad_array):
        return np.log(var)

    val = np.log(var.val)
    der = var.l_jac_mul(1 / var.val)
    return Ad_array(val, der)

def sign(var):
    if not isinstance(var, Ad_array):
        return np.sign(var)
    else:
        return np.sign(var.val)

def abs(var):
    if not isinstance(var, Ad_array):
        return np.abs(var)
    else:
        val = np.abs(var.val)
        jac = var.l_jac_mul(sign(var))
        return Ad_array(val, jac)
    
