# webrtc_NoiseSuppressor_cpp_build test unit with wmv
# author: gamefunc
#    website: https://www.gamefunc.top:9029
#    github: https://github.com/gamefunc
#    qq: 32686647
#    weixin: gamefunc
#    mail: fevefun@hotmail.com
# free to use and modify, but need keep the above information.

# test env:
#     win_10: cl: 19.35.32215;
#     debian_11: gcc: 10.2.1; 

cmake_minimum_required(VERSION 3.20.0)
set(CMAKE_VERBOSE_MAKEFILE ON)
project(webrtc_ns_cpp VERSION 2022)

# mkdir build && cd build && cmake  ..
# cmake --build . --config Release --verbose

set(CMAKE_CXX_STANDARD_REQUIRED 20)
set(CMAKE_C_STANDARD_REQUIRED 99)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_C_STANDARD 99)


set(MY_DIR ${CMAKE_CURRENT_SOURCE_DIR})
message("当前cmakelist.txt 所在目录: ${MY_DIR}")
# set(GAMEFUNC_DIR "D:/Win10FD/OneDrive/1_myCode/C++/1_cPart")


include_directories(${MY_DIR})
# include_directories(${GAMEFUNC_DIR})

if(ANDROID)
    add_compile_options(-frtti)
    add_compile_options(-fexceptions)
    add_definitions(-DWEBRTC_POSIX)
    add_definitions(-DWEBRTC_HAS_NEON)
elseif(WIN32)
    add_definitions(-D_CRT_SECURE_NO_WARNINGS)
    add_definitions(-DNDEBUG)
    add_compile_options("/utf-8")
    add_definitions(-DWEBRTC_WIN)
elseif(UNIX) # gcc:
    add_definitions(-DWEBRTC_POSIX)
endif()


file(GLOB_RECURSE   MAIN_FILES 
    ${MY_DIR}/*
)
list(FILTER MAIN_FILES EXCLUDE REGEX "${MY_DIR}/build/.*" )
list(FILTER MAIN_FILES EXCLUDE REGEX "${MY_DIR}/system_wrappers/.*" )
list(FILTER MAIN_FILES EXCLUDE REGEX "${MY_DIR}/[^\.]*\.txt" )
list(FILTER MAIN_FILES EXCLUDE REGEX "${MY_DIR}/[^\.]*\.wav" )
list(FILTER MAIN_FILES EXCLUDE REGEX "${MY_DIR}/[^\.]*\.jpg" )
list(FILTER MAIN_FILES EXCLUDE REGEX "${MY_DIR}/[^\.]*\.py" )
list(FILTER MAIN_FILES EXCLUDE REGEX "${MY_DIR}/ns_test_unit_non_wav.cpp" )
list(FILTER MAIN_FILES EXCLUDE REGEX "${MY_DIR}/ns_test_unit_wav.cpp" )

message("will build: ${MAIN_FILES}")

# to exe: test:
set(MAIN_FILES ${MAIN_FILES} 
    # ${GAMEFUNC_DIR}/gamefunc/Os_Control.cpp
    # ns_test_unit_non_wav.cpp
    ns_test_unit_wav.cpp
)
add_executable(webrtc_ns_cpp  ${MAIN_FILES})

# # to static lib:
# add_library(webrtc_ns_cpp
#     ${MAIN_FILES})


# # to dll: do extra c and dll export yourself:
# add_library(webrtc_ns_cpp SHARED
#     ${MAIN_FILES})


message("report: github gamefunc; qq 32686647;")
message("https://www.gamefunc.top:9029")

