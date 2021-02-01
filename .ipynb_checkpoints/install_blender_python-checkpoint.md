### Written by Tianfu Wang 02/01/2020
### Download Blender Scource Files

Clone blender repository from github and update to lastest version

```
mkdir ~/blender-git
cd ~/blender-git
git clone https://git.blender.org/blender.git
cd blender
git submodule update --init --recursive
git submodule foreach git checkout master
git submodule foreach git pull --rebase origin master
```

Download Libraries needed to compile blender

```
mkdir ~/blender-git/lib
cd ~/blender-git/lib
svn checkout https://svn.blender.org/svnroot/bf-blender/trunk/lib/linux_centos7_x86_64
```

### Edit the Blender source files for our specific needs

#### Change CMake Build Settings
Go to `~/blender-git/blender/GNUmakefile` and change code at line 301:

Change this 
```
CMAKE_CONFIG = cmake $(CMAKE_CONFIG_ARGS) \
                     -H"$(BLENDER_DIR)" \
                     -B"$(BUILD_DIR)" \
                     -DCMAKE_BUILD_TYPE_INIT:STRING=$(BUILD_TYPE)

```

to  
```
CMAKE_CONFIG = cmake $(CMAKE_CONFIG_ARGS) \
                     -H"$(BLENDER_DIR)" \
                     -B"$(BUILD_DIR)" \
                     -DCMAKE_BUILD_TYPE_INIT:STRING=$(BUILD_TYPE)\
                     -DPNG_LIBRARY_RELEASE:FILEPATH=/home/tianfuwang/blender-git/lib/linux_centos7_x86_64/png/lib/libpng16.a \
                     -DCMAKE_INSTALL_PREFIX=/home/tianfuwang/.conda/envs/blender_python/lib/python3.7/site-packages \
                     -DWITH_INSTALL_PORTABLE=ON\
                     -DWITH_AUDASPACE=OFF\
```

Here `-DCMAKE_INSTALL_PREFIX=` should be followed by the `site-packages` directory of your python environment 

#### Changes in the source code

Blender source code needs to be changed to enable directly saving render in RAM buffer while running in the background, as shown in here https://blender.stackexchange.com/questions/69230/python-render-script-different-outcome-when-run-in-background/81240#81240

In the file `source/blender/compositor/operations/COM_ViewerOperation.h`, line ~58:

```
bool isOutputOperation(bool /*rendering*/) const { if (G.background) return false; return isActiveViewerOutput();
```
should be changed to

```
bool isOutputOperation(bool /*rendering*/) const {return isActiveViewerOutput(); }
```
and in file source/blender/compositor/operations/COM_PreviewOperation.h, line ~48:

```
bool isOutputOperation(bool /*rendering*/) const { return !G.background; }
```
should be changed to
```
bool isOutputOperation(bool /*rendering*/) const { return true; }
```

### Compile Blender
Make sure the CMake version is at least 3.9.0
```
export CC=clang-9
export CXX=clang++-9
```
To compile blender, run 
```
cd ~/blender-git/blender
make bpy
```

### Run Blender in Python

Now in the python environment where Blender is installed run the following 

```python
import bpy
bpy.context.scene.render.engine = 'CYCLES'
bpy.ops.render.render()
```
After `import bpy` there might be an warning saying `/run/user/1008/gvfs/ non-existent directory` but this seems to not have visible effects on anything.

If everything is installed correctly this should run fine.

Note that CYCLES is the only render that can run in blender python.

### References
https://wiki.blender.org/wiki/Building_Blender/Linux/Ubuntu
https://wiki.blender.org/wiki/Building_Blender/Other/BlenderAsPyModule


