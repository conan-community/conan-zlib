import os
from conan.packager import ConanMultiPackager
import sys
import platform
from copy import copy

def add_visual_builds(builder, visual_version, arch):

    base_set = {"compiler": "Visual Studio", 
                "compiler.version": visual_version, 
                "arch": arch}
    sets = []
    sets.append([{"build_type": "Release", "compiler.runtime": "MT"}, {"zlib:shared":False}])        
    sets.append([{"build_type": "Debug", "compiler.runtime": "MTd"}, {"zlib:shared":False}])
    sets.append([{"build_type": "Debug", "compiler.runtime": "MDd"}, {"zlib:shared":False}])
    sets.append([{"build_type": "Release", "compiler.runtime": "MD"}, {"zlib:shared":False}])
    sets.append([{"build_type": "Debug", "compiler.runtime": "MDd"}, {"zlib:shared":True}])
    sets.append([{"build_type": "Release", "compiler.runtime": "MD"}, {"zlib:shared":True}])        
      
    for setting, options in sets:
       tmp = copy(base_set)
       tmp.update(setting)
       builder.add(tmp, options)
       
def add_other_builds(builder):
    # Not specified compiler or compiler version, will use the auto detected     
    for arch in ["x86", "x86_64"]:
        for shared in [True, False]:
            for build_type in ["Debug", "Release"]:
                builder.add({"arch":arch, "build_type": build_type}, {"zlib:shared": shared})
           

if __name__ == "__main__":
    channel = os.getenv("CONAN_CHANNEL", "testing")
    username = os.getenv("CONAN_USERNAME", "lasote")
    current_page = os.getenv("CONAN_CURRENT_PAGE", "1")
    total_pages = os.getenv("CONAN_TOTAL_PAGES", "1")
    gcc_versions = os.getenv("CONAN_GCC_VERSIONS", None)
    gcc_versions = gcc_versions.split(",") if gcc_versions else None
    use_docker = os.getenv("CONAN_USE_DOCKER", False)
    upload = os.getenv("CONAN_UPLOAD", False)
    reference = os.getenv("CONAN_REFERENCE")
    password = os.getenv("CONAN_PASSWORD")
    travis = os.getenv("TRAVIS", False)
    travis_branch = os.getenv("TRAVIS_BRANCH", None)
    appveyor = os.getenv("APPVEYOR", False)
    appveyor_branch = os.getenv("APPVEYOR_REPO_BRANCH", None)
    
    if travis:
        if travis_branch=="master":
            channel = "stable"
        else:
            channel = channel
        os.environ["CONAN_CHANNEL"] = channel
        
    if appveyor:
        if appveyor_branch=="master" and not os.getenv("APPVEYOR_PULL_REQUEST_NUMBER"):
            channel = "stable"
        else:
            channel = channel
        os.environ["CONAN_CHANNEL"] = channel
    
    args = " ".join(sys.argv[1:])
    builder = ConanMultiPackager(args, username, channel)
    if platform.system() == "Windows":
        for visual_version in [10, 12, 14]:
            for arch in ["x86", "x86_64"]:
                add_visual_builds(builder, visual_version, arch)
    else:
        add_other_builds(builder)
    
    if use_docker:  
        builder.docker_pack(current_page, total_pages, gcc_versions)
    else:
        builder.pack(current_page, total_pages)
    
    if upload and reference and password:
        builder.upload_packages(reference, password)
