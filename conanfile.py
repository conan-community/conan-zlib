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
    exports = ["CMakeLists.txt", "FindZLIB.cmake"]
    url = "http://github.com/lasote/conan-zlib"
    license = "http://www.zlib.net/zlib_license.html"
    description = "A Massively Spiffy Yet Delicately Unobtrusive Compression Library " \
                  "(Also Free, Not to Mention Unencumbered by Patents)"
    
    def config(self):
        del self.settings.compiler.libcxx 

    def source(self):
        zip_name = "zlib-%s.tar.gz" % self.version
        tools.download("http://downloads.sourceforge.net/project/libpng/zlib/%s/%s" % (self.version, zip_name), zip_name)
        tools.unzip(zip_name)
        os.unlink(zip_name)
        if self.settings.os != "Windows":
            self.run("chmod +x ./%s/configure" % self.ZIP_FOLDER_NAME)

    def build(self):
        """ Define your project building. You decide the way of building it
            to reuse it later in any other project.
        """
        if self.settings.os == "Linux" or self.settings.os == "Macos":
            env_build = AutoToolsBuildEnvironment(self)
            if self.settings.arch == "x86" or self.settings.arch == "x86_64":
                env_build.flags.append('-mstackrealign')
                env_build.fpic = True

            if self.settings.os == "Macos":
                old_str = '-install_name $libdir/$SHAREDLIBM'
                new_str = '-install_name $SHAREDLIBM'
                tools.replace_in_file("./%s/configure" % self.ZIP_FOLDER_NAME, old_str, new_str)

            with tools.environment_append(env_build.vars):
                with tools.chdir(self.ZIP_FOLDER_NAME):
                    self.run("./configure")
                    self.run("make")
        else:
            cmake = CMake(self.settings)
            files.mkdir("_build")
            with tools.chdir("./_build"):
                cmake.configure(self)
                cmake.build(self)

    def package(self):
        """ Define your conan structure: headers, libs, bins and data. After building your
            project, this method is called to create a defined structure:
        """
        # Copy findZLIB.cmake to package
        self.copy("FindZLIB.cmake", ".", ".")
        
        # Copying zlib.h, zutil.h, zconf.h
        self.copy("*.h", "include", "%s" % self.ZIP_FOLDER_NAME, keep_path=False)
        self.copy("*.h", "include", "%s" % "_build", keep_path=False)

        # Copying static and dynamic libs
        if self.settings.os == "Windows":
            if self.options.shared:
                self.copy(pattern="*.dll", dst="bin", src="_build", keep_path=False)
                self.copy(pattern="*zlibd.lib", dst="lib", src="_build", keep_path=False)
                self.copy(pattern="*zlib.lib", dst="lib", src="_build", keep_path=False)
                self.copy(pattern="*zlib.lib", dst="lib", src="_build", keep_path=False)
                self.copy(pattern="*zlib.dll.a", dst="lib", src="_build", keep_path=False)
            else:
                self.copy(pattern="*zlibstaticd.*", dst="lib", src="_build", keep_path=False)
                self.copy(pattern="*zlibstatic.*", dst="lib", src="_build", keep_path=False)
        else:
            if self.options.shared:
                if self.settings.os == "Macos":
                    self.copy(pattern="*.dylib", dst="lib", keep_path=False)
                else:
                    self.copy(pattern="*.so*", dst="lib", src=self.ZIP_FOLDER_NAME, keep_path=False)
            else:
                self.copy(pattern="*.a", dst="lib", src="%s/_build" % self.ZIP_FOLDER_NAME, keep_path=False)
                self.copy(pattern="*.a", dst="lib", src=self.ZIP_FOLDER_NAME, keep_path=False)

    def package_info(self):
        if self.settings.os == "Windows":
            if self.options.shared:
                if self.settings.build_type == "Debug" and self.settings.compiler == "Visual Studio":
                    self.cpp_info.libs = ['zlibd']
                else:
                    self.cpp_info.libs = ['zlib']
            else:
                if self.settings.build_type == "Debug" and  self.settings.compiler == "Visual Studio":
                    self.cpp_info.libs = ['zlibstaticd']
                else:
                    self.cpp_info.libs = ['zlibstatic']
        else:
            self.cpp_info.libs = ['z']
