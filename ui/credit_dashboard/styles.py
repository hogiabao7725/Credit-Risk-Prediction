import streamlit as st


def apply_global_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --ink: #172033;
            --muted: #667085;
            --line: #dbe3ef;
            --panel: #ffffff;
            --soft: #f6f8fb;
            --blue: #1d4ed8;
            --teal: #0f766e;
            --green: #047857;
            --red: #c2410c;
            --amber: #b45309;
            --violet: #6d28d9;
        }

        .stApp {
            background: linear-gradient(180deg, #f7f9fc 0%, #ffffff 42%, #f6f8fb 100%);
            color: var(--ink);
        }

        .block-container {
            max-width: 1280px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #111827 0%, #172033 100%);
        }

        section[data-testid="stSidebar"] * {
            color: #f8fafc;
        }

        section[data-testid="stSidebar"] [role="radiogroup"] label {
            border-radius: 8px;
            padding: 6px 8px;
        }

        div[data-testid="stMetric"] {
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 14px 16px;
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.05);
        }

        .hero-panel {
            display: grid;
            grid-template-columns: minmax(0, 1.45fr) minmax(260px, 0.55fr);
            gap: 26px;
            align-items: stretch;
            background:
                linear-gradient(135deg, rgba(29, 78, 216, 0.08), rgba(15, 118, 110, 0.07)),
                #ffffff;
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 30px;
            box-shadow: 0 18px 45px rgba(23, 32, 51, 0.08);
            margin-bottom: 22px;
        }

        .hero-copy {
            min-width: 0;
        }

        .eyebrow {
            color: var(--blue);
            font-weight: 700;
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0;
        }

        .hero-panel h1 {
            font-size: clamp(2rem, 4vw, 3.7rem);
            line-height: 1.05;
            margin: 0.15rem 0 0.65rem 0;
            letter-spacing: 0;
        }

        .hero-panel p {
            max-width: 820px;
            color: var(--muted);
            font-size: 1.03rem;
            line-height: 1.65;
            margin-bottom: 0;
        }

        .hero-meta {
            display: inline-flex;
            align-items: center;
            color: #344054;
            background: #eef4ff;
            border: 1px solid #d8e5ff;
            border-radius: 999px;
            padding: 8px 12px;
            margin-top: 16px;
            font-size: 0.9rem;
            font-weight: 650;
        }

        .hero-visual {
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 210px;
            background:
                linear-gradient(180deg, rgba(255,255,255,0.72), rgba(255,255,255,0.36)),
                repeating-linear-gradient(90deg, rgba(29,78,216,0.08) 0, rgba(29,78,216,0.08) 1px, transparent 1px, transparent 22px);
            border: 1px solid rgba(29, 78, 216, 0.16);
            border-radius: 8px;
        }

        .risk-ring {
            width: 172px;
            height: 172px;
            border-radius: 50%;
            display: grid;
            place-items: center;
            text-align: center;
            background:
                radial-gradient(circle at center, #ffffff 0 48%, transparent 49%),
                conic-gradient(var(--blue) 0 38%, var(--teal) 38% 70%, var(--amber) 70% 100%);
            box-shadow: inset 0 0 0 1px rgba(23, 32, 51, 0.08), 0 14px 30px rgba(23, 32, 51, 0.12);
        }

        .risk-ring span,
        .risk-ring strong,
        .risk-ring small {
            grid-area: 1 / 1;
            display: block;
        }

        .risk-ring span {
            transform: translateY(-22px);
            color: var(--blue);
            font-weight: 850;
            font-size: 2rem;
        }

        .risk-ring strong {
            transform: translateY(12px);
            color: var(--ink);
            font-size: 0.95rem;
        }

        .risk-ring small {
            transform: translateY(38px);
            color: var(--muted);
            font-size: 0.72rem;
        }

        .metric-card {
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 16px 18px;
            min-height: 122px;
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.05);
            position: relative;
            overflow: hidden;
        }

        .metric-card:after {
            content: "";
            position: absolute;
            inset: auto 0 0 0;
            height: 3px;
            background: linear-gradient(90deg, var(--blue), var(--teal));
        }

        .metric-label {
            color: var(--muted);
            font-size: 0.83rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0;
        }

        .metric-value {
            color: var(--ink);
            font-size: 1.85rem;
            font-weight: 800;
            margin-top: 6px;
        }

        .metric-help {
            color: var(--muted);
            font-size: 0.9rem;
            margin-top: 5px;
        }

        .story-card {
            background: #ffffff;
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 18px 18px;
            min-height: 150px;
            box-shadow: 0 10px 28px rgba(23, 32, 51, 0.05);
        }

        .story-card.blue { border-top: 4px solid var(--blue); }
        .story-card.green { border-top: 4px solid var(--green); }
        .story-card.amber { border-top: 4px solid var(--amber); }
        .story-card.violet { border-top: 4px solid var(--violet); }

        .story-title {
            color: var(--ink);
            font-weight: 800;
            font-size: 1.02rem;
            margin-bottom: 8px;
        }

        .story-body {
            color: var(--muted);
            line-height: 1.55;
            font-size: 0.95rem;
        }

        .workflow-step {
            display: grid;
            grid-template-columns: 44px minmax(0, 1fr);
            gap: 13px;
            align-items: start;
            background: #ffffff;
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 14px;
            min-height: 112px;
        }

        .step-number {
            width: 34px;
            height: 34px;
            border-radius: 8px;
            background: #172033;
            color: #ffffff;
            display: grid;
            place-items: center;
            font-weight: 800;
        }

        .step-title {
            font-weight: 800;
            color: var(--ink);
            margin-bottom: 4px;
        }

        .step-body {
            color: var(--muted);
            font-size: 0.92rem;
            line-height: 1.45;
        }

        .section-heading {
            margin: 28px 0 12px 0;
        }

        .section-heading h2 {
            margin: 0;
            font-size: 1.45rem;
            letter-spacing: 0;
            color: var(--ink);
        }

        .section-heading p {
            margin: 5px 0 0 0;
            color: var(--muted);
            font-size: 0.96rem;
        }

        .insight {
            background: #f8fbff;
            border: 1px solid #d8e5ff;
            border-left: 4px solid var(--blue);
            border-radius: 8px;
            padding: 14px 16px;
            color: #334155;
            margin: 12px 0;
            line-height: 1.55;
        }

        div[data-testid="stDataFrame"] {
            border: 1px solid var(--line);
            border-radius: 8px;
            overflow: hidden;
        }

        div[data-testid="stTabs"] button {
            border-radius: 8px 8px 0 0;
            font-weight: 700;
        }

        @media (max-width: 900px) {
            .hero-panel {
                grid-template-columns: 1fr;
                padding: 22px;
            }

            .hero-visual {
                min-height: 180px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
