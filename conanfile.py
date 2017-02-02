from conans import ConanFile
from conans import tools

import os
from os import path


class WafInstaller(ConanFile):
    name = "waf"
    version = "0.1.1"
    license = "MIT"
    url = "http://github.com/paulobrizolara/waf-conan"
    options = {"version": ["1.9.7"]}
    default_options = "version=1.9.7"
    build_policy="missing"
    
    description="Package to simplify installing the waf build system (https://waf.io/) binary in conan packages"
    
    def build(self):
        bin_url = "https://waf.io/waf-%s" % self.options.version
        tools.download(bin_url, "waf")
        self.add_exec_permission("waf")

    def package(self):
        self.copy("waf", dst="")

    def package_info(self):
#        waf_path = os.path.join(self.package_folder, "waf")
        
        # Adds to path waf installation folder
        self.env_info.path.append(self.package_folder)
        
        self.cpp_info.includedirs = []  
        self.cpp_info.libdirs = [] 
        self.cpp_info.resdirs = []

    def add_exec_permission(self, file):
        import stat
        
        current_permissions = stat.S_IMODE(os.lstat(file).st_mode)
        os.chmod(file, current_permissions | stat.S_IXUSR)
