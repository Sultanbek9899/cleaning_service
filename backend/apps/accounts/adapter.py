from allauth.account.adapter import DefaultAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=False, *args, **kwargs):
        user = super().save_user(request, user, form, commit,)
        data = form.cleaned_data
        user.company_name = data.get('company_name')
        user.logo = data.get('logo')
        user.phone_number = data.get('phone_number')
        user.save()
        return user