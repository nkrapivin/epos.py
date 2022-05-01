# This is a testcase file for epos.py, it should not crash with an error and exit normally.
import epos


def testcase_main():
    print('pre-testcase...')
    e = epos.EposClient()

    # achtung paroli!!!
    login = input("Login (E-Mail): ")
    password = input("Password: ")

    loginok = e.login_password(login, password)
    agreement = e.check_agreement()
    eposok = e.auth_epos_student()
    epossessions = e.epos_get_sessions()
    myuserid = epossessions['id']
    myprofid = epossessions['profiles'][0]['id']
    eposacadem = e.epos_get_academic_years(myprofid)
    eposmessages = e.epos_get_system_messages(myprofid, True, True)
    eposprogress = e.epos_get_progress(myprofid, eposacadem[-1]['id'], True)
    eposnotifs = e.epos_get_notifications(myprofid)
    # ?????????????????
    eposusers = e.epos_get_users([myuserid, myuserid], myprofid)
    # print results
    print('loginOk=', loginok)
    print('agreement=', agreement)
    print('eposOk=', eposok)
    print('eposSessions=', epossessions)
    print('eposAcademYears=', eposacadem)
    print('eposMessages=', eposmessages)
    print('eposUserData=', eposusers)
    print('eposNotifs=', eposnotifs)
    print('eposProgress=', eposprogress)
    eposlogout = e.epos_logout()
    rsaaglogout = e.logout()
    print('eposLogout=', eposlogout)
    print('rsaagLogout=', rsaaglogout)
    print('testcase PASS :D')


# the fun starts here
if __name__ == '__main__':
    testcase_main()
