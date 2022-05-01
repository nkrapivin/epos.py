# This is a sample Python script.
import epos


def testcase_main():
    e = epos.EposClient()

    login = input("Login (E-Mail): ")
    password = input("Password: ")

    loginok = e.login_password(login, password)
    agreement = e.check_agreement()
    eposok = e.auth_epos_student()
    epossessions = e.epos_get_sessions()
    myuserid = epossessions['id']
    myprofid = epossessions['profiles'][0]['id']
    eposacadem = e.epos_get_academic_years(myprofid)
    print('loginOk=', loginok)
    print('agreement=', agreement)
    print('eposOk=', eposok)
    print('eposSessions=', epossessions)
    print('eposAcademYears=', eposacadem)
    e.epos_logout()
    e.logout()
    print('again=', e.epos_get_sessions())


if __name__ == '__main__':
    testcase_main()
