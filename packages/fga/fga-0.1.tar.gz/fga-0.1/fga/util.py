import numpy as np
from math import atan2, cos, sin
norm = np.linalg.norm

def get_area(cell):
    """
    Get area of the cell.
    :cell: ase atom cell or (2x2) xy cell
    :return: 2d area along xy plane
    """
    a = np.array([[cell[0][0],cell[0][1]],[cell[1][0],cell[1][1]]])
    return abs(np.linalg.det(a))

def rot(vector, angle):
    """
    Multiplying vector by rotation matrix
    :vector: vector of size (2,1)
    :angle: Angle in radians
    :return: rotated vector
    """
    return [(vector[0] * cos(angle)) - (vector[1] * sin(angle)),
                (vector[0] * sin(angle)) + (vector[1] * cos(angle))]

def square_up(atoms):
    """
    To rotate all the atoms cell such that x vector is parallel to x axis
    :atoms: ase atoms object
    :return: ase atoms object with rotated cell
    """
    angle = -atan2(atoms.cell[0][1], atoms.cell[0][0]) #angle of x-vector with x-axis
    atoms.cell[0][0:2] = rot(atoms.cell[0][0:2], angle) #Rotating x-vector by that angle
    atoms.cell[1][0:2] = rot(atoms.cell[1][0:2], angle) #Rotating y-vactor by that angle                                                                                                                   
    for atom in atoms:                                                                                                                                                       
        atom.position[0:2] = rot(atom.position[0:2], angle) #Rotate position of each atom position                                                                                                                
    atoms.center() #centers the atom in the unit cell
    
    return atoms

def remove_doubles(atoms, eps=1e-5):
    """
    Helper function to remove repeated atom images
    :atoms: ase atoms object
    :return: ase atoms object
    """
    atoms.set_scaled_positions(atoms.get_scaled_positions())
    valid = [0]
    for x in range(len(atoms)):
        for y in valid:
            xa = atoms[x].position
            ya = atoms[y].position
            if norm(xa-ya) < eps:  
                break
        else:
            valid.append(x)                            
    del atoms[[i for i in range(len(atoms)) if i not in valid]]
    
    return atoms

def check(x, y, tol=1e-4):
    """
    Check equality with some tolerance
    :x and y: (float) two values to check equality for
    :tol: (float) tolerance
    :return: Boolean
    """
    return abs(x-y)<tol

def calc_error(a, b): 
    error = 0
    for i in range(len(a)):
        error += norm((a[i][0] - b[i][0], a[i][1] - b[i][1]))**2  
    return error

def distortion(a, b):
    """
    % Change in the film vector wrt to substrate vector
    :a and b: input vectors
    :return: % change
    """
    return round((norm(b) - norm(a))/norm(b)*100, 4)

def clock_angle(v1, v2):
    """
    Angle between two vectors
    tan(angle) = dot(v1,v2)/det(v1,v2)
    
    :v1 and v2: input vectors
    :return: angle between the two vectors
    """
    r1 = np.dot(v1, v2)
    det = np.linalg.det([v1, v2])
    angle = atan2(det, r1) 
    return angle
