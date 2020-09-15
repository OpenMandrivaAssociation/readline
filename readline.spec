# Readline is used by various wine dependencies
%ifarch %{x86_64}
%bcond_without compat32
%endif

%define major 8
%define libname %mklibname %{name} %{major}
%define libhist %mklibname history %{major}
# Unfortunately, readline uses version numbers as sonames,
# even if the ABI remains stable...
%define libname6 %mklibname %{name} 6
%define libhist6 %mklibname history 6
%define libname7 %mklibname %{name} 7
%define libhist7 %mklibname history 7
%define devname %mklibname %{name} -d
%define lib32name %mklib32name %{name} %{major}
%define lib32hist %mklib32name history %{major}
%define lib32name6 %mklib32name %{name} 6
%define lib32hist6 %mklib32name history 6
%define lib32name7 %mklib32name %{name} 7
%define lib32hist7 %mklib32name history 7
%define dev32name %mklib32name %{name} -d
%define patchlevel 4
%define pre %{nil}

%global optflags %{optflags} -Oz

Summary:	Library for reading lines from a terminal
Name:		readline
Version:	8.0
%if "%{pre}" != ""
Release:	0.%{pre}.1
Source0:	ftp://ftp.cwru.edu/pub/bash/%{name}-%{version}-%{pre}.tar.gz
%else
Release:	5
Source0:	ftp://ftp.gnu.org/gnu/readline/%{name}-%{version}.tar.gz
%endif
License:	GPLv2+
Group:		System/Libraries
Url:		http://tiswww.case.edu/php/chet/readline/rltop.html
# Upstream patches
%if 0%{patchlevel}
%(for i in $(seq 1 %{patchlevel}); do echo Patch$i: ftp://ftp.gnu.org/pub/gnu/readline/readline-%{version}-patches/readline$(echo %{version} |sed -e 's,\.,,g')-$(echo 000$i |rev |cut -b1-3 |rev); done)
%endif
Patch1000:	readline-4.3-no_rpath.patch
Patch1003:	readline-4.1-outdated.patch
Patch1004:	rl-header.patch
Patch1005:	rl-attribute.patch
Patch1008:	readline-6.2-fix-missing-linkage.patch
BuildRequires:	ncurses-devel
%if %{with compat32}
BuildRequires:	devel(libncurses)
%endif

%description
The "readline" library will read a line from the terminal and return it,
allowing the user to edit the line with the standard emacs editing keys.
It allows the programmer to give the user an easier-to-use and more
intuitive interface.

%package -n %{libname}
Summary:	Shared libreadline library for readline
Group:		System/Libraries
Provides:	%{name} = %{EVRD}
Conflicts:	%{_lib}history < 6.2-13
Obsoletes:	%{_lib}history < 6.2-13
%rename		%{libname6}
%rename		%{libname7}
%if "%{_lib}" == "lib64"
Provides:	libreadline.so.6()(64bit)
Provides:	libreadline.so.7()(64bit)
%else
Provides:	libreadline.so.6
Provides:	libreadline.so.7
%endif
Provides:	libreadline.so.6%{?_isa}
Provides:	libreadline.so.7%{?_isa}

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked to readline.

%package -n %{libhist}
Summary:	Shared libhistory library for readline
Group:		System/Libraries
Conflicts:	%{_lib}readline6 < 6.2-13
Obsoletes:	%{_lib}readline6 < 6.2-13
%rename		%{libhist6}
%rename		%{libhist7}
%if "%{_lib}" == "lib64"
Provides:	libhistory.so.6()(64bit)
Provides:	libhistory.so.7()(64bit)
%else
Provides:	libhistory.so.6
Provides:	libhistory.so.7
%endif
Provides:	libreadline.so.6%{?_isa}
Provides:	libreadline.so.7%{?_isa}

%description -n %{libhist}
This package contains the libhistory library from readline.

%package doc
Summary:	Readline documentation in GNU info format
Group:		Books/Computer books
Provides:	%{name}-doc = %{EVRD}
Obsoletes:	%{libname}-doc < %{EVRD}
BuildArch:	noarch

%description doc
This package contains readline documentation in the GNU info format.

%package -n %{devname}
Summary:	Files for developing programs that use the readline library
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Requires:	%{libhist} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
The "readline" library will read a line from the terminal and return it,
using prompt as a prompt.  If prompt is null, no prompt is issued.  The
line returned is allocated with malloc(3), so the caller must free it when
finished.  The line returned has the final newline removed, so only the
text of the line remains.

%if %{with compat32}
%package -n %{lib32name}
Summary:	Shared libreadline library for readline (32-bit)
Group:		System/Libraries
%rename		%{lib32name6}
%rename		%{lib32name7}
Provides:	libreadline.so.6
Provides:	libreadline.so.7

%description -n %{lib32name}
This package contains the library needed to run programs dynamically
linked to readline.

%package -n %{lib32hist}
Summary:	Shared libhistory library for readline (32-bit)
Group:		System/Libraries
%rename		%{lib32hist6}
%rename		%{lib32hist7}
Provides:	libhistory.so.6
Provides:	libhistory.so.7

%description -n %{lib32hist}
This package contains the libhistory library from readline.

%package -n %{dev32name}
Summary:	Files for developing programs that use the readline library (32-bit)
Group:		Development/C
Requires:	%{devname} = %{EVRD}
Requires:	%{lib32name} = %{EVRD}
Requires:	%{lib32hist} = %{EVRD}

%description -n %{dev32name}
The "readline" library will read a line from the terminal and return it,
using prompt as a prompt.  If prompt is null, no prompt is issued.  The
line returned is allocated with malloc(3), so the caller must free it when
finished.  The line returned has the final newline removed, so only the
text of the line remains.
%endif

%prep
%if "%{pre}" != ""
%setup -qn %{name}-%{version}-%{pre}
%else
%setup -q
%endif
# Upstream patches
%if 0%{patchlevel}
%(for i in `seq 1 %{patchlevel}`; do echo %%patch$i -p0; done)
%endif

%patch1000 -p1
%patch1003 -p1
%patch1004 -p1
%patch1005 -p1
%patch1008 -p1

find . -name "*.orig" |xargs rm

sed -e 's#/usr/local#%{_prefix}#g' -i doc/texi2html
libtoolize --copy --force

export CONFIGURE_TOP="$(pwd)"

%if %{with compat32}
mkdir build32
cd build32
%configure32 \
    --enable-static=no \
    --with-curses \
    --enable-multibyte
cd ..
%endif

mkdir build
cd build
%configure \
    --enable-static=no \
    --with-curses \
    --enable-multibyte

%build
%if %{with compat32}
%make_build -C build32
%endif
%make_build -C build

%install
mkdir -p %{buildroot}%{_libdir}/pkgconfig
%if %{with compat32}
mkdir -p %{buildroot}%{_prefix}/lib/pkgconfig
%make_install -C build32
%endif
%make_install -C build
if [ -e %{buildroot}%{_includedir}/readline/rlmbutil.h ]; then
    printf '%ss\n' "rlmbutil.h is installed now -- please remove the workaround from the spec"
    exit 1
else
    cp rlmbutil.h %{buildroot}%{_includedir}/readline/
fi

# put all libs in /lib because some package needs it
# before /usr is mounted
install -d %{buildroot}/%{_lib}
for l in libhistory.so libreadline.so; do
    rm %{buildroot}%{_libdir}/${l}
    mv %{buildroot}%{_libdir}/${l}.%{major}* %{buildroot}/%{_lib}
    ln -sr %{buildroot}/%{_lib}/${l}.%{major}.* %{buildroot}%{_libdir}/${l}
# Unfortunately, readline uses version numbers as sonames,
# even if the ABI remains stable...
    ln -s ${l}.%{major} %{buildroot}/%{_lib}/${l}.6
    ln -s ${l}.%{major} %{buildroot}/%{_lib}/${l}.7
%if %{with compat32}
    ln -s ${l}.%{major} %{buildroot}%{_prefix}/lib/${l}.6
    ln -s ${l}.%{major} %{buildroot}%{_prefix}/lib/${l}.7
%endif
done

rm -rf %{buildroot}%{_docdir}/readline/{CHANGES,INSTALL,README}

%files -n %{libhist}
/%{_lib}/libhistory.so.%{major}*
/%{_lib}/libhistory.so.7
/%{_lib}/libhistory.so.6

%files -n %{libname}
/%{_lib}/libreadline.so.%{major}*
/%{_lib}/libreadline.so.7
/%{_lib}/libreadline.so.6

%files doc
%{_infodir}/history.info*
%{_infodir}/readline.info*
%{_infodir}/rluserman.info*

%files -n %{devname}
%doc MANIFEST README USAGE
%doc doc examples support
%{_mandir}/man3/*
%{_includedir}/readline
%{_libdir}/libhistory.so
%{_libdir}/libreadline.so
%{_libdir}/pkgconfig/readline.pc

%if %{with compat32}
%files -n %{lib32hist}
%{_prefix}/lib/libhistory.so.%{major}*
%{_prefix}/lib/libhistory.so.7
%{_prefix}/lib/libhistory.so.6

%files -n %{lib32name}
%{_prefix}/lib/libreadline.so.%{major}*
%{_prefix}/lib/libreadline.so.7
%{_prefix}/lib/libreadline.so.6

%files -n %{dev32name}
%{_prefix}/lib/libhistory.so
%{_prefix}/lib/libreadline.so
%{_prefix}/lib/pkgconfig/readline.pc
%endif
