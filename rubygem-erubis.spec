%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

# Generated from erubis-2.6.5.gem by gem2rpm -*- rpm-spec -*-
%global gem_name erubis


Summary: A fast and extensible eRuby implementation
Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 2.7.0
Release: 15%{?dist}
Group: Development/Languages
License: MIT
URL: http://www.kuwata-lab.com/erubis/
Source0: http://gems.rubyforge.org/gems/%{gem_name}-%{version}.gem
# needed for tests, to get it, run
# git clone https://github.com/kwatch/erubis && cd erubis
# git checkout 14d3eab57f && tar czvf erubis-2.7.0-public_html.tgz public_html
Source1: %{gem_name}-%{version}-public_html.tgz
# Fixes issues with test suite using Psych.
# https://github.com/kwatch/erubis/pull/2
Patch0: rubygem-erubis-2.7.0-ruby-2.0-compatibility.patch
# https://github.com/kwatch/erubis/pull/5
Patch1: rubygem-erubis-2.7-Add-support-for-Ruby-2.1.patch
Patch2: rubygem-erubis-2.7.0-Add-support-for-Ruby-2.2.patch

Requires: %{?scl_prefix_ruby}ruby(rubygems)
Requires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}rubygem(test-unit)
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}

%description
Erubis is a very fast, secure, and extensible implementation of eRuby.

%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
# contrib/erubis-run.rb is BSD
License: MIT and BSD
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}

%description doc
This package contains documentation for %{pkg_name}.

%prep
mkdir -p .%{_bindir}
%{?scl:scl enable %{scl} - << \EOF}
%gem_install -n %{SOURCE0}
%{?scl:EOF}

pushd .%{gem_instdir}
%patch0 -p1
%patch1 -p1
%patch2 -p1
popd

%build

%install
mkdir -p %{buildroot}%{gem_dir}
mkdir -p %{buildroot}%{_bindir}

cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}/
cp -a .%{_bindir}/* %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

%{?scl:scl enable %{scl} - << \EOF}
find %{buildroot}%{gem_instdir}/ -type f | \
  xargs -n 1 sed -i -e "s|^#\!/usr/bin/env ruby|#\!`which ruby`|"
%{?scl:EOF}

%check
%{?scl:scl enable %{scl} - << \EOF}
set -e
export GEM_PATH=%{buildroot}%{gem_dir}:%{gem_dir}:$GEM_PATH
export PATH=%{buildroot}%{_bindir}:$PATH

pushd .%{gem_instdir}
tar xzf %{SOURCE1}

# Wrong filename - reported upstream via
# http://rubyforge.org/tracker/?func=detail&aid=27330&group_id=1320&atid=5201
mv test/data/users-guide/{E,e}xample.ejava

# test_untabify2(MainTest) test fails. It is not obvious how to make it run
# with Psych, since Psych by design denies tabified YAML, where it was
# acceptable for Syck (if I am not mistaken).
# TODO: This could be ignored by --ignore-name= param if only it worked.
# https://github.com/test-unit/test-unit/issues/92
sed -i '/^  def test_untabify2/,/^  end$/ s/^/#/' test/test-main.rb

ruby -I.:lib -e "Dir.glob('./test/test-*.rb').each {|t| require t}" \
 | grep '158 tests, 234 assertions, 3 failures, 0 errors, 0 pendings, 0 omissions'
popd
%{?scl:EOF}

%files
%{_bindir}/erubis
%doc %{gem_instdir}/CHANGES.txt
%doc %{gem_instdir}/MIT-LICENSE
%doc %{gem_instdir}/README.txt
%dir %{gem_instdir}

# We install via gem
%exclude %{gem_instdir}/setup.rb
# Only needed for tests
%exclude %{gem_instdir}/public_html

%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%{gem_instdir}/benchmark
%{gem_instdir}/test
%{gem_instdir}/examples
%{gem_instdir}/contrib

# Prefer generated rdoc
%exclude %{gem_instdir}/doc-api

%{gem_instdir}/doc
%{gem_docdir}

%changelog
* Thu Apr 07 2016 Pavel Valena <pvalena@redhat.com> - 2.7.0-15
- Fix changelog entry

* Wed Apr 06 2016 Pavel Valena <pvalena@redhat.com> - 2.7.0-14
- Make test failure fail the build
- Allow 3 failing tests

* Wed Mar 02 2016 Pavel Valena <pvalena@redhat.com> - 2.7.0-13
- Fix shebang path replacement

* Tue Feb 23 2016 Pavel Valena <pvalena@redhat.com> - 2.7.0-12
- Enable tests

* Mon Feb 22 2016 Pavel Valena <pvalena@redhat.com> - 2.7.0-11
- Rebuilt for rh-ror42

* Thu Jan 15 2015 Josef Stribny <jstribny@redhat.com> - 2.7.0-8
- rebuilt for ror41

* Fri Mar 21 2014 Vít Ondruch <vondruch@redhat.com> - 2.7.0-7
- Rebuid against new scl-utils to depend on -runtime package.
  Resolves: rhbz#1069109

* Mon Feb 03 2014 Josef Stribny <jstribny@redhat.com> - 2.7.0-6
- Fix license in -doc subpackage

* Thu Jun 13 2013 Josef Stribny <jstribny@redhat.com> - 2.7.0-5
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Wed Jul 25 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 2.7.0-4
- Exclude cached gem, not libdir.

* Wed Jul 25 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 2.7.0-3
- Specfile cleanup

* Thu May 31 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 2.7.0-2
- Removed uneeded patch from specfile.

* Mon Apr 02 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 2.7.0-1
- Rebuilt for scl.
- Updated to 2.7.0.

* Tue Jan 31 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 2.6.6-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 14 2011 Vít Ondruch <vondruch@redhat.com> - 2.6.6-1
- Updated to the latest upstream (#670589).
- Removed flawed require check.
- Removed obsolete BuildRoot.
- Removed obsolete cleanup.
- Package setup and test execution reworked.
- Removed bindir magick.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Oct 29 2009 Matthew Kent <mkent@magoazul.com> - 2.6.5-2
- Move file rename to build stage (#530275).
- Simplify %%check stage (#530275).
- Remove disable of test_syntax2, fixed by new ruby build (#530275).

* Mon Oct 19 2009 Matthew Kent <mkent@magoazul.com> - 2.6.5-1
- Initial package
