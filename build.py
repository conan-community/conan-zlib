import os
import platform
import sys

default_user = "lasote"
default_channel = "testing"

if __name__ == "__main__":
    channel = os.getenv("CONAN_CHANNEL", default_channel)
    username = os.getenv("CONAN_USERNAME", default_user)
    print("User: '%s' Channel: '%s'" % (username, channel))
    os.system('conan export %s/%s' % (username, channel))
   
    def test(settings):
        argv =  " ".join(sys.argv[1:])
        command = "conan test %s %s" % (settings, argv)
        retcode = os.system(command)
        if retcode != 0:
            exit("Error while executing:\n\t %s" % command)

    if platform.system() == "Windows":
        for visual_version in [10, 12, 14]:
            compiler = '-s compiler="Visual Studio" -s compiler.version=%s ' % str(visual_version)
            # Static x86
            test(compiler + '-s arch=x86 -s build_type=Debug -s compiler.runtime=MDd -o zlib:shared=False')
            test(compiler + '-s arch=x86 -s build_type=Debug -s compiler.runtime=MTd -o zlib:shared=False')
            test(compiler + '-s arch=x86 -s build_type=Release -s compiler.runtime=MD -o zlib:shared=False')
            test(compiler + '-s arch=x86 -s build_type=Release -s compiler.runtime=MT -o zlib:shared=False')
    
            # Shared x86
            test(compiler + '-s arch=x86 -s build_type=Debug -s compiler.runtime=MDd -o zlib:shared=True')
            test(compiler + '-s arch=x86 -s build_type=Debug -s compiler.runtime=MTd -o zlib:shared=True')
            test(compiler + '-s arch=x86 -s build_type=Release -s compiler.runtime=MD -o zlib:shared=True')
            test(compiler + '-s arch=x86 -s build_type=Release -s compiler.runtime=MT -o zlib:shared=True')
    
            if visual_version != 10:
                # Static x86_64
                test(compiler + '-s arch=x86_64 -s build_type=Debug -s compiler.runtime=MDd -o zlib:shared=False')
                test(compiler + '-s arch=x86_64 -s build_type=Debug -s compiler.runtime=MTd -o zlib:shared=False')
                test(compiler + '-s arch=x86_64 -s build_type=Release -s compiler.runtime=MD -o zlib:shared=False')
                test(compiler + '-s arch=x86_64 -s build_type=Release -s compiler.runtime=MT -o zlib:shared=False')
                
                # Shared x86_64
                test(compiler + '-s arch=x86_64 -s build_type=Debug -s compiler.runtime=MDd -o zlib:shared=True')
                test(compiler + '-s arch=x86_64 -s build_type=Debug -s compiler.runtime=MTd -o zlib:shared=True')
                test(compiler + '-s arch=x86_64 -s build_type=Release -s compiler.runtime=MD -o zlib:shared=True')
                test(compiler + '-s arch=x86_64 -s build_type=Release -s compiler.runtime=MT -o zlib:shared=True')

    else:  # Compiler and version not specified, please set it in your home/.conan/conan.conf (Valid for Macos and Linux)

        # Static x86
        test('-s arch=x86 -s build_type=Debug -o zlib:shared=False')
        test('-s arch=x86 -s build_type=Release -o zlib:shared=False')

        # Shared x86
        test('-s arch=x86 -s build_type=Debug -o zlib:shared=True')
        test('-s arch=x86 -s build_type=Release -o zlib:shared=True')

        # Static x86_64
        test('-s arch=x86_64 -s build_type=Debug -o zlib:shared=False')
        test('-s arch=x86_64 -s build_type=Release -o zlib:shared=False')

        # Shared x86_64
        test('-s arch=x86_64 -s build_type=Debug -o zlib:shared=True')
        test('-s arch=x86_64 -s build_type=Release -o zlib:shared=True')
