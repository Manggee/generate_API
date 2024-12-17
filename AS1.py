import random
import mysql.connector
import requests
from utils.db_config import DB_CONFIG
from utils.generate_ import generate, generate_group

api = 'http://52.79.199.83:9090/api/v1'

# 회원 가입 또는 로그인에서 받아오는 Response에서 member의 id를 추출 후 고정된 memberId를 사용
memberId = None


# DB_CONFIG = {
#     'host': '54.180.151.205',
#     'port': 3366,
#     'user': 'tripcok',
#     'password': 'tripcok1234',
#     'database': 'tripcok_db'
# }


# 로그인
def login(email=None, password=None):
    connection = None  # connection 변수를 초기화
    try:
        if not email or not password:
            # 데이터베이스 연결 시도
            connection = mysql.connector.connect(
                host=DB_CONFIG['host'],
                port=DB_CONFIG['port'],
                user=DB_CONFIG['user'],
                password=DB_CONFIG['password'],
                database=DB_CONFIG['database']
            )
            cursor = connection.cursor(dictionary=True)

            # 데이터베이스에서 랜덤으로 사용자 선택
            cursor.execute("SELECT id, email, password FROM member ORDER BY RAND() LIMIT 1")
            user = cursor.fetchone()

            # 사용자가 없으면 로그인 실패 처리
            if not user:
                print("사용자를 찾을 수 없습니다.")
                return False

            # 사용자 이메일과 비밀번호 추출
            email, password = user['email'], user['password']
            # memberId = user['id']

        # API를 통해 로그인 요청
        response = requests.put(api + '/member/login', json={'email': email, 'password': password})

        if response.status_code == 200:
            print(f"로그인 성공: {email}, memberId: {response.json()['id']}")
            # return memberId
            return response.json()

        else:
            print(f"로그인 실패: {email}")
            return False
    except mysql.connector.Error as err:
        # 데이터베이스 에러 발생 시 로그 출력
        print(f"DB 에러 발생: {err}")
        return False
    finally:
        # connection이 초기화된 경우에만 닫기 시도
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

    response = requests.get(api + '/member/login', params={'email': email, 'password': password})
    if not response.status_code == 200:
        return False


# 회원가입
def register():
    #  사용자 정보 생성
    data = generate()
    print(f"생성된 사용자 데이터: {data}")

    # 회원가입 API 통신
    response = requests.post(api + '/member/register', json=data, headers={'Content-Type': 'application/json'})
    print(f"회원가입 응답 코드: {response.status_code}")  # 응답 상태 코드 출력
    print(f"회원가입 응답 내용: {response.text}")  # 응답 본문 출력

    # 회원가입 API 통신을 성공 할 경우
    if response.status_code == 201:
        login_success = login(data['email'], data['password'])
        return data if login_success else None
    else:
        print(f"회원가입 실패: {response.status_code}, {response.text}")


# 모임 생성
def create_group(group_data):
    print(f"생성된 모임 데이터: {group_data}")
    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.post(api + '/group', json=group_data, headers=headers)
    print(f"모임 생성 응답 코드: {response.status_code}")
    print(f"모임 생성 응답 내용: {response.text}")

    if response.status_code == 201:
        return response.json()
    else:
        print(f"모임 생성 실패: {response.status_code}, {response.text}")
        return None


if __name__ == '__main__':

    # 회원가입 및 로그인 둘중 하나 선택
    choice_num = random.choice([1, 2, 3, 4, 5, 6])

    if choice_num in [1, 2]:
        print("로그인을 실행합니다.")
        login()
    elif choice_num in [3]:
        print("회원가입을 실행합니다.")
        register()
    else:
        print("로그인 후 모임 생성을 실행합니다.")
        memberId = login()
        if memberId:
            print(f"로그인한 memberId: {memberId}")
            group_data = generate_group(memberId)
            print(f"생성된 모임 데이터 : {group_data}")
            create_group(group_data)
        else:
            print("모임 생성을 위한 멤버 ID를 가져오지 못했습니다.")
