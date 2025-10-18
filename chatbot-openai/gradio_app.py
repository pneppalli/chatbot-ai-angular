import os
import traceback
from typing import List, Tuple, Optional, Dict, Any

import gradio as gr

from app import make_openai_client, get_api_key, _extract_chat_content


def _build_messages_from_history(history: Optional[List[Any]]) -> List[dict]:
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    if not history:
        return messages

    if isinstance(history, list) and len(history) > 0 and isinstance(history[0], (list, tuple)):
        for user, assistant in history:
            messages.append({"role": "user", "content": user})
            if assistant:
                messages.append({"role": "assistant", "content": assistant})
        return messages

    for item in history:
        try:
            role = item.get("role") if isinstance(item, dict) else None
            content = item.get("content") if isinstance(item, dict) else None
        except Exception:
            role = None
            content = None
        if role and content is not None:
            messages.append({"role": role, "content": content})
    return messages


def handle_message(user_message: str, history: Optional[List[Dict[str, Any]]], mode: str, model: str, temperature: float = 0.7):
    if history is None:
        history = []

    try:
        try:
            get_api_key()
        except Exception as e:
            history.append({"role": "user", "content": user_message})
            history.append({"role": "assistant", "content": f"ERROR: {e}"})
            return history, ""

        client = make_openai_client()

        if mode == "basic":
            prompt_parts = []
            if len(history) > 0 and isinstance(history[0], (list, tuple)):
                for u, a in history:
                    prompt_parts.append(f"User: {u}")
                    if a:
                        prompt_parts.append(f"Assistant: {a}")
            else:
                for item in history:
                    if not isinstance(item, dict):
                        continue
                    r = item.get("role")
                    c = item.get("content", "")
                    if r == "user":
                        prompt_parts.append(f"User: {c}")
                    elif r == "assistant":
                        prompt_parts.append(f"Assistant: {c}")

            prompt_parts.append(f"User: {user_message}")
            prompt_parts.append("Assistant:")
            prompt = "\n".join(prompt_parts)

            if hasattr(client, "completions"):
                resp = client.completions.create(model=model or "text-davinci-003", prompt=prompt, max_tokens=300, temperature=temperature)
            else:
                import openai
                resp = openai.Completion.create(model=model or "text-davinci-003", prompt=prompt, max_tokens=300, temperature=temperature)

            reply = _extract_chat_content(resp).strip()

        else:
            messages = _build_messages_from_history(history)
            messages.append({"role": "user", "content": user_message})

            if hasattr(client, "chat"):
                resp = client.chat.completions.create(model=model or "gpt-3.5-turbo", messages=messages, temperature=temperature)
            else:
                import openai
                resp = openai.ChatCompletion.create(model=model or "gpt-3.5-turbo", messages=messages, temperature=temperature)

            reply = _extract_chat_content(resp).strip()

        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": reply})
        return history, ""

    except Exception as exc:
        tb = traceback.format_exc()
        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": f"ERROR: {exc}\n{tb}"})
        return history, ""


def launch_ui():
    css = """
    :root { --bg-1: #0f172a; --bg-2: #071033; --card: #0b1220; --muted:#94a3b8; --accent: #3b82f6; }
    body { background: linear-gradient(180deg, var(--bg-1) 0%, var(--bg-2) 100%); color: #e6eef8; font-family: Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial; }

    /* Overall container */
    .gradio-container { width:95%; max-width:1600px; margin: 18px auto; height: calc(100vh - 36px); display:flex; flex-direction:column; }

    /* Chatbox */
    #chatbox {
        width: 100% !important;
        max-width: none !important;
        flex: 1 1 auto;
        display: flex;
        flex-direction: column;
        min-height: 300px;
        max-height: calc(100vh - 120px);
        margin: 0 auto;
    }

    #chatbox .scroll-area, #chatbox .gr-scrollable, #chatbox .messages { overflow:auto; }
    .chatbox .user, .chatbox .assistant { max-width: 95% !important; }

    /* Input row */
    #input-row { display:flex; gap:8px; align-items:center; margin-top:8px }
    #input-row > div:first-child { flex:1 1 auto; min-width:0 }
    #input-box textarea, #input-box input { width:100% !important; }

    /* Send button smaller */
    #send-btn .gr-button, #send-btn button {
        background: linear-gradient(90deg, var(--accent), #1e40af);
        color: #fff;
        border: none;
        height:36px;
        padding: 0 8px;
        width:50px; /* reduced width */
        border-radius:10px;
        box-shadow: 0 6px 18px rgba(16,24,40,0.35);
        font-weight:600;
        font-size:13px;
    }
    #send-btn .gr-button:hover, #send-btn button:hover { filter:brightness(1.03); transform:translateY(-1px); }

    .footer { text-align:center; color:var(--muted); font-size:12px; margin-top:8px }

    @media (max-width:900px) {
        .gradio-container { padding:8px }
        #chatbox { max-height: calc(100vh - 100px); }
    }
    """

    theme = gr.themes.Soft()
    with gr.Blocks(theme=theme, css=css, title="Local OpenAI Chatbot") as demo:

        # Main chat area only
        with gr.Column(elem_id="main", variant="compact"):
            chatbot = gr.Chatbot(elem_id="chatbox", label="Conversation", type="messages")
            with gr.Row(elem_id="input-row"):
                txt = gr.Textbox(show_label=False, placeholder="Ask a question... Press Enter to send", lines=2, elem_id="input-box")
                send = gr.Button("Send", elem_id="send-btn")

        def submit(msg, history):
            return handle_message(msg, history, "chat", "gpt-3.5-turbo", temperature=0.7)

        send.click(fn=submit, inputs=[txt, chatbot], outputs=[chatbot, txt])
        txt.submit(fn=submit, inputs=[txt, chatbot], outputs=[chatbot, txt])

        def do_clear():
            return []

        # Optional: Clear chat button
        clear = gr.Button("Clear Chat")
        clear.click(fn=do_clear, outputs=[chatbot])

        # Footer only
        gr.Markdown("<div class='footer'>UI version: clean-theme-2025-10-18 — running locally on 127.0.0.1:7860</div>")

        # JS: Enter submits (unless Shift+Enter)
        gr.HTML("""
        <script>
        (function(){
          function attach() {
            const wrapper = document.querySelector('#input-box');
            const sendButton = document.querySelector('#send-btn button, #send-btn .gr-button');
            if(!wrapper || !sendButton) return;
            const ta = wrapper.querySelector('textarea, input');
            if(!ta) return;
            if(ta._enterSubmitAttached) return;
            ta._enterSubmitAttached = true;
            ta.addEventListener('keydown', function(e){
              if(e.key === 'Enter' && !e.shiftKey){
                e.preventDefault();
                sendButton.click();
              }
            });
          }
          setTimeout(attach, 300);
          const obs = new MutationObserver(function(){ attach(); });
          obs.observe(document.body, { childList: true, subtree: true });
        })();
        </script>
        """)

    demo.launch(server_name="127.0.0.1", server_port=7860, share=False)


if __name__ == "__main__":
    launch_ui()
