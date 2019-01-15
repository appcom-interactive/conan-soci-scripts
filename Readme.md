# Conan for SOCI - The C++ Database Access Library

This repository contains the conan receipe that is used to build the SOCI packages at appcom.

For Infos about the library please visit [Github](https://github.com/SOCI/soci).
The library is licensed under the [Boost Software License 1.0](https://github.com/SOCI/soci/blob/master/LICENSE_1_0.txt).
This repository is licensed under the [MIT License](LICENSE).


## macOS

To create a package for macOS you can run the conan command like this:

`conan create . soci/3.2.3@appcom/stable -s os=Macos -s os.version=10.14 -s arch=x86_64 -s build_type=Release -o shared=False -o mysql=True -o sqlite=True`

### Requirements

* [CMake](https://cmake.org/)
* [Conan](https://conan.io/)
* [Xcode](https://developer.apple.com/xcode/)
