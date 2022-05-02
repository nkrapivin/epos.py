# epos.py by nkrapivindev :3
# licensed under public domain, meaning I don't care at all.

import requests
from urllib.parse import urljoin, urlencode

from lxml import etree

from utils import bool_to_lower


_HEADERS = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.10 '
                  'Safari/537.36 ',

    "Sec-CH-UA": '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
    "Sec-CH-UA-Mobile": '?0',
    "Sec-CH-UA-Platform": '"Windows"',
    "Pragma": 'no-cache',
    "Cache-Control": 'no-cache',
    "Accept": 'application/json, text/plain, text/html, */*',
    "Accept-Language": 'en-US,en;q=0.9',
    "Upgrade-Insecure-Requests": '1',
    "X-Requested-With": 'XMLHttpRequest'
}
_EPOS_URL = "'https://school.permkrai.ru"
_CABINET_URL = "https://cabinet.permkrai.ru"


class EposClient:
    def __init__(self):
        self._session: requests.Session = requests.Session()
        self._session.headers.update(_HEADERS)

    def _refresh_csrf(self):
        r = self._session.get(
            url=urljoin(_CABINET_URL, 'login')
        )

        html = etree.fromstring(r.text, etree.XMLParser(recover=True))
        csrf_meta = html.find('.//meta[@name="csrf-token"]')
        csrf_token = csrf_meta.get('content')

        self._session.headers['X-CSRF-Token'] = csrf_token
        self._session.headers['X-XSRF-Token'] = self._session.cookies['XSRF-TOKEN']

    def login(self, rsaag_login: str, rsaag_password: str):
        self._refresh_csrf()

        r = self._session.post(
            url=urljoin(_CABINET_URL, 'login'),
            data={
                '_token': self._session.headers['X-CSRF-Token'],
                'login': rsaag_login,
                'password': rsaag_password
            }
        )

        r.raise_for_status()

    def cabinet_logout(self):
        self._refresh_csrf()

        r = self._session.get(
            url=urljoin(_CABINET_URL, 'logout')
        )

        r.raise_for_status()

    def check_agreement(self):
        self._refresh_csrf()

        r = self._session.post(
            url=urljoin(_CABINET_URL, 'check_agreement')
        )

        return r.json()

    def _auth(self, auth_app: str) -> str:
        self._refresh_csrf()

        params = {
            'mode': 'oauth',
            'app': auth_app
        }
        r = self._session.get(
            url=urljoin(_EPOS_URL, f'authenticate?{urlencode(params)}')
        )
        r.raise_for_status()

        # ..... ?????????? ???????????
        self._session.headers['auth-token'] = self._session.cookies['auth_token']
        self._session.headers['profile-id'] = self._session.cookies['profile_id']

        # the IB Whiteboard client seems to save this auth-token value into some storage, might be useful?
        return self._session.headers['auth-token']

    def auth_student(self):
        return self._auth(auth_app='rsaags')

    def auth_parent(self):
        return self._auth(auth_app='rsaag')

    def auth_teacher(self):
        return self._auth(auth_app='rsaa')

    def logout(self):
        params = {
            'authentication_token': self._session.headers['auth-token']
        }

        r = self._session.delete(
            url=urljoin(_EPOS_URL, f'lms/api/sessions?{urlencode(params)}'),
            json=[]
        )

        r.raise_for_status()

    def get_sessions(self):
        r = self._session.post(
            url=urljoin(_EPOS_URL, f"lms/api/sessions?pid={self._session.headers['profile-id']}"),
            json={
                'auth_token': self._session.headers['auth-token']
            }
        )

        return r.json()

    def get_academic_years(self, profile_id: int):
        r = self._session.get(
            url=urljoin(_EPOS_URL, f"core/api/academic_years?pid={profile_id}")
        )

        return r.json()

    def get_system_messages(self, profile_id: int, published: bool, today: bool):
        params = {
            'pid': profile_id,
            'published': bool_to_lower(published),
            'today': bool_to_lower(today)
        }

        r = self._session.get(
            url=urljoin(_EPOS_URL, f"acl/api/system_messages?{urlencode(params)}")
        )

        return r.json()

    def get_users(self, user_ids: list[int], profile_id: int):
        params = {
            'ids': ','.join(str(_id) for _id in user_ids),
            'pid': profile_id
        }

        r = self._session.get(
            url=urljoin(_EPOS_URL, f"acl/api/users?{urlencode(params)}")
        )

        return r.json()

    def get_student_profiles(self, profile_id: int, academic_year_id: int = -1):
        params = {
            "pid": profile_id,
            "academic_year_id": academic_year_id if academic_year_id >= 0 else ''
        }

        r = self._session.get(
            url=urljoin(_EPOS_URL, f'core/api/student_profiles/{profile_id}?{urlencode(params)}')
        )

        return r.json()

    def get_progress(self, profile_id: int, academic_year_id: int, hide_half_years: bool):
        params = {
            "academic_year_id": academic_year_id,
            "hide_half_years": bool_to_lower(hide_half_years),
            "pid": profile_id,
            "student_profile_id": profile_id
        }

        r = self._session.get(
            url=urljoin(_EPOS_URL, f'reports/api/progress/json?{urlencode(params)}' + str(academic_year_id))
        )

        return r.json()

    def get_notifications(self, profile_id: int):
        params = {
            'pid': profile_id,
            'student_id': profile_id
        }

        r = self._session.get(
            url=urljoin(_EPOS_URL, f'notification/api/notifications/status?{urlencode(params)}')
        )

        return r.json()


__all__ = ["EposClient"]
