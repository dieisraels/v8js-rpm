# v8 and v8js RPM binary spec

These RPM were built to have an easy way to install the [google's javascript engine v8 5.x](https://developers.google.com/v8/) and [v8js](https://github.com/phpv8/v8js) php extension for EL7 users.

## Building the Binary RPM on RHEL 7 / CentOS 7


### Prerequisites:

- GNU make 
- g++ 4.8 or newer
- libicu-devel


```bash
yum install gcc-c++ make libicu-devel
```

## Compile V8 6.9.x ... 7.3.x (using GN)

### install depot_tools

  ```bash
  cd /tmp
  git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git
  ```

### adding PATH variable

  ```bash
  export PATH=`pwd`/depot_tools:"$PATH"
  ```

### download v8 source
  ```bash
  cd depot_tools
  fetch v8
  cd v8
  ```

### (optional) If you'd like to build a certain version (version >= 7.4 not working with default libstdc++.so.6 on EL7 (`GLIBCXX_3.4.20` missing)):
  ```bash
  git checkout 7.3.492.25
  gclient sync
  ```

### All build dependencies are fetched by running:
  ```bash
  gclient sync
  ```

### Setup GN
  ```bash
  tools/dev/v8gen.py -vv x64.release -- is_component_build=true
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

## compile v8js

### Prerequisites:

- V8 7.3.x
- PHP 7.x from [SCL](https://www.softwarecollections.org/en/scls/rhscl/rh-php72/) or EPEL

#### SCL

```bash
sudo yum install centos-release-scl
sudo yum install rh-php72
scl enable rh-php72 bash
sudo yum install rh-php72-php-devel
```

#### EPEL

```bash
sudo yum -y install epel-release
sudo yum-config-manager --enable remi-php73
sudo yum update
sudo yum install php php-devel

```

### clone v8js (special version for compatibility with V8 7.3.x)

  ```bash
  cd /tmp
  git clone https://github.com/phpv8/v8js
  cd v8js
  git checkout 85097c1
  ```

### compile

  ```bash
  phpize
  # check path for php-config
  which php-config
  ./configure --with-php-config=[PATH_TO_PHP_CONFIG] --with-v8js=/opt/v8 LDFLAGS="-lstdc++"
  make
  make test
  ```

### create v8js binary rpm package

change */home/v8/v8js* to your v8js checkout directory.

```bash
rpmbuild -bb v8js.spec --define="pre_built_dir /home/v8/v8js"
```

### alternativ copy module and ini files manually

```bash
# check path for php modules
php-config --extension-dir
sudo su
cp /tmp/v8js/modules/v8js.so [PATH_TO_PHP_EXTENSION_DIR]
echo -e "; Enable v8js extension module\nextension=v8js.so" >  [PATH_TO_PHP_INI_DIR]/99-v8js.ini
```
