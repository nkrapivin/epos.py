# epos.py by nkrapivindev :3
# licensed under public domain, meaning I don't care at all.

# :(
import requests


class EposClient:
    __cabinetUrl__ = 'https://cabinet.permkrai.ru/'
    __eposUrl__ = 'https://school.permkrai.ru/'
    __session__ = requests.Session()

    def __setheaders__(self):
        # pycharm's weird o_O?
        self.__session__.headers['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, ' \
                                                 'like Gecko) Chrome/98.0.4758.10 Safari/537.36 '
        # imitate a Chrome browser as much as possible
        self.__session__.headers['sec-ch-ua'] = '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"'
        self.__session__.headers['sec-ch-ua-mobile'] = '?0'
        self.__session__.headers['sec-ch-ua-platform'] = '"Windows"'
        self.__session__.headers['pragma'] = 'no-cache'
        self.__session__.headers['accept-language'] = 'en-US,en;q=0.9'
        self.__session__.headers['cache-control'] = 'no-cache'
        self.__session__.headers['accept'] = 'application/json, text/plain, text/html, */*'
        self.__session__.headers['upgrade-insecure-requests'] = '1'
        self.__session__.headers['x-requested-with'] = 'XMLHttpRequest'

    def __refreshcsrf__(self):
        self.__setheaders__()

        r = self.__session__.get(
            url=self.__cabinetUrl__ + 'login'
        )

        html = r.text
        # grab the csrf token from the html layout (very awful but works)
        startpos = html.find('"csrf-token" content="') + len('"csrf-token" content="')
        endpos = html.find('" id="csrf"')
        csrftoken = html[startpos:endpos]

        self.__session__.headers['x-csrf-token'] = csrftoken
        self.__session__.headers['x-xsrf-token'] = self.__session__.cookies['XSRF-TOKEN']

    def login_password(self, rsaag_login: str, rsaag_password: str):
        self.__refreshcsrf__()

        r = self.__session__.post(
            url=self.__cabinetUrl__ + 'login',
            data={
                '_token': self.__session__.headers['x-csrf-token'],
                'login': rsaag_login,
                'password': rsaag_password
            }
        )

        return r.status_code < 400

    # def login_gosuslugi O_O

    def logout(self):
        self.__refreshcsrf__()

        r = self.__session__.get(
            url=self.__cabinetUrl__ + 'logout'
        )

        return r.status_code < 400

    def check_agreement(self):
        self.__refreshcsrf__()

        r = self.__session__.post(
            url=self.__cabinetUrl__ + 'check_agreement'
        )

        return r.json()

    def auth_epos(self, auth_app: str):
        self.__refreshcsrf__()

        r = self.__session__.get(
            url=self.__eposUrl__ + 'authenticate?mode=oauth&app=' + auth_app
        )

        # ..... ?????????? ???????????
        self.__session__.headers['auth-token'] = self.__session__.cookies['auth_token']
        self.__session__.headers['profile-id'] = self.__session__.cookies['profile_id']

        # the IB Whiteboard client seems to save this auth-token value into some storage, might be useful?
        return [r.status_code < 400, self.__session__.headers['auth-token']]

    def auth_epos_student(self):
        return self.auth_epos('rsaags')

    def auth_epos_parent(self):
        return self.auth_epos('rsaag')

    def auth_epos_teacher(self):
        return self.auth_epos('rsaa')

    def epos_logout(self):
        r = self.__session__.delete(
            url=self.__eposUrl__
            + 'lms/api/sessions?authentication_token=' + str(self.__session__.headers['auth-token']),
            json=[]
        )

        return r.status_code < 400

    def epos_get_sessions(self):
        r = self.__session__.post(
            url=self.__eposUrl__
            + 'lms/api/sessions?pid=' + self.__session__.headers['profile-id'],
            json={
                'auth_token': self.__session__.headers['auth-token']
            }
        )

        return r.json()

    def epos_get_academic_years(self, profile_id: int):
        r = self.__session__.get(
            url=self.__eposUrl__ + 'core/api/academic_years?pid=' + str(profile_id)
        )

        return r.json()

    def epos_get_system_messages(self, profile_id: int, published: bool, today: bool):
        r = self.__session__.get(
            url=self.__eposUrl__
            + 'acl/api/system_messages?pid=' + str(profile_id)
            + '&published=' + str(published).lower()
            + '&today=' + str(today).lower()
        )

        return r.json()

    def epos_get_users(self, user_ids: list[int], profile_id: int):
        r = self.__session__.get(
            url=self.__eposUrl__
            + 'acl/api/users?ids=' + ','.join([str(el) for el in user_ids])
            + '&pid=' + str(profile_id)
        )

        return r.json()

    def epos_get_student_profiles(self, profile_id: int, academic_year_id: int = -1):
        r = self.__session__.get(
            url=self.__eposUrl__
            + 'core/api/student_profiles/' + str(profile_id) + '?pid=' + str(profile_id)
            + '&academic_year_id=' + str(academic_year_id) if academic_year_id >= 0 else ''
        )

        return r.json()

    def epos_get_progress(self, profile_id: int, academic_year_id: int, hide_half_years: bool):
        r = self.__session__.get(
            url=self.__eposUrl__
            + 'reports/api/progress/json?academic_year_id=' + str(academic_year_id)
            + '&hide_half_years=' + str(hide_half_years).lower()
            + '&pid=' + str(profile_id)
            + '&student_profile_id=' + str(profile_id)
        )

        return r.json()

    def epos_get_notifications(self, profile_id: int):
        r = self.__session__.get(
            url=self.__eposUrl__
            + 'notification/api/notifications/status?pid=' + str(profile_id)
            + '&student_id=' + str(profile_id)
        )

        return r.json()
