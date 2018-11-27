from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class MasterTestWrapper:
    class BasicMasterTests(APITestCase):
        endpoint = None
        methods = []
        kwargs = {}

        def get_url(self, *args, **kwargs):
            if not kwargs:
                kwargs = self.get_kwargs()
            return reverse(self.endpoint, args=args, kwargs=kwargs)

        def get_kwargs(self):
            return self.kwargs

        def authorize(self, user=None):
            if not user:
                user = self.user
            self.refresh = RefreshToken.for_user(user)
            self.access_token = self.refresh.access_token
            self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        def setUp(self):
            self.admin_user = User.objects.create_user(
                username='admin_user',
                password='super_secure',
                email='admin@test.com',
                is_staff=True
            )
            self.other_user = User.objects.create_user(
                username='other_user',
                password='super_secure',
                email='other_user@test.com',
                is_staff=False
            )

    class MasterTests(BasicMasterTests):
        def test_unauthorized_requests(self):
            url = self.get_url(**self.get_kwargs())
            for m in self.methods:
                try:
                    method = getattr(self.client, m.lower())
                    response = method(url)
                    if response:
                        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
                except AttributeError:
                    raise Exception(f"No such method {m}")
