Summary:	Cross PPC GNU binary utility development utilities - gcc
Summary(es):	Utilitarios para desarrollo de binarios de la GNU - PPC gcc
Summary(fr):	Utilitaires de développement binaire de GNU - PPC gcc
Summary(pl):	Skro¶ne narzêdzia programistyczne GNU dla PPC - gcc
Summary(pt_BR):	Utilitários para desenvolvimento de binários da GNU - PPC gcc
Summary(tr):	GNU geliþtirme araçlarý - PPC gcc
Name:		crossppc-gcc
Version:	4.0.1
%define		_snap	20050507
Release:	0.%{_snap}.1
Epoch:		1
License:	GPL
Group:		Development/Languages
#Source0:	ftp://gcc.gnu.org/pub/gcc/releases/gcc-%{version}/gcc-%{version}.tar.bz2
Source0:	ftp://gcc.gnu.org/pub/gcc/snapshots/4.0-%{_snap}/gcc-4.0-%{_snap}.tar.bz2
# Source0-md5:	701f385de867d117f3648165174b254a
%define		_llh_ver	2.6.11.2
Source1:	http://ep09.pld-linux.org/~mmazur/linux-libc-headers/linux-libc-headers-%{_llh_ver}.tar.bz2
# Source1-md5:	2d21d8e7ff641da74272b114c786464e
%define		_glibc_ver	2.3.5
Source2:	ftp://sources.redhat.com/pub/glibc/releases/glibc-%{_glibc_ver}.tar.bz2
# Source2-md5:	93d9c51850e0513aa4846ac0ddcef639
Source3:	ftp://sources.redhat.com/pub/glibc/releases/glibc-linuxthreads-%{_glibc_ver}.tar.bz2
# Source3-md5:	77011b0898393c56b799bc011a0f37bf
Patch0:		%{name}-libc-sysdeps-configure.patch
URL:		http://gcc.gnu.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	crossppc-binutils
BuildRequires:	fileutils >= 4.0.41
BuildRequires:	flex
BuildRequires:	texinfo >= 4.1
Requires:	crossppc-binutils
Requires:	gcc-dirs
ExcludeArch:	ppc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		target		ppc-pld-linux
%define		arch		%{_prefix}/%{target}
%define		gccarch		%{_libdir}/gcc/%{target}
%define		gcclib		%{gccarch}/%{version}

%define		_noautostrip	.*/libgc.*\\.a

%description
This package contains a cross-gcc which allows the creation of
binaries to be run on PPC linux (architecture ppc-linux) on
other machines.

%description -l de
Dieses Paket enthält einen Cross-gcc, der es erlaubt, auf einem
anderem Rechner Code für ppc-Linux zu generieren.

%description -l pl
Ten pakiet zawiera skro¶ny gcc pozwalaj±cy na robienie na innych
maszynach binariów do uruchamiania na PPC (architektura "ppc-linux").

%package c++
Summary:	C++ support for crossppc-gcc
Summary(pl):	Obs³uga C++ dla crossppc-gcc
Group:		Development/Languages
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description c++
This package adds C++ support to the GNU Compiler Collection for PPC.

%description c++ -l pl
Ten pakiet dodaje obs³ugê C++ do kompilatora gcc dla PPC.

%prep
#setup -q -n gcc-%{version} -a1 -a2 -a3
%setup -q -n gcc-4.0-%{_snap} -a1 -a2 -a3
mv linuxthreads* glibc-%{_glibc_ver}
%patch0 -p1

%build
FAKE_ROOT=$PWD/fake-root

rm -rf $FAKE_ROOT && install -d $FAKE_ROOT/usr/include
cp -r linux-libc-headers-%{_llh_ver}/include/{asm-ppc,linux} $FAKE_ROOT/usr/include
ln -s asm-ppc $FAKE_ROOT/usr/include/asm

cd glibc-%{_glibc_ver}
cp -f /usr/share/automake/config.* scripts
rm -rf builddir && install -d builddir && cd builddir
../configure \
	--prefix=$FAKE_ROOT/usr \
	--build=%{_target_platform} \
	--host=%{target} \
	--disable-nls \
	--enable-add-ons=linuxthreads \
	--with-headers=$FAKE_ROOT/usr/include \
	--disable-sanity-checks \
	--enable-hacker-mode

%{__make} sysdeps/gnu/errlist.c
%{__make} install-headers

install bits/stdio_lim.h $FAKE_ROOT/usr/include/bits
touch $FAKE_ROOT/usr/include/gnu/stubs.h
cd ../..

cp -f /usr/share/automake/config.* .
rm -rf obj-%{target}
install -d obj-%{target}
cd obj-%{target}

CFLAGS="%{rpmcflags}" \
CXXFLAGS="%{rpmcflags}" \
TEXCONFIG=false \
../configure \
	--prefix=%{_prefix} \
	--infodir=%{_infodir} \
	--mandir=%{_mandir} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libdir} \
	--disable-shared \
	--disable-threads \
	--enable-languages="c,c++" \
	--enable-c99 \
	--enable-long-long \
	--disable-nls \
	--with-gnu-as \
	--with-gnu-ld \
	--with-demangler-in-ld \
	--with-system-zlib \
	--disable-multilib \
	--with-sysroot=$FAKE_ROOT \
	--without-x \
	--target=%{target} \
	--host=%{_target_platform} \
	--build=%{_target_platform}

%{__make} all-gcc

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C obj-%{target} install-gcc \
	DESTDIR=$RPM_BUILD_ROOT

install obj-%{target}/gcc/specs $RPM_BUILD_ROOT%{gcclib}

# don't want this here
rm -f $RPM_BUILD_ROOT%{_libdir}/libiberty.a

# include/ contains install-tools/include/* and headers that were fixed up
# by fixincludes, we don't want former
gccdir=$RPM_BUILD_ROOT%{gcclib}
mkdir	$gccdir/tmp
# we have to save these however
mv -f	$gccdir/include/syslimits.h $gccdir/tmp
rm -rf	$gccdir/include
mv -f	$gccdir/tmp $gccdir/include
cp -f	$gccdir/install-tools/include/*.h $gccdir/include
# but we don't want anything more from install-tools
rm -rf	$gccdir/install-tools

%if 0%{!?debug:1}
%{target}-strip -g -R.note -R.comment $RPM_BUILD_ROOT%{gcclib}/libgcc.a
%{target}-strip -g -R.note -R.comment $RPM_BUILD_ROOT%{gcclib}/libgcov.a
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{target}-gcc
%attr(755,root,root) %{_bindir}/%{target}-cpp
%dir %{gccarch}
%dir %{gcclib}
%attr(755,root,root) %{gcclib}/cc1
%attr(755,root,root) %{gcclib}/collect2
%{gcclib}/*crt*.o
%{gcclib}/libgcc.a
%{gcclib}/specs*
%dir %{gcclib}/include
%{gcclib}/include/*.h
%{_mandir}/man1/%{target}-cpp.1*
%{_mandir}/man1/%{target}-gcc.1*

%files c++
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{target}-g++
%attr(755,root,root) %{gcclib}/cc1plus
%{_mandir}/man1/%{target}-g++.1*
