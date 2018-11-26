import numpy as np

def normal_multipole(k, I, z0):
    '''
    Computes the normal multipole of order k, for a single wire carrying a current I.
    The field is evaluated at a position z0 wrt to the wire (complex plane)
    Input: 
    k [int] : order of considered multipoles
    I [float, A]   : current carried by the wire 
    z0 [complex, mm] : coordinate of the evalutation point 
    '''
    mu0 = 1.2566370614359173e-06
    aux = 1e3*mu0*I/2/np.pi/z0**k
    return np.real(aux)

def skew_multipole(k, I, z0):
    '''
    Computes the skew multipole of order k, for a single wire carrying a current I.
    The field is evaluated at a position z0 wrt to the wire (complex plane)
    Input: 
    k [int] : order of considered multipoles
    I [float, A]   : current carried by the wire 
    z0 [complex, mm] : coordinate of the evalutation point 
    '''
    mu0 = 1.2566370614359173e-06
    aux = 1e3*mu0*I/2/np.pi/z0**k
    return np.imag(aux)

def multipoles_non_round(width, height, N, x0, y0, k, I_tot):
    '''
    Computes the multipoles (normal and skew) of order k, for a non-round (rectangle) wire carrying a current I_tot.
    The field is evaluated at a position (x0,y0) wrt to the wire (complex plane)
    Input: 
    width [float, mm] : width of the wire
    height [float, mm] : height of the wire
    N [int] : number of point of the grid
    k [int] : order of considered multipoles
    I_tot [float, A]   : current carried by the wire 
    x0, y0 [real, mm] : coordinate of the evalutation point 
    '''
    #  Center
    z0 = complex(x0,y0)

    # Grid 

    x_init = x0-width/2.
    x_fin = x0+width/2.

    y_init = y0-height/2.
    y_fin = y0+height/2.

    x_wire = np.linspace(x_init,x_fin,N)
    y_wire = np.linspace(y_init,y_fin,N)

    XX, YY = np.meshgrid(x_wire,y_wire)
    ZZ = XX+1j*YY

    # Compute the field

    I_wire = I_tot/N
    order = range(1,100)

    normal_coef = np.sum(normal_multipole(k, I_tot, ZZ))/N**2
    skew_coef = np.sum(skew_multipole(k,I_tot,ZZ))/N**2
    return np.array([normal_coef,skew_coef])
