# CERES Ray Tracer (CRT)
[![GitHub Release](https://img.shields.io/github/v/release/ceres-navigation/ceres-raytracer?include_prereleases)](https://github.com/ceres-navigation/ceres-pathtracer/releases)
[![GitHub issues](https://img.shields.io/github/issues/ceres-navigation/ceres-raytracer)](https://github.com/ceres-navigation/ceres-pathtracer/issues)
[![GitHub Contributers](https://img.shields.io/github/contributors/ceres-navigation/ceres-raytracer)](https://github.com/ceres-navigation/ceres-raytracer/graphs/contributors)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


This project was developed as part of [CERES](https://ceresnavigation.org) and aims to provide scientifically useful path tracing capabilities for:
- Rendering photo-real images
- Simulating multi-bounce behavior accounting for wavelength and polarization
- Modeling solar radiation and albedo radiation pressure on spacecraft

### Available Environments
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
<!-- ![Mac OS](https://img.shields.io/badge/mac%20os-000000?style=for-the-badge&logo=macos&logoColor=F0F0F0) -->
<!-- ![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white) -->

| Environment   | Build         |  Notes  |
| ------------- |:-------------:| :-------:|
| Ubuntu 20.04  | [![](https://github.com/ceres-navigation/ceres-raytracer/actions/workflows/cmake_ubuntu20.yml/badge.svg)](https://github.com/ceres-navigation/ceres-raytracer/actions) |   |
| Ubuntu 18.04  | [![](https://github.com/ceres-navigation/ceres-raytracer/actions/workflows/cmake_ubuntu18.yml/badge.svg)](https://github.com/ceres-navigation/ceres-raytracer/actions) | Using `export CXX="g++-9" CC="gcc-9"` |
<!-- | macOS 11      | [![](https://github.com/ceres-navigation/ceres-raytracer/actions/workflows/cmake_macos11.yml/badge.svg)](https://github.com/ceres-navigation/ceres-raytracer/actions) |  |
| macOS 10.15   | [![](https://github.com/ceres-navigation/ceres-raytracer/actions/workflows/cmake_macos10.yml/badge.svg)](https://github.com/ceres-navigation/ceres-raytracer/actions) |  | -->


***
## Quick Start:
### Install from PyPI:
```
pip install ceres-raytracer
```

***
## Building from Source:

### Build from source::

```
git clone https://github.com/ceres-navigation/ceres-raytracer.git
pip install .
```
**NOTE for 18.04 ONLY:** Because `std::filesystem` is not implemented in GNU libstdc++ prior to 9.1 and LLVM libc++ prior to 9.0, you must first upgrade your compiler.  Simply run:
```
sudo add-apt-repository ppa:ubuntu-toolchain-r/test
sudo apt update
sudo apt install gcc-9 g++-9
export CXX="g++-8" CC="gcc-8"
```

***
## Demos:
The follow demos can be found [ceres-raytracer-demos](https://github.com/ceres-navigation/ceres-raytracer-demos).  Simply clone the repository (after isntalling `ceres-raytracer`) and run any of the `.py` example files:


![](https://raw.githubusercontent.com/ceres-navigation/ceres-raytracer-demos/master/results/cornell.png)


### Static Scene:
The file `demos/bunny.py` provides an example of how to setup a static scene.  Simply navigate to the `demos/` directory of the cloned `ceres-raytracer` repository, and run:
```
python bunny.py
```
Doing so will produce an image sequence of a light moving around the stanford bunny.

![](https://raw.githubusercontent.com/ceres-navigation/ceres-raytracer-demos/master/results/bunny.gif)


***
## Tasks:
- [ ] Implement physically based radiance tracking for paths
- [ ] Improve the adaptive sampling noise calculation
- [ ] Triangular meshes
  - [ ] Add vertex color support
  - [x] Add parent object support
  - [ ] Add parsers for more mesh type (.PLY, .GLTF/.GLB)
  - [ ] Add texture mapping and normal maps
- [x] Python Refactor
  - [x] Reorganize code into classes
  - [x] Add python bindings with pybind11
  - [x] Animation/sequence support
  - [x] Add wrapper classes with keyword arguments and state handling
  - [x] Setup build system using setuptools (for pip install)
  - [x] Distribute on PyPI
  - [x] Add Static BVH cacheing
- [ ] Importance Sampling
  - [ ] Implement Malley's method for cosine importance
  - [ ] Investigate alternative importance sampling method for planetary bodies (where primary indirect contribution is near horizon)
- [ ] Lighting
  - [x] Add output intensity to light objects
  - [ ] Add circular area lights
  - [ ] Add emissive mesh geometries
  - [ ] Add polarized light
  - [ ] Add specific wavelength support
- [ ] Cameras
  - [ ] Add linear pushbroom camera model
  - [ ] Add calibrated camera model
- [ ] Materials
  - [ ] Add McEwen BRDF
  - [ ] Add PBR textures
- [ ] Simulation
  - [ ] Add radiation pressure modeling

***
## Attributions
### madmann91's Modern C++ BVH Construction and Traversal Library
This project utilizes a BVH construction and traversal library built by [madmann91](https://github.com/madmann91).  While we have made some modifications to their implementation, their work forms most of the basis of the bounding volume hierarchy used in this project.  Their originally source code can be found in the [bvh repository](https://github.com/madmann91/bvh)


### National Science Foundation Graduate Research Fellowship
This material is based upon work supported by the [National Science Foundation Graduate Research Fellowship](https://www.nsfgrfp.org/) under Grant No. 2020305048.  NSF GRFP gave Chris Gnam the flexibility and resources required to complete his research in spacecraft navigation, and this project is meant to serve as an open source implementation of his dissertation.

***
## Contact
All questions, comments, and concerns should be directed to Chris Gnam: crgnam@buffalo.edu
