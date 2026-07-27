"""Gradio frontend for the Feature Launch Kit demo.

Screens: Select release + scope -> Generating -> Review (Pass/Fail) -> Download.
Talks to the backend through one seam: content_pipeline.generate_kit(). Swapping
the stub in that module for the real pipeline requires no changes here.
"""

import html
import json
import logging
import os
import subprocess
import tempfile
import time
from pathlib import Path

import gradio as gr

from content_pipeline import generate_kit, list_releases
from llm_integration import LLMError

logger = logging.getLogger(__name__)
_escape = html.escape

SRC_DIR = Path(__file__).parent
REPO_ROOT = SRC_DIR.parent
QMD_TEMPLATE = SRC_DIR / "render_template.qmd"
LOGO_PATH = REPO_ROOT / "assets" / "logo_smartivate.png"

SCOPE_LABELS = {
    "all": "Complete kit",
    "marketing": "Marketing kit",
    "customer_success": "Customer Success kit",
    "sales": "Sales kit",
}
SCOPE_CHOICES = list(SCOPE_LABELS.values())
SCOPE_BY_LABEL = {v: k for k, v in SCOPE_LABELS.items()}

SECTION_LABELS = {
    "email": "MARKETING KIT",
    "guide": "CUSTOMER SUCCESS KIT",
    "onepager": "SALES KIT",
}

SCREENS = ["select", "generating", "review", "download"]

LK_THEME = gr.themes.Base(
    primary_hue=gr.themes.colors.indigo,
    neutral_hue=gr.themes.colors.slate,
    font=gr.themes.GoogleFont("DM Sans"),
    font_mono=gr.themes.GoogleFont("DM Mono"),
).set(
    body_background_fill="#F7F7F9",
    body_background_fill_dark="#0D0D14",
    background_fill_primary="#FFFFFF",
    background_fill_primary_dark="#18181F",
    border_color_primary="#DDDDE8",
    border_color_primary_dark="#2A2A38",
    body_text_color="#111118",
    body_text_color_dark="#EBEBF5",
    button_primary_background_fill="#2F2FEB",
    button_primary_background_fill_dark="#4F4FFF",
    button_primary_background_fill_hover="#2626C4",
    button_primary_text_color="#FFFFFF",
    button_secondary_background_fill="transparent",
    button_secondary_background_fill_dark="transparent",
    button_secondary_border_color="#DDDDE8",
    button_secondary_border_color_dark="#2A2A38",
    button_secondary_text_color="#111118",
    button_secondary_text_color_dark="#EBEBF5",
    input_background_fill="#FFFFFF",
    input_background_fill_dark="#18181F",
    input_border_color="#DDDDE8",
    input_border_color_dark="#2A2A38",
    block_background_fill="#FFFFFF",
    block_background_fill_dark="#18181F",
    block_border_color="#DDDDE8",
    block_border_color_dark="#2A2A38",
    block_radius="8px",
    button_large_radius="6px",
)

THEME_CSS = """
:root {
    --lk-bg: #F7F7F9; --lk-fg: #111118; --lk-card: #FFFFFF;
    --lk-primary: #2F2FEB; --lk-muted: #72727A; --lk-border: #DDDDE8;
    --lk-success: #16A34A;
}
@media (prefers-color-scheme: dark) {
    :root {
        --lk-bg: #0D0D14; --lk-fg: #EBEBF5; --lk-card: #18181F;
        --lk-primary: #4F4FFF; --lk-muted: #8888A0; --lk-border: #2A2A38;
        --lk-success: #22C55E;
    }
}
body, .gradio-container {
    background: var(--lk-bg) !important;
    font-family: 'DM Sans', system-ui, sans-serif !important;
}
.gradio-container { max-width: none !important; }
#lk-shell { max-width: 680px; margin: 0 auto; padding: 0 24px 80px; }
#lk-header {
    border-bottom: 1px solid var(--lk-border);
    background: var(--lk-card);
    padding: 14px 24px;
    display: flex; align-items: center; justify-content: space-between;
    margin: 0 calc(-1 * max(24px, (100% - 680px) / 2)) 32px;
}
#lk-header .lk-brand { display: flex; align-items: center; gap: 10px; font-size: 13px; }
#lk-header .lk-brand .lk-logo {
    height: 32px; width: auto; display: inline-block;
}
#lk-header .lk-app-name { font-weight: 500; color: var(--lk-fg); }
#lk-header .lk-steps { display: flex; gap: 6px; align-items: center; }
#lk-header .lk-steps span { height: 6px; border-radius: 3px; background: var(--lk-border); display: inline-block; }
.lk-page-title { font-size: 28px; font-weight: 700; letter-spacing: -0.02em; color: var(--lk-fg); margin: 0 0 8px; }
.lk-page-sub { font-size: 14px; color: var(--lk-muted); margin: 0 0 32px; line-height: 1.6; }
.lk-label { font-size: 11px; font-weight: 600; letter-spacing: .08em; text-transform: uppercase; color: var(--lk-muted); margin-bottom: 8px; }
.lk-card {
    border: 1px solid var(--lk-border) !important;
    border-radius: 8px !important;
    background: var(--lk-card) !important;
    overflow: hidden;
    margin-bottom: 16px;
}
.lk-card-header {
    padding: 12px 20px; border-bottom: 1px solid var(--lk-border);
    font-size: 11px; font-weight: 600; letter-spacing: .08em; text-transform: uppercase;
    color: var(--lk-muted); background: color-mix(in srgb, var(--lk-primary) 4%, var(--lk-card));
}
.lk-card textarea {
    background: var(--lk-card) !important;
    color: var(--lk-fg) !important;
    font-size: 13px !important;
    line-height: 1.6 !important;
    max-height: 320px;
    padding: 16px !important;
}
.lk-status-row { display: flex; align-items: center; gap: 12px; font-size: 14px; font-weight: 500; color: var(--lk-fg); }
.lk-spinner {
    box-sizing: border-box !important;
    display: inline-block !important;
    width: 20px !important; height: 20px !important;
    border-radius: 50% !important; flex-shrink: 0;
    border: 3px solid #DDDDE8 !important;
    border-top: 3px solid #2F2FEB !important;
    border-top-color: #2F2FEB !important;
    animation: lk-spin 0.9s linear infinite !important;
}
.lk-check {
    width: 20px; height: 20px; border-radius: 50%; background: var(--lk-success);
    display: flex; align-items: center; justify-content: center; flex-shrink: 0; color: white; font-size: 12px;
}
@keyframes lk-spin { to { transform: rotate(360deg); } }
.lk-progress-track { height: 4px; background: var(--lk-border); border-radius: 2px; overflow: hidden; margin-top: 20px; }
.lk-progress-fill { height: 100%; background: var(--lk-primary); border-radius: 2px; transition: width .3s ease; }
.lk-success-badge {
    width: 56px; height: 56px; border-radius: 50%;
    background: color-mix(in srgb, var(--lk-success) 12%, transparent);
    border: 2px solid var(--lk-success);
    display: flex; align-items: center; justify-content: center; margin: 0 auto 20px;
    color: var(--lk-success); font-size: 24px;
}
#lk-fail-btn, #lk-start-over-btn, #lk-fail-btn button, #lk-start-over-btn button {
    background: var(--lk-card) !important;
    color: var(--lk-fg) !important;
    border: 1px solid var(--lk-border) !important;
    opacity: 1 !important;
}
/* Gradio dims any output component while its update is "pending" (.generating);
   our own HTML status card already communicates progress, so don't double-dim it. */
#lk-shell .generating, #lk-shell.generating {
    opacity: 1 !important;
}
"""


def _step_dots_html(active: str) -> str:
    idx = SCREENS.index(active)
    dots = []
    for i in range(len(SCREENS)):
        width = 20 if i == idx else 6
        color = "var(--lk-primary)" if i <= idx else "var(--lk-border)"
        dots.append(f'<span style="width:{width}px;background:{color};"></span>')
    return (
        '<div id="lk-header">'
        f'<div class="lk-brand"><img src="/gradio_api/file={LOGO_PATH}" alt="Smartivate" class="lk-logo">'
        '<span style="color:var(--lk-border);">|</span>'
        '<span class="lk-app-name">Feature Launch Kit</span></div>'
        f'<div class="lk-steps">{"".join(dots)}</div>'
        '</div>'
    )


def _status_html(text: str, done: bool, progress: int) -> str:
    icon = '<div class="lk-check">✓</div>' if done else '<div class="lk-spinner"></div>'
    return (
        '<div class="lk-card" style="padding:32px 28px;">'
        f'<div class="lk-status-row">{icon}<span>{_escape(text)}</span></div>'
        f'<div class="lk-progress-track"><div class="lk-progress-fill" style="width:{progress}%;"></div></div>'
        '</div>'
    )


def _box_updates(content: dict) -> list:
    """gr.update() pairs (wrapper visibility, textbox value) for every output
    key in SECTION_LABELS, in that fixed order — matches output_boxes wiring."""
    updates = []
    for key in SECTION_LABELS:
        if key in content:
            updates.append(gr.update(visible=True))
            updates.append(gr.update(value=content[key]))
        else:
            updates.append(gr.update(visible=False))
            updates.append(gr.update(value=""))
    return updates


def _render_quarto(release: str, scope_label: str, content: dict) -> str:
    """Render the approved content to a styled HTML doc via Quarto. Returns the output file path.

    Quarto's --output-dir doesn't relocate embedded resource lookups correctly for
    this template, so we render next to render_template.qmd (its natural working
    directory) and then move the result into a fresh temp dir for Gradio to serve.
    """
    payload = {
        "subtitle": scope_label,
        "release": release,
        "sections": [
            {"label": SECTION_LABELS.get(k, k), "body": v} for k, v in content.items()
        ],
    }
    data_path = SRC_DIR / ".render_payload.json"
    data_path.write_text(json.dumps(payload), encoding="utf-8")

    local_out = QMD_TEMPLATE.with_suffix(".html")
    env = dict(os.environ, KIT_RENDER_DATA=str(data_path))
    try:
        result = subprocess.run(
            ["quarto", "render", str(QMD_TEMPLATE), "--to", "html"],
            env=env, capture_output=True, cwd=SRC_DIR, text=True,
        )
        if result.returncode != 0:
            logger.error("Quarto render failed (exit %s): %s", result.returncode, result.stderr)
            raise gr.Error("Couldn't build the download document. Please try Pass again.")
        tmp_dir = Path(tempfile.mkdtemp(prefix="launch_kit_"))
        out_path = tmp_dir / "launch_kit.html"
        out_path.write_bytes(local_out.read_bytes())
    finally:
        data_path.unlink(missing_ok=True)
        local_out.unlink(missing_ok=True)
    return str(out_path)


with gr.Blocks(title="Feature Launch Kit") as demo:
    state_content = gr.State({})
    state_release = gr.State("")
    state_scope_label = gr.State("")
    state_out_path = gr.State("")

    with gr.Column(elem_id="lk-shell"):
        header_html = gr.HTML(_step_dots_html("select"))

        # ── Screen 1: Select ────────────────────────────────────────────
        with gr.Column(visible=True) as select_screen:
            gr.HTML('<div class="lk-page-title">Feature Launch Kit</div>'
                    '<div class="lk-page-sub">Select a release and the materials you need. '
                    "We'll generate them grounded in the product's knowledge base.</div>")
            gr.HTML('<div class="lk-label">Select a release</div>')
            release_dd = gr.Dropdown(show_label=False, choices=list_releases(), interactive=True)
            gr.HTML('<div class="lk-label" style="margin-top:16px;">What do you need?</div>')
            scope_radio = gr.Radio(show_label=False, choices=SCOPE_CHOICES, value=SCOPE_CHOICES[0])
            generate_btn = gr.Button("Generate →", variant="primary")

        # ── Screen 2: Generating ─────────────────────────────────────────
        with gr.Column(visible=False) as generating_screen:
            gr.HTML('<div class="lk-page-title">Feature Launch Kit</div>'
                    '<div class="lk-page-sub">Building your launch materials...</div>')
            status_html = gr.HTML(_status_html("Loading knowledge base...", False, 10))

        # ── Screen 3: Review ─────────────────────────────────────────────
        with gr.Column(visible=False) as review_screen:
            gr.HTML('<div class="lk-page-title">Review</div>')
            review_sub = gr.HTML(
                '<div class="lk-page-sub">Edit the text below if needed, then Pass to package it for download.</div>'
            )
            output_boxes = {}
            for key in SECTION_LABELS:
                with gr.Column(visible=False, elem_classes=["lk-card"]) as box_wrap:
                    gr.HTML(f'<div class="lk-card-header">{SECTION_LABELS[key]}</div>')
                    box = gr.Textbox(show_label=False, lines=12, max_lines=20, container=False)
                output_boxes[key] = (box_wrap, box)
            with gr.Row():
                fail_btn = gr.Button("✕ Fail — Regenerate", variant="secondary", elem_id="lk-fail-btn")
                pass_btn = gr.Button("✓ Pass", variant="primary")

        # ── Screen 4: Download ───────────────────────────────────────────
        with gr.Column(visible=False) as download_screen:
            gr.HTML('<div class="lk-page-title">Feature Launch Kit</div>')
            download_status = gr.HTML("")
            download_file = gr.File(label="Download", interactive=False)
            start_over_btn = gr.Button("Start over", variant="secondary", elem_id="lk-start-over-btn")

    # ── Wiring ───────────────────────────────────────────────────────────

    def on_generate_start(release):
        if not release:
            raise gr.Error("Select a release first.")
        return (
            gr.update(visible=False),                       # select_screen
            gr.update(visible=True),                         # generating_screen
            _step_dots_html("generating"),                   # header_html
            _status_html("Loading knowledge base...", False, 15),
        )

    def on_generate_progress():
        time.sleep(0.7)
        return _status_html("Generating content...", False, 65)

    def on_generate_run(release, scope_label):
        time.sleep(0.6)
        try:
            content = generate_kit(release, SCOPE_BY_LABEL[scope_label])
        except LLMError:
            logger.exception("generate_kit failed (all LLM providers down)")
            raise gr.Error("Generation failed — both LLM providers are unavailable. Try again shortly.")
        return _status_html("Done", True, 100), content

    def on_generate_finish(release, scope_label, content):
        time.sleep(0.4)
        return (
            gr.update(visible=False),   # generating_screen
            gr.update(visible=True),    # review_screen
            _step_dots_html("review"),  # header_html
            f'<div class="lk-page-sub">{len(content)} output(s) generated. '
            'Edit the text below if needed, then Pass to package it for download.</div>',
            *_box_updates(content),
            release,
            scope_label,
        )

    _box_outputs = [comp for pair in output_boxes.values() for comp in pair]

    generate_btn.click(
        on_generate_start,
        inputs=[release_dd],
        outputs=[select_screen, generating_screen, header_html, status_html],
        show_progress="hidden",
    ).then(
        on_generate_progress,
        outputs=[status_html],
        show_progress="hidden",
    ).then(
        on_generate_run,
        inputs=[release_dd, scope_radio],
        outputs=[status_html, state_content],
        show_progress="hidden",
    ).then(
        on_generate_finish,
        inputs=[release_dd, scope_radio, state_content],
        outputs=[generating_screen, review_screen, header_html, review_sub, *_box_outputs,
                 state_release, state_scope_label],
        show_progress="hidden",
    )

    def on_fail_start():
        return (
            gr.update(visible=False),   # review_screen
            gr.update(visible=True),    # generating_screen
            _step_dots_html("generating"),
            _status_html("Regenerating...", False, 20),
        )

    def on_fail_progress():
        time.sleep(0.6)
        return _status_html("Generating content...", False, 65)

    def on_fail_run(release, scope_label):
        time.sleep(0.5)
        # Higher temperature than the first pass so a regenerate reads
        # differently instead of nearly repeating the same phrasing.
        try:
            content = generate_kit(release, SCOPE_BY_LABEL[scope_label], temperature=1.0)
        except LLMError:
            logger.exception("generate_kit (regenerate) failed (all LLM providers down)")
            raise gr.Error("Regeneration failed — both LLM providers are unavailable. Try again shortly.")
        return _status_html("Done", True, 100), content

    def on_fail_finish(content):
        time.sleep(0.4)
        return (
            gr.update(visible=False),   # generating_screen
            gr.update(visible=True),    # review_screen
            _step_dots_html("review"),
            f'<div class="lk-page-sub">{len(content)} output(s) generated. '
            'Edit the text below if needed, then Pass to package it for download.</div>',
            *_box_updates(content),
        )

    fail_btn.click(
        on_fail_start,
        outputs=[review_screen, generating_screen, header_html, status_html],
        show_progress="hidden",
    ).then(
        on_fail_progress,
        outputs=[status_html],
        show_progress="hidden",
    ).then(
        on_fail_run,
        inputs=[state_release, state_scope_label],
        outputs=[status_html, state_content],
        show_progress="hidden",
    ).then(
        on_fail_finish,
        inputs=[state_content],
        outputs=[generating_screen, review_screen, header_html, review_sub, *_box_outputs],
        show_progress="hidden",
    )

    def on_pass_start():
        return (
            gr.update(visible=False),   # review_screen
            gr.update(visible=True),    # generating_screen
            _status_html("Rendering your launch kit...", False, 40),
        )

    def on_pass_render(release, scope_label, original_content, *box_values):
        time.sleep(0.5)
        # Use whatever's currently in each textbox (the user may have edited
        # it) for every key that was actually generated for this scope.
        edited_content = {
            key: box_values[i]
            for i, key in enumerate(SECTION_LABELS)
            if key in original_content
        }
        out_path = _render_quarto(release, scope_label, edited_content)
        return _status_html("Done", True, 100), out_path

    def on_pass_finish(release, scope_label, out_path):
        time.sleep(0.4)
        return (
            gr.update(visible=False),     # generating_screen
            gr.update(visible=True),      # download_screen
            _step_dots_html("download"),  # header_html
            ('<div class="lk-card" style="padding:40px 28px;text-align:center;">'
             '<div class="lk-success-badge">✓</div>'
             '<div style="font-size:18px;font-weight:700;margin-bottom:6px;">Your launch kit is ready</div>'
             f'<div style="font-size:13px;color:var(--lk-muted);">{_escape(scope_label)} · {_escape(release)}</div>'
             '</div>'),
            out_path,
        )

    pass_btn.click(
        on_pass_start,
        outputs=[review_screen, generating_screen, status_html],
        show_progress="hidden",
    ).then(
        on_pass_render,
        inputs=[state_release, state_scope_label, state_content,
                *[box for _, box in output_boxes.values()]],
        outputs=[status_html, state_out_path],
        show_progress="hidden",
    ).then(
        on_pass_finish,
        inputs=[state_release, state_scope_label, state_out_path],
        outputs=[generating_screen, download_screen, header_html, download_status, download_file],
        show_progress="hidden",
    )

    def on_start_over():
        return (
            gr.update(visible=True),    # select_screen
            gr.update(visible=False),   # download_screen
            _step_dots_html("select"),  # header_html
            None,
        )

    start_over_btn.click(
        on_start_over,
        outputs=[select_screen, download_screen, header_html, download_file],
    )


if __name__ == "__main__":
    demo.launch(
        css=THEME_CSS,
        theme=LK_THEME,
        allowed_paths=[str(LOGO_PATH)],
        inbrowser=True,
    )
