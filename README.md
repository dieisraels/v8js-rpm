# v8 and v8js RPM binary spec

These RPM were built to have an easy way to install the [google's javascript engine v8 5.x](https://developers.google.com/v8/) and [v8js](https://github.com/phpv8/v8js) php extension for EL7 users.

## Install from RPM Package

- You can install prebuilt rpm binary package from here. (Recommended method)


```bash
$ wget https://github.com/lesstif/v8js-rpm/releases/download/5.2.371/v8-5.2.371-1.x86_64.rpm
$ wget https://github.com/lesstif/v8js-rpm/releases/download/1.3.1-1/v8js-1.3.1-2.x86_64.rpm
$ sudo yum localinstall v8*.rpm -y 
```

## Building the Binary RPM on RHEL 7


### Prerequisites:

- GNU make 
- g++ 4.8 or newer
- libicu-devel


```bash
yum install gcc-c++ make libicu-devel
```

## Compile V8 5.6 and newer (using GN)

### install depot_tools

  ```bash
  git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git
  cd depot_tools
  ```

### adding PATH variable

  ```bash
  export PATH=`pwd`/depot_tools:"$PATH"
  ```

### download v8 source
  ```bash
  fetch v8
  cd v8
  ```

### (optional) If you'd like to build a certain version:
  ```bash
  git checkout 6.5.237
  gclient sync
  ```

### All build dependencies are fetched by running:
  ```bash
  gclient sync
  ```

### Setup GN
  ```bash
  tools/dev/v8gen.py -vv x64.release
  echo is_component_build = true >> out.gn/x64.release/args.gn
  ```

### Build
  ```bash
  ninja -C out.gn/x64.release/
  ```

### Prepare to rpm build, copy to ~/opt-v8/
  ```bash
  mkdir -p ~/opt-v8/{bin,lib,include}
  cp out.gn/x64.release/d8 ~/opt-v8/bin/
  cp out.gn/x64.release/lib*.so out.gn/x64.release/*_blob.bin out.gn/x64.release/icudtl.dat ~/opt-v8/lib/
  cp -R include/* ~/opt-v8/include/
  ```

  ```bash
  rpmbuild -ba v8.spec
  ```

## Compile V8 versions 5.5 and older (using Gyp)

### install depot_tools

  ```bash
  git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git
  cd depot_tools
  ```

### adding PATH variable

  ```bash
  export PATH=`pwd`/depot_tools:"$PATH"
  ```

### download v8 source

  ```bash
  fetch v8
  cd v8
  ```

### (optional) If you'd like to build a certain version:
  ```bash
  git checkout 5.2.1
  gclient sync
  ```

### All build dependencies are fetched by running:

  ```bash
  gclient sync
  ```

### setting build variable

  ```bash
  # use libicu of operating system
  export GYPFLAGS="-Duse_system_icu=1"

  # Build (with internal snapshots)
  export GYPFLAGS="${GYPFLAGS} -Dv8_use_snapshot=true -Dv8_use_external_startup_data=0 "

  # eliminates swarming_client dependency
  export GYPFLAGS="${GYPFLAGS} -Dtest_isolation_mode=noop"

  # Force gyp to use system-wide ld.gold
  export GYPFLAGS="${GYPFLAGS} -Dlinux_use_bundled_gold=0"
  ```

### compile

  ```bash
  make x64.release library=shared snapshot=on i18nsupport=on -j8
  ```

### create v8 binary rpm package

change */home/v8/v8* to your v8 checkout directory.

```bash
rpmbuild -bb v8.spec --buildroot=/tmp/v8 --define="pre_built_dir /home/lesstif/v8"
```

## compile v8js


### clone v8js

  ```bash
  cd ~
  git clone https://github.com/phpv8/v8js
  ```

### checkout tag

  ```bash
  git checkout php7
  ```

### compile

  ```bash
  phpize
  ./configure --with-v8js=/opt/v8 LDFLAGS="-lstdc++"
  make
  make test
  ```

### create v8js binary rpm package

change */home/v8/v8js* to your v8js checkout directory.

```bash
rpmbuild -bb v8js.spec --define="pre_built_dir /home/v8/v8js"
```
