function Tab_onClick(id) {
    if (id === "preset") {
        document.getElementById("preset").className = "tab-pane fade px-4 py-5 show active";
        document.getElementById("custom_flush").className = "tab-pane fade px-4 py-5";
        document.getElementById("custom_get").className = "tab-pane fade px-4 py-5";
        document.getElementById("preset-tab").className = "nav-link border-0 text-uppercase font-weight-bold active";
        document.getElementById("custom_flush-tab").className = "nav-link border-0 text-uppercase font-weight-bold";
        document.getElementById("custom_get-tab").className = "nav-link border-0 text-uppercase font-weight-bold";
    } else if (id === "custom_flush") {
        document.getElementById("preset").className = "tab-pane fade px-4 py-5";
        document.getElementById("custom_flush").className = "tab-pane fade px-4 py-5 show active";
        document.getElementById("custom_get").className = "tab-pane fade px-4 py-5";
        document.getElementById("preset-tab").className = "nav-link border-0 text-uppercase font-weight-bold";
        document.getElementById("custom_flush-tab").className = "nav-link border-0 text-uppercase font-weight-bold active";
        document.getElementById("custom_get-tab").className = "nav-link border-0 text-uppercase font-weight-bold";
    } else if (id === "custom_get") {
        document.getElementById("preset").className = "tab-pane fade px-4 py-5";
        document.getElementById("custom_flush").className = "tab-pane fade px-4 py-5";
        document.getElementById("custom_get").className = "tab-pane fade px-4 py-5 show active";
        document.getElementById("preset-tab").className = "nav-link border-0 text-uppercase font-weight-bold";
        document.getElementById("custom_flush-tab").className = "nav-link border-0 text-uppercase font-weight-bold";
        document.getElementById("custom_get-tab").className = "nav-link border-0 text-uppercase font-weight-bold active";
    }
}