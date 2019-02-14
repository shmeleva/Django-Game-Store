from django.shortcuts import redirect

class UserRoleValidationMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, req):
        if not req.path in ['/auth/redirect/', '/logout/'] and req.user.is_authenticated and req.user.userprofile.role == '':
            return redirect('/auth/redirect')

        return self.get_response(req)
