import streamlit as st


def load_theme(theme: str = "light"):
    """
    Apply global theme CSS supporting both Light Mode and Dark Mode.
    Both themes are always injected as CSS; JavaScript flips the
    data-theme attribute on <html> for instant, no-reload switching.
    The `theme` parameter sets the initial value on page load.
    """

    if theme not in ("light", "dark"):
        theme = "light"

    st.markdown(
        f"""
        <style>
        /* =========================================================
           THEME VARIABLES — always present; JS switches data-theme
           ========================================================= */

        :root {{
            /* ===== LIGHT MODE (default) ===== */
            color-scheme: light;
            -webkit-color-scheme: light;

            --accent: #0f766e;
            --accent-strong: #0b5c56;
            --accent-soft: #e6f7f4;
            --accent-gradient: linear-gradient(135deg, #14b8a6 0%, #0f766e 55%, #0b5c56 100%);

            --bg: #f5f5f7;
            --surface: #ffffff;
            --surface-alt: #fbfbfd;

            --text-primary: #1d1d1f;
            --text-secondary: #6e6e73;
            --text-tertiary: #94a3b8;

            --border: #e5e5ea;
            --border-strong: #d2d2d7;

            --shadow-xs: 0 1px 2px rgba(0,0,0,0.04);
            --shadow-sm: 0 4px 14px rgba(0,0,0,0.05);
            --shadow-md: 0 10px 30px rgba(0,0,0,0.07);
            --shadow-lg: 0 20px 48px rgba(0,0,0,0.10);

            --navbar-logo-border: rgba(255,255,255,0.95);

            --radius-sm: 12px;
            --radius-md: 18px;
            --radius-lg: 24px;
            --radius-pill: 999px;
            --ease: cubic-bezier(0.16, 1, 0.3, 1);
        }}

        :root[data-theme="dark"] {{
            /* ===== DARK MODE overrides ===== */
            color-scheme: dark;
            -webkit-color-scheme: dark;

            --accent: #14b8a6;
            --accent-strong: #2dd4bf;
            --accent-soft: rgba(20, 184, 166, 0.16);
            --accent-gradient: linear-gradient(135deg, #2dd4bf 0%, #0f766e 65%, #0a4d47 100%);

            --bg: #0c1117;
            --surface: #151c26;
            --surface-alt: #1c2635;

            --text-primary: #f8fafc;
            --text-secondary: #cbd5e1;
            --text-tertiary: #94a3b8;

            --border: rgba(255,255,255,0.10);
            --border-strong: rgba(255,255,255,0.18);

            --shadow-xs: 0 1px 2px rgba(0,0,0,0.35);
            --shadow-sm: 0 4px 14px rgba(0,0,0,0.45);
            --shadow-md: 0 10px 30px rgba(0,0,0,0.55);
            --shadow-lg: 0 20px 48px rgba(0,0,0,0.65);

            --navbar-logo-border: rgba(45, 212, 191, 0.35);
        }}

        /* Apply bg/color on root elements immediately */
        html, body {{
            background: var(--bg) !important;
            color: var(--text-primary) !important;
        }}

        /* Tighten top padding */
        header[data-testid="stHeader"] {{
            background: transparent !important;
            height: 1.5rem !important;
            min-height: 1.5rem !important;
        }}

        .stMainBlockContainer,
        [data-testid="stMainBlockContainer"],
        [data-testid="stAppViewBlockContainer"],
        .main .block-container,
        .block-container {{
            padding-top: 0.5rem !important;
            margin-top: 0 !important;
        }}

        div[data-testid="stElementContainer"]:has(> style),
        div[data-testid="stElementContainer"]:empty {{
            display: none !important;
            height: 0 !important;
            min-height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
        }}

        /* Collapse zero-height / script-only utility iframes */
        iframe[height="0"],
        iframe.stIFrame,
        iframe[data-testid="stIFrame"],
        div[data-testid="stCustomComponentV1"]:has(iframe[height="0"]),
        .st-key-theme_js_runner,
        div[class*="st-key-theme_js_runner"],
        div[data-testid="stElementContainer"]:has(iframe.stIFrame),
        div[data-testid="stElementContainer"]:has(iframe[data-testid="stIFrame"]),
        div[data-testid="stElementContainer"]:has(div.st-key-theme_js_runner) {{
            height: 0 !important;
            min-height: 0 !important;
            max-height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            border: none !important;
            line-height: 0 !important;
            overflow: hidden !important;
        }}

        iframe.stIFrame,
        iframe[data-testid="stIFrame"] {{
            position: absolute !important;
            top: 0 !important;
            left: 0 !important;
            width: 0 !important;
            opacity: 0 !important;
            pointer-events: none !important;
        }}

        /* =========================================================
           STREAMLIT APP CONTAINERS
           ========================================================= */

        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"] {{
            background-color: var(--bg) !important;
            color: var(--text-primary) !important;
        }}

        [data-testid="stHeader"] {{
            background-color: transparent !important;
            color: var(--text-primary) !important;
        }}

        [data-testid="stSidebar"] {{
            background-color: var(--surface) !important;
            border-right: 1px solid var(--border) !important;
            color: var(--text-primary) !important;
        }}

        /* =========================================================
           BUTTONS
           ========================================================= */

        .stButton > button {{
            border-radius: var(--radius-sm);
        }}

        .stButton > button * {{
            background: transparent !important;
            border: none !important;
            outline: none !important;
            box-shadow: none !important;
            color: inherit !important;
        }}

        .stButton > button p,
        .stButton > button span,
        .stButton > button div {{
            background: transparent !important;
            border: none !important;
            outline: none !important;
            box-shadow: none !important;
            color: inherit !important;
        }}

        .stButton > button[kind="secondary"] {{
            color: var(--text-primary) !important;
            -webkit-text-fill-color: var(--text-primary) !important;
            background-color: var(--surface) !important;
            border: 1px solid var(--border-strong) !important;
            font-weight: 600 !important;
        }}

        .stButton > button[kind="secondary"]:hover {{
            color: var(--accent-strong) !important;
            -webkit-text-fill-color: var(--accent-strong) !important;
            background-color: var(--accent-soft) !important;
            border-color: var(--accent) !important;
        }}

        .stButton > button[kind="secondary"]:focus,
        .stButton > button[kind="secondary"]:focus-visible,
        .stButton > button[kind="secondary"]:active {{
            background-color: var(--surface) !important;
            color: var(--text-primary) !important;
            -webkit-text-fill-color: var(--text-primary) !important;
            border-color: var(--accent) !important;
            box-shadow: none !important;
        }}

        .stButton > button[kind="primary"] {{
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            background: var(--accent-gradient) !important;
            border: none !important;
            font-weight: 600 !important;
        }}

        .stButton > button[kind="primary"]:focus,
        .stButton > button[kind="primary"]:focus-visible,
        .stButton > button[kind="primary"]:active {{
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            background: var(--accent-gradient) !important;
        }}

        /* =========================================================
           FORM CONTROLS, INPUTS, AND LABELS
           ========================================================= */

        [data-testid="stWidgetLabel"] label,
        [data-testid="stWidgetLabel"] p,
        [data-testid="stWidgetLabel"] span,
        label[data-baseweb="checkbox"],
        label[data-baseweb="radio"],
        [data-testid="stRadio"] label,
        [data-testid="stCheckbox"] label,
        [data-testid="stRadio"] label p,
        [data-testid="stCheckbox"] label p {{
            color: var(--text-primary) !important;
            -webkit-text-fill-color: var(--text-primary) !important;
        }}

        [data-testid="stCaptionContainer"] p,
        [data-testid="stCaptionContainer"] span {{
            color: var(--text-secondary) !important;
            -webkit-text-fill-color: var(--text-secondary) !important;
        }}

        [data-testid="stTextInput"] input,
        [data-testid="stNumberInput"] input,
        [data-testid="stTextArea"] textarea,
        [data-baseweb="input"] input {{
            background-color: var(--surface) !important;
            color: var(--text-primary) !important;
            -webkit-text-fill-color: var(--text-primary) !important;
            border: 1px solid var(--border-strong) !important;
        }}

        ::placeholder,
        input::placeholder,
        textarea::placeholder,
        [data-placeholder="true"] {{
            color: var(--text-secondary) !important;
            -webkit-text-fill-color: var(--text-secondary) !important;
            opacity: 0.8 !important;
        }}

        [data-testid="stTextInput"] input:focus,
        [data-testid="stNumberInput"] input:focus,
        [data-testid="stTextArea"] textarea:focus {{
            border-color: var(--accent) !important;
            box-shadow: 0 0 0 2px var(--accent-soft) !important;
        }}

        [data-testid="stNumberInputStepDown"],
        [data-testid="stNumberInputStepUp"] {{
            background-color: transparent !important;
            color: var(--text-primary) !important;
            -webkit-text-fill-color: var(--text-primary) !important;
        }}

        /* =========================================================
           SELECTBOXES, MULTISELECT, AND BASEWEB DROPDOWNS
           ========================================================= */

        [data-baseweb="select"] > div {{
            background-color: var(--surface) !important;
            border: 1px solid var(--border-strong) !important;
        }}

        [data-baseweb="select"],
        [data-baseweb="select"] *,
        [data-baseweb="select"] div,
        [data-baseweb="select"] span,
        [data-baseweb="select"] input {{
            color: var(--text-primary) !important;
            -webkit-text-fill-color: var(--text-primary) !important;
        }}

        [data-baseweb="select"] [data-placeholder="true"],
        [data-baseweb="select"] [aria-placeholder] {{
            color: var(--text-secondary) !important;
            -webkit-text-fill-color: var(--text-secondary) !important;
        }}

        [data-baseweb="select"] svg {{
            fill: var(--text-secondary) !important;
        }}

        /* MultiSelect chips / tags — always white text on teal background */
        [data-baseweb="tag"],
        [data-tag],
        .stMultiSelect [data-tag],
        .stMultiSelect span[data-tag],
        span[data-tag],
        span[data-tag] * {{
            background-color: var(--accent) !important;
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            border: 1px solid var(--accent) !important;
        }}

        [data-baseweb="tag"],
        [data-baseweb="tag"] *,
        [data-baseweb="tag"] span,
        [data-tag],
        [data-tag] *,
        [data-tag] span,
        .stMultiSelect [data-tag],
        .stMultiSelect [data-tag] *,
        .stMultiSelect [data-tag] span,
        .stMultiSelect [data-baseweb="tag"],
        .stMultiSelect [data-baseweb="tag"] * {{
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
        }}

        [data-baseweb="tag"] svg,
        [data-tag] svg,
        .stMultiSelect [data-tag] svg,
        [data-tag] button,
        [data-tag] button * {{
            fill: #ffffff !important;
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
        }}

        /* Dropdown popover list — use CSS vars which cascade from :root */
        div[data-baseweb="popover"],
        div[data-baseweb="popover"] > div,
        div[data-baseweb="menu"],
        ul[role="listbox"],
        [role="listbox"] {{
            background-color: var(--surface) !important;
            border: 1px solid var(--border) !important;
            box-shadow: var(--shadow-md) !important;
            border-radius: var(--radius-sm) !important;
        }}

        div[data-baseweb="popover"] *,
        div[data-baseweb="menu"] *,
        ul[role="listbox"] *,
        [role="listbox"] * {{
            background-color: var(--surface) !important;
            color: var(--text-primary) !important;
            -webkit-text-fill-color: var(--text-primary) !important;
        }}

        [role="option"] {{
            background-color: var(--surface) !important;
            color: var(--text-primary) !important;
            -webkit-text-fill-color: var(--text-primary) !important;
        }}

        [role="option"]:hover,
        [role="option"][aria-selected="true"] {{
            background-color: var(--surface-alt) !important;
            color: var(--accent-strong) !important;
            -webkit-text-fill-color: var(--accent-strong) !important;
        }}

        [role="option"]:hover *,
        [role="option"][aria-selected="true"] * {{
            background-color: var(--surface-alt) !important;
            color: var(--accent-strong) !important;
            -webkit-text-fill-color: var(--accent-strong) !important;
        }}

        /* =========================================================
           TOOLTIPS (Buttons and widgets with help=..., e.g., GPS, Clear)
           ========================================================= */

        .react-aria-Tooltip,
        [role="tooltip"],
        [data-testid="stTooltipContent"],
        [data-testid="stTooltipErrorContent"],
        .stTooltipContent,
        .stTooltipErrorContent,
        div.stTooltipContent,
        div[class*="stTooltipContent"] {{
            background-color: var(--surface) !important;
            background: var(--surface) !important;
            color: var(--text-primary) !important;
            -webkit-text-fill-color: var(--text-primary) !important;
            border: 1px solid var(--border-strong) !important;
            box-shadow: var(--shadow-md) !important;
            border-radius: var(--radius-sm) !important;
        }}

        .react-aria-Tooltip *,
        [role="tooltip"] *,
        [data-testid="stTooltipContent"] *,
        [data-testid="stTooltipErrorContent"] *,
        .stTooltipContent *,
        .stTooltipErrorContent *,
        div.stTooltipContent *,
        div[class*="stTooltipContent"] * {{
            color: var(--text-primary) !important;
            -webkit-text-fill-color: var(--text-primary) !important;
        }}

        :root[data-theme="dark"] .react-aria-Tooltip,
        :root[data-theme="dark"] [role="tooltip"],
        :root[data-theme="dark"] [data-testid="stTooltipContent"],
        :root[data-theme="dark"] [data-testid="stTooltipErrorContent"],
        :root[data-theme="dark"] .stTooltipContent,
        :root[data-theme="dark"] .stTooltipErrorContent,
        :root[data-theme="dark"] div.stTooltipContent,
        :root[data-theme="dark"] div[class*="stTooltipContent"] {{
            background-color: #151c26 !important;
            background: #151c26 !important;
            color: #f8fafc !important;
            -webkit-text-fill-color: #f8fafc !important;
            border: 1px solid rgba(255, 255, 255, 0.18) !important;
        }}

        :root[data-theme="dark"] .react-aria-Tooltip *,
        :root[data-theme="dark"] [role="tooltip"] *,
        :root[data-theme="dark"] [data-testid="stTooltipContent"] *,
        :root[data-theme="dark"] [data-testid="stTooltipErrorContent"] *,
        :root[data-theme="dark"] .stTooltipContent *,
        :root[data-theme="dark"] .stTooltipErrorContent *,
        :root[data-theme="dark"] div.stTooltipContent *,
        :root[data-theme="dark"] div[class*="stTooltipContent"] * {{
            color: #f8fafc !important;
            -webkit-text-fill-color: #f8fafc !important;
        }}

        /* =========================================================
           EXPANDERS, METRICS, CHAT
           ========================================================= */

        [data-testid="stExpander"] {{
            background-color: var(--surface) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-sm) !important;
            color: var(--text-primary) !important;
        }}

        [data-testid="stExpander"] summary,
        [data-testid="stExpander"] summary p,
        [data-testid="stExpander"] summary span {{
            color: var(--text-primary) !important;
            -webkit-text-fill-color: var(--text-primary) !important;
        }}

        [data-testid="stExpander"] summary svg {{
            fill: var(--text-primary) !important;
        }}

        [data-testid="stBottom"] > div {{
            background-color: var(--bg) !important;
        }}

        [data-testid="stChatInput"] {{
            background-color: var(--surface) !important;
            border: 1px solid var(--border-strong) !important;
        }}

        [data-testid="stChatInput"] > div,
        [data-testid="stChatInput"] [data-baseweb="textarea"] {{
            background-color: var(--surface) !important;
        }}

        [data-testid="stChatInputTextArea"] {{
            background-color: transparent !important;
            color: var(--text-primary) !important;
            -webkit-text-fill-color: var(--text-primary) !important;
        }}

        [data-testid="stChatInputSubmitButton"] {{
            color: var(--accent) !important;
        }}

        [data-testid="stMetricValue"] {{
            color: var(--text-primary) !important;
        }}

        [data-testid="stMetricLabel"] {{
            color: var(--text-secondary) !important;
        }}

        h1, h2, h3, h4, h5, h6 {{
            color: var(--text-primary) !important;
        }}

        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] span,
        [data-testid="stMarkdownContainer"] li {{
            color: inherit;
        }}

        footer,
        #MainMenu {{
            visibility: hidden;
        }}
        </style>

        <script>
        /* Set the initial data-theme from Python session state.
           JS toggle in the navbar will change it without any Python rerun. */
        (function() {{
            try {{
                document.documentElement.setAttribute('data-theme', '{theme}');
                document.documentElement.style.colorScheme = '{theme}';
                if (document.body) {{
                    document.body.setAttribute('data-theme', '{theme}');
                }}
            }} catch(e) {{}}
        }})();
        </script>
        """,
        unsafe_allow_html=True,
    )
