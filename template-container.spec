# Template for a repo that ships a container, for the gemini-rtsw-ci pipeline.
# The RPM installs a systemd unit; the unit pulls and runs the image.
# To reuse: rename this file, change Name, set Version, and set appimage to
# ghcr.io/gemini-rtsw/<your repo name>.

# $GIT_HASH is passed in by build_rpm.sh; git is only the fallback.
%define git_hash %(if [ -n "$GIT_HASH" ]; then echo "$GIT_HASH"; else git rev-parse --short HEAD 2>/dev/null || echo nogit; fi)
%global appimage ghcr.io/gemini-rtsw/template-container

Name:      template-container
Version:   0.1.0
Release:   1.git%{git_hash}%{?dist}
Summary:   Template container service for the gemini-rtsw-ci pipeline
License:   Proprietary
Source0:   %{name}-%{version}.tar.gz
BuildArch: noarch
BuildRequires: systemd-rpm-macros
Requires:  systemd

%description
Runs the template-container image as a systemd service.

%prep
%autosetup

%build
# Pin the unit to the exact image built alongside this RPM.
sed -e 's|@IMAGE@|%{appimage}:%{version}-git%{git_hash}|' deploy/%{name}.service.in > %{name}.service
if grep -q '@IMAGE@' %{name}.service; then echo "ERROR: placeholder not substituted" >&2; exit 1; fi

%install
install -Dpm 0644 %{name}.service %{buildroot}%{_unitdir}/%{name}.service
install -Dpm 0644 deploy/%{name}.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/%{name}

%post
%systemd_post %{name}.service
%preun
%systemd_preun %{name}.service
%postun
%systemd_postun %{name}.service

%files
# Not a config file: the unit carries the image tag, so upgrades must overwrite it.
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}

%changelog
* Wed Sep 30 2026 Hawi Stecher <hawi.stecher@noirlab.edu> - 0.1.0-1
- Initial template.
