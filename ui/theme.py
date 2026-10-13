import streamlit as st


def load_theme():
    """
    Apply global Streamlit theme adjustments and enforce light mode
    even when the user device or browser is configured for dark mode.

    Detailed application styling is handled through:
    ui/styles/main.css
    ui/styles/cards.css
    ui/styles/navbar.css
    ui/styles/responsive.css
    """

    st.markdown(
        """
        <style>
        :root {
            /* Force light color scheme for browsers and user-agents */
            color-scheme: light !important;
            -webkit-color-scheme: light !important;

            /* Apple-inspired light palette, tuned to the app's teal brand accent */
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

            --shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.04);
            --shadow-sm: 0 4px 14px rgba(0, 0, 0, 0.05);
            --shadow-md: 0 10px 30px rgba(0, 0, 0, 0.07);
            --shadow-lg: 0 20px 48px rgba(0, 0, 0, 0.10);

            --radius-sm: 12px;
            --radius-md: 18px;
            --radius-lg: 24px;
            --radius-pill: 999px;

            --ease: cubic-bezier(0.16, 1, 0.3, 1);
        }

        /* Enforce light variables and scheme even if OS/browser media query reports dark */
        @media (prefers-color-scheme: dark) {
            :root {
                color-scheme: light !important;
                -webkit-color-scheme: light !important;
                --bg: #f5f5f7 !important;
                --surface: #ffffff !important;
                --surface-alt: #fbfbfd !important;
                --text-primary: #1d1d1f !important;
                --text-secondary: #6e6e73 !important;
                --text-tertiary: #94a3b8 !important;
                --border: #e5e5ea !important;
                --border-strong: #d2d2d7 !important;
                --accent: #0f766e !important;
                --accent-strong: #0b5c56 !important;
                --accent-soft: #e6f7f4 !important;
            }

            html,
            body,
            .stApp,
            [data-testid="stAppViewContainer"] {
                color-scheme: light !important;
                -webkit-color-scheme: light !important;
                background-color: var(--bg) !important;
                color: var(--text-primary) !important;
            }
        }

        html,
        body {
            color-scheme: light !important;
            -webkit-color-scheme: light !important;
            font-family:
                -apple-system,
                BlinkMacSystemFont,
                "SF Pro Display",
                "SF Pro Text",
                "Segoe UI",
                Inter,
                Roboto,
                Helvetica,
                Arial,
                sans-serif;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }

        body {
            background: var(--bg) !important;
            color: var(--text-primary) !important;
        }

        /* Streamlit top-level containers forced to light theme */
        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"] {
            color-scheme: light !important;
            -webkit-color-scheme: light !important;
            background-color: var(--bg) !important;
            color: var(--text-primary) !important;
        }

        [data-testid="stHeader"] {
            background-color: transparent !important;
            color: var(--text-primary) !important;
        }

        [data-testid="stSidebar"] {
            background-color: var(--surface) !important;
            color: var(--text-primary) !important;
        }

        /* Form Controls, Inputs, and Labels */
        [data-testid="stWidgetLabel"] label,
        [data-testid="stWidgetLabel"] p,
        label[data-baseweb="checkbox"],
        label[data-baseweb="radio"] {
            color: var(--text-primary) !important;
        }

        [data-testid="stTextInput"] input,
        [data-testid="stNumberInput"] input,
        [data-testid="stTextArea"] textarea {
            background-color: var(--surface) !important;
            color: var(--text-primary) !important;
            border-color: var(--border-strong) !important;
            color-scheme: light !important;
        }

        [data-testid="stNumberInputStepDown"],
        [data-testid="stNumberInputStepUp"] {
            background-color: transparent !important;
            color: var(--text-primary) !important;
        }

        /* Selectboxes and Dropdowns */
        [data-baseweb="select"] > div {
            background-color: var(--surface) !important;
            color: var(--text-primary) !important;
            border-color: var(--border-strong) !important;
        }

        [data-baseweb="select"] * {
            color: var(--text-primary);
        }

        [data-baseweb="select"] svg {
            fill: var(--text-secondary) !important;
        }

        /* MultiSelect chips / tags */
        [data-baseweb="tag"] {
            background-color: var(--accent-soft) !important;
            color: var(--accent-strong) !important;
            border: 1px solid var(--accent) !important;
        }

        [data-baseweb="tag"] span {
            color: var(--accent-strong) !important;
        }

        [data-baseweb="tag"] svg {
            fill: var(--accent-strong) !important;
        }

        /* Dropdown popover list (BaseWeb portal rendered at body level) */
        div[data-baseweb="popover"],
        div[data-baseweb="popover"] > div,
        div[data-baseweb="menu"],
        ul[role="listbox"] {
            background-color: var(--surface) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border) !important;
            box-shadow: var(--shadow-md) !important;
            color-scheme: light !important;
        }

        li[role="option"] {
            background-color: var(--surface) !important;
            color: var(--text-primary) !important;
        }

        li[role="option"]:hover,
        li[role="option"][aria-selected="true"] {
            background-color: var(--accent-soft) !important;
            color: var(--accent-strong) !important;
        }

        /* Expanders, Metrics, Radio, Checkbox */
        [data-testid="stExpander"] {
            background-color: var(--surface) !important;
            border: 1px solid var(--border) !important;
            color: var(--text-primary) !important;
        }

        [data-testid="stExpander"] summary,
        [data-testid="stExpander"] summary p,
        [data-testid="stExpander"] summary span {
            color: var(--text-primary) !important;
        }

        [data-testid="stExpander"] summary svg {
            fill: var(--text-primary) !important;
        }

        [data-testid="stRadio"] label,
        [data-testid="stCheckbox"] label {
            color: var(--text-primary) !important;
        }

        [data-testid="stRadio"] label p,
        [data-testid="stCheckbox"] label p {
            color: var(--text-primary) !important;
        }

        /* Chat input container */
        [data-testid="stBottom"] > div {
            background-color: var(--bg) !important;
        }

        [data-testid="stChatInput"] {
            background-color: var(--surface) !important;
            border: 1px solid var(--border-strong) !important;
        }

        [data-testid="stChatInputTextArea"] {
            background-color: transparent !important;
            color: var(--text-primary) !important;
        }

        [data-testid="stChatInputSubmitButton"] {
            color: var(--accent) !important;
        }

        footer,
        #MainMenu {
            visibility: hidden;
        }
        </style>

        <script>
        (function() {
            try {
                // Ensure document root signals light color-scheme to browser
                document.documentElement.style.colorScheme = 'light';
                document.documentElement.setAttribute('data-theme', 'light');
                if (document.body) {
                    document.body.style.colorScheme = 'light';
                }

                // Clear any stored dark theme preferences in localStorage
                var themeKeys = ['stActiveTheme', 'theme', 'stCustomTheme', 'stTheme'];
                themeKeys.forEach(function(k) {
                    try {
                        var val = localStorage.getItem(k);
                        if (val && val.toLowerCase().indexOf('dark') !== -1) {
                            localStorage.removeItem(k);
                        }
                    } catch(e) {}
                });
            } catch(e) {}
        })();
        </script>
        """,
        unsafe_allow_html=True,
    )
