import os
import platform
import sys

if __name__ == "__main__":

    if len(sys.argv)==2:
         versions = [sys.argv[1]]
    else:
         versions = ["4.6", "4.8", "4.9", "5.2", "5.3"]
        
    for gcc_version in versions:
        image_name = "lasote/conangcc%s" % gcc_version.replace(".", "")
        os.system("sudo mkdir ~/.conan/data && sudo chmod -R 777 ~/.conan/data")
        os.system("ls -la  ~/.conan && ls -la ~/.conan/data")
        os.system("sudo docker pull %s" % image_name)
        curdir = os.path.abspath(os.path.curdir)
        command = 'sudo docker run --rm  -v %s:/home/conan/project -v '\
                  '~/.conan/data:/home/conan/.conan/data -it %s /bin/sh -c '\
                  '"ls -la /home/conan/.conan/data && cd project && sudo pip install conan --upgrade && python build.py"' % (curdir, image_name)
        os.system(command)
