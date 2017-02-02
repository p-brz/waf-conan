# Waf-Conan Installer

Conan package to simplify installing the waf build system (https://waf.io/) binary in conan packages.

Inspired by the [conan-cmake-installer](https://github.com/lasote/conan-cmake-installer).

## How to use

1) Includes the dependency in your conanfile.

        requires = "waf/<version>@paulobrizolara/stable"

2) In your build, use the `ConfigureEnvironment` to use the waf executable

        def build(self):
            ...
            env = ConfigureEnvironment(self)
            cmd = "%s waf configure build -o %s" % (env.command_line_env, self.build_path)
            
            self.run(cmd, cwd=self.conanfile_directory)
            
3) (optional) You can import the waf executable to use it directly

        def imports(self):
            ...
            # Copy waf executable to project folder
            self.copy("waf", dst=".")
            

## Quickstart

Snippet to use in your projects. Using also [Waf Conan Generator](https://github.com/paulobrizolara/waf-conangenerator)


```python
from conans import ConanFile, ConfigureEnvironment

import os
from os import path

class MyConanFile(ConanFile):
    settings = "os", "compiler", "build_type", "arch"

    #Conan dependencies
    requires = (
	"waf/0.1.1@paulobrizolara/stable"
    )

    def imports(self):
	# Copy waf executable to project folder
	self.copy("waf", dst=".")

        self.copy("*.dll", dst="bin", src="bin") # From bin to bin
        self.copy("*.dylib*", dst="bin", src="lib") # From lib to bin
        
    def build(self):
        self.build_path = path.abspath("build")
        
        env = ConfigureEnvironment(self)
        cmd = "%s waf configure build %s -o %s" % (env.command_line_env, self.get_options(), self.build_path)
        
        self.run(cmd, cwd=self.conanfile_directory)
        
    def package(self):
        env = ConfigureEnvironment(self)
        
        # Install your project files on destination (package_folder)
        self.run("{} waf install".format(env.command_line_env))

    def get_options(self):
        opts = []

        # Add other options here to pass to your build

        if not hasattr(self, "package_folder"):
            self.package_folder = path.abspath(path.join(".", "package"))
            
        opts.append("--prefix=%s" % self.package_folder)
            
        return " ".join(opts)

```
