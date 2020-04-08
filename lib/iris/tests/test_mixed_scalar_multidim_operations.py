import pytest
from scipy import constants

import iris


# I want to perform operations on a multidimensional cube involving scalar constants
# Ideally I would use the iris built-in functionality of automatically determining units
# rather than having to do the operation with numpy arrays and doing the units manually
# Currently this does not work.

# The calculation of Exner pressure calculation is a good first example of where this
# doesn't work.
def exner_pressure(P, P_0, R, c_p):
    return (P / P_0) ** (R / c_p)


@pytest.fixture
def pressure():
    dim_coord = iris.coords.DimCoord(
        points=[0, 1, 2, 3],
        standard_name='longitude',
        units='degrees'
    )

    # Example cube of pressure
    P = iris.cube.Cube(
        data=[100000, 100100, 100000, 99800],
        standard_name='air_pressure',
        units='Pa',
        dim_coords_and_dims=[(dim_coord, 0)]
    )
    return P


# Ideally this would work with the scalar variables defined as cubes. Using a coord
# instead works for some of the operations but is a much less intuitive way to do it.
@pytest.mark.parametrize("scalar_type", [iris.cube.Cube, iris.coords.Coord])
def test_cube_and_scalar_operation(scalar_type, pressure):
    # Standard atmospheric pressure
    P_0 = scalar_type(constants.bar, units='Pa')

    # Specific Gas Constant for  dry air
    R = scalar_type(287.058, units='J kg-1 K-1')

    # Heat capacity of air at constant pressure
    c_p = scalar_type(1006.0, units='J kg-1 K-1')

    exner = exner_pressure(pressure, P_0, R, c_p)

    assert exner.units == 1

    return
