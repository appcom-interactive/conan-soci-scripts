from conans import ConanFile, CMake, tools
import os

class SociConan(ConanFile):
    name = "SOCI"
    version = "3.2.3"
    author = "Ralph-Gordon Paul (gordon@rgpaul.com)"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "android_ndk": "ANY", "android_stl_type":["c++_static", "c++_shared"]}
    default_options = "shared=False", "android_ndk=None", "android_stl_type=c++_static"
    description = "The C++ Database Access Library"
    url = "https://github.com/Manromen/conan-soci-scripts"
    license = "BSL-1.0"
    exports_sources = "patches/*"

    # download zlib sources
    def source(self):
        url = "https://github.com/SOCI/soci/archive/%s.tar.gz" % self.version
        tools.get(url)

        if self.version == "3.2.3":
            tools.patch(patch_file="patches/3.2.3.patch")
        
    # compile using cmake
    def build(self):
        cmake = CMake(self)
        cmake.verbose = True

        library_folder = "soci-%s/src" % self.version

        cmake.definitions["SOCI_TESTS"] = "OFF"

        cmake.definitions["SOCI_SHARED"] = "ON" if self.options.shared == True else "OFF"
        cmake.definitions["SOCI_STATIC"] = "OFF" if self.options.shared == True else "ON"
        
        if self.settings.os == "Android":
            cmake.definitions["CMAKE_SYSTEM_VERSION"] = self.settings.os.api_level
            cmake.definitions["CMAKE_ANDROID_NDK"] = os.environ["ANDROID_NDK_PATH"]
            cmake.definitions["CMAKE_ANDROID_NDK_TOOLCHAIN_VERSION"] = self.settings.compiler
            cmake.definitions["CMAKE_ANDROID_STL_TYPE"] = self.options.android_stl_type

        if self.settings.os == "iOS":
            ios_toolchain = "cmake-modules/Toolchains/ios.toolchain.cmake"
            cmake.definitions["CMAKE_TOOLCHAIN_FILE"] = ios_toolchain
            if self.settings.arch == "x86" or self.settings.arch == "x86_64":
                cmake.definitions["IOS_PLATFORM"] = "SIMULATOR"
            else:
                cmake.definitions["IOS_PLATFORM"] = "OS"

        if self.settings.os == "Macos":
            cmake.definitions["CMAKE_OSX_ARCHITECTURES"] = tools.to_apple_arch(self.settings.arch)

        cmake.configure(source_folder=library_folder)
        cmake.build()
        cmake.install()

    def requirements(self):
        self.requires("Boost/1.68.0@%s/%s" % (self.user, self.channel))
        self.requires("MySQLClient/6.1.9@%s/%s" % (self.user, self.channel))
        self.requires("SQLite/3.24.0@%s/%s" % (self.user, self.channel))

#    def package(self):
#        self.copy("*", dst="include", src='include')
#        self.copy("*.lib", dst="lib", src='lib', keep_path=False)
#        self.copy("*.dll", dst="bin", src='bin', keep_path=False)
#        self.copy("*.so", dst="lib", src='lib', keep_path=False)
#        self.copy("*.dylib", dst="lib", src='lib', keep_path=False)
#        self.copy("*.a", dst="lib", src='lib', keep_path=False)
        
    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.includedirs = ['include']

    def config_options(self):
        # remove android specific option for all other platforms
        if self.settings.os != "Android":
            del self.options.android_ndk
            del self.options.android_stl_type
