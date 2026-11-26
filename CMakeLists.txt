
cmake_minimum_required(VERSION 3.23)

project(pbkdf2 LANGUAGES CXX)

include(GNUInstallDirs)

find_package(OpenSSL REQUIRED)
find_package(CLI11 REQUIRED)
find_package(nlohmann_json REQUIRED)

if(NOT PBKDF2_PROJECT_VERSION)
    set(PBKDF2_PROJECT_VERSION 0.1.0)
endif()

add_library(pbkdf2)

target_sources(pbkdf2
    PRIVATE
        src/pbkdf2.cxx
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS include
        FILES
            include/pbkdf2.hpp
            include/pbkdf2/compatibility.hpp
)

target_link_libraries(pbkdf2
    PRIVATE
        OpenSSL::Crypto
)

target_compile_definitions(pbkdf2
    PUBLIC
        PBKDF2_VERSION="${PBKDF2_PROJECT_VERSION}"
)

if(NOT BUILD_SHARED_LIBS)
    target_compile_definitions(pbkdf2
        PUBLIC
            PBKDF2_STATIC
    )
endif()

add_executable(derive_key
    src/app_arguments.cxx
    src/main.cxx
    src/hex.cxx
    src/app_arguments.hpp
    src/hex.hpp
)

target_link_libraries(derive_key
    PRIVATE
        pbkdf2
        nlohmann_json::nlohmann_json
        CLI11::CLI11
)

install(
    TARGETS pbkdf2 derive_key
    FILE_SET HEADERS DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
)
