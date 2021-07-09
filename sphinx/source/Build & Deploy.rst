Build & Deploy
================

**Prerequisites**

The software runs on an Atlas 200DK board, which has `Python 3.7.5`, `ffmpeg` and the `pyACL` library installed. All of the following is done on the Atlas board.

Python 3.7.5
The python version is checked in the `setup.sh` script. (See setup step below).

This scripts tests the versions of the default python3-interpreter and (if available) the interpreter at

`/usr/local/python3.7.5/bin/python3.7`

(That is the location, python is installed to when following the da-vinci-a-scaleable-architecture-for-neural-network-computing-v6.pdf [https://www.schihei.eu/blog/da-vinci-a-scalable-architecture-for-neural-network-computing-updated-v6], page 103.)

ffmpeg (4.1.3)
We follow the guide from the da-vinci-a-scaleable-architecture-for-neural-network-computing-v6.pdf[https://www.schihei.eu/blog/da-vinci-a-scalable-architecture-for-neural-network-computing-updated-v6], page 119.

Since we also need ffmpeg to support some codecs, the installation process is somewhat different:

1) Install codecs

    `sudo apt install libvpx-dev libmp3lame-dev libopus-dev libtheora-dev libvorbis-dev`

2) Build x264 codec from source

   `git clone  https://code.videolan.org/videolan/x264.git && cd x264` (ae03d92b)

   `./configure --enable-shared --enable-pic --enable-static --prefix=/home/HwHiAiUser/ascend_ddk/arm/`

   `make -j8`

   `make install`


3) Build ffmpeg from source

    When running `configure`, additional flags are needed to enable the installed video- and audio-codecs:
    `cd ffmpeg-4.1.3`

    `export CFLAGS="-I/home/HwHiAiUser/ascend_ddk/arm/include"`

    `export LDFLAGS="-L/home/HwHiAiUser/ascend_ddk/arm/lib"`


    ./configure --enable-shared --enable-pic --enable-static --disable-yasm \
    --enable-libmp3lame --enable-libopus --enable-libvpx --enable-libvorbis \
    --enable-libtheora --enable-libx264 --enable-gpl --prefix=/home/HwHiAiUser/ascend_ddk/arm


    `make -j8`

    `make install`


**pyACL**

To verify, that `pyACL` is available, one can run the script `scripts/check_acl_libary.sh`.

**OpenCV**

OpenCV is automatically installed into the virtual environment, it doesn't have to be available system-wide.

**Setup**

The script `scripts/setup.sh` sets up a virtual environment for python initially.

If the environment is set up already, it updates the dependencies.

**Build**

There is no explicit build step. It can be run directly after a successful setup.

**Test**

To execute the tests, run the script `scripts/test.sh`.

**Run**

The script `script/run.sh` starts the webservice and prints the URL. One can open it in the browser and start using the software.