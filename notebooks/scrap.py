import numpy as np
from scipy.stats import norm

def zstat(x, y, s, cm, n):
    """
    float: Get Fisher's Z statistics.
    """
 
    def log_q1pm(r):
        return np.log1p(2 * r / (1 - r))

    r = pcor_order(x, y, s, cm)
    zstat = np.sqrt(n - len(s) - 3) * 0.5 * log_q1pm(r)
    if np.isnan(zstat):
        return 0
    else:
        return zstat

def ci_test_gauss(data_matrix, x, y, s, **kwargs):
    '''
    Conditional independence test
    
    '''

    assert 'corr_matrix' in kwargs
    cm = kwargs['corr_matrix']
    n = data_matrix.shape[0]

    z = zstat(x, y, list(s), cm, n)
    p_val = 2.0 * norm.sf(np.absolute(z))
    return p_val