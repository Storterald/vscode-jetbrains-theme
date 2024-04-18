cmake_minimum_required(VERSION 3.23)
# set the project name
project(Tutorial)
message([=[      This is the first line in a bracket argument with bracket length 1.      ]=])
# specify the C++ standard
if(ENABLE_CXX_20)
  set(CMAKE_CXX_STANDARD 20)
else()
  set(CMAKE_CXX_STANDARD 17)
endif()
# add the MathFunctions library
add_subdirectory(MathFunctions)

#  Semantic highlighting:
#  Generated spectrum to pick colors for local variables and parameters:
#   Color#1 SC1.1 SC1.2 SC1.3 SC1.4 Color#2 SC2.1 SC2.2 SC2.3 SC2.4 Color#3
#   Color#3 SC3.1 SC3.2 SC3.3 SC3.4 Color#4 SC4.1 SC4.2 SC4.3 SC4.4 Color#5
# add the executable
add_executable(Tutorial tutorial.cxx)
set_target_properties(Tutorial PROPERTIES
    CXX_STANDARD 11
    CXX_EXTENSIONS OFF
    CUDA_STANDARD 11
    CUDA_EXTENSIONS ON)
target_link_libraries(Tutorial PUBLIC MathFunctions)
target_include_directories(Tutorial PUBLIC
                          "$PROJECT_BINARY_DIR"
                          "${PROJECT_SOURCE_DIR}/MathFunctions")