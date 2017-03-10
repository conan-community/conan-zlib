from conans import ConanFile, tools, CMake, AutoToolsBuildEnvironment
from conans.util import files
from conans import __version__ as conan_version
import os


class ZlibConan(ConanFile):
    name = "zlib"
    version = "1.2.11"
    ZIP_FOLDER_NAME = "zlib-%s" % version
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    exports = ["CMakeLists.txt", "FindZLIB.cmake"]
    url = "http://github.com/lasote/conan-zlib"
    license = "http://www.zlib.net/zlib_license.html"
    description = "A Massively Spiffy Yet Delicately Unobtrusive Compression Library " \
                  "(Also Free, Not to Mention Unencumbered by Patents)"
    
    def configure(self):
        del self.settings.compiler.libcxx
        if conan_version < "0.20.0":
            raise ConanException("This recipe works with conan >= 0.20.0, please update your conan client version")

    def source(self):
        zip_name = "zlib-%s.tar.gz" % self.version
        tools.download("http://downloads.sourceforge.net/project/libpng/zlib/%s/%s" % (self.version, zip_name), zip_name)
        tools.unzip(zip_name)
        os.unlink(zip_name)
        if self.settings.os != "Windows":
            self.run("chmod +x ./%s/configure" % self.ZIP_FOLDER_NAME)

    def build(self):
        with tools.chdir(self.ZIP_FOLDER_NAME):
            files.mkdir("_build")
            with tools.chdir("_build"):
                if self.settings.os == "Linux" or self.settings.os == "Macos":
                    env_build = AutoToolsBuildEnvironment(self)
                    if self.settings.arch == "x86" or self.settings.arch == "x86_64":
                        env_build.flags.append('-mstackrealign')
                        env_build.fpic = True
    
                    if self.settings.os == "Macos":
                        old_str = '-install_name $libdir/$SHAREDLIBM'
                        new_str = '-install_name $SHAREDLIBM'
                        tools.replace_in_file("../configure", old_str, new_str)
    
                    with tools.environment_append(env_build.vars):
                        self.run("../configure")
                        self.run("make")
                else:
                    cmake = CMake(self.settings)                
                    cmake.configure(self, build_dir=".")
                    cmake.build(self, build_dir=".")

    def package(self):
        # Copy findZLIB.cmake to package
        self.copy("FindZLIB.cmake", ".", ".")

        # Copy pc file
        self.copy("*.pc", dst="", keep_path=False)
        
        # Copying zlib.h, zutil.h, zconf.h
        self.copy("*.h", "include", "%s" % self.ZIP_FOLDER_NAME, keep_path=False)
        self.copy("*.h", "include", "%s" % "_build", keep_path=False)

        # Copying static and dynamic libs
        build_dir = os.path.join(self.ZIP_FOLDER_NAME, "_build")
        if self.settings.os == "Windows":
            if self.options.shared:
                self.copy(pattern="*.dll", dst="bin", src=build_dir, keep_path=False)
                self.copy(pattern="*zlibd.lib", dst="lib", src=build_dir, keep_path=False)
                self.copy(pattern="*zlib.lib", dst="lib", src=build_dir, keep_path=False)
                self.copy(pattern="*zlib.dll.a", dst="lib", src=build_dir, keep_path=False)
            else:
                self.copy(pattern="*zlibstaticd.*", dst="lib", src=build_dir, keep_path=False)
                self.copy(pattern="*zlibstatic.*", dst="lib", src=build_dir, keep_path=False)
        else:
            if self.options.shared:
                if self.settings.os == "Macos":
                    self.copy(pattern="*.dylib", dst="lib", src=build_dir, keep_path=False)
                else:
                    self.copy(pattern="*.so*", dst="lib", src=build_dir, keep_path=False)
            else:
                self.copy(pattern="*.a", dst="lib", src=build_dir, keep_path=False)

    def package_info(self):
        if self.settings.os == "Windows":
            self.cpp_info.libs = ['zlib'] if self.options.shared else ['zlibstatic']
            if self.settings.build_type == "Debug" and self.settings.compiler == "Visual Studio":
                self.cpp_info.libs[0] += "d"
        else:
            self.cpp_info.libs = ['z']
