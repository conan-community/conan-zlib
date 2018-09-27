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
        if not tools.os_info.is_windows:
            self.run("chmod +x ./%s/configure" % self.ZIP_FOLDER_NAME)

    def build(self):
        with tools.chdir(os.path.join(self.source_folder, self.ZIP_FOLDER_NAME)):
            for filename in ['zconf.h', 'zconf.h.cmakein', 'zconf.h.in']:
                tools.replace_in_file(filename,
                                      '#ifdef HAVE_UNISTD_H    /* may be set to #if 1 by ./configure */',
                                      '#if defined(HAVE_UNISTD_H) && (1-HAVE_UNISTD_H-1 != 0)')
                tools.replace_in_file(filename,
                                      '#ifdef HAVE_STDARG_H    /* may be set to #if 1 by ./configure */',
                                      '#if defined(HAVE_STDARG_H) && (1-HAVE_STDARG_H-1 != 0)')
            files.mkdir("_build")
            with tools.chdir("_build"):
                if not tools.os_info.is_windows:
                    env_build = AutoToolsBuildEnvironment(self)
                    if self.settings.arch in ["x86", "x86_64"] and self.settings.compiler in ["apple-clang", "clang", "gcc"]:
                        env_build.flags.append('-mstackrealign')

                    env_build.fpic = True

                    if self.settings.os == "Macos":
                        old_str = '-install_name $libdir/$SHAREDLIBM'
                        new_str = '-install_name $SHAREDLIBM'
                        tools.replace_in_file("../configure", old_str, new_str)

                    if self.settings.os == "Windows":  # Cross building to Linux
                        tools.replace_in_file("../configure", 'LDSHAREDLIBC="${LDSHAREDLIBC--lc}"', 'LDSHAREDLIBC=""')
                    # Zlib configure doesnt allow this parameters
                    if self.settings.os == "Windows" and tools.os_info.is_linux:
                        # Let our profile to declare what is needed.
                        tools.replace_in_file("../win32/Makefile.gcc", 'LDFLAGS = $(LOC)', '')
                        tools.replace_in_file("../win32/Makefile.gcc", 'AS = $(CC)', '')
                        tools.replace_in_file("../win32/Makefile.gcc", 'AR = $(PREFIX)ar', '')
                        tools.replace_in_file("../win32/Makefile.gcc", 'CC = $(PREFIX)gcc', '')
                        tools.replace_in_file("../win32/Makefile.gcc", 'RC = $(PREFIX)windres', '')
                        self.run("cd .. && make -f win32/Makefile.gcc")
                    else:
                        env_build.configure("../", build=False, host=False, target=False)
                        env_build.make()
                else:
                    cmake = CMake(self)
                    cmake.configure(build_dir=".")
                    cmake.build(build_dir=".")

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

        # Copy pc file
        self.copy("*.pc", dst="", keep_path=False)

        # Copy headers
        for header in ["zlib.h", "_build/zconf.h"]:
            self.copy(header, "include", "%s" % self.ZIP_FOLDER_NAME, keep_path=False)
            self.copy(header, "include", "%s" % "_build", keep_path=False)

        # Copying static and dynamic libs
        build_dir = os.path.join(self.ZIP_FOLDER_NAME, "_build")
        lib_path = os.path.join(self.package_folder, "lib")
        suffix = "d" if self.settings.build_type == "Debug" else ""
        if self.settings.os == "Windows":
            if self.options.shared:
                build_dir = os.path.join(self.ZIP_FOLDER_NAME, "_build")
                self.copy(pattern="*.dll", dst="bin", src=build_dir, keep_path=False)
                build_dir = os.path.join(self.ZIP_FOLDER_NAME, "_build/lib")
                self.copy(pattern="*zlibd.lib", dst="lib", src=build_dir, keep_path=False)
                self.copy(pattern="*zlib.lib", dst="lib", src=build_dir, keep_path=False)
                self.copy(pattern="*zlib.dll.a", dst="lib", src=build_dir, keep_path=False)
                if tools.os_info.is_linux:
                    self.copy(pattern="*libz.dll.a", dst="lib", src=self.ZIP_FOLDER_NAME)
                if self.settings.compiler == "Visual Studio":
                    current_lib = os.path.join(lib_path, "zlib%s.lib" % suffix)
                    os.rename(current_lib, os.path.join(lib_path, "zlib.lib"))
            else:
                build_dir = os.path.join(self.ZIP_FOLDER_NAME, "_build/lib")
                if self.settings.os == "Windows":
                    if tools.os_info.is_windows:
                        # MinGW
                        self.copy(pattern="libzlibstaticd.a", dst="lib", src=build_dir, keep_path=False)
                        self.copy(pattern="libzlibstatic.a", dst="lib", src=build_dir, keep_path=False)
                        # Visual Studio
                        self.copy(pattern="zlibstaticd.lib", dst="lib", src=build_dir, keep_path=False)
                        self.copy(pattern="zlibstatic.lib", dst="lib", src=build_dir, keep_path=False)
                    if tools.os_info.is_linux:
                        self.copy(pattern="libz.a", dst="lib", src=self.ZIP_FOLDER_NAME, keep_path=False)
                if self.settings.compiler == "Visual Studio":
                    current_lib = os.path.join(lib_path, "zlibstatic%s.lib" % suffix)
                    os.rename(current_lib, os.path.join(lib_path, "zlib.lib"))
                elif self.settings.compiler == "gcc":
                    if not tools.os_info.is_linux:
                        current_lib = os.path.join(lib_path, "libzlibstatic.a")
                        os.rename(current_lib, os.path.join(lib_path, "libzlib.a"))
        else:
            if self.options.shared:
                if self.settings.os == "Macos":
                    self.copy(pattern="*.dylib", dst="lib", src=build_dir, keep_path=False)
                else:
                    self.copy(pattern="*.so*", dst="lib", src=build_dir, keep_path=False)
            else:
                self.copy(pattern="*.a", dst="lib", src=build_dir, keep_path=False)

    def package_info(self):
        if self.settings.os == "Windows" and not tools.os_info.is_linux:
            self.cpp_info.libs = ['zlib']
        else:
            self.cpp_info.libs = ['z']
