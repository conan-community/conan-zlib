from conans import ConanFile
import os
from conans.tools import download, unzip, replace_in_file
from conans import CMake, ConfigureEnvironment


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
    license="http://www.zlib.net/zlib_license.html"
    
    def config(self):
        try: # Try catch can be removed when conan 0.8 is released
            del self.settings.compiler.libcxx 
        except: 
            pass
        
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
            env = ConfigureEnvironment(self.deps_cpp_info, self.settings)
            env_line = env.command_line_env.replace('CFLAGS="', 'CFLAGS="-fPIC ')
            if self.settings.arch == "x86" or self.settings.arch == "x86_64":
                env_line = env_line.replace('CFLAGS="', 'CFLAGS="-mstackrealign ')
            self.output.warn(env_line)
                        
            if self.settings.os == "Macos":
                old_str = '-install_name $libdir/$SHAREDLIBM'
                new_str = '-install_name $SHAREDLIBM'
                replace_in_file("./%s/configure" % self.ZIP_FOLDER_NAME, old_str, new_str)
                     
            self.run("cd %s && %s ./configure" % (self.ZIP_FOLDER_NAME, env_line))
            #self.run("cd %s && %s make check" % (self.ZIP_FOLDER_NAME, env.command_line_env))
            self.run("cd %s && %s make" % (self.ZIP_FOLDER_NAME, env_line))
         
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