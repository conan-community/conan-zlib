from conans import ConanFile, tools, CMake, AutoToolsBuildEnvironment
from conans.util import files
from conans import __version__ as conan_version
import os


class ZlibConan(ConanFile):
    name = "zlib"
    version = "1.2.8"
    ZIP_FOLDER_NAME = "zlib-%s" % version
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    exports = ["CMakeLists.txt"]
    url = "http://github.com/lasote/conan-zlib"
    license = "http://www.zlib.net/zlib_license.html"
    description = "A Massively Spiffy Yet Delicately Unobtrusive Compression Library " \
                  "(Also Free, Not to Mention Unencumbered by Patents)"
    
    def configure(self):
        del self.settings.compiler.libcxx

    def source(self):
        zip_name = "zlib-%s.tar.gz" % self.version
        tools.download("http://downloads.sourceforge.net/project/libpng/zlib/%s/%s" % (self.version, zip_name), zip_name)
        tools.unzip(zip_name)
        os.unlink(zip_name)
        files.rmdir("%s/contrib" % self.ZIP_FOLDER_NAME)
        if self.settings.os != "Windows":
            self.run("chmod +x ./%s/configure" % self.ZIP_FOLDER_NAME)
        elif self.settings.compiler == "Visual Studio":
            tools.replace_in_file("%s/zconf.h.cmakein" % self.ZIP_FOLDER_NAME, "#    include <unistd.h>", "// no unistd.h on windows")
            tools.replace_in_file("%s/zconf.h.in" % self.ZIP_FOLDER_NAME, "#    include <unistd.h>", "// no unistd.h on windows")
            
    def build(self):
        with tools.chdir(self.ZIP_FOLDER_NAME):
            if not tools.OSInfo().is_windows:
                env_build = AutoToolsBuildEnvironment(self)
                if self.settings.arch == "x86" or self.settings.arch == "x86_64":
                    env_build.flags.append('-mstackrealign')

                env_build.fpic = True
                if self.settings.os == "Macos":
                    old_str = '-install_name $libdir/$SHAREDLIBM'
                    new_str = '-install_name $SHAREDLIBM'
                    tools.replace_in_file("./configure", old_str, new_str)

                # Zlib configure doesnt allow this parameters (in 1.2.8)
                env_build.configure("./", build=False, host=False, target=False)
                env_build.make()

            else:
                files.mkdir("_build")
                with tools.chdir("_build"):
                    cmake = CMake(self)
                    cmake.configure(build_dir=".")
                    cmake.build(build_dir=".")

    def package(self):
        # Extract the License/s from the header to a file
        with tools.chdir(self.ZIP_FOLDER_NAME):
            tmp = tools.load("zlib.h")
            license_contents = tmp[2:tmp.find("*/", 1)]
            tools.save("LICENSE", license_contents)

        # Copy the license files
        self.copy("LICENSE", src=self.ZIP_FOLDER_NAME, dst=".")

        # Copy pc file
        self.copy("*.pc", dst="", keep_path=False)
        
        # Copying zlib.h, zutil.h, zconf.h
        self.copy("*.h", "include", "%s" % self.ZIP_FOLDER_NAME, keep_path=False)
        self.copy("*.h", "include", "%s" % "_build", keep_path=False)

        # Copying static and dynamic libs
        if tools.os_info.is_windows:
            if self.options.shared:
                build_dir = os.path.join(self.ZIP_FOLDER_NAME, "_build")
                self.copy(pattern="*.dll", dst="bin", src=build_dir, keep_path=False)
                build_dir = os.path.join(self.ZIP_FOLDER_NAME, "_build/lib")
                self.copy(pattern="*zlibd.lib", dst="lib", src=build_dir, keep_path=False)
                self.copy(pattern="*zlib.lib", dst="lib", src=build_dir, keep_path=False)
                self.copy(pattern="*zlib.dll.a", dst="lib", src=build_dir, keep_path=False)
            else:
                build_dir = os.path.join(self.ZIP_FOLDER_NAME, "_build/lib")
                # MinGW
                self.copy(pattern="libzlibstaticd.a", dst="lib", src=build_dir, keep_path=False)
                self.copy(pattern="libzlibstatic.a", dst="lib", src=build_dir, keep_path=False)
                # Visual Studio
                self.copy(pattern="zlibstaticd.lib", dst="lib", src=build_dir, keep_path=False)
                self.copy(pattern="zlibstatic.lib", dst="lib", src=build_dir, keep_path=False)
                
                lib_path = os.path.join(self.package_folder, "lib")
                suffix = "d" if self.settings.build_type == "Debug" else ""
                if self.settings.compiler == "Visual Studio":
                    current_lib = os.path.join(lib_path, "zlibstatic%s.lib" % suffix)
                    os.rename(current_lib, os.path.join(lib_path, "zlib%s.lib" % suffix))
                elif self.settings.compiler == "gcc":
                    current_lib = os.path.join(lib_path, "libzlibstatic.a")
                    os.rename(current_lib, os.path.join(lib_path, "libzlib.a"))
        else:
            build_dir = os.path.join(self.ZIP_FOLDER_NAME)
            if self.options.shared:
                if self.settings.os == "Macos":
                    self.copy(pattern="*.dylib", dst="lib", src=build_dir, keep_path=False)
                else:
                    self.copy(pattern="*.so*", dst="lib", src=build_dir, keep_path=False)
            else:
                self.copy(pattern="*.a", dst="lib", src=build_dir, keep_path=False)

    def package_info(self):
        if self.settings.os == "Windows":
            self.cpp_info.libs = ['zlib']
            if self.settings.build_type == "Debug" and self.settings.compiler == "Visual Studio":
                self.cpp_info.libs[0] += "d"
        else:
            self.cpp_info.libs = ['z']
