from conans import ConanFile, tools, CMake
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
    exports_sources = ["CMakeLists.txt", "CMakeLists.patch"]
    url = "http://github.com/lasote/conan-zlib"
    license = "http://www.zlib.net/zlib_license.html"
    description = "A Massively Spiffy Yet Delicately Unobtrusive Compression Library " \
                  "(Also Free, Not to Mention Unencumbered by Patents)"

    def configure(self):
        del self.settings.compiler.libcxx

    def source(self):
        z_name = "zlib-%s.tar.gz" % self.version
        tools.download("https://zlib.net/zlib-%s.tar.gz" %
                       self.version, z_name)
        tools.unzip(z_name)
        os.unlink(z_name)
        files.rmdir("%s/contrib" % self.ZIP_FOLDER_NAME)

    def build(self):
        with tools.chdir(os.path.join(self.source_folder, self.ZIP_FOLDER_NAME)):
            # prevent '#define WIDECHAR' under MSYS
            # Note: MSYS is based on CYGWIN! CK
            self.output.warn("conan: patch %s/gzguts.h" % self.ZIP_FOLDER_NAME)
            tools.replace_in_file("gzguts.h", '#if defined(_WIN32) || defined(__CYGWIN__)',
                                  '#if defined(_WIN32) && !defined(__CYGWIN__)')
            self.output.warn("conan: patch %s/CMakeLists.txt" %
                             self.ZIP_FOLDER_NAME)
            # Note: build either SHARED or STATIC zlib! CK
            # prevent use of win32/zlib1.rc under MSYS too
            tools.patch(patch_file="../CMakeLists.patch")

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
                # # TBD: may be added later? CK
                # if not tools.cross_building(self.settings):
                #     cmake.test()
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
        if self.settings.os == "Windows" and self.settings.compiler == "Visual Studio":
            self.cpp_info.libs = ['zlib']
            # IMHO: unwanted with conan! CK
            if self.settings.build_type == "Debug" and self.settings.compiler == "Visual Studio":
                self.cpp_info.libs[0] += "d"
        else:
            self.cpp_info.libs = ['z']
