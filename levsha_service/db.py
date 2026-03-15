# db.py
import pymysql


def connect_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="nata2006=",
        database="levsha_service_simple",
        port=3306,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )


# === Пользователи ===

def get_user_by_login(login):
    conn = connect_db()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE login = %s", (login,))
            return cur.fetchone()
    finally:
        conn.close()


def get_user_by_id(user_id):
    if not user_id:
        return None
    conn = connect_db()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            return cur.fetchone()
    finally:
        conn.close()


def create_user(login, password, full_name, phone, email):
    conn = connect_db()
    try:
        with conn.cursor() as cur:
            sql = """
                INSERT INTO users (login, password_hash, full_name, role, phone, email)
                VALUES (%s, %s, %s, 'client', %s, %s)
            """
            cur.execute(sql, (login, password, full_name, phone, email))
            return cur.lastrowid
    finally:
        conn.close()


def get_all_users():
    conn = connect_db()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users ORDER BY id")
            return cur.fetchall()
    finally:
        conn.close()


def update_user_admin(user_id, login, full_name, role, phone, email):
    conn = connect_db()
    try:
        with conn.cursor() as cur:
            sql = """
                UPDATE users
                SET login=%s, full_name=%s, role=%s, phone=%s, email=%s
                WHERE id=%s
            """
            cur.execute(sql, (login, full_name, role, phone, email, user_id))
    finally:
        conn.close()


def get_users_by_role(role):
    conn = connect_db()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE role = %s ORDER BY full_name", (role,))
            return cur.fetchall()
    finally:
        conn.close()


# === Отзывы ===

def get_published_reviews(limit=5):
    conn = connect_db()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT r.*, u.full_name AS client_name_full "
                "FROM reviews r "
                "LEFT JOIN users u ON r.client_id = u.id "
                "WHERE r.is_published = 1 "
                "ORDER BY r.created_at DESC "
                "LIMIT %s",
                (limit,)
            )
            return cur.fetchall()
    finally:
        conn.close()


# === Заказы ===

def create_order(client_id, client_name, client_phone,
                 device_model, problem_description, approx_price,
                 manager_id, master_id=None):
    conn = connect_db()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) AS cnt FROM orders")
            row = cur.fetchone()
            next_num = (row["cnt"] or 0) + 1
            order_number = f"L-{next_num:04d}"

            sql = """
                INSERT INTO orders (
                    order_number, client_id, client_name, client_phone,
                    device_model, problem_description, diagnostic_result,
                    status, approx_price, final_price,
                    manager_id, master_id
                )
                VALUES (%s, %s, %s, %s, %s, %s, NULL,
                        'new', %s, NULL, %s, %s)
            """
            cur.execute(sql, (
                order_number, client_id, client_name, client_phone,
                device_model, problem_description,
                approx_price, manager_id, master_id
            ))
            return cur.lastrowid
    finally:
        conn.close()


def get_orders_by_client(client_id):
    conn = connect_db()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM orders WHERE client_id = %s ORDER BY created_at DESC",
                (client_id,)
            )
            return cur.fetchall()
    finally:
        conn.close()


def get_orders_for_manager():
    """Все заказы для менеджера (и для админа, можно использовать тоже)."""
    conn = connect_db()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT o.*, "
                "cm.full_name AS manager_name, "
                "mm.full_name AS master_name "
                "FROM orders o "
                "LEFT JOIN users cm ON o.manager_id = cm.id "
                "LEFT JOIN users mm ON o.master_id = mm.id "
                "ORDER BY o.created_at DESC"
            )
            return cur.fetchall()
    finally:
        conn.close()


def get_orders_for_master(master_id):
    """Заказы, назначенные на мастера и не в статусе 'ready'."""
    conn = connect_db()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM orders "
                "WHERE master_id = %s AND status <> 'ready' "
                "ORDER BY created_at DESC",
                (master_id,)
            )
            return cur.fetchall()
    finally:
        conn.close()


def update_order_manager(order_id, status, master_id):
    """Менеджер может менять статус и мастера."""
    conn = connect_db()
    try:
        with conn.cursor() as cur:
            sql = "UPDATE orders SET status=%s, master_id=%s WHERE id=%s"
            cur.execute(sql, (status, master_id if master_id else None, order_id))
    finally:
        conn.close()


def update_order_master(order_id, problem_description, diagnostic_result,
                        status, approx_price, final_price):
    """Мастер меняет описание, диагностику, статус и цены."""
    conn = connect_db()
    try:
        with conn.cursor() as cur:
            sql = """
                UPDATE orders
                SET problem_description=%s,
                    diagnostic_result=%s,
                    status=%s,
                    approx_price=%s,
                    final_price=%s
                WHERE id=%s
            """
            cur.execute(sql, (
                problem_description,
                diagnostic_result,
                status,
                approx_price,
                final_price,
                order_id
            ))
    finally:
        conn.close()


def update_order_admin(order_id, client_name, client_phone, device_model,
                       problem_description, diagnostic_result,
                       status, approx_price, final_price,
                       manager_id, master_id):
    """Админ может править все основные поля заказа."""
    conn = connect_db()
    try:
        with conn.cursor() as cur:
            sql = """
                UPDATE orders
                SET client_name=%s,
                    client_phone=%s,
                    device_model=%s,
                    problem_description=%s,
                    diagnostic_result=%s,
                    status=%s,
                    approx_price=%s,
                    final_price=%s,
                    manager_id=%s,
                    master_id=%s
                WHERE id=%s
            """
            cur.execute(sql, (
                client_name, client_phone, device_model,
                problem_description, diagnostic_result,
                status, approx_price, final_price,
                manager_id if manager_id else None,
                master_id if master_id else None,
                order_id
            ))
    finally:
        conn.close()


# === Обратные звонки ===

def create_callback_request(phone, processed_by=None):
    conn = connect_db()
    try:
        with conn.cursor() as cur:
            sql = """
                INSERT INTO callback_requests (phone, status, processed_by)
                VALUES (%s, 'new', %s)
            """
            cur.execute(sql, (phone, processed_by))
            return cur.lastrowid
    finally:
        conn.close()


def get_all_callbacks():
    conn = connect_db()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT c.*, u.full_name AS processed_by_name "
                "FROM callback_requests c "
                "LEFT JOIN users u ON c.processed_by = u.id "
                "ORDER BY c.created_at DESC"
            )
            return cur.fetchall()
    finally:
        conn.close()


def delete_callback(callback_id):
    conn = connect_db()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM callback_requests WHERE id = %s", (callback_id,))
    finally:
        conn.close()
