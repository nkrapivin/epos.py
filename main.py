# This is a testcase file for epos.py
# It should finish normally without catching an exception

import requests.exceptions

import epos


def testcase_main():
    print('Creating Epos Client...')
    e = epos.EposClient()

    # achtung paroli!!!
    print("Input your Epos account credentials below:")

    login = input("Login (E-Mail): ")
    password = input("Password: ")

    try:
        e.login(login, password)

        agreement = e.check_agreement()
        print(f"{agreement=}")

        auth_token = e.auth_student()
        print(f"{auth_token=}")

        sessions = e.get_sessions()
        print(f"{sessions=}")

        user_id = sessions['id']
        profile_id = sessions['profiles'][0]['id']
        print(f"{user_id=}", f"{profile_id=}")

        academic_years = e.get_academic_years(profile_id)
        print(f"{academic_years=}")

        sys_messages = e.get_system_messages(profile_id, True, True)
        print(f"{sys_messages=}")

        progress = e.get_progress(profile_id, academic_years[-1]['id'], True)
        print(f"{progress=}")

        notifications = e.get_notifications(profile_id)
        print(f"{notifications=}")

        # ?????????????????
        users = e.get_users([user_id, user_id], profile_id)

        e.logout()

        print('Testcase Passed!')
    except requests.exceptions.HTTPError as e:
        print(f"Error occurred while executing: {e}")


if __name__ == '__main__':
    testcase_main()
