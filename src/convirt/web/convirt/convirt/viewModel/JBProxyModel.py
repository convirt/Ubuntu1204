#   ConVirt   -  Copyright (c) 2008 Convirture Corp.
#   ======
#
# ConVirt is a Virtualization management tool with a graphical user
# interface that allows for performing the standard set of VM operations
# (start, stop, pause, kill, shutdown, reboot, snapshot, etc...). It
# also attempts to simplify various aspects of VM lifecycle management.
#
#
# This software is subject to the GNU General Public License, Version 2 (GPLv2)
# and for details, please consult it at:
#
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt
# author : Jd <jd_jedi@users.sourceforge.net>

class JBProxyModel:

    url_list = [ ("NAV_REGISTER_APPLIANCE", ("Register",'register')),
                 ("NAV_INFO" ,  ("Info",'info')),
                 ("NAV_NETWORK_CONFIG", ("Network",'staticip')),
                 ("NAV_PROXY_CONFIG",  ("Proxy",'proxy')),
                 ("NAV_SET_TIME_ZONE" , ("Time Zone",'timezone')),
                 ("NAV_BACKUP" , ("Backup",'backup')),
               ]

    def __init__(self):
        # initialize the UI component
        #self.ui = JBUI()
        pass

    def get_path(self, in_opcode):
        for (opcode,(desc, path)) in self.url_list:
            if opcode == in_opcode:
                return path

    def getProxyIntegration(self):
        ops = []
        ops.append(("SPECIFY_DETAILS", "Specify Details"))
        ops.append(("SEPARATOR", "--"))
        ops.append(("VISIT_APPLICATION", "Application"))
        ops.append(("SEPARATOR", "--"))
        for op, details in self.url_list:
            desc, url = details
            ops.append((op,desc))

        return ops

    def get_keys(self):
        return ("host", "app_protocol", "app_port", "app_path",\
                            "app_mgmt_protocol", "app_mgmt_port")

    def is_valid_info(self,vm):
        if vm and vm.get_config():
            config = vm.get_config()
            for vkey in self.get_keys():
                if not config.get(vkey):
                    return False
            return True
        
    def get_info(self, vm, username=None, password=None):
        if vm and vm.get_config():
            config = vm.get_config()

            (port,app_port)=("","")
            host = config["host"]
            proto = config["app_mgmt_protocol"]
            if config["app_mgmt_port"]:
                port = int(config["app_mgmt_port"])
            app_proto= config["app_protocol"]
            if config["app_port"]:
                app_port = int(config["app_port"])
            if config["app_path"] :
                app_path = config["app_path"]
            else:
                app_path = "/"

            # TBD : credential management needs to be done properly
            if username is None:
                username = "admin"
            if password is None:
                password = "password"

            return ((app_proto, host, app_port, app_path),
                    (proto, host, port),
                    (username, password))

    # get the web url
    def get_web_url(self, vm):
        (app_url, mgmt_url, creds) = self. get_info(vm)
        (proto, host, port, path) = app_url
        url = "%s://%s:%d/%s" % (proto, host, port, path)
        return url

    # get the mgmt web url
    def get_mgmt_web_url(self, vm, path):
        (app_url, mgmt_url, creds) = self. get_info(vm)
        (proto, host, port) = mgmt_url
        (u, p) = creds
        url = "%s://%s:%d/%s" % (proto, host, port, path)
        return url

    # Callback
#    def executeOp(self, context, opcode):
#        vm = context
#        if opcode.find('NAV_') == 0:
#            self.ui.JumpTo(vm, self.get_path(opcode))
#        elif opcode == "VISIT_APPLICATION" :
#            self.ui.JumpToApp(vm)
#        elif opcode == "SPECIFY_DETAILS" :
#            self.ui.SpecifyDetails(vm)
#        else:
#            raise Exception("Invalid operation " + opcode)

if __name__ == "__main__":
    print "Hello";