from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect


class NoNewUsersAccountAdapter(DefaultAccountAdapter):

    def is_open_for_signup(self, request):
        """
        Checks whether or not the site is open for signups.

        Next to simply returning True/False you can also intervene the
        regular flow by raising an ImmediateHttpResponse

        (Comment reproduced from the overridden method.)
        """
        return False

class CustomSocialAccountAdapter(DefaultAccountAdapter):

    def pre_social_login(self, request, sociallogin):
        u = sociallogin.user
        #print("User:",u)
        #print("Email:",u.email.split('@')[1])
        if u.email.split('@')[1] == "dialpad.com":
            return render(request, 'index.html', {
            })
        else:
            return render(request, 'login.html', {
                "message": "Invalid User Permission !!!"
            })




