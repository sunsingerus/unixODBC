#
# Conditional build:
# _without_gnome	- without GNOME1 GUI stuff
# _without_qt		- without QT GUI stuff
#
Summary:	unixODBC - a complete, free/open, ODBC solution for UNIX/Linux
Summary(pl):	unixODBC - kompletne, darmowe/otwarte ODBC dla UNIX/Linuksa
Name:		unixODBC
Version:	2.2.6
Release:	2
License:	LGPL
Group:		Libraries
# WARNING: they place snapshots of new versions using %{name}-%{version}.tar.gz
# scheme - so check for official releases on URL!
Source0:	ftp://ftp.easysoft.com/pub/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	748ce54e34b2b339c99a8b1ddaee54f5
Source1:	DataManager.desktop
Source2:	ODBCConfig.desktop
Source3:	%{name}.png
Patch0:		%{name}-ac_fix.patch
Patch1:		%{name}-no_libnsl.patch
Patch2:		%{name}-libltdl-shared.patch
Patch3:		%{name}-flex.patch
Patch4:		%{name}-gODBCConfig.patch
Icon:		unixODBC.xpm
URL:		http://www.unixodbc.com/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
%{!?_without_gnome:BuildRequires:	gnome-libs-devel}
BuildRequires:	libltdl-devel
BuildRequires:	libtool >= 1:1.4.2-9
BuildRequires:	readline-devel >= 4.2
%{!?_without_qt:BuildRequires:	qt-devel >= 2.0}
Requires(post):	/sbin/ldconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildConflicts:	kdesupport-odbc
Obsoletes:	libunixODBC2

%description
unixODBC is a complete, free/open, ODBC solution for UNIX/Linux.

%description -l pl
unixODBC - kompletne, darmowe/otwarte ODBC dla systemów UNIX/Linux.

%package devel
Summary:	unixODBC header files and development documentation
Summary(pl):	Pliki nagłówkowe i dokunentacja do unixODBC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libltdl-devel
Obsoletes:	libunixODBC2-devel

%description devel
unixODBC header files and development documentation.

%description devel -l pl
Pliki nagłówkowe i dokunentacja do unixODBC.

%package static
Summary:	unixODBC static libraries
Summary(pl):	Biblioteki statyczne unixODBC
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
unixODBC static libraries.

%description static -l pl
Biblioteki statyczne unixODBC.

%package gnome
Summary:	GNOME library and configuration GUI for unixODBC
Summary(pl):	Oparta na GNOME biblioteka i graficzny konfigurator dla unixODBC
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description gnome
GNOME library (libgtkodbcconfig) and configuration GUI (gODBCConfig)
for unixODBC.

%description gnome
Oparta na GNOME biblioteka (libgtkodbcconfig) i graficzny konfigurator
(gODBCConfig) do unixODBC.

%package gnome-devel
Summary:	Header file for libgtkodbcconfig library
Summary(pl):	Plik nagłówkowy biblioteki libgtkodbcconfig
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	%{name}-gnome = %{version}-%{release}
Requires:	gnome-libs-devel

%description gnome-devel
Header file for libgtkodbcconfig library.

%description gnome-devel -l pl
Plik nagłówkowy biblioteki libgtkodbcconfig.

%package gnome-static
Summary:	Static libgtkodbcconfig library
Summary(pl):	Statyczna biblioteka libgtkodbcconfig
Group:		X11/Development/Libraries
Requires:	%{name}-gnome-devel = %{version}-%{release}

%description gnome-static
Static libgtkodbcconfig library.

%description gnome-static -l pl
Statyczna biblioteka libgtkodbcconfig.

%package qt
Summary:	Qt-based GUIs for unixODBC
Summary(pl):	Oparte na Qt graficzne interfejsy dla unixODBC
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description qt
Qt-based GUIs for unixODBC - libodbcinstQ plugin for libodbcinst
library and applications: DataManager, DataManagerII, ODBCConfig,
odbctest.

%description qt -l pl
Oparte na Qt graficzne interfejsy użytkownika do unixODBC - wtyczka
libodbcinstQ dla biblioteki libodbcinst oraz aplikacje: DataManager,
DataManagerII, ODBCConfig, odbctest.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--%{?_without_qt:dis}%{!?_without_qt:en}able-gui \
	--enable-threads \
	--enable-drivers \
	--enable-shared \
	--enable-static

%{__make}

%if 0%{!?_without_gnome:1}
cd gODBCConfig
%{__gettextize}
%{__libtoolize}
%{__aclocal} -I macros
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if 0%{!?_without_qt:1}
install -d $RPM_BUILD_ROOT{%{_applnkdir}/System,%{_pixmapsdir}}
install %{SOURCE1} %{SOURCE2} $RPM_BUILD_ROOT%{_applnkdir}/System
install %{SOURCE3} $RPM_BUILD_ROOT%{_pixmapsdir}
%endif

%if 0%{!?_without_gnome:1}
%{__make} install -C gODBCConfig \
	DESTDIR=$RPM_BUILD_ROOT
%endif

find doc -name Makefile\* -exec rm -f {} \;

# libodbcinstQ.so.1 is lt_dlopened
rm -f $RPM_BUILD_ROOT%{_libdir}/libodbcinstQ.{so,la,a}
# libodbccr.so.1. is lt_dlopened
rm -f $RPM_BUILD_ROOT%{_libdir}/libodbccr.{so,la,a}
# Setup drivers are lt_dlopened by given name (let it be SONAME)
rm -f $RPM_BUILD_ROOT%{_libdir}/lib{odbc{mini,my,psql,drvcfg{1,2},nn,txt},oraodbc,esoob,oplodbc,sapdb,tds}S.{so,la,a}
# Drivers are lt_dlopened by given name (let it be SONAME)
rm -f $RPM_BUILD_ROOT%{_libdir}/lib{odbcpsql,nn,template,odbctxt}.{so,la,a}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
# install text driver
/usr/bin/odbcinst -i -d -r <<EOF
[TXT]
Description = Text file driver
Driver = %{_libdir}/libodbctxt.so.1
Setup = %{_libdir}/libodbctxtS.so.1
EOF
# install postgresql driver
/usr/bin/odbcinst -i -d -r <<EOF
[PostgreSQL]
Description = PostgreSQL driver
Driver = %{_libdir}/libodbpsql.so.1
Setup = %{_libdir}/libodbpsqlS.so.1
EOF

%postun -p /sbin/ldconfig

%post	gnome -p /sbin/ldconfig
%postun	gnome -p /sbin/ldconfig

%post	qt -p /sbin/ldconfig
%postun	qt -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS doc/AdministratorManual doc/UserManual
%attr(755,root,root) %{_bindir}/dltest
%attr(755,root,root) %{_bindir}/isql
%attr(755,root,root) %{_bindir}/iusql
%attr(755,root,root) %{_bindir}/odbcinst
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%{!?_without_gnome:%exclude %{_libdir}/libgtkodbcconfig.*}
%{!?_without_qt:%exclude %{_libdir}/libodbcinstQ.*}
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/odbc*.ini

%files devel
%defattr(644,root,root,755)
%doc ChangeLog doc/ProgrammerManual
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{!?_without_gnome:%exclude %{_libdir}/libgtkodbcconfig.*}
%{!?_without_qt:%exclude %{_libdir}/libodbcinstQ.*}
%{_includedir}/*.h
%{!?_without_gnome:%exclude %{_includedir}/odbcconfig.h}

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%{!?_without_gnome:%exclude %{_libdir}/libgtkodbcconfig.*}
%{!?_without_qt:%exclude %{_libdir}/libodbcinstQ.*}

%if 0%{!?_without_gnome:1}
%files gnome
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gODBCConfig
%attr(755,root,root) %{_libdir}/libgtkodbcconfig.so.*.*.*
%{_pixmapsdir}/gODBCConfig

%files gnome-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgtkodbcconfig.so
%{_libdir}/libgtkodbcconfig.la
%{_includedir}/odbcconfig.h

%files gnome-static
%defattr(644,root,root,755)
%{_libdir}/libgtkodbcconfig.a
%endif

%if 0%{!?_without_qt:1}
%files qt
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/DataManager
%attr(755,root,root) %{_bindir}/DataManagerII
%attr(755,root,root) %{_bindir}/ODBCConfig
%attr(755,root,root) %{_bindir}/odbctest
%attr(755,root,root) %{_libdir}/libodbcinstQ.so.*.*.*
%{_applnkdir}/System/*
%{_pixmapsdir}/*.png
%endif
