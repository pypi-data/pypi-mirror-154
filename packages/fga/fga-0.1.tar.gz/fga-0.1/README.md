## Film Generation Algorithm (FGA)
> Latest edits: Kaustubh Sawant (21st May 2022)

FGA consists of tools that can stack films ontop of atom slabs such that the strain in non-pseudomorphic, periodic overlayer films is minimized.

### Requirements
- [Python](https://www.python.org/) 3.6  or later
- [NumPy](https://numpy.org/doc/stable/reference/)
- [ASE](https://wiki.fysik.dtu.dk/ase/ase/atoms.html) 3.19 or later

### Installation
Install using pip

~~~bash
pip install .
~~~


Alternatively, you can just add ./fga to your $PYTHONPATH. (not recommended)

~~~bash
export PYTHONPATH=$PYTHONPATH:"<path_to_fga>"
~~~

### Examples

1. All the possible overlayer structures for given set of films and substrates can be constructed using [run_fga.py](https://github.itap.purdue.edu/GreeleyGroup/fga/blob/master/bin/run_fga.py). Please note that the film is slightly distorted to fit on the substrate since there is almost never a perfect match.

~~~bash
python run_fga.py -s <path_to_substrates> -f <path_to_films>
~~~

Theoritically there are infinite possible structures. For practical purposes we have set a few constraints which are discussed in later sections.

2. The best structure can be found using a simple function [get_best_cell()](https://github.itap.purdue.edu/GreeleyGroup/fga/blob/master/fga/fga.py#L310)

~~~python
from fga import get_best_cell

unit_substrate_path = './Substrates/POSCAR_Au'
unit_film_path = './Films/POSCAR_ZnO'

best_cell_atoms = get_best_cell(unit_substrate_path,unit_film_path)
~~~

### Parameters
#### 1. Film Search Space 
    --film_search, -film_search, -fs, 
    type: int, default: 4, 
    Defines repetition of the film unit cell
    
#### 2.  Substrate Search Space 
    --sub_search, -sub_search, -ss, 
    type: int, default: 4, 
    Defines repetition of the substrate unit cell
    
#### 3. Maximum size of cell diagonal
    --max_size, -max_size, -msize, 
    type: float, default: 40, 
    Max diagonal distance of the cells that are created (a way to limit size of cell)
    
#### 4.  Maximum allowed atoms in the final structure
    --max_num_of_atoms, -max_num_of_atoms, -matoms, 
    type: int, default: 200, 
    Maximum number of atom you want in the system -- will filter out big cells
    
#### 5. Distance between film and substrate  
    --buffer, -buffer, -b, 
    type: float, default: 2, 
    This is the distance between the lowest atoms in your film and the highest atoms in your substrate
    
#### 6.  The vacuum between z images
    --vacuum, -vacuum, -v, 
    type: float, default: 10,
    
#### 7. The maximum ratio change
    --max_ratio_change, -max_ratio_change, -mrc,
    type: float, default: 0.5
    This is the range of structures that will be looked at on each side of the sturcutre that will have the minimum strain
    
#### 8. Maximum length ratio
    --max_length_ratio, -max_length_ratio, -ml',
    type: float, default: 1.5,
    This is the max ratio between the x vector and the y vector (and its reciprocal) that is allowable. 
    This prevents dealing with really thin cells which are hard to work with (though they may be useful cells).
    
    
### Cite
Original idea by Joseph Kubal and implemented by Kaustubh Sawant
