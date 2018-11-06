#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import stat
import shutil
from conans import ConanFile, tools, CMake, AutoToolsBuildEnvironment


class ZlibConan(ConanFile):
    name = "zlib"
    version = "1.2.9"
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
    exports_sources = ["CMakeLists.txt", "FindZLIB.cmake"]
    generators = "cmake"
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC
    
    def config(self):
        del self.settings.compiler.libcxx 

    def source(self):
        tools.get("http://downloads.sourceforge.net/project/libpng/{}/{}/{}-{}.tar.gz".format(self.name, self.version, self.name, self.version))
        os.rename("{}-{}".format(self.name, self.version), self._source_subfolder)
        tools.rmdir(os.path.join(self._source_subfolder, "contrib"))
        if self.settings.os != "Windows":
            configure_file = os.path.join(self._source_subfolder, "configure")
            st = os.stat(configure_file)
            os.chmod(configure_file, st.st_mode | stat.S_IEXEC)

    def build(self):
        """ Define your project building. You decide the way of building it
            to reuse it later in any other project.
        """
        if self.settings.os != "Windows":
            with tools.chdir(self._source_subfolder):
                env_build = AutoToolsBuildEnvironment(self)
                if self.settings.arch == "x86" or self.settings.arch == "x86_64":
                    env_build.flags.append('-mstackrealign')

                if self.settings.os == "Macos":
                    old_str = '-install_name $libdir/$SHAREDLIBM'
                    new_str = '-install_name $SHAREDLIBM'
                    tools.replace_in_file("configure", old_str, new_str)

                env_build.configure(build=False, host=False, target=False)
                env_build.make()
        else:
            cmake = CMake(self)
            cmake.configure(build_folder=self._build_subfolder)
            cmake.build()

    def package(self):
        """ Define your conan structure: headers, libs, bins and data. After building your
            project, this method is called to create a defined structure:
        """
        with tools.chdir(self._source_subfolder):
            tmp = tools.load("zlib.h")
            license_contents = tmp[2:tmp.find("*/", 1)]
            tools.save("LICENSE", license_contents)

        self.copy("LICENSE", dst="licenses", src=self._source_subfolder)

        # Copy findZLIB.cmake to package
        self.copy("FindZLIB.cmake", ".", ".")
        
        # Copying zlib.h, zutil.h, zconf.h
        self.copy("*.h", "include", self._source_subfolder, keep_path=False)

        # Copying static and dynamic libs
        if self.settings.os == "Windows":
            self.copy(pattern="*.h", dst="include", src=self._build_subfolder, keep_path=False)
            self.copy(pattern="*.dll", dst="bin", src=self._build_subfolder, keep_path=False)
            self.copy(pattern="*.lib", dst="lib", src=self._build_subfolder, keep_path=False)
            self.copy(pattern="*.a", dst="lib", src=self._build_subfolder, keep_path=False)
            if not self.options.shared:
                lib_path = os.path.join(self.package_folder, "lib")
                suffix = "d" if self.settings.build_type == "Debug" else ""
                if self.settings.compiler == "Visual Studio":
                    current_lib = os.path.join(lib_path, "zlibstatic%s.lib" % suffix)
                    shutil.move(current_lib, os.path.join(lib_path, "zlib%s.lib" % suffix))
                elif self.settings.compiler == "gcc":
                    current_lib = os.path.join(lib_path, "libzlibstatic.a")
                    shutil.move(current_lib, os.path.join(lib_path, "libzlib.a"))
        else:
            if self.options.shared:
                if self.settings.os == "Macos":
                    self.copy(pattern="*.dylib", dst="lib", keep_path=False)
                else:
                    self.copy(pattern="*.so*", dst="lib", src=self._source_subfolder, keep_path=False)
            else:
                self.copy(pattern="*.a", dst="lib", src=os.path.join(self._source_subfolder, self._source_subfolder), keep_path=False)
                self.copy(pattern="*.a", dst="lib", src=self._source_subfolder, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
