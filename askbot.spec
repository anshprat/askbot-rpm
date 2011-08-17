Name:           askbot
Version:        0.7.19
Release:        1%{?dist}
Summary:        Question and Answer forum
Group:          Development/Languages
License:        GPLv3+
URL:            http://askbot.org
Source0:        http://pypi.python.org/packages/source/a/%{name}/%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python-setuptools python-devel gettext

Requires:       Django Django-south  
Requires:       django-keyedcache django-robots django-countries 
Requires:       django-kombu django-threaded-multihost 
Requires:       python-html5lib python-oauth2 python-coffin python-markdown2  
Requires:       python-recaptcha-client MySQL-python python-openid python-amqplib
Requires:       python-unidecode python-httplib2 python-dateutil python-psycopg2
Requires:       django-recaptcha-works django-picklefield
# optional dependencies 
Requires:       django-followit django-avatar
# for building the doc
Requires:       python-sphinx
Requires:       django-celery = 2.2.7

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

# remove empty files
rm -rf %{name}/doc/build/html/.buildinfo

# remove shebang
sed -i -e '1d' %{name}/setup_templates/manage.py

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Language files; not under /usr/share, need to be handled manually
(cd %{buildroot} && find . -name 'django.?o' && find . -name 'djangojs.?o') | sed -e 's|^.||' | sed -e \
  's:\(.*/locale/\)\([^/_]\+\)\(.*\.mo$\):%lang(\2) \1\2\3:' \
  >> %{name}.lang


%files -f %{name}.lang 
%doc PKG-INFO LICENSE COPYING AUTHORS README.rst
%{_bindir}/askbot-setup
%dir %{python_sitelib}/%{name}/
%dir %{python_sitelib}/%{name}/locale/
%{python_sitelib}/%{name}/doc
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
* Thu Aug 17 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.19-1
- new upstream bug fix release
  * fixes google plus and facebook login to work again
  * some styling improvements for questions sidebar
  * fixes moderation tab misalignment issue reported by me
  * replaces favorite by follow in questions
  * fixes follow user functions

* Thu Aug 11 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.18-1
- new upstream bugfix release includes improved notifications

* Thu Aug 11 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.17-1
- new upstream release
  * fixes issue with referencing username with capitalization differences
  * allow admins to add others as admins 
- requires django-celery 2.2.7

* Thu Aug 07 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.15-1
- new upstream release
- change upstream url
- add the new readme file to doc
- upstream dropped empty version.py file

* Thu Aug 03 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.7.14-1
- new upstream release.  
- upstream has renamed startforum to askbot-setup
- included copy of license and some documentation fixes
- upstream removed empty files, unnecessary executable bit and shebang in files
- drop requires on django-recaptcha since askbot uses django-recaptcha-works now

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

