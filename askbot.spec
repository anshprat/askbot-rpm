Name:           askbot
Version:        0.7.12
Release:        1%{?dist}
Summary:        Question and Answer forum
Group:          Development/Languages
License:        GPLv3+
URL:            http://pypi.python.org/pypi/%{name}
Source0:        http://pypi.python.org/packages/source/a/%{name}/%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python-setuptools python-devel gettext

Requires:       Django Django-south  
Requires:       django-keyedcache django-robots django-countries django-celery
Requires:       django-kombu django-recaptcha django-threaded-multihost 
Requires:       python-html5lib python-oauth2 python-coffin python-markdown2  
Requires:       python-recaptcha-client MySQL-python python-openid python-amqplib
Requires:       python-unidecode python-httplib2 python-dateutil python-psycopg2
Requires:       django-recaptcha-works django-picklefield
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

# move license file to base
mv %{name}/LICENSE .

# remove outdated bundled docs
rm -rf %{name}/doc
rm -rf %{name}/docs

# remove empty files
rm -rf %{name}/skins/default/media/images/flags/.DS_Store
rm -rf %{name}/deps/livesettings/locale/es/LC_MESSAGES/django.po
rm -rf %{name}/setup_templates/log/askbot.log
rm -rf %{name}/version.py

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
chmod -x %{name}/bin/rmpyc

# remove shebang
sed -i -e '1d' %{name}/utils/diff.py
sed -i -e '1d' %{name}/setup_templates/manage.py
sed -i -e '1d' %{name}/bin/show_profile_stats.py
sed -i -e '1d' %{name}/bin/generate_modules.py
sed -i -e '1d' %{name}/cron/askbot_cron_job

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Language files; not under /usr/share, need to be handled manually
(cd %{buildroot} && find . -name 'django.?o' && find . -name 'djangojs.?o') | sed -e 's|^.||' | sed -e \
  's:\(.*/locale/\)\([^/_]\+\)\(.*\.mo$\):%lang(\2) \1\2\3:' \
  >> %{name}.lang


%files -f %{name}.lang 
%doc PKG-INFO LICENSE
%{_bindir}/startforum
%dir %{python_sitelib}/%{name}/
%dir %{python_sitelib}/%{name}/locale/
%{python_sitelib}/%{name}/*.py*
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
* Wed Aug 03 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.12-1
- new upstream release
- another fix for a unicode issue
- consolidate removal of empty files, executable bits and shebang in prep
- remove outdated bundled documentation

* Wed Aug 03 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.11-1
- new upstream release
- fixes a couple of minor bugs reported by me

* Mon Aug 01 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.10-1
- new upstream release
- fixes live search in response to problem reported by me
- now using django-recaptcha-works module

* Sun Jul 31 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.9-1
- new upstream release
- resolves bug in the sharing footer of answerless question reported by me

* Sun Jul 31 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.8-1
- new upstream release
- use django_openid_forms.patch from PJP
- add requires on django-picklefield and python-amqplib
- remove requires on python-grapefruit.  Module removed upstream
- drop all patches.  upstream removed bundled copy of python-openid

* Wed Jul 18 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.7-3
- add requires on MySQL-python. Don't remove openid

* Mon Jul 18 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.7-2
- changes from Praveen Kumar to fix all relevant rpmlint warnings and errors

* Thu Jul 14 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.7-1
- new upstream release.  
- split out bundled grapefruit, django recaptcha dependencies

* Sun Jun 26 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.1-1
- new upstream release

* Mon Apr 25 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.6.78-1
- new upstream release

* Thu Apr 18 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.6.76-1
- initial spec

