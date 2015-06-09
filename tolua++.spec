Summary:	Extended version of tolua, a tool to integrate C/C++ code with Lua
Summary(pl.UTF-8):	Rozszerzona wersja tolua, narzędzia integrującego kod C/C++ z Lua
Name:		tolua++
Version:	1.0.93
Release:	6
License:	MIT
Group:		Development/Tools
Source0:	http://www.codenix.com/~tolua/%{name}-%{version}.tar.bz2
# Source0-md5:	100aa6907b8108582080b37d79c0afd7
Patch0:		%{name}-lua51.patch
URL:		http://www.codenix.com/~tolua/
BuildRequires:	lua51-devel
BuildRequires:	scons
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
tolua++ is an extension of tolua, a tool to integrate C/C++ code with
Lua. tolua++ includes new features oriented to c++, such as class
templates.

tolua is a tool that greatly simplifies the integration of C/C++ code
with Lua. Based on a "cleaned" header file, tolua automatically
generates the binding code to access C/C++ features from Lua.

%description -l pl.UTF-8
tolua++ jest rozszerzeniem tolua, narzędzia integrującego kod C/C++ z
Lua. tolua++ zawiera nowe, zorientowane na c++ cechy takie jak wzorce
klas.

tolua jest narzędziem które znacznie upraszcza integracje kodu C/C++ z
Lua. Bazując na "oczyszczonych" plikach nagłówkowych tolua
automatycznie generuje kod umożliwiający Lua dostęp do struktur i
funkcji C/C++.

%package libs
Summary:	tolua++ shared library
Summary(pl.UTF-8):	Biblioteka współdzielona tolua++
Group:		Libraries
Conflicts:	tolua++-devel < 1.0.93-5

%description libs
tolua++ shared library.

%description libs -l pl.UTF-8
Biblioteka współdzielona tolua++.

%package devel
Summary:	tolua++ header files
Summary(pl.UTF-8):	Pliki nagłówkowe tolua++
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for tolua++.

%description devel -l pl.UTF-8
Pliki nagłówkowe tolua++.

%package static
Summary:	tolua++ static library
Summary(pl.UTF-8):	Biblioteka statyczna tolua++
Group:		Development/Tools
Requires:	%{name}-devel = %{version}-%{release}

%description static
tolua++ static library.

%description static -l pl.UTF-8
Biblioteka statyczna tolua++.

%prep
%setup -q
%patch0 -p1

%build
%scons \
	CCFLAGS="%{rpmcflags} -I/usr/include/lua51 -ansi -fPIC" \
	LINKFLAGS="%{rpmldflags}"

%{__cc} %{rpmldflags} -shared src/lib/tolua_{event,is,map,push,to}.o -o lib/libtolua++.so -llua51 -ldl -lm
%{__cc} %{rpmldflags} -Llib src/bin/toluabind.o src/bin/tolua.o -o bin/tolua++ -ltolua++ -llua51

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_includedir},%{_libdir}}

install bin/tolua++ $RPM_BUILD_ROOT%{_bindir}
install include/tolua++.h $RPM_BUILD_ROOT%{_includedir}
install lib/lib* $RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/tolua++

%files libs
%defattr(644,root,root,755)
%doc COPYRIGHT README README-5.1 doc/*
%attr(755,root,root) %{_libdir}/libtolua++.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/tolua++.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libtolua++.a
%{_libdir}/libtolua++_static.a
