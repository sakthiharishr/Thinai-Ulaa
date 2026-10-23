import streamlit as st


def render_rating(rating, rating_count=0):
    try:
        rating = float(rating)
    except (TypeError, ValueError):
        rating = 0.0

    rating = max(0.0, min(5.0, rating))

    if rating <= 0:
        st.markdown(
            """
            <div class="rating-stars">
                ☆☆☆☆☆
                <span style="color:var(--text-tertiary);">Not yet rated</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    full_stars = int(rating)
    half_star = 1 if rating - full_stars >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star

    stars = (
        "★" * full_stars
        + "⯨" * half_star
        + "☆" * empty_stars
    )

    count_text = ""

    if rating_count:
        try:
            count_text = f" ({int(rating_count):,} ratings)"
        except (TypeError, ValueError):
            count_text = ""

    st.markdown(
        f"""
        <div class="rating-stars">
            {stars}
            <span style="color:var(--text-secondary);">
                {rating:.1f}{count_text}
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_rating_badge(rating):
    try:
        rating = float(rating)
    except (TypeError, ValueError):
        rating = 0.0

    st.markdown(
        f"""
        <span class="badge"
              style="background:rgba(245, 158, 11, 0.16);color:#f59e0b;font-weight:600;">
            ⭐ {rating:.1f}
        </span>
        """,
        unsafe_allow_html=True,
    )
