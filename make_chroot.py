import os
import sys

class chrootCreate:

    def __init__(self,CHROOT_DIR):
        self.CHROOT_DIR = CHROOT_DIR
        self.CHROOT_BIN = CHROOT_DIR + "/" + "bin/"
        self.__execute('mkdir -p ' + self.CHROOT_BIN)

    def __check_status(self,cmd):
        if int(os.popen('echo $?').read().strip()) != 0:
            print "command "+ cmd + "failed to execute"
            exit(1)
    
    def __execute(self,cmd):
        os.system(cmd)
        self.__check_status(cmd)

    def __get_command_libraries(self,cmd):
        libs = os.popen('which '+cmd+' | xargs -I {} ldd {} | grep -v vdso').read()
        lib_files = [i.split("=>")[1].strip() for i in libs.split("\n") if '=>' in i]
        lib_files += [i.strip() for i in libs.split("\n") if not '=>' in i]
        lib_files = [i.split(" ")[0] for i in lib_files if i]
        return lib_files


    def __lib_copy(self,addr):
        loc = self.CHROOT_DIR + '/'.join(addr.split('/')[:-1])
        self.__execute('mkdir -p '+loc)
        self.__execute('cp ' + addr + ' ' + loc)

    def install(self,cmd):
        for i in self.__get_command_libraries(cmd):
            self.__lib_copy(i)
        self.__execute('cp ' + os.popen('which '+cmd).read().strip()+' '+self.CHROOT_BIN)
        


if __name__ == "__main__":

    required_cmds = ['bash','ls','clear']
    cc = chrootCreate(sys.argv[1])

    for cmd in required_cmds:
        print "installing command :",cmd
        cc.install(cmd)


