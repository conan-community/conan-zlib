#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import stat
from conans import ConanFile, tools, CMake, AutoToolsBuildEnvironment
from conans.util import files


class ZlibConan(ConanFile):
    name = "zlib"
    version = "1.2.8"
    url = "http://github.com/conan-community/conan-zlib"
    homepage = "https://zlib.net"
    author = "Conan Community"
    license = "Zlib"
    description = ("A Massively Spiffy Yet Delicately Unobtrusive Compression Library "
                  "(Also Free, Not to Mention Unencumbered by Patents)")
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    exports = "LICENSE"
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"
    
    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx
    
    def source(self):
        tools.get("http://downloads.sourceforge.net/project/libpng/{}/{}/{}-{}.tar.gz".format(self.name, self.version, self.name, self.version))
        os.rename("{}-{}".format(self.name, self.version), self._source_subfolder)
        files.rmdir(os.path.join(self._source_subfolder, "contrib"))
        if self.settings.os != "Windows":
            configure_file = os.path.join(self._source_subfolder, "configure")
            st = os.stat(configure_file)
            os.chmod(configure_file, st.st_mode | stat.S_IEXEC)
            
    def build(self):
        with tools.chdir(self._source_subfolder):
            if self.settings.os != "Windows":
                env_build = AutoToolsBuildEnvironment(self)
                if self.settings.arch == "x86" or self.settings.arch == "x86_64":
                    env_build.flags.append('-mstackrealign')

                if self.settings.os == "Macos":
                    old_str = '-install_name $libdir/$SHAREDLIBM'
                    new_str = '-install_name $SHAREDLIBM'
                    tools.replace_in_file("./configure", old_str, new_str)

                # Zlib configure doesnt allow this parameters (in 1.2.8)
                env_build.configure("./", build=False, host=False, target=False)
                env_build.make()

            else:
                files.mkdir(self._build_subfolder)
                with tools.chdir(self._build_subfolder):
                    cmake = CMake(self)
                    cmake.configure(build_dir=".")
                    cmake.build(build_dir=".")

    def package(self):
        # Extract the License/s from the header to a file
        with tools.chdir(self._source_subfolder):
            tmp = tools.load("zlib.h")
            license_contents = tmp[2:tmp.find("*/", 1)]
            tools.save("LICENSE", license_contents)

        # Copy the license files
        self.copy("LICENSE", src=self._source_subfolder, dst="licenses")

        # Copy pc file
        self.copy("*.pc", dst="", keep_path=False)
        
        # Copying zlib.h, zutil.h, zconf.h
        self.copy("*.h", "include", "%s" % self._source_subfolder, keep_path=False)
        self.copy("*.h", "include", self._build_subfolder, keep_path=False)

        # Copying static and dynamic libs
        if tools.os_info.is_windows:
            if self.options.shared:
                build_dir = os.path.join(self._source_subfolder, "_build")
                self.copy(pattern="*.dll", dst="bin", src=build_dir, keep_path=False)
                build_dir = os.path.join(self._source_subfolder, "_build/lib")
                self.copy(pattern="*zlibd.lib", dst="lib", src=build_dir, keep_path=False)
                self.copy(pattern="*zlib.lib", dst="lib", src=build_dir, keep_path=False)
                self.copy(pattern="*zlib.dll.a", dst="lib", src=build_dir, keep_path=False)
            else:
                build_dir = os.path.join(self._source_subfolder, "_build/lib")
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
            build_dir = os.path.join(self._source_subfolder)
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
