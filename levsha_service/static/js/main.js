// static/js/main.js

document.addEventListener("DOMContentLoaded", function () {
    // Переключение между входом и регистрацией на login.html
    const loginBlock = document.getElementById("login-form-block");
    const registerBlock = document.getElementById("register-form-block");
    const showRegister = document.getElementById("show-register");
    const backToLogin = document.getElementById("back-to-login");

    if (showRegister && backToLogin && loginBlock && registerBlock) {
        showRegister.addEventListener("click", function (e) {
            e.preventDefault();
            loginBlock.classList.add("hidden");
            registerBlock.classList.remove("hidden");
        });

        backToLogin.addEventListener("click", function (e) {
            e.preventDefault();
            registerBlock.classList.add("hidden");
            loginBlock.classList.remove("hidden");
        });
    }

    // Модалки: заказ (главная) и обратный звонок (главная)
    const orderModal = document.getElementById("order-modal");
    const callbackModal = document.getElementById("callback-modal");

    const openOrderBtnHeader = document.getElementById("open-order-modal-btn");
    const openOrderBtnBanner = document.getElementById("open-order-modal-btn-banner");
    const openCallbackBtnBanner = document.getElementById("open-callback-modal-btn");

    function openModal(modalEl) {
        if (modalEl) {
            modalEl.style.display = "block";
        }
    }

    function closeModal(modalEl) {
        if (modalEl) {
            modalEl.style.display = "none";
        }
    }

    if (openOrderBtnHeader && orderModal) {
        openOrderBtnHeader.addEventListener("click", function () {
            openModal(orderModal);
        });
    }

    if (openOrderBtnBanner && orderModal) {
        openOrderBtnBanner.addEventListener("click", function () {
            openModal(orderModal);
        });
    }

    if (openCallbackBtnBanner && callbackModal) {
        openCallbackBtnBanner.addEventListener("click", function () {
            openModal(callbackModal);
        });
    }

    // ====== СЕРВИС: модалки создания заказов и пользователей ======
    const serviceOrderModal = document.getElementById("service-order-modal");
    const serviceUserModal = document.getElementById("service-user-modal");

    const openServiceOrderBtn = document.getElementById("open-service-order-modal-btn");
    const openServiceUserBtn = document.getElementById("open-service-user-modal-btn");

    if (openServiceOrderBtn && serviceOrderModal) {
        openServiceOrderBtn.addEventListener("click", function () {
            openModal(serviceOrderModal);
        });
    }

    if (openServiceUserBtn && serviceUserModal) {
        openServiceUserBtn.addEventListener("click", function () {
            openModal(serviceUserModal);
        });
    }

    // Закрытие всех модалок по крестику
    document.querySelectorAll(".modal-close").forEach(function (btn) {
        btn.addEventListener("click", function () {
            const targetId = this.getAttribute("data-close");
            const modal = document.getElementById(targetId);
            closeModal(modal);
        });
    });

    // Закрытие по клику вне контента
    window.addEventListener("click", function (e) {
        if (e.target === orderModal) {
            closeModal(orderModal);
        }
        if (e.target === callbackModal) {
            closeModal(callbackModal);
        }
        if (e.target === serviceOrderModal) {
            closeModal(serviceOrderModal);
        }
        if (e.target === serviceUserModal) {
            closeModal(serviceUserModal);
        }
    });
});
