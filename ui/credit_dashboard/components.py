import streamlit as st


def page_hero(eyebrow: str, title: str, body: str, meta: str | None = None) -> None:
    meta_html = f'<div class="hero-meta">{meta}</div>' if meta else ""
    st.markdown(
        f"""
        <div class="hero-panel">
            <div class="hero-copy">
                <div class="eyebrow">{eyebrow}</div>
                <h1>{title}</h1>
                <p>{body}</p>
                {meta_html}
            </div>
            <div class="hero-visual">
                <div class="risk-ring">
                    <span>F1</span>
                    <strong>Recall</strong>
                    <small>Risk first</small>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_card(label: str, value: str, help_text: str | None = None) -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            {f'<div class="metric-help">{help_text}</div>' if help_text else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )


def story_card(title: str, body: str, accent: str = "blue") -> None:
    st.markdown(
        f"""
        <div class="story-card {accent}">
            <div class="story-title">{title}</div>
            <div class="story-body">{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def workflow_step(number: str, title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="workflow-step">
            <div class="step-number">{number}</div>
            <div>
                <div class="step-title">{title}</div>
                <div class="step-body">{body}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(title: str, subtitle: str | None = None) -> None:
    subtitle_html = f"<p>{subtitle}</p>" if subtitle else ""
    st.markdown(
        f"""
        <div class="section-heading">
            <h2>{title}</h2>
            {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def insight(text: str) -> None:
    st.markdown(f'<div class="insight">{text}</div>', unsafe_allow_html=True)
