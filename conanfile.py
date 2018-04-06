from conans import ConanFile, tools, CMake, AutoToolsBuildEnvironment
from conans.util import files
import os


class ZlibConan(ConanFile):
    name = "zlib"
    version = "1.2.11"
    ZIP_FOLDER_NAME = "zlib-%s" % version
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    exports_sources = ["CMakeLists.txt"]
    url = "http://github.com/lasote/conan-zlib"
    license = "http://www.zlib.net/zlib_license.html"
    description = "A Massively Spiffy Yet Delicately Unobtrusive Compression Library " \
                  "(Also Free, Not to Mention Unencumbered by Patents)"

    def configure(self):
        del self.settings.compiler.libcxx

    def source(self):
        z_name = "zlib-%s.tar.gz" % self.version
        tools.download("https://zlib.net/zlib-%s.tar.gz" % self.version, z_name)
        tools.unzip(z_name)
        os.unlink(z_name)
        files.rmdir("%s/contrib" % self.ZIP_FOLDER_NAME)

    def build(self):
        with tools.chdir(os.path.join(self.source_folder, self.ZIP_FOLDER_NAME)):
            files.mkdir("_build")
            with tools.chdir("_build"):
                cmake = CMake(self)
                if self.options.shared:
                    definitions = {
                        "BUILD_SHARED_LIBS": "ON"
                    }
                    cmake.configure(defs=definitions)
                else:
                    cmake.configure()
                cmake.build()
                cmake.install()

    def package(self):
        self.output.warn("local cache: %s" % self.in_local_cache)
        self.output.warn("develop: %s" % self.develop)
        # Extract the License/s from the header to a file
        with tools.chdir(os.path.join(self.source_folder, self.ZIP_FOLDER_NAME)):
            tmp = tools.load("zlib.h")
            license_contents = tmp[2:tmp.find("*/", 1)]
            tools.save("LICENSE", license_contents)

        # Copy the license files
        self.copy("LICENSE", src=self.ZIP_FOLDER_NAME, dst=".")

        # NOTE: other files are installed with cmake.install()

    def package_info(self):
        if self.settings.os == "Windows":
            self.cpp_info.libs = ['zlib']
            # TBD: IMHO unwanted with conan!
            # if self.settings.build_type == "Debug" and self.settings.compiler == "Visual Studio":
            #     self.cpp_info.libs[0] += "d"
        else:
            self.cpp_info.libs = ['z']
