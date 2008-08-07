## Do not apply library policy!!
%define	name	readline
%define	version	5.2
%define	release	%mkrel 9

%define major 5
%define lib_name_orig lib%{name}
%define lib_name %mklibname %{name} %{major}

Summary:	Library for reading lines from a terminal
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPLv2+
Group:		System/Libraries
Url:		http://tiswww.case.edu/php/chet/readline/rltop.html
Source0:	ftp://ftp.gnu.org/gnu/readline/%{name}-%{version}.tar.gz
Source1:	%{SOURCE0}.sig
Patch0:		readline-4.3-no_rpath.patch
Patch1:		readline-5.2-inv.patch
Patch3:		readline-4.1-outdated.patch
Patch4:		rl-header.patch
Patch5:		rl-attribute.patch
# (tpg) upstream patches
Patch10:	readline52-001.patch
Patch11:	readline52-002.patch
Patch12:	readline52-003.patch
Patch13:	readline52-004.patch
Patch14:	readline52-005.patch
Patch15:	readline52-006.patch
Patch16:	readline52-007.patch
Patch17:	readline52-008.patch
Patch18:	readline52-009.patch
Patch19:	readline52-010.patch
Patch20:	readline52-011.patch
BuildRequires:	libncurses-devel 
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The "readline" library will read a line from the terminal and return it,
allowing the user to edit the line with the standard emacs editing keys.
It allows the programmer to give the user an easier-to-use and more
intuitive interface.

%package -n	%{lib_name}
Summary:	Shared libraries for readline
Group:		System/Libraries
Obsoletes:	%{name}
Provides:	%{name} = %{version}-%{release}

%description -n	%{lib_name}
This package contains the library needed to run programs dynamically
linked to readline.

%package -n	%{lib_name}-doc
Summary:	Readline documentation in GNU info format
Group:		Books/Computer books
Provides:	%{name}-doc = %{version}-%{release}
Requires:	%{lib_name} = %{version}-%{release}

%description -n	%{lib_name}-doc
This package contains readline documentation in the GNU info format.

%package -n	%{lib_name}-devel
Summary:	Files for developing programs that use the readline library
Group:		Development/C
Requires:	%{lib_name} = %{version}-%{release}
Obsoletes:	%{name}-devel
Provides:	%{lib_name_orig}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Requires:	libncurses-devel 

%description -n	%{lib_name}-devel
The "readline" library will read a line from the terminal and return it,
using prompt as a prompt.  If prompt is null, no prompt is issued.  The
line returned is allocated with malloc(3), so the caller must free it when
finished.  The line returned has the final newline removed, so only the
text of the line remains.

%prep
%setup -q
%patch0 -p1 -b .no_rpath
%patch1 -p1 -b .inv
%patch3 -p1 -b .outdated
%patch4 -p1 -b .header
%patch5 -p1 -b .attribute
libtoolize --copy --force
%patch10 -p0 -b .001
%patch11 -p0 -b .002
%patch12 -p0 -b .003
%patch13 -p0 -b .004
%patch14 -p0 -b .005
%patch15 -p0 -b .006
%patch16 -p0 -b .007
%patch17 -p0 -b .008
%patch18 -p0 -b .009
%patch19 -p0 -b .010
%patch20 -p0 -b .011

%build
export LDFLAGS="-I%{_includedir}/ncurses -lncurses"
export CFLAGS="%{optflags} -I%{_includedir}/ncurses -lncurses"
export CXXFLAGS="%{optflags} -I%{_includedir}/ncurses -lncurses"

%configure2_5x \
	 --with-curses

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
%post -n %{lib_name} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{lib_name} -p /sbin/ldconfig
%endif

%post -n %{lib_name}-doc
%{_install_info history.info}
%{_install_info readline.info}

%preun -n %{lib_name}-doc
%{_remove_install_info history.info}
%{_remove_install_info readline.info}

%files -n %{lib_name}
%defattr(-,root,root)
/%{_lib}/lib*.so.%{major}*

%files -n %{lib_name}-doc
%{_infodir}/*info*

%files -n %{lib_name}-devel
%defattr(-,root,root)
%doc CHANGELOG CHANGES MANIFEST README USAGE
%doc doc examples support
%{_mandir}/man3/*
%{_includedir}/readline
%{_libdir}/lib*.a
%{_libdir}/lib*.so
/%{_lib}/*so
