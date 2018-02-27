%define        pre_built_dir ~/opt-v8

Name: v8
Summary: V8 is Google's open source high-performance JavaScript engine, written in C++ and used in Google Chrome, the open source browser from Google. It implements ECMAScript as specified in ECMA-262, 3rd edition, and runs on Windows XP or later, Mac OS X 10.5+, and Linux systems that use IA-32, ARM or MIPS processors. V8 can run standalone, or can be embedded into any C++ application.
Version: 6.5.237
Release: 1
License: BSD
Group: Development/Tools
URL: https://developers.google.com/v8/
Vendor:         The Chromium Project
Requires: glibc
Requires: libicu
BuildRoot: %{_tmppath}/%{name}

%description
%{summary}

%prep

%build
# Empty section.

%install
rm -rf %{buildroot}
mkdir -p  %{buildroot}/opt/v8/{include,lib}
#mkdir -p  %{buildroot}/usr/share/v8

## binary & lib
cp %{pre_built_dir}/lib/* %{buildroot}/opt/v8/lib

## header files
cp -R %{pre_built_dir}/include/* %{buildroot}/opt/v8/include/

%clean

%files
%defattr(-,root,root,-)
/opt/v8/*

%changelog
* Tue Feb 27 2018 Sergey Bondarev <s.bondarev@southbridge.ru>
- Bump to version 6.5

* Mon Aug 22 2016 KwangSeob Jeong <lesstif@gmail.com>
- First Build
