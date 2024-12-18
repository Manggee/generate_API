import mysql.connector
from utils.db_config import DB_CONFIG

def fetch_available_categories():
    # 데이터베이스에서 랜덤으로 카테고리를 가져오기
    connection = None
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        cursor.execute("SELECT place_category_id FROM place_category")  # place_category 테이블에서 ID 가져오기
        categories = [row[0] for row in cursor.fetchall()]  # 결과를 리스트로 변환
        return categories
    except mysql.connector.Error as err:
        print(f"DB 에러 발생: {err}")
        return []
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def fetch_random_member_id():
    # 데이터베이스에서 랜덤으로 회원의 memberId를 가져오기
    connection = None
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT id FROM member WHERE id IS NOT NULL ORDER BY RAND() LIMIT 1")  # member 테이블에서 랜덤으로 1명 선택
        result = cursor.fetchone()
        if result:
            print(f"랜덤으로 선택된 memberId: {result['id']}")
            return result['id']  # memberId 반환
        else:
            raise ValueError("데이터베이스에 저장된 회원이 없습니다.")
    except mysql.connector.Error as err:
        print(f"DB 에러 발생: {err}")
        return None
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


def fetch_random_group_id(member_id):
    connection = None
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)

        # 본인이 생성하거나 가입하지 않은 랜덤 모임 가져오기
        query = """
            SELECT group_id
            FROM groups
            WHERE group_id NOT IN (
                SELECT group_id FROM group_member WHERE member_id = %s
            )
            AND group_id NOT IN (
                SELECT group_id 
                FROM group_member
                WHERE member_id = %s AND role = 'ADMIN'
            )
            AND recruiting = TRUE
            ORDER BY RAND() LIMIT 1
            """
        cursor.execute(query, (member_id, member_id))
        result = cursor.fetchone()

        if result:
            return result['group_id']
        else:
            print("사용 가능한 랜덤 모임이 없습니다.")
            return None
    except mysql.connector.Error as err:
        print(f"DB 에러 발생: {err}")
        return None
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()