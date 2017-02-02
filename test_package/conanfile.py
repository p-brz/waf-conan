#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, ConfigureEnvironment
import os
from os import path

channel = os.getenv("CONAN_CHANNEL", "testing")
username = os.getenv("CONAN_USERNAME", "paulobrizolara")
version  = "0.1.1"
name     = "waf"

class TestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = (
        "%s/%s@%s/%s" % (name, version, username, channel),
    )
    exports = "wscript"

    def build(self):
        self.build_path = path.abspath("build")
        
        env = ConfigureEnvironment(self)
        
        cmd = "waf configure build -o %s" % (self.build_path)
        
        self.output.info("ENV:\n{}".format(env.command_line_env))
        self.output.info(cmd)
        
        self.run("{} {}".format(env.command_line_env, cmd), cwd=self.conanfile_directory)

    def imports(self):
        self.copy("*.dll", "bin", "bin")
        self.copy("*.dylib", "bin", "bin")

    def test(self):
        self.run(os.path.join(self.build_path, "test"))
