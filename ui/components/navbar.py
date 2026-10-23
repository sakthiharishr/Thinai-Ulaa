import base64
import functools
from pathlib import Path

import streamlit as st


@functools.lru_cache(maxsize=1)
def _get_logo_b64() -> str:
    assets_dir = Path(__file__).resolve().parent.parent.parent / "assets"
    for name in ("logo_web.png", "logo_round.png", "logo.png", "logo.jpg"):
        candidate = assets_dir / name
        if candidate.exists():
            mime = "image/jpeg" if candidate.suffix.lower() in (".jpg", ".jpeg") else "image/png"
            data = candidate.read_bytes()
            return f"data:{mime};base64,{base64.b64encode(data).decode('utf-8')}"
    return ""


def render_navbar(active_page="Explore"):
    pages = [
        "Explore",
        "Recommendations",
        "Itinerary",
        "Chatbot",
    ]

    url_page = st.query_params.get(
        "page"
    )

    if (
        "active_page" not in st.session_state
        and url_page in pages
    ):
        st.session_state[
            "active_page"
        ] = url_page

    selected_page = st.session_state.get(
        "active_page",
        active_page,
    )

    if (
        st.query_params.get("page")
        != selected_page
    ):
        st.query_params[
            "page"
        ] = selected_page

    current_theme = st.session_state.get("theme", "light")
    # Initial icon: 🌙 when currently light (click → go dark), ☀️ when dark
    toggle_icon = "🌙" if current_theme == "light" else "☀️"

    logo_b64 = _get_logo_b64()
    logo_html = (
        f'<img src="{logo_b64}" class="navbar-logo" alt="Thinai Ulaa Logo" />'
        if logo_b64
        else ""
    )

    # The theme toggle button lives INSIDE the .navbar div so it appears on
    # the right (navbar uses justify-content: space-between).
    # No onclick attribute — scripts in st.markdown() don't execute (browser
    # blocks innerHTML scripts). Instead, components.html() runs the JS from
    # a same-origin iframe where window.parent reaches the main document.
    st.markdown(
        f"""
        <div class="navbar">
            <div class="navbar-brand">
                {logo_html}
                <div class="navbar-brand-text">
                    <p class="navbar-title">Thinai Ulaa</p>
                    <p class="navbar-subtitle">Discover &bull; Plan &bull; Explore</p>
                </div>
            </div>
            <button class="theme-toggle-btn" id="thinai-theme-btn" title="Toggle light / dark mode">{toggle_icon}</button>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Inject JS via an iframe — window.parent accesses the main Streamlit document.
    theme_toggle_js = """
        <style>html, body { margin: 0 !important; padding: 0 !important; height: 0 !important; overflow: hidden !important; }</style>
        <script>
        (function() {
            try {
                if (window.frameElement) {
                    window.frameElement.style.display = 'none';
                    var c = window.frameElement.closest("[data-testid='stIFrame'], [data-testid='element-container'], [data-testid='stElementContainer']");
                    if (c) c.style.display = 'none';
                }
            } catch (e) {}

            function attach() {
                var btn = window.parent.document.getElementById('thinai-theme-btn');
                if (!btn) { setTimeout(attach, 100); return; }
                btn.onclick = function() {
                    var root = window.parent.document.documentElement;
                    var cur  = root.getAttribute('data-theme') || 'light';
                    var next = cur === 'dark' ? 'light' : 'dark';
                    root.setAttribute('data-theme', next);
                    root.style.colorScheme = next;
                    if (window.parent.document.body) {
                        window.parent.document.body.setAttribute('data-theme', next);
                    }
                    btn.textContent = next === 'dark' ? '☀️' : '🌙';
                    try {
                        var u = new URL(window.parent.location.href);
                        u.searchParams.set('theme', next);
                        window.parent.history.replaceState(null, '', u.toString());
                    } catch(e) {}
                };
            }
            attach();
        })();
        </script>
    """

    with st.container(key="theme_js_runner"):
        if hasattr(st, "iframe"):
            st.iframe(theme_toggle_js, height="content", width="content")
        else:
            import streamlit.components.v1 as components
            components.html(theme_toggle_js, height=0, scrolling=False)

    nav = st.container(
        key="main_nav"
    )

    cols = nav.columns(
        len(pages),
        gap="small",
    )

    for index, page in enumerate(pages):

        with cols[index]:

            button_type = (
                "primary"
                if page == selected_page
                else "secondary"
            )

            if st.button(
                page,
                key=f"nav_{page.lower()}",
                use_container_width=True,
                type=button_type,
            ):
                st.session_state[
                    "active_page"
                ] = page

                st.query_params[
                    "page"
                ] = page

                st.session_state.pop(
                    "selected_place_id",
                    None,
                )

                st.rerun()

    return selected_page
