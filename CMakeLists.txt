cmake_minimum_required(VERSION 3.18)
project(unitree_actuator_sdk)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3")

include_directories(include)
link_directories(lib)

if(NOT CMAKE_SYSTEM_NAME STREQUAL "Linux")
    message(FATAL_ERROR "The bundled Unitree motor libraries require Linux (x86-64 or ARM64).")
endif()

string(TOLOWER "${CMAKE_SYSTEM_PROCESSOR}" UNITREE_PROCESSOR)
if(UNITREE_PROCESSOR MATCHES "^(aarch64|arm64)$")
    set(EXTRA_LIBS libUnitreeMotorSDK_Arm64.so)
elseif(UNITREE_PROCESSOR MATCHES "^(x86_64|amd64)$")
    set(EXTRA_LIBS libUnitreeMotorSDK_Linux64.so)
else()
    message(FATAL_ERROR "Unsupported Unitree motor SDK architecture: ${CMAKE_SYSTEM_PROCESSOR}")
endif()

option(UNITREE_BUILD_EXAMPLES "Build C++ motor examples" ON)
if(UNITREE_BUILD_EXAMPLES)
#example
add_executable(example_a1_motor example/example_a1_motor.cpp)
target_link_libraries(example_a1_motor ${EXTRA_LIBS})

add_executable(example_a1_motor_output example/example_a1_motor_output.cpp)
target_link_libraries(example_a1_motor_output ${EXTRA_LIBS})

add_executable(example_b1_motor example/example_b1_motor.cpp)
target_link_libraries(example_b1_motor ${EXTRA_LIBS})

add_executable(example_goM8010_6_motor example/example_goM8010_6_motor.cpp)
target_link_libraries(example_goM8010_6_motor ${EXTRA_LIBS})

add_executable(changeID example/changeID.cpp)
target_link_libraries(changeID ${EXTRA_LIBS})
endif()

find_package(Python 3.7 REQUIRED COMPONENTS Interpreter Development.Module)
set(PYBIND11_FINDPYTHON ON)

if(SKBUILD)
    # Isolated wheel builds must not write extensions into the source checkout.
    set(LIBRARY_OUTPUT_PATH "${CMAKE_CURRENT_BINARY_DIR}")
else()
    set(LIBRARY_OUTPUT_PATH "${CMAKE_CURRENT_SOURCE_DIR}/lib")
endif()
add_subdirectory(thirdparty/pybind11)
pybind11_add_module(unitree_actuator_sdk thirdparty/python_wrapper/wrapper.cpp)
target_link_libraries(unitree_actuator_sdk PRIVATE ${EXTRA_LIBS})
set_target_properties(unitree_actuator_sdk PROPERTIES LIBRARY_OUTPUT_DIRECTORY "${LIBRARY_OUTPUT_PATH}")
set_target_properties(unitree_actuator_sdk PROPERTIES
    INSTALL_RPATH "$ORIGIN/unitree_actuator_sdk.libs"
    INSTALL_RPATH_USE_LINK_PATH FALSE)

install(TARGETS unitree_actuator_sdk LIBRARY DESTINATION .)
install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/lib/${EXTRA_LIBS}"
    DESTINATION unitree_actuator_sdk.libs)

include(CTest)
if(BUILD_TESTING)
    add_test(NAME python_bindings
        COMMAND "${CMAKE_COMMAND}" -E env
            "PYTHONPATH=$<TARGET_FILE_DIR:unitree_actuator_sdk>"
            "${Python_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/tests/test_python_bindings.py")
endif()
