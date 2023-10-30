import os
import re
import shutil
from conans import ConanFile, CMake, tools

class grpcConan(ConanFile):
  name = "Conan Package for gRPC"
  version = "v1.50.0"
  license = "<Apache License 2.0>"
  author = "Anh Tran"
  url = "https://github.com/grpc/grpc"
  description = "gRPC – An RPC library and framework"
  topics = ("open source", "conan package", "grpc")
  settings = "cppstd", "os", "compiler", "build_type", "arch"
  options = {"shared": [True, False], "fPIC": [True, False]}
  default_options = {"shared": True, "fPIC": True}
  generators = "cmake"
  exports_sources = [ "src/*", "CMakeLists.txt" ]
  no_copy_source = True

  def requirements(self):
    self.settings.compiler.libcxx = "libstdc++11"
    if self.settings.os == "Windows":
      del self.options.fPIC

  def build(self):
    GRPC_SYSROOT_DIR = "sysroot"
    try:
      os.mkdir(GRPC_SYSROOT_DIR, 0o755)
    except FileExistsError as err:
      pass
    global ABS_SYSROOT_DIR
    ABS_SYSROOT_DIR = os.path.join(os.getcwd(), GRPC_SYSROOT_DIR)

    cmake = CMake(self)
    cmake.definitions["gRPC_INSTALL"] = "ON"
    cmake.definitions["CMAKE_INSTALL_PREFIX"] = ABS_SYSROOT_DIR
    cmake.definitions["gRPC_BUILD_TESTS"] = "OFF"
    cmake.definitions["BUILD_SHARED_LIBS"] = "ON"
    cmake.definitions["CMAKE_BUILD_TYPE"] = "Release"
    cmake.definitions["ABSL_PROPAGATE_CXX_STD"] = "ON"
    cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = True
    cmake.definitions["ABSL_ENABLE_INSTALL"] = "ON"

    cmake.definitions["gRPC_ABSL_PROVIDER"]     = "module"
    cmake.definitions["gRPC_CARES_PROVIDER"]    = "module"
    cmake.definitions["gRPC_PROTBUF_PROVIDER"]  = "module"
    cmake.definitions["gRPC_RES2_PROVIDER"]     = "module"
    cmake.definitions["gRPC_SSL_PROVIDER"]      = "package"
    cmake.definitions["gRPC_ZLIB_PROVIDER"]     = "package"

    if (tools.get_env("target") == "LINUX_PC"):
      cmake.definitions["TARGET"] = "LINUX_PC"
    if (tools.get_env("target") == "ARM64"):
      cmake.definitions["TARGET"] = "ARM64"
      cmake.definitions["CMAKE_SYSTEM_PROCESSOR"] = "aarch64"
    else:
      cmake.definitions["TARGET"] = "LINUX_PC"

    cmake.configure(source_folder="src/grpc")
    cmake.build()
    cmake.install()

  def package(self):
    self.copy("*", src=ABS_SYSROOT_DIR, keep_path=True, symlinks=True)
    self.copy(".*", src=ABS_SYSROOT_DIR, keep_path=True, symlinks=True)
    self.copy(".*.*", src=ABS_SYSROOT_DIR, keep_path=True, symlinks=True)

  def packae_info(self):
    self.cpp_info.libs = ["conan-grpc"]
