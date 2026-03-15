# app.py
from functools import wraps

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
)

from db import (
    get_user_by_login,
    get_user_by_id,
    create_user,
    get_published_reviews,
    create_order,
    get_orders_by_client,
    create_callback_request,
    get_orders_for_manager,
    get_orders_for_master,
    update_order_manager,
    update_order_master,
    update_order_admin,
    get_all_callbacks,
    delete_callback,
    get_all_users,
    update_user_admin,
    get_users_by_role,
)

app = Flask(__name__)
app.secret_key = "my_secret_key"


# =========================
#   ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# =========================

def current_user():
    uid = session.get("user_id")
    if not uid:
        return None
    return get_user_by_id(uid)


def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            flash("Для доступа к этой странице нужно войти.", "error")
            return render_template("login.html")
        return view_func(*args, **kwargs)
    return wrapper


def staff_required(view_func):
    """
    Доступ только для ролей: admin, manager, master.
    """
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        user = current_user()
        if not user:
            flash("Сначала войдите в систему.", "error")
            return render_template("login.html")
        if user["role"] not in ("admin", "manager", "master"):
            flash("У вас нет прав доступа к разделу 'Сервис'.", "error")
            return redirect(url_for("index"))
        return view_func(*args, **kwargs)
    return wrapper


@app.context_processor
def inject_user():
    return {"current_user": current_user()}


# =========================
#       АВТОРИЗАЦИЯ
# =========================

@app.route("/")
def root():
    return redirect(url_for("index"))


@app.route("/login_page")
def login_page():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    login_val = request.form.get("login")
    password = request.form.get("password")

    user = get_user_by_login(login_val)

    if not user or user["password_hash"] != password:
        flash("Неверный логин или пароль", "error")
        return render_template("login.html")

    session["user_id"] = user["id"]
    flash("Вы успешно вошли!", "success")
    return redirect(url_for("index"))


@app.route("/register", methods=["POST"])
def register():
    full_name = request.form.get("full_name")
    phone = request.form.get("phone")
    email = request.form.get("email")
    login_val = request.form.get("login")
    password = request.form.get("password")

    if not all([full_name, login_val, password]):
        flash("Заполните ФИО, логин и пароль.", "error")
        return render_template("login.html")

    if get_user_by_login(login_val):
        flash("Этот логин уже занят.", "error")
        return render_template("login.html")

    user_id = create_user(login_val, password, full_name, phone, email)
    session["user_id"] = user_id

    flash("Регистрация успешна!", "success")
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.clear()
    flash("Вы вышли из аккаунта.", "info")
    return redirect(url_for("index"))


# =========================
#        СТРАНИЦЫ
# =========================

@app.route("/home")
def index():
    reviews = get_published_reviews(limit=5)
    return render_template("index.html", reviews=reviews)


@app.route("/contacts")
def contacts():
    return render_template("contacts.html")


@app.route("/profile")
@login_required
def profile():
    user = current_user()
    orders = get_orders_by_client(user["id"])
    return render_template("profile.html", user=user, orders=orders)


# =========================
#     ДЕЙСТВИЯ ПОЛЬЗОВАТЕЛЯ
# =========================

@app.route("/create_order", methods=["POST"])
@login_required
def create_order_route():
    user = current_user()

    device_model = request.form.get("device_model")
    problem_description = request.form.get("problem_description")
    approx_price = request.form.get("approx_price")

    try:
        approx_price_val = float(approx_price) if approx_price else None
    except ValueError:
        approx_price_val = None

    create_order(
        client_id=user["id"],
        client_name=user["full_name"],
        client_phone=user["phone"] or "",
        device_model=device_model,
        problem_description=problem_description,
        approx_price=approx_price_val,
        manager_id=user["id"],  # в учебном варианте сам себе менеджер
        master_id=None
    )

    flash("Запрос на ремонт отправлен.", "success")
    return redirect(url_for("index"))


@app.route("/create_callback", methods=["POST"])
@login_required
def create_callback_route():
    user = current_user()
    phone = request.form.get("phone") or user["phone"]

    if not phone:
        flash("Введите номер телефона.", "error")
        return redirect(url_for("index"))

    create_callback_request(phone)
    flash("Заявка отправлена!", "success")
    return redirect(url_for("index"))


# =========================
#       СЕРВИС (РОЛИ)
# =========================

@app.route("/service")
@login_required
@staff_required
def service():
    user = current_user()
    role = user["role"]

    context = {"role": role}

    if role == "manager":
        context["orders"] = get_orders_for_manager()
        context["callbacks"] = get_all_callbacks()
        context["masters"] = get_users_by_role("master")

    elif role == "master":
        context["orders"] = get_orders_for_master(user["id"])

    elif role == "admin":
        context["orders"] = get_orders_for_manager()   # все заказы
        context["callbacks"] = get_all_callbacks()
        context["users_list"] = get_all_users()
        context["managers"] = get_users_by_role("manager")
        context["masters"] = get_users_by_role("master")

    return render_template("service.html", **context)


# === Менеджер / админ: создание заказа из сервиса ===

@app.route("/service/order/create", methods=["POST"])
@login_required
@staff_required
def service_order_create():
    user = current_user()
    var = user["role"]

    client_name = request.form.get("client_name")
    client_phone = request.form.get("client_phone")
    device_model = request.form.get("device_model")
    problem_description = request.form.get("problem_description")
    approx_price = request.form.get("approx_price") or None
    master_id = request.form.get("master_id") or None

    try:
        approx_price_val = float(approx_price) if approx_price else None
    except ValueError:
        approx_price_val = None

    # Для простоты, client_id None (если создаёт менеджер/админ без привязки к аккаунту)
    client_id = None

    # Менеджер по умолчанию — тот, кто создаёт
    manager_id = user["id"]

    create_order(
        client_id=client_id,
        client_name=client_name,
        client_phone=client_phone,
        device_model=device_model,
        problem_description=problem_description,
        approx_price=approx_price_val,
        manager_id=manager_id,
        master_id=int(master_id) if master_id else None
    )

    flash("Заказ создан.", "success")
    return redirect(url_for("service"))


# === Менеджер: изменение статуса и мастера ===

@app.route("/service/order/update_manager", methods=["POST"])
@login_required
@staff_required
def service_order_update_manager():
    user = current_user()
    if user["role"] not in ("manager", "admin"):
        flash("Недостаточно прав.", "error")
        return redirect(url_for("service"))

    order_id = request.form.get("order_id")
    status = request.form.get("status")
    master_id = request.form.get("master_id") or None

    update_order_manager(order_id, status, master_id)
    flash("Заказ обновлён.", "success")
    return redirect(url_for("service"))


# === Мастер: изменение своего заказа ===

@app.route("/service/order/update_master", methods=["POST"])
@login_required
@staff_required
def service_order_update_master():
    user = current_user()
    if user["role"] != "master":
        flash("Недостаточно прав.", "error")
        return redirect(url_for("service"))

    order_id = request.form.get("order_id")
    problem_description = request.form.get("problem_description")
    diagnostic_result = request.form.get("diagnostic_result")
    status = request.form.get("status")
    approx_price = request.form.get("approx_price") or None
    final_price = request.form.get("final_price") or None

    try:
        approx_price_val = float(approx_price) if approx_price else None
    except ValueError:
        approx_price_val = None

    try:
        final_price_val = float(final_price) if final_price else None
    except ValueError:
        final_price_val = None

    update_order_master(
        order_id,
        problem_description,
        diagnostic_result,
        status,
        approx_price_val,
        final_price_val
    )

    flash("Заказ обновлён.", "success")
    return redirect(url_for("service"))


# === Админ: полное редактирование заказа ===

@app.route("/service/order/update_admin", methods=["POST"])
@login_required
@staff_required
def service_order_update_admin():
    user = current_user()
    if user["role"] != "admin":
        flash("Недостаточно прав.", "error")
        return redirect(url_for("service"))

    order_id = request.form.get("order_id")
    client_name = request.form.get("client_name")
    client_phone = request.form.get("client_phone")
    device_model = request.form.get("device_model")
    problem_description = request.form.get("problem_description")
    diagnostic_result = request.form.get("diagnostic_result")
    status = request.form.get("status")
    approx_price = request.form.get("approx_price") or None
    final_price = request.form.get("final_price") or None
    manager_id = request.form.get("manager_id") or None
    master_id = request.form.get("master_id") or None

    try:
        approx_price_val = float(approx_price) if approx_price else None
    except ValueError:
        approx_price_val = None

    try:
        final_price_val = float(final_price) if final_price else None
    except ValueError:
        final_price_val = None

    update_order_admin(
        order_id,
        client_name,
        client_phone,
        device_model,
        problem_description,
        diagnostic_result,
        status,
        approx_price_val,
        final_price_val,
        int(manager_id) if manager_id else None,
        int(master_id) if master_id else None
    )

    flash("Заказ обновлён (админ).", "success")
    return redirect(url_for("service"))


# === Обратные звонки: удаление (менеджер/админ) ===

@app.route("/service/callback/delete", methods=["POST"])
@login_required
@staff_required
def service_callback_delete():
    user = current_user()
    if user["role"] not in ("manager", "admin"):
        flash("Недостаточно прав.", "error")
        return redirect(url_for("service"))

    callback_id = request.form.get("callback_id")
    delete_callback(callback_id)
    flash("Запись обратного звонка удалена.", "success")
    return redirect(url_for("service"))


# === Админ: управление пользователями ===

@app.route("/service/user/update", methods=["POST"])
@login_required
@staff_required
def service_user_update():
    user = current_user()
    if user["role"] != "admin":
        flash("Недостаточно прав.", "error")
        return redirect(url_for("service"))

    user_id = request.form.get("user_id")
    login_val = request.form.get("login")
    full_name = request.form.get("full_name")
    role = request.form.get("role")
    phone = request.form.get("phone")
    email = request.form.get("email")

    update_user_admin(user_id, login_val, full_name, role, phone, email)
    flash("Пользователь обновлён.", "success")
    return redirect(url_for("service"))


@app.route("/service/user/create", methods=["POST"])
@login_required
@staff_required
def service_user_create():
    user = current_user()
    if user["role"] != "admin":
        flash("Недостаточно прав.", "error")
        return redirect(url_for("service"))

    full_name = request.form.get("full_name")
    phone = request.form.get("phone")
    email = request.form.get("email")
    login_val = request.form.get("login")
    password = request.form.get("password")
    role = request.form.get("role") or "client"

    if not all([full_name, login_val, password]):
        flash("ФИО, логин и пароль обязательны.", "error")
        return redirect(url_for("service"))

    new_id = create_user(login_val, password, full_name, phone, email)
    # после создания по умолчанию роль client, можно отдельным апдейтом поправить
    update_user_admin(new_id, login_val, full_name, role, phone, email)

    flash("Пользователь создан.", "success")
    return redirect(url_for("service"))


# =========================
#      ЗАПУСК СЕРВЕРА
# =========================

if __name__ == "__main__":
    app.run(debug=True)
