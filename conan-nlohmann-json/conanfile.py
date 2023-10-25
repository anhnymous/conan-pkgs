import os
import re
from pathlib import Path
import xml.etree.ElementTree as ET
from conans import ConanFile, CMake, tools

class NlohmannJsonConan(ConanFile):
  name = "nlohmann-json"
  version = "v3.11.2"
  license = "MIT License"
  author = "Nlohmann"
  url = "https://github.com/nlohmann/json"
  description = "JSON for Modern C++"
  topics = ("open source", "conan package", "json")
  settings = "cppstd", "os", "compiler", "build_type", "arch"
  options = {"shared": [True, False], "fPIC": [True, False]}
  default_options = {"shared": False, "fPIC": True}
  generators = "cmake"
  exports_sources = [ "json/include/nlohmann/*" ]
  no_copy_source = True

  def requirements(self):
    self.settings.compiler.libcxx = "libstdc++11"
    if self.settings.os == "Windows":
      del self.options.fPIC

  def package(self):
    self.copy("*.hpp", dst="include/nlohmann",
               keep_path=True, src="json/include/nlohmann")

  def package_id(self):
    self.info.header_only()

  def packae_info(self):
    self.cpp_info.libs = ["nlohmann-json"]
