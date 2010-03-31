%define major 6
%define lib_name_orig lib%{name}
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	Library for reading lines from a terminal
Name:		readline
Version:	6.1
Release:	%mkrel 2
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
Patch10:    readline61-001
Patch12:    readline61-002
BuildRequires:	libncurses-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The "readline" library will read a line from the terminal and return it,
allowing the user to edit the line with the standard emacs editing keys.
It allows the programmer to give the user an easier-to-use and more
intuitive interface.

%package -n %{libname}
Summary:	Shared libraries for readline
Group:		System/Libraries
Obsoletes:	%{name}
Provides:	%{name} = %{version}-%{release}

%description -n	%{libname}
This package contains the library needed to run programs dynamically
linked to readline.

%package doc
Summary:	Readline documentation in GNU info format
Group:		Books/Computer books
Provides:	%{name}-doc = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Obsoletes:	%{libname}-doc

%description doc
This package contains readline documentation in the GNU info format.

%package -n %{develname}
Summary:	Files for developing programs that use the readline library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Obsoletes:	%{name}-devel < 6.0-2
Provides:	%{lib_name_orig}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Requires:	libncurses-devel 
Obsoletes:	%{mklibname readline 5 -d}

%description -n	%{develname}
The "readline" library will read a line from the terminal and return it,
using prompt as a prompt.  If prompt is null, no prompt is issued.  The
line returned is allocated with malloc(3), so the caller must free it when
finished.  The line returned has the final newline removed, so only the
text of the line remains.

%prep
%setup -q
%patch0 -p1 -b .no_rpath
%patch3 -p1 -b .outdated
%patch4 -p1 -b .header
%patch5 -p1 -b .attribute
%patch6 -p1 -b .fix-perms
%patch10 -p0 -b .001
%patch12 -p0 -b .002
libtoolize --copy --force

%build
export LDFLAGS="-I%{_includedir}/ncurses -lncurses"
export CFLAGS="%{optflags} -I%{_includedir}/ncurses -lncurses"
export CXXFLAGS="%{optflags} -I%{_includedir}/ncurses -lncurses"

%configure2_5x \
	 --with-curses \
	 --enable-multibyte

perl -p -i -e 's|-Wl,-rpath.*||' shlib/Makefile

%make

%install
rm -rf %{buildroot}
%makeinstall_std

# put all libs in /lib because some package needs it
# before /usr is mounted
install -d %{buildroot}/%{_lib}
mv %{buildroot}%{_libdir}/*.so* %{buildroot}/%{_lib}
ln -s ../../%{_lib}/lib{history,readline}.so %{buildroot}%{_libdir}

# The make install moves the existing libs with a suffix of old. Urgh.
rm -f %{buildroot}/%{_lib}/*.old

perl -p -i -e 's|/usr/local/bin/perl|/usr/bin/perl|' doc/texi2html

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%post doc
%{_install_info history.info}
%{_install_info readline.info}

%preun doc
%{_remove_install_info history.info}
%{_remove_install_info readline.info}

%files -n %{libname}
%defattr(-,root,root)
/%{_lib}/lib*.so.%{major}*

%files doc
%{_infodir}/*info*

%files -n %{develname}
%defattr(-,root,root)
%doc CHANGELOG CHANGES MANIFEST README USAGE
%doc doc examples support
%{_mandir}/man3/*
%{_datadir}/readline
%{_includedir}/readline
%{_libdir}/lib*.a
%{_libdir}/lib*.so
/%{_lib}/*so
