%define	major	0
%define	libname		%mklibname origin %major
%define develname	%mklibname origin -d

Name:		liborigin
Version:	20080225
Release:	%mkrel 1
Summary:	Library for reading OriginLab OPJ project files
License:	GPLv2+
Group:		System/Libraries
URL:		http://sourceforge.net/projects/%{name}/
Source:		http://belnet.dl.sourceforge.net/sourceforge/liborigin/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}
BuildRequires:	cmake
Requires:	%{libname} = %{version}


%description
A library for reading OriginLab OPJ project files.

%package -n	%{libname}
Summary:	Dynamic libraries from %{name}
Group:		System/Libraries
Provides: 	%{name} = %{version}-%{release}

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
%setup -q

%build

# fix for hardcoded path of %{_libdir}
%ifarch x86_64 sparc64 ppc64 amd64
%{__sed} -i "s|install(TARGETS origin DESTINATION lib)|install(TARGETS origin DESTINATION lib64)|" CMakeLists.txt
%endif

%cmake
%make

%install
rm -rf %{buildroot}
cd build
%makeinstall_std
cd -
find . -type d | sed '1,2d;s,^\.,\%attr(755\,root\,root) \%dir ,' > $RPM_BUILD_DIR/file.list.%{name}
find . -type f -o -type l | sed 's,^\.,\%attr(-\,root\,root) ,' >> $RPM_BUILD_DIR/file.list.%{name}

install -d  %{buildroot}%{_includedir}/%{name}/
install -pm 644 OPJFile.h tree.hh %{buildroot}%{_includedir}/%{name}/

#W: spurious-executable-perm 
chmod 0644 ws4.opj

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING README ws4.opj import.qs
%{_bindir}/opj2dat

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.%{major}
%{_libdir}/*.so.%{major}.*

%files -n %{develname}
%defattr(-,root,root,-)
%{_includedir}/%{name}/
%{_libdir}/%{name}.so

