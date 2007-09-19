## Do not apply library policy!!
%define	name	readline
%define	version	5.2
%define	release	%mkrel 6

%define lib_major	5
%define lib_name_orig	lib%{name}
%define lib_name	%mklibname %{name} %{lib_major}

Summary:	Library for reading lines from a terminal
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Libraries
Url:		http://cnswww.cns.cwru.edu/php/chet/readline/rltop.html
Source0:	ftp://ftp.gnu.org/pub/gnu/readline/%{name}-%{version}.tar.bz2
Patch3:		readline-4.1-outdated.patch
#Patch11:	ftp://ftp.cwru.edu/pub/bash/readline-5.1-patches/readline51-001
Patch12:	readline52-001
Patch16:	readline-4.3-no_rpath.patch
#Patch18:	readline-wrap.patch
 
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
Requires:	%{lib_name} = %{version}

%description -n	%{lib_name}-doc
This package contains readline documentation in the GNU info format.

%package -n	%{lib_name}-devel
Summary:	Files for developing programs that use the readline library
Group:		Development/C
Requires:	%{lib_name} = %{version}-%{release}
Obsoletes:	%{name}-devel
Provides:	%{lib_name_orig}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{lib_name}-devel
The "readline" library will read a line from the terminal and return it,
using prompt as a prompt.  If prompt is null, no prompt is issued.  The
line returned is allocated with malloc(3), so the caller must free it when
finished.  The line returned has the final newline removed, so only the
text of the line remains.

%prep
%setup -q
%patch3 -p1 -b .outdated
libtoolize --copy --force
%patch12 -p0 -b .001
%patch16 -p1 -b .no_rpath
#%patch18 -p1 -b .wrap

%build
export CFLAGS="$RPM_OPT_FLAGS"
%configure2_5x --with-curses=ncurses
perl -p -i -e 's|-Wl,-rpath.*||' shlib/Makefile
%make static shared

%install
rm -rf $RPM_BUILD_ROOT
%{makeinstall} install-shared
# put all libs in /lib because some package needs it
# before /usr is mounted
install -d $RPM_BUILD_ROOT/%{_lib}
mv $RPM_BUILD_ROOT%{_libdir}/*.so* $RPM_BUILD_ROOT/%{_lib}
ln -s ../../%{_lib}/lib{history,readline}.so $RPM_BUILD_ROOT%{_libdir}
for i in history readline; do
   ln -s ../%{_lib}/lib$i.so.4 $RPM_BUILD_ROOT/%{_lib}/lib$i.so.4.1
   ln -s ../%{_lib}/lib$i.so.4 $RPM_BUILD_ROOT/%{_lib}/lib$i.so.4.2
done


# The make install moves the existing libs with a suffix of old. Urgh.
rm -f $RPM_BUILD_ROOT/%{_lib}/*.old

perl -p -i -e 's|/usr/local/bin/perl|/usr/bin/perl|' doc/texi2html

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %{lib_name} -p /sbin/ldconfig
%postun -n %{lib_name} -p /sbin/ldconfig

%post -n %{lib_name}-doc
%{_install_info history.info}
%{_install_info readline.info}

%preun -n %{lib_name}-doc
%{_remove_install_info history.info}
%{_remove_install_info readline.info}

%files -n %{lib_name}
%defattr(-,root,root)
/%{_lib}/lib*.so.*

%files -n %{lib_name}-doc
%{_infodir}/*info*

%files -n %{lib_name}-devel
%defattr(-,root,root)
%doc CHANGELOG CHANGES INSTALL MANIFEST README USAGE
%doc doc examples support
%{_mandir}/man3/*
%{_includedir}/readline
%{_libdir}/lib*.a
%{_libdir}/lib*.so
/%{_lib}/*so


