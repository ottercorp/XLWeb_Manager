if (window.location.pathname === "/config") {
    document.getElementById("config").className = "nav-link active";
} else if (window.location.pathname === "/flush") {
    document.getElementById("flush").className = "nav-link active";
} else if (window.location.pathname === "/analytics") {
    document.getElementById("analytics").className = "nav-link active";
} else if (window.location.pathname === "/upload_dalamud_log") {
    document.getElementById("loganalysis").className = "nav-link active";
} else if (window.location.pathname === "/plugin_status") {
    document.getElementById("plugins").className = "nav-link active";
} else if (window.location.pathname.startsWith("/feedback")) {
    document.getElementById("feedback").className = "nav-link active";
} else {
    document.getElementById("index").className = "nav-link active";
}