if (window.location.pathname === "/config") {
    document.getElementById("config").className = "nav-link active";
} else if (window.location.pathname === "/flush") {
    document.getElementById("flush").className = "nav-link active";
} else if (window.location.pathname === "/analytics") {
    document.getElementById("analytics").className = "nav-link active";
} else {
    document.getElementById("index").className = "nav-link active";
}