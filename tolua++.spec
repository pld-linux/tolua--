Summary:	Extended version of tolua, a tool to integrate C/C++ code with Lua
Summary(pl.UTF-8):	Rozszerzona wersja tolua, narzędzia integrującego kod C/C++ z Lua
Name:		tolua++
Version:	1.0.4
Release:	1
License:	Free
Group:		Development/Tools
Source0:	http://www.codenix.com/~tolua/%{name}-%{version}.tar.bz2
# Source0-md5:	8785100f7c9d9253cb47b530d97a32f6
URL:		http://www.codenix.com/~tolua/
BuildRequires:	lua50-devel >= 5.0.2-2
BuildRequires:	scons
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
tolua++ is an extension of tolua, a tool to integrate C/C++ code with
Lua. tolua++ includes new features oriented to c++, such as class
templates.

tolua is a tool that greatly simplifies the integration of C/C++ code
with Lua. Based on a "cleaned" header file, tolua automatically
generates the binding code to access C/C++ features from Lua. Using
Lua-5.0 API and tag method facilities, the current version
automatically maps C/C++ constants, external variables, functions,
namespace, classes, and methods to Lua. It also provides facilities to
create Lua modules.

%description -l pl.UTF-8
tolua++ jest rozszerzeniem tolua, narzędzia integrującego kod C/C++ z
Lua. tolua++ zawiera nowe, zorientowane na c++ cechy takie jak wzorce
klas.

tolua jest narzędziem które znacznie upraszcza integracje kodu C/C++ z
Lua. Bazując na "oczyszczonych" plikach nagłówkowych tolua
automatycznie generuje kod umożliwiający Lua dostęp do struktur i
funkcji C/C++. Dzięki użyciu API Lua 5.0, bieżąca wersja automatycznie
mapuje stałe, zewnętrzne zmienne, funkcje, przestrzenie nazw, klasy i
metody z C/C++ do Lua. Umożliwia również tworzenie modułów Lua.

%package libs
Summary:	tolua++ dynamic library
Summary(pl.UTF-8):	Biblioteka dynamiczna tolua++
Group:		Development/Tools

%description libs
tolua++ dynamic library.

%description libs -l pl.UTF-8
Biblioteka dynamiczna tolua++.

%package static
Summary:	tolua++ static library
Summary(pl.UTF-8):	Biblioteka statyczna tolua++
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}

%description static
tolua++ static library.

%description static -l pl.UTF-8
Biblioteka statyczna tolua++.

%prep
%setup -q

%build
scons \
	CC="%{__cc}" \
	LUA="%{_prefix}" \
	CCFLAGS="%{rpmcflags} -fPIC -I/usr/include/lua50"

%{__cc} src/lib/tolua_{event,is,map,push,to}.o -shared -llua50 -llualib50 -ldl -lm -o lib/libtolua++.so
%{__cc} -o bin/tolua++ src/bin/toluabind.o src/bin/tolua.o -Llib -ltolua++

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_includedir},%{_libdir}}

install bin/tolua++ $RPM_BUILD_ROOT%{_bindir}
install include/tolua++.h $RPM_BUILD_ROOT%{_includedir}
install lib/lib* $RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README doc/*
%attr(755,root,root) %{_bindir}/*
%{_includedir}/*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
