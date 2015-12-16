from conans import ConanFile
import os
from conans.tools import download, unzip, replace_in_file
from conans import CMake


class ZlibConan(ConanFile):
    name = "zlib"
    version = "1.2.8"
    ZIP_FOLDER_NAME = "zlib-1.2.8"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    exports = ["CMakeLists.txt", "FindZLIB.cmake"]
    url="http://github.com/lasote/conan-zlib"

    def conan_info(self):
        # We don't want to change the package for each compiler version but
        # we need the setting to compile with cmake
        if self.settings.os == "Macos":
            self.info.settings.compiler.version = "any"

    def source(self):
        zip_name = "zlib-1.2.8.zip"
        download("http://zlib.net/zlib128.zip", zip_name)
        unzip(zip_name)
        os.unlink(zip_name)
        if self.settings.os != "Windows":
            self.run("chmod +x ./%s/configure" % self.ZIP_FOLDER_NAME)

    def build(self):
        """ Define your project building. You decide the way of building it
            to reuse it later in any other project.
        """
        if self.settings.os == "Linux" or self.settings.os == "Macos":
            self.run("cd %s &&  mkdir _build" % self.ZIP_FOLDER_NAME)
            cd_build = "cd %s && cd _build" % self.ZIP_FOLDER_NAME
            arch = "-m32 " if self.settings.arch == "x86" else ""
            self.run("cd %s && CFLAGS='%s -mstackrealign -fPIC -O3' ./configure" % (self.ZIP_FOLDER_NAME, arch))
            if self.settings.os == "Macos":
                old_str = 'LDSHARED=gcc -dynamiclib -install_name ${exec_prefix}/lib/libz.1.dylib'
                new_str = 'LDSHARED=gcc -dynamiclib -install_name libz.1.dylib'
                replace_in_file("./%s/Makefile" % self.ZIP_FOLDER_NAME, old_str, new_str)
            self.run("cd %s && make" % self.ZIP_FOLDER_NAME)
        else:
            cmake = CMake(self.settings)
            if self.settings.os == "Windows":
                self.run("IF not exist _build mkdir _build")
            else:
                self.run("mkdir _build")
            cd_build = "cd _build"
            self.output.warn('%s && cmake .. %s' % (cd_build, cmake.command_line))
            self.run('%s && cmake .. %s' % (cd_build, cmake.command_line))
            self.output.warn("%s && cmake --build . %s" % (cd_build, cmake.build_config))
            self.run("%s && cmake --build . %s" % (cd_build, cmake.build_config))

    def package(self):
        """ Define your conan structure: headers, libs, bins and data. After building your
            project, this method is called to create a defined structure:
        """
        # Copy findZLIB.cmake to package
        self.copy("FindZLIB.cmake", ".", ".")
        
        # Copying zlib.h, zutil.h, zconf.h
        self.copy("*.h", "include", "%s" % (self.ZIP_FOLDER_NAME), keep_path=False)
        self.copy("*.h", "include", "%s" % ("_build"), keep_path=False)

        # Copying static and dynamic libs
        if self.settings.os == "Windows":
            if self.options.shared:
                self.copy(pattern="*.dll", dst="bin", src="_build", keep_path=False)
                self.copy(pattern="*zlibd.lib", dst="lib", src="_build", keep_path=False)
                self.copy(pattern="*zlib.lib", dst="lib", src="_build", keep_path=False)
            else:
                self.copy(pattern="*zlibstaticd.lib", dst="lib", src="_build", keep_path=False)
                self.copy(pattern="*zlibstatic.lib", dst="lib", src="_build", keep_path=False)
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
                if self.settings.build_type == "Debug":
                    self.cpp_info.libs = ['zlibd']
                else:
                    self.cpp_info.libs = ['zlib']
            else:
                if self.settings.build_type == "Debug":
                    self.cpp_info.libs = ['zlibstaticd']
                else:
                    self.cpp_info.libs = ['zlibstatic']
        else:
            self.cpp_info.libs = ['z']
