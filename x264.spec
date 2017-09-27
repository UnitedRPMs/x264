%global api 152
%global gitdate 20170926
%global commit0 ba24899b0bf23345921da022f7a51e0c57dbe73d
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global gver .git%{shortcommit0}

%bcond_with 10bit-depth

Name:     x264
Version:  0.%{api}
Release:  2%{?gver}%{?dist}
Epoch:	  1
Summary:  A free h264/avc encoder - encoder binary
License:  GPLv2
Group:    Applications/Multimedia
Url:      http://developers.videolan.org/x264.html
Source0:	http://repo.or.cz/x264.git/snapshot/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
Source1: 	x264-snapshot.sh
BuildRequires:  nasm
BuildRequires:  pkgconfig
BuildRequires:  yasm-devel >= 1.2.0
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Provides:	%{name} = %{epoch}:%{version}-%{release}
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}


%description
x264 is a free library for encoding next-generation H264/AVC video
streams. The code is written from scratch by Laurent Aimar, Loren
Merritt, Eric Petit (OS X), Min Chen (vfw/asm), Justin Clay (vfw), Mans
Rullgard, Radek Czyz, Christian Heine (asm), Alex Izvorski (asm), and
Alex Wright. It is released under the terms of the GPL license. This
package contains a shared library and a commandline tool for encoding
H264 streams. This library is needed for mplayer/mencoder for H264
encoding support.

Encoder features:
- CAVLC/CABAC
- Multi-references
- Intra: all macroblock types (16x16, 8x8, and 4x4 with all predictions)
- Inter P: all partitions (from 16x16 down to 4x4)
- Inter B: partitions from 16x16 down to 8x8 (including skip/direct)
- Ratecontrol: constant quantizer, single or multipass ABR, optional VBV
- Scene cut detection
- Adaptive B-frame placement
- B-frames as references / arbitrary frame order
- 8x8 and 4x4 adaptive spatial transform
- Lossless mode
- Custom quantization matrices
- Parallel encoding of multiple slices (currently disabled)

Be aware that the x264 library is still in early development stage. The
command line tool x264 can handle only raw YUV 4:2:0 streams at the
moment so please use mencoder or another tool that supports x264 library
for all other file types.

%package libs
Summary: Library for encoding H264/AVC video streams
Group: Development/Libraries
Provides:	%{name}-libs = %{version}-%{release}
Provides:	%{name}-libs = %{epoch}:%{version}-%{release}

%description libs
x264 is a free library for encoding H264/AVC video streams, written from
scratch.

%package devel
Summary:        Libraries and include file for the %{name} encoder
Group:          Development/Libraries
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Requires: 	pkgconfig
Provides:       x264-devel = %{version}-%{release}
Provides:	x264-devel = %{epoch}:%{version}-%{release}
Obsoletes:      x264-devel < %{version}

%description devel
x264 is a free library for encoding next-generation H264/AVC video
streams. The code is written from scratch by Laurent Aimar, Loren
Merritt, Eric Petit (OS X), Min Chen (vfw/asm), Justin Clay (vfw), Mans
Rullgard, Radek Czyz, Christian Heine (asm), Alex Izvorski (asm), and
Alex Wright. It is released under the terms of the GPL license. This
package contains a static library and a header needed for the
development with libx264. This library is needed to build
mplayer/mencoder with H264 encoding support.

%prep
%autosetup -n x264-%{shortcommit0}

%build

#  pushd %{_builddir}/%{name}-%{shortcommit0}

%configure --enable-shared \
      --enable-pic 

make %{?_smp_mflags}

%if %{with 10bit-depth}
cp -r %{_builddir}/%{name}-%{shortcommit0} %{_builddir}/%{name}-10bit
pushd %{_builddir}/%{name}-10bit

%configure --enable-shared \
      --enable-pic \
      --bit-depth=10

make %{?_smp_mflags}
%endif


%install

  make -C %{_builddir}/%{name}-%{shortcommit0} DESTDIR=%{buildroot} install-cli
%if %{with 10bit-depth}
  install -m 755 %{_builddir}/%{name}-10bit/x264 %{buildroot}/%{_bindir}/x264-10bit
%endif

  install -dm 755 %{buildroot}/%{_libdir}
  make -C %{_builddir}/%{name}-%{shortcommit0} DESTDIR=%{buildroot} install-lib-shared %{?_smp_mflags}
%if %{with 10bit-depth}
  make -C %{_builddir}/%{name}-10bit DESTDIR=%{buildroot} install-lib-shared %{?_smp_mflags}
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_bindir}/x264
%if %{with 10bit-depth}
%{_bindir}/x264-10bit
%endif

%files libs
%{_libdir}/libx264.so.%{api}

%files devel
%defattr(0644,root,root)
%{_includedir}/x264.h
%{_includedir}/x264_config.h
%{_libdir}/pkgconfig/x264.pc
%{_libdir}/libx264.so


%changelog

* Tue Sep 26 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> 0.152-2.gitba24899
- Updated to 152-2.gitba24899

* Wed May 24 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> 0.148-20.gitd32d7bf
- Updated to 148-20.gitd32d7bf

* Sun Feb 26 2017 David Vásquez <davidjeremias82 AT gmail DOT com> 0.148-18-20170226git90a61ec
- Rebuilt for bad integrity
- New changes in sources

* Sun Feb 26 2017 David Vásquez <davidjeremias82 AT gmail DOT com> 0.148-17-20170226git90a61ec
- Updated to 148-17-20170226git90a61ec

* Tue Nov 29 2016 David Vásquez <davidjeremias82 AT gmail DOT com> 0.148-7-20161129git72d53ab
- Legacy support
- Updated to 0.148-20161129git72d53ab

* Mon Sep 12 2016 David Vásquez <davidjeremias82 AT gmail DOT com> 0.148-6-20160906git3f5ed56
- Added epoch for sub-packages libs and devel

* Tue Sep 06 2016 David Vásquez <davidjeremias82 AT gmail DOT com> 0.148-4-20160906git3f5ed56
- Epoch tag

* Thu Jul 07 2016 David Vásquez <davidjeremias82 AT gmail DOT com> 0.148-3-20160707git3f5ed56
- Updated to 0.148-20160707git3f5ed56

* Wed Apr 20 2016 David Vásquez <davidjeremias82 AT gmail DOT com> 0.148-2-20160420git3b70645
- Updated to x264-0.148-20160420-3b70645
- Built x264-10bit

* Sat Feb 20 2016 David Vasquez <davidjeremias82 at gmail dot com> - 0.148-1-20160220gita01e339
- Updated to 0.148-20160220-a01e339

* Mon Jul 13 2015 David Vasquez <davidjeremias82 at gmail dot com> - 0.146-1-20150713git121396c
- Upstream
- Updated to 0.146-20150713git121396c
- Added git tag in x264-snapshot.sh

* Tue Nov 19 2013 obs@botter.cc
- add -fno-aggressive-loop-optimizations to extra-cflags in
  configure for >= 13.1 (specfile), see also
  https://bugs.launchpad.net/ubuntu/+source/x264/+bug/1241772
  MAY BE REMOVED on upstream fix
