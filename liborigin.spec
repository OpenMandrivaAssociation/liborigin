%define	major	1
%define	libname		%mklibname origin %major
%define develname	%mklibname origin -d

Name:		liborigin
Version:	20090326
Release:	%mkrel 3
Summary:	Library for reading OriginLab OPJ project files
License:	GPLv2+
Group:		System/Libraries
URL:		http://sourceforge.net/projects/%{name}/
Source:		http://belnet.dl.sourceforge.net/sourceforge/liborigin/%{name}2-%{version}.tar.gz
Patch0:		liborigin2-20090326-boost-1.33.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}
BuildRequires:	qt4-devel
BuildRequires:	boost-devel
Requires:	%{libname} = %{version}


%description
A library for reading OriginLab OPJ project files.

%package -n	%{libname}
Summary:	Dynamic libraries from %{name}
Group:		System/Libraries
Provides: 	%{name} = %{version}-%{release}
Obsoletes:	liborigin

%description -n	%{libname}
Dynamic libraries from %{name}.

%package -n	%{develname}
Summary: 	Header files, libraries and development documentation for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	origin-devel = %{version}-%{release}

%description -n	%{develname}
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%setup -q -n %{name}2-%{version}
%patch0 -p0

%build
%qmake_qt4
%make

%install
rm -rf %{buildroot}

#install headers, *.hpp is not needed (or is it ??)
mkdir -p %{buildroot}%{_includedir}/%{name}
rm -f *.hpp
for n in *.h* ; do
    install -m 644 $n %{buildroot}%{_includedir}/%{name}
done

# install libs, preserving links
mkdir -p %{buildroot}%{_libdir}
chmod 644 liborigin2.so*
for n in liborigin2.so* ; do
    cp -d $n %{buildroot}%{_libdir}
done

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root,-)
%doc COPYING README FORMAT
%{_includedir}/%{name}/*.h
%{_includedir}/%{name}/*.hh
%{_libdir}/%{name}2.so

