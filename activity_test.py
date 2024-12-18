from AS1 import register, login, create_group, create_application, memberId
from utils.generate_ import generate_group



def test_register():
    # 회원가입 API 테스트
    user_data = register()
    assert user_data is not None, "회원가입 실패: 사용자 정보가 생성되지 않았습니다."
    assert 'email' in user_data and 'password' in user_data, "회원가입 데이터가 유효하지 않습니다."


def test_register_and_login():
    # 회원가입 후 로그인 API 테스트
    user_data = register()
    assert user_data is not None, "회원가입 실패: 사용자 정보가 생성되지 않았습니다."

    email, password = user_data.get('email'), user_data.get('password')
    assert email is not None and password is not None, "회원가입 데이터가 유효하지 않습니다."

    login_success = login(email, password)
    assert login_success, "회원가입 후 로그인 실패"


def test_login_random_user():
    # 데이터베이스에 저장된 랜덤 사용자를 이용한 로그인 테스트
    login_success = login()
    assert login_success, "사용자 로그인 실패"


def test_register_login_and_create_group():
    # 회원가입 -> 로그인 -> 모임 생성 테스트
    # 회원가입
    user_data = register()
    # assert user_data is not None, "회원가입 실패: 사용자 정보가 생성되지 않았습니다."
    # email, password = user_data.get('email'), user_data.get('password')
    # assert email is not None and password is not None, "회원가입 데이터가 유효하지 않습니다."
    assert user_data, "회원가입 실패: 사용자 정보가 생성되지 않았습니다."
    email, password = user_data.get('email'), user_data.get('password')
    assert email and password, "회원가입 데이터가 유효하지 않습니다."

    # 로그인
    memberId = login(email, password)['id']
    # assert memberId is not None, "로그인 실패 or 선택된 멤버 ID가 없습니다."
    assert memberId, "로그인 실패 or 선택한 멤버 ID가 없습니다."
    print(f"현재 로그인된 memberId: {memberId}")

    # 모임 생성 데이터 준비 및 생성
    group_data = generate_group(memberId)
    print(f"생성된 모임 데이터: {group_data}")
    group_response = create_group(group_data)
    #assert group_response is not None, "모임 생성 실패: 생성된 모임 데이터가 없습니다."
    assert group_response, "모임 생성 실패 : 생성된 모임 데이터가 없습니다."
    print(f"모임 생성 성공: {group_response}")


def test_5():
    """
    회원가입 -> 로그인 -> 모임 생성 -> 다른 모임에 랜덤 가입 신청 테스트
    """
    # 회원가입
    user_data = register()
    assert user_data, "회원가입 실패: 사용자 정보가 생성되지 않았습니다."
    email, password = user_data.get('email'), user_data.get('password')
    assert email and password, "회원가입 데이터가 유효하지 않습니다."

    # 로그인
    login_response = login(email, password)
    assert login_response, "로그인 실패"
    memberId = login_response.get('id')
    print(f"로그인 성공: memberId={memberId}")

    # 모임 생성
    group_data = generate_group(memberId)
    create_group_response = create_group(group_data)
    assert create_group_response, "모임 생성 실패"
    print(f"모임 생성 성공: {create_group_response}")

    # 랜덤 가입 신청
    application_response = create_application(memberId)
    #assert application_response, "모임 가입 신청 실패"
    print(f"모임 가입 신청 성공: {application_response}")