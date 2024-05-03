Name:           sysmotd
Version:        0.0.7
Release:        1%{?dist}
Summary:        Generates a MOTD (Message Of The Day) including system information on Fedora Linux
BuildArch:      noarch

License:        GPLv3+
URL:            https://github.com/innovara/sysmotd
Source0:        %{name}-%{version}.tar.gz

Requires:       bash
Requires:       coreutils
Requires:       dnf
Requires:       figlet
Requires:       findutils
Requires:       gawk
Requires:       lolcat
Requires:       procps-ng
Requires:       systemd

%description
Sysmotd produces a MOTD that includes system information being collected
on a regular basis. Users will see the MOTD when logging in via ssh.


%prep
%autosetup


%build


%install

mkdir -p %{buildroot}/%{_libexecdir}
%{__install} -Dm744 %{name} %{buildroot}/%{_libexecdir}/%{name}

mkdir -p %{buildroot}/%{_unitdir}
%{__install} -Dm644 %{name}.service %{buildroot}/%{_unitdir}/%{name}.service
%{__install} -Dm644 %{name}.timer %{buildroot}/%{_unitdir}/%{name}.timer

%{__install} -Dm644 %{name}.preset %{buildroot}/%{_presetdir}/50-%{name}.preset


%files
%license LICENSE.txt
%doc README.txt
%{_libexecdir}/%{name}
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}.timer
%{_presetdir}/50-%{name}.preset


%post
%systemd_post %{name}.timer
systemctl start %{name}.timer > /dev/null 2>&1


%preun
%systemd_preun %{name}.timer
%systemd_preun %{name}.service


%postun
%systemd_postun %{name}.timer
%systemd_postun %{name}.service
rm -f /run/motd.d/*%{name}*


%changelog
* Fri May 3 2024 Manuel Fombuena <mfombuena@innovara.co.uk>
- Version 0.0.7-1: removed Requires=sysmotd.service on sysmotd.timer

* Tue Apr 30 2024 Manuel Fombuena <mfombuena@innovara.co.uk>
- Version 0.0.6-1: LogLevelMax=3 added to sysmotd.service

* Mon Apr 29 2024 Manuel Fombuena <mfombuena@innovara.co.uk>
- Version 0.0.5-1: changed sysmotd.timer starting point to OnActiveSec 
- Version 0.0.5-1: added %systemd_postun macro when uninstalling

* Mon Oct 2 2023 Manuel Fombuena <mfombuena@innovara.co.uk>
- Version 0.0.4-1: mem_perc re-added

* Sun Oct 1 2023 Manuel Fombuena <mfombuena@innovara.co.uk>
- Version 0.0.3-1: system information layout changed to a table to prevent misalignment of items

* Thu Apr 27 2023 Manuel Fombuena <mfombuena@innovara.co.uk>
- Version 0.0.2-1: SElinux info added

* Mon Dec 26 2022 Manuel Fombuena <mfombuena@innovara.co.uk>
- Version 0.0.1-1: first version packaged
