include(Compiler/IntelLLVM)
__compiler_intel_llvm(CXX)

if("x${CMAKE_CXX_COMPILER_FRONTEND_VARIANT}" STREQUAL "xMSVC")
  set(CMAKE_CXX_COMPILE_OPTIONS_EXPLICIT_LANGUAGE -TP)
  set(CMAKE_CXX_CLANG_TIDY_DRIVER_MODE "cl")
  set(CMAKE_CXX_INCLUDE_WHAT_YOU_USE_DRIVER_MODE "cl")
  if((NOT DEFINED CMAKE_DEPENDS_USE_COMPILER OR CMAKE_DEPENDS_USE_COMPILER)
      AND CMAKE_GENERATOR MATCHES "Makefiles|WMake"
      AND CMAKE_DEPFILE_FLAGS_CXX)
    set(CMAKE_CXX_DEPENDS_USE_COMPILER TRUE)
  endif()
else()
  set(CMAKE_CXX_COMPILE_OPTIONS_EXPLICIT_LANGUAGE -x c++)
  if((NOT DEFINED CMAKE_DEPENDS_USE_COMPILER OR CMAKE_DEPENDS_USE_COMPILER)
      AND CMAKE_GENERATOR MATCHES "Makefiles|WMake"
      AND CMAKE_DEPFILE_FLAGS_CXX)
    # dependencies are computed by the compiler itself
    set(CMAKE_CXX_DEPFILE_FORMAT gcc)
    set(CMAKE_CXX_DEPENDS_USE_COMPILER TRUE)
  endif()

  set(CMAKE_CXX_COMPILE_OPTIONS_VISIBILITY_INLINES_HIDDEN "-fvisibility-inlines-hidden")

  string(APPEND CMAKE_CXX_FLAGS_MINSIZEREL_INIT " -DNDEBUG")
  string(APPEND CMAKE_CXX_FLAGS_RELEASE_INIT " -DNDEBUG")
  string(APPEND CMAKE_CXX_FLAGS_RELWITHDEBINFO_INIT " -DNDEBUG")
endif()

set(CMAKE_CXX98_STANDARD__HAS_FULL_SUPPORT ON)
set(CMAKE_CXX11_STANDARD__HAS_FULL_SUPPORT ON)
set(CMAKE_CXX14_STANDARD__HAS_FULL_SUPPORT ON)

if(NOT "x${CMAKE_CXX_SIMULATE_ID}" STREQUAL "xMSVC")
  set(CMAKE_CXX98_STANDARD_COMPILE_OPTION  "-std=c++98")
  set(CMAKE_CXX98_EXTENSION_COMPILE_OPTION "-std=gnu++98")

  set(CMAKE_CXX11_STANDARD_COMPILE_OPTION  "-std=c++11")
  set(CMAKE_CXX11_EXTENSION_COMPILE_OPTION "-std=gnu++11")

  set(CMAKE_CXX14_STANDARD_COMPILE_OPTION  "-std=c++14")
  set(CMAKE_CXX14_EXTENSION_COMPILE_OPTION "-std=gnu++14")

  set(CMAKE_CXX17_STANDARD_COMPILE_OPTION  "-std=c++17")
  set(CMAKE_CXX17_EXTENSION_COMPILE_OPTION "-std=gnu++17")

  set(CMAKE_CXX20_STANDARD_COMPILE_OPTION  "-std=c++20")
  set(CMAKE_CXX20_EXTENSION_COMPILE_OPTION "-std=gnu++20")
else()
  set(CMAKE_CXX98_STANDARD_COMPILE_OPTION  "")
  set(CMAKE_CXX98_EXTENSION_COMPILE_OPTION "")

  set(CMAKE_CXX11_STANDARD_COMPILE_OPTION  "-Qstd=c++11")
  set(CMAKE_CXX11_EXTENSION_COMPILE_OPTION "-Qstd=c++11")

  set(CMAKE_CXX14_STANDARD_COMPILE_OPTION  "-Qstd=c++14")
  set(CMAKE_CXX14_EXTENSION_COMPILE_OPTION "-Qstd=c++14")

  set(CMAKE_CXX17_STANDARD_COMPILE_OPTION  "-Qstd=c++17")
  set(CMAKE_CXX17_EXTENSION_COMPILE_OPTION "-Qstd=c++17")

  set(CMAKE_CXX20_STANDARD_COMPILE_OPTION  "-Qstd=c++20")
  set(CMAKE_CXX20_EXTENSION_COMPILE_OPTION "-Qstd=c++20")
endif()

__compiler_check_default_language_standard(CXX 2020 14)
