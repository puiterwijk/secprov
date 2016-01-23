Name:           secprov
Version:        1.0.0
Release:        1%{?dist}
Summary:        Secure System Provisioning

License:        BSD
URL:            https://github.com/puiterwijk/secprov
# Generated with: git archive --format=tgz -o secprov.tar.gz --prefix="secprov/" HEAD
Source0:        secprov.tar.gz
BuildArch:      noarch

Requires:       trousers

%description
A tool to enable unattended, secure system provisioning with prior preparation.

%prep
%setup -q -n secprov

%build
%install
mkdir -p %{buildroot}%{_bindir}
install secprov %{buildroot}%{_bindir}/
install secprov-prepare %{buildroot}%{_bindir}/

%files
%doc README.md
%{_bindir}/secprov
%{_bindir}/secprov-prepare


%changelog
* Sat Jan 23 2016 Patrick Uiterwijk <puiterwijk@redhat.com>
- Initial packaging
