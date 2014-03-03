%define	major	6
%define	libname	%mklibname %{name} %{major}
%define	libhist	%mklibname history %{major}
%define	devname	%mklibname %{name} -d

%bcond_without	uclibc

Summary:	Library for reading lines from a terminal
Name:		readline
Version:	6.3
Release:	1
License:	GPLv2+
Group:		System/Libraries
Url:		http://tiswww.case.edu/php/chet/readline/rltop.html
Source0:	ftp://ftp.gnu.org/gnu/readline/%{name}-%{version}.tar.gz
Source1:	ftp://ftp.gnu.org/gnu/readline/%{name}-%{version}.tar.gz.sig
Patch0:		readline-4.3-no_rpath.patch
Patch3:		readline-4.1-outdated.patch
Patch4:		rl-header.patch
Patch5:		rl-attribute.patch
Patch6:		readline-6.0-fix-shared-libs-perms.patch
Patch8:		readline-6.2-fix-missing-linkage.patch
BuildRequires:	ncurses-devel
%if %{with uclibc}
BuildRequires:	uClibc-devel >= 0.9.33.2-11
%endif

%description
The "readline" library will read a line from the terminal and return it,
allowing the user to edit the line with the standard emacs editing keys.
It allows the programmer to give the user an easier-to-use and more
intuitive interface.

%package -n	%{libname}
Summary:	Shared libreadline library for readline
Group:		System/Libraries
Provides:	%{name} = %{EVRD}
Conflicts:	%{_lib}history < 6.2-13
Obsoletes:	%{_lib}history < 6.2-13

%description -n	%{libname}
This package contains the library needed to run programs dynamically
linked to readline.

%package -n	uclibc-%{libname}
Summary:	Shared libreadline library for readline (uClibc build)
Group:		System/Libraries
Conflicts:	uclibc-%{_lib}history < 6.2-13

%description -n	uclibc-%{libname}
This package contains the library needed to run programs dynamically
linked to readline.

%package -n	%{libhist}
Summary:	Shared libhistory library for readline
Group:		System/Libraries
Conflicts:	%{_lib}readline6 < 6.2-13
Obsoletes:	%{_lib}readline6 < 6.2-13

%description -n	%{libhist}
This package contains the libhistory library from readline.

%package -n	uclibc-%{libhist}
Summary:	Shared libhistory library for readline (uClibc Build)
Group:		System/Libraries
Conflicts:	uclibc-%{_lib}readline6 < 6.2-13

%description -n	uclibc-%{libhist}
This package contains the libhistory library from readline.

%package	doc
Summary:	Readline documentation in GNU info format
Group:		Books/Computer books
Provides:	%{name}-doc = %{EVRD}
Obsoletes:	%{libname}-doc < %{EVRD}
BuildArch:	noarch

%description	doc
This package contains readline documentation in the GNU info format.

%package -n	%{devname}
Summary:	Files for developing programs that use the readline library
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Requires:	%{libhist} = %{EVRD}
%if %{with uclibc}
Requires:	uclibc-%{libname} = %{EVRD}
Requires:	uclibc-%{libhist} = %{EVRD}
%endif
Provides:	%{name}-devel = %{EVRD}

%description -n	%{devname}
The "readline" library will read a line from the terminal and return it,
using prompt as a prompt.  If prompt is null, no prompt is issued.  The
line returned is allocated with malloc(3), so the caller must free it when
finished.  The line returned has the final newline removed, so only the
text of the line remains.

%prep
%setup -q
%apply_patches

sed -e 's#/usr/local#%{_prefix}#g' -i doc/texi2html
libtoolize --copy --force

%build
CONFIGURE_TOP=$PWD

%if %{with uclibc}
mkdir -p uclibc
pushd uclibc
%uclibc_configure \
	--enable-static=no \
	--with-curses \
	--enable-multibyte

%make
popd
%endif

mkdir -p system
pushd system
%configure2_5x \
	--enable-static=no \
	--with-curses \
	--enable-multibyte

%make
popd

%install
%if %{with uclibc}
%makeinstall_std -C uclibc
install -d %{buildroot}%{uclibc_root}/%{_lib}
for l in libhistory.so libreadline.so; do
	rm %{buildroot}%{uclibc_root}%{_libdir}/${l}
	mv %{buildroot}%{uclibc_root}%{_libdir}/${l}.%{major}* %{buildroot}%{uclibc_root}/%{_lib}
	ln -sr %{buildroot}%{uclibc_root}/%{_lib}/${l}.%{major}.* %{buildroot}%{uclibc_root}%{_libdir}/${l}
done
%endif

%makeinstall_std -C system
# put all libs in /lib because some package needs it
# before /usr is mounted
install -d %{buildroot}/%{_lib}
for l in libhistory.so libreadline.so; do
	rm %{buildroot}%{_libdir}/${l}
	mv %{buildroot}%{_libdir}/${l}.%{major}* %{buildroot}/%{_lib}
	ln -sr %{buildroot}/%{_lib}/${l}.%{major}.* %{buildroot}%{_libdir}/${l}
done

rm -rf %{buildroot}%{_docdir}/readline/{CHANGES,INSTALL,README} \
	%{buildroot}%{_prefix}/uclibc%{_docdir}/readline/{CHANGES,INSTALL,README}

%files -n %{libhist}
/%{_lib}/libhistory.so.%{major}*

%files -n %{libname}
/%{_lib}/libreadline.so.%{major}*

%if %{with uclibc}
%files -n uclibc-%{libhist}
%{uclibc_root}/%{_lib}/libhistory.so.%{major}*

%files -n uclibc-%{libname}
%{uclibc_root}/%{_lib}/libreadline.so.%{major}*
%endif

%files doc
%{_infodir}/history.info*
%{_infodir}/readline.info*
%{_infodir}/rluserman.info*

%files -n %{devname}
%doc CHANGELOG CHANGES MANIFEST README USAGE
%doc doc examples support
%{_mandir}/man3/*
%{_includedir}/readline
%{_libdir}/libhistory.so
%{_libdir}/libreadline.so
%if %{with uclibc}
%{uclibc_root}%{_libdir}/libhistory.so
%{uclibc_root}%{_libdir}/libreadline.so
%endif

