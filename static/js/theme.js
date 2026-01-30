(function () {
    const root = document.documentElement;
    const toggle = document.getElementById("theme-toggle");

    const THEMES = ["light", "dark", "system"];

    function getSystemTheme() {
        return window.matchMedia("(prefers-color-scheme: dark)").matches
            ? "dark"
            : "light";
    }

    function applyTheme(theme) {
        if (theme === "system") {
            root.setAttribute("data-theme", getSystemTheme());
        } else {
            root.setAttribute("data-theme", theme);
        }

        updateIcon(theme);

        // Save locally only if logged in
        if (document.body.dataset.authenticated === "true") {
            localStorage.setItem("theme", theme);

            fetch("/accounts/theme/save/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken()
                },
                body: JSON.stringify({ theme })
            }).catch(() => {});
        }
    }

    function updateIcon(theme) {
        if (!toggle) return;

        if (theme === "light") {
            toggle.textContent = "🌞";
            toggle.title = "Theme: Light";
        } else if (theme === "dark") {
            toggle.textContent = "🌙";
            toggle.title = "Theme: Dark";
        } else {
            toggle.textContent = "🖥";
            toggle.title = "Theme: System";
        }
    }

    function cycleTheme() {
        const current = toggle.dataset.theme || "system";
        const next = THEMES[(THEMES.indexOf(current) + 1) % THEMES.length];
        toggle.dataset.theme = next;
        applyTheme(next);
    }

    // ==============================
    // 🔑 INITIAL LOAD LOGIC (ROBUST)
    // ==============================

    const isAuthenticated = document.body.dataset.authenticated === "true";

    let initialTheme = "system";

    if (isAuthenticated) {
        // Priority:
        // 1️⃣ Backend-injected theme (if present)
        // 2️⃣ LocalStorage fallback
        // 3️⃣ System

        initialTheme =
            document.body.dataset.userTheme ||
            localStorage.getItem("theme") ||
            "system";
    } else {
        // Anonymous users → always system
        localStorage.removeItem("theme");
        initialTheme = "system";
    }

    toggle && (toggle.dataset.theme = initialTheme);
    applyTheme(initialTheme);

    // Click handler
    toggle && toggle.addEventListener("click", cycleTheme);

    // React to OS theme change in system mode
    window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => {
        if (toggle && toggle.dataset.theme === "system") {
            applyTheme("system");
        }
    });

    // ==============================
    // CSRF helper
    // ==============================
    function getCSRFToken() {
        const match = document.cookie.match(/csrftoken=([^;]+)/);
        return match ? match[1] : "";
    }
})();
