# https://github.com/scikit-build/scikit-build-sample-projects/tree/master/projects/hello-pybind11
project(mupifAccel LANGUAGES CXX)
cmake_minimum_required(VERSION 3.12)
set(CMAKE_CXX_STANDARD 14)

include(GNUInstallDirs)
include(FetchContent)

# workaround for Windows where MCSV + gfortran is detected (ouch)
# https://gitlab.com/libeigen/eigen/-/issues/114
set(EIGEN_BUILD_TESTING OFF)

FetchContent_Declare(
  Eigen3
  URL https://gitlab.com/libeigen/eigen/-/archive/3.4.0/eigen-3.4.0.tar.gz
  URL_HASH SHA256=8586084f71f9bde545ee7fa6d00288b264a2b7ac3607b974e54d13e7162c1c72
)
FetchContent_MakeAvailable(Eigen3)

# set(CMAKE_Fortran_COMPILER NOTFOUND) # try this instead
#find_package(Eigen3 REQUIRED NO_MODULES)
# pybind11[global] from pyproject.toml does not work under windows, so use FetchContent instead


if(WIN32)
  FetchContent_Declare(
    pybind11
    GIT_REPOSITORY "https://github.com/pybind/pybind11"
    GIT_TAG "v2.9.2"
    GIT_SHALLOW ON
  )
  FetchContent_MakeAvailable(pybind11)
else(WIN32)
  # installed via pyproject.toml
  find_package(pybind11 REQUIRED)
endif(WIN32)





# find_package(Boost COMPONENTS multi_array)

pybind11_add_module(fastOctant src/mupifAccel/fastOctant.cpp)
target_link_libraries(fastOctant PRIVATE Eigen3::Eigen)
install(TARGETS fastOctant LIBRARY DESTINATION .)
