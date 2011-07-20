Name:           askbot
Version:        0.7.7
Release:        2%{?dist}
Summary:        Question and Answer forum
Group:          Development/Languages
License:        GPLv3+
URL:            http://pypi.python.org/pypi/%{name}
Source0:        http://pypi.python.org/packages/source/a/%{name}/%{name}-%{version}.tar.gz
Patch0:         use_system_modules.patch
BuildArch:      noarch
BuildRequires:  python-setuptools python-devel gettext
Requires:       Django Django-south 
Requires:       django-keyedcache django-robots django-countries django-celery
Requires:       django-kombu django-recaptcha django-threaded-multihost 
Requires:       python-html5lib python-oauth2 python-coffin python-markdown2  
Requires:       python-recaptcha-client python-grapefruit
Requires:       python-unidecode python-httplib2 python-dateutil python-psycopg2
# optional dependencies
Requires:       django-followit django-avatar

%description
Question and Answer forum written in python and Django. It is similar to 
Stack Overflow or Yahoo Answers. 

Features:

   * standard Q&A functionality including votes, reputation system, etc.
   * user levels: admin, moderator, regular, suspended, blocked
   * per-user in-box for responses & flagged items (for moderators)
   * email alerts - instant and delayed, optionally tag filtered
   * search by full text and a set of tags simultaneously
   * can import data from stack-exchange database file

%prep
%setup -q 
%patch0 -p1

# remove unneeded doc
rm -rf askbot/doc/askbot-docs.zip

# remove bundled deps
rm -rf %{name}/deps/grapefruit.py
rm -rf %{name}/deps/recaptcha_django
rm -rf %{name}/deps/openid

# remove empty files
rm -rf %{name}/doc/build/html/.buildinfo
rm -rf %{name}/skins/default/media/images/flags/.DS_Store

# fix permission issues
chmod -x %{name}/skins/README
chmod -x %{name}/setup_templates/upfiles/README
chmod -x %{name}/views/README
chmod -x %{name}/skins/default/media/js/wmd/*.js
chmod -x %{name}/skins/default/media/js/*.bat
chmod -x %{name}/skins/default/media/style/*.css
chmod -x %{name}/skins/default/media/jquery-openid/openid.css
chmod -x %{name}/skins/default/media/js/wmd/wmd-test.html
chmod -x %{name}/skins/default/media/jquery-openid/jquery.openid.js
chmod -x %{name}/skins/default/media/js/wmd/wmd.css

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Language files; not under /usr/share, need to be handled manually
(cd %{buildroot} && find . -name 'django.?o' && find . -name 'djangojs.?o') | sed -e 's|^.||' | sed -e \
  's:\(.*/locale/\)\([^/_]\+\)\(.*\.mo$\):%lang(\2) \1\2\3:' \
  >> %{name}.lang

# remove shebang 
sed -i -e '1d' %{buildroot}%{python_sitelib}/%{name}/utils/diff.py
sed -i -e '1d' %{buildroot}%{python_sitelib}/%{name}/setup_templates/manage.py
sed -i -e '1d' %{buildroot}%{python_sitelib}/%{name}/bin/show_profile_stats.py
sed -i -e '1d' %{buildroot}%{python_sitelib}/%{name}/bin/generate_modules.py 
sed -i -e '1d' %{buildroot}%{python_sitelib}/%{name}/cron/askbot_cron_job

# remove empty files
rm -rf %{buildroot}%{python_sitelib}/%{name}/version.*
rm -rf %{buildroot}%{python_sitelib}/%{name}/setup_templates/log/askbot.log
rm -rf %{buildroot}%{_defaultdocdir}/%{name}-%{version}/doc/build/html/.buildinfo

# fix permission issues
chmod -x %{buildroot}%{python_sitelib}/%{name}/skins/README
chmod -x %{buildroot}%{python_sitelib}/%{name}/setup_templates/upfiles/README
chmod -x %{buildroot}%{python_sitelib}/%{name}/views/README
chmod -x %{buildroot}%{python_sitelib}/%{name}/bin/rmpyc


%files -f %{name}.lang 
%doc askbot/doc/ askbot/docs/

%{_bindir}/startforum
%dir %{python_sitelib}/%{name}/
%dir %{python_sitelib}/%{name}/locale/
%{python_sitelib}/%{name}/*.py*
%{python_sitelib}/%{name}/LICENSE
%{python_sitelib}/%{name}/bin/
%{python_sitelib}/%{name}/conf/
%{python_sitelib}/%{name}/const/
%{python_sitelib}/%{name}/cron/
%{python_sitelib}/%{name}/deployment/
%{python_sitelib}/%{name}/skins/
%{python_sitelib}/%{name}/templatetags/
%{python_sitelib}/%{name}/tests/
%{python_sitelib}/%{name}/utils/
%{python_sitelib}/%{name}/views/
%{python_sitelib}/%{name}/setup_templates/
%{python_sitelib}/%{name}/doc/
%{python_sitelib}/%{name}/docs/
%{python_sitelib}/%{name}/migrations/
%{python_sitelib}/%{name}/models/
%{python_sitelib}/%{name}/management/
%dir %{python_sitelib}/%{name}/deps/
%{python_sitelib}/%{name}/deps/*.py*
%{python_sitelib}/%{name}/deps/README
%{python_sitelib}/%{name}/deps/django_authopenid/
%dir %{python_sitelib}/%{name}/deps/livesettings/
%dir %{python_sitelib}/%{name}/deps/livesettings/locale/
%{python_sitelib}/%{name}/deps/livesettings/*.py*
%{python_sitelib}/%{name}/deps/livesettings/README
%{python_sitelib}/%{name}/deps/livesettings/temp*
%{python_sitelib}/%{name}/importers/
%{python_sitelib}/%{name}/middleware/
%{python_sitelib}/%{name}/migrations_api/
%{python_sitelib}/%{name}/patches/
%{python_sitelib}/%{name}/search/
%{python_sitelib}/%{name}/user_messages/
%{python_sitelib}/%{name}/upfiles/
%{python_sitelib}/askbot*.egg-info

%changelog
* Mon Jul 18 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.7-2
- Changes from Praveen Kumar to fix all relevant rpmlint warnings and errors

* Thu Jul 14 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.7-1
- new upstream release.  
- split out bundled grapefruit, django recaptcha dependencies

* Sun Jun 26 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.1-1
- new upstream release

* Mon Apr 25 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.6.78-1
- new upstream release

* Thu Apr 18 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.6.76-1
- initial spec

