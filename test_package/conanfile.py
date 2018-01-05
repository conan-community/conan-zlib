from conans.model.conan_file import ConanFile, tools
from conans import CMake
import os, platform


class DefaultNameConan(ConanFile):
    name = "DefaultName"
    version = "0.1"
    settings = "os", "compiler", "arch", "build_type"
    generators = "cmake"

    def build(self):
        # Compatibility with Conan < 1.0 (#2234)
        generator = "Unix Makefiles" if platform.system() != "Windows" else None 
        cmake = CMake(self, generator=generator)
        cmake.configure()
        cmake.build()

    def imports(self):
        self.copy(pattern="*.dll", dst="bin", src="bin")
        self.copy(pattern="*.dylib", dst="bin", src="lib")
        
    def test(self):
        if not tools.cross_building(self.settings):
            self.run("cd bin && .%senough" % os.sep)
        assert os.path.exists(os.path.join(self.deps_cpp_info["zlib"].rootpath, "LICENSE"))

