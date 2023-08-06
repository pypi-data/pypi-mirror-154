from skbuild import setup
import sys

# this is necessary, otherwise skbuild tried Ninja first which picks up MSVC but then
# tries to configure Eigen with gfortran.exe with MSVC flags and fails. This forces
# native MSVC generator for CMake which won't fint gfortran.exe at all
if sys.platform=='win32': cmake_args=['-G','Visual Studio 16 2019']
else: cmake_args=[]

setup(
    name="mupif-accel",
    version="0.0.2",
    description="Optional accelerated components for MuPIF",
    author='Václav Šmilauer',
    license="LGPLv3",
    packages=['mupifAccel'],
    package_dir={'': 'src'},
    cmake_install_dir='src/mupifAccel',
    python_requires='>=3.8',
    cmake_args=cmake_args
)
