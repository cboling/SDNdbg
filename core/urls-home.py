"""
Copyright (c) 2015 - 2016.  Boling Consulting Solutions, BCSW.net

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

urlpatterns = [

    # Example: /
    # url(r'^$', Login.as_view(), name='Login'),
    # url(r'^$', permission_required('core.')(Login.as_view())),

    # url(r'login/$', login, name='login',
    #     kwargs={'template_name': 'core/login.html'}),
    #
    # url(r'logout/$', logout, name='logout',
    #     kwargs={'next_page': '/'}),
    #
    # url(r'^password_change$', password_change,
    #     name='password_change', kwargs={
    #         'template_name': 'accounts/password_change_form.html',
    #         'post_change_redirect':'accounts:password_change_done',
    #     }
    #     ),
    # url(r'^password_change_done$', password_change_done,
    #     name='password_change_done', kwargs={
    #         'template_name': 'accounts/password_change_done.html'
    #     }
    #     ),
]
