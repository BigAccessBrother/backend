from django.contrib.auth import get_user_model
from rest_framework import status

from project.api.models import SecurityStandard
from project.api.tests.master_tests import MasterTestWrapper

User = get_user_model()


class ListStandardsTest(MasterTestWrapper.MasterTests):
    endpoint = 'new_standards'
    methods = ['GET']

    def setUp(self):
        super().setUp()
        for i in range(3):
            SecurityStandard.objects.create(
                    id={i},
                    system_serial_number="5GH8LH2",
                    agent_version="0.1.0",
                    os_type="Microsoft Windows 10 Home",
                    os_version="10.0.17134 N/A Build 17134",
                    system_manufacturer="Dell Inc.",
                    system_model="Inspiron 7577",
                    system_type="x64-based PC",
                    bios_version="Dell Inc. 1.6.1, 16-Aug-18",
                    antispyware_enabled=True,
                    antispyware_signature_last_updated="14",
                    antivirus_enabled=True,
                    antivirus_signature_last_updated="14",
                    behavior_monitor_enabled=True,
                    full_scan_age="7",
                    nis_enabled=True,
                    nis_signature_last_updated="14",
                    nis_signature_version="1.281.510.0",
                    on_access_protection_enabled=True,
                    quick_scan_age="3",
                    real_time_protection_enabled=True,
                    disk_encryption_status="Protection Off",
            )

    def test_method_not_allowed(self):
        url = self.get_url()
        self.authorize()
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_standard_count(self):
        url = self.get_url()
        self.authorize()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_standard_order(self):
        url = self.get_url()
        self.authorize()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0].get('id'), '2')


class AddStandardsTest(MasterTestWrapper.MasterTests):
    endpoint = 'new_standards'
    methods = ['POST']

    def test_method_not_allowed(self):
        url = self.get_url()
        self.authorize()
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_unauthorized(self):
        url = self.get_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_standards(self):
        url = self.get_url()
        self.authorize()
        SecurityStandard.objects.create()
        response = self.client.post(url, {
          "system_serial_number": "5GH8LH2",
          "agent_version": "0.1.0",
          "os_type": "Microsoft Windows 10 Home",
          "os_version": "10.0.17134 N/A Build 17134",
          "system_manufacturer": "Dell Inc.",
          "system_model": "Inspiron 7577",
          "system_type": "x64-based PC",
          "bios_version": "Dell Inc. 1.6.1, 16-Aug-18",
          "antispyware_enabled": True,
          "antispyware_signature_last_updated": "14",
          "antivirus_enabled": True,
          "antivirus_signature_last_updated": "14",
          "behavior_monitor_enabled": True,
          "full_scan_age": "7",
          "nis_enabled": True,
          "nis_signature_last_updated": "14",
          "nis_signature_version": "1.281.510.0",
          "on_access_protection_enabled": True,
          "quick_scan_age": "3",
          "real_time_protection_enabled": True,
          "disk_encryption_status": "Protection Off"
          }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SecurityStandard.objects.count(), 1)
        self.assertEqual(SecurityStandard.objects.first().on_access_protection_enabled, True)
        self.assertEqual(SecurityStandard.objects.first().os_type, '"Microsoft Windows 10 Home"')
        # Test date_created
