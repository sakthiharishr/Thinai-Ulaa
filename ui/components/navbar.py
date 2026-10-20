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

    logo_b64 = _get_logo_b64()
    logo_html = (
        f'<img src="{logo_b64}" class="navbar-logo" alt="Thinai Ulaa Logo" />'
        if logo_b64
        else ""
    )

    st.markdown(
        f"""
        <div class="navbar">
            <div class="navbar-brand">
                {logo_html}
                <div class="navbar-brand-text">
                    <p class="navbar-title">
                        Thinai Ulaa
                    </p>
                    <p class="navbar-subtitle">
                        Discover • Plan • Explore
                    </p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

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