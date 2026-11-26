
from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import collect_libs


class PBKDF2Recipe(ConanFile):
    name = "pbkdf2"
    version = "0.1.0"
    package_type = "library"

    settings = "os", "compiler", "build_type", "arch"

    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }

    default_options = {
        "shared": False,
        "fPIC": True,
    }

    exports_sources = (
        "CMakeLists.txt",
        "src/*",
        "include/*",
        "include/pbkdf2/*",
    )

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.rm_safe("fPIC")

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def requirements(self):
        self.requires("openssl/[>=3 <4]", options={"no_fips": True})
        self.requires("cli11/[>=2 <3]")
        self.requires("nlohmann_json/[>=3 <4]")

    def layout(self):
        cmake_layout(self)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()

        tc = CMakeToolchain(self)
        tc.cache_variables["PBKDF2_PROJECT_VERSION"] = self.version
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = collect_libs(self)
        if not self.options.shared:
            self.cpp_info.defines.append("PBKDF2_STATIC")
