from oauth2_provider.views.mixins import ProtectedResourceMixin, OAuthLibMixin
from crud_framework.views.base_views import *


@method_decorator([csrf_exempt, view_catch_error], name='dispatch')
class OauthCrudView(ProtectedResourceMixin, OAuthLibMixin, BaseCrudView):
    pass
