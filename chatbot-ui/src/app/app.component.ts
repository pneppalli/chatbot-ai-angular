import { Component } from '@angular/core';

interface ChatMessage {
  role: 'you' | 'bot';
  text: string;
}

@Component({
  selector: 'app-root',
  template: `
    <div class="page">
      <div class="shell">
        <main class="main">
          <div class="header">
            <div class="logo">CB</div>
            <div>
              <h1 class="title">Talksy</h1>
              <div class="subtitle">Simple, human, and always listening</div>
            </div>
          </div>

          <section
            class="conversation"
            id="log"
            role="log"
            aria-live="polite"
          >
            <div
              *ngFor="let m of messages"
              [ngClass]="{
                msg: true,
                you: m.role === 'you',
                bot: m.role === 'bot'
              }"
            >
              <div class="bubble">{{ m.text }}</div>
            </div>

            <div *ngIf="isTyping" class="msg bot">
              <div class="typing">
                <span class="dot"></span>
                <span class="dot"></span>
                <span class="dot"></span>
              </div>
            </div>
          </section>

          <form class="composer" (submit)="send($event)">
            <input
              #msgInput
              [(ngModel)]="message"
              name="message"
              autocomplete="off"
              placeholder="Type your message..."
              (keydown.enter)="send($event)"
            />
            <button type="submit" [disabled]="!message.trim() || sending">
              {{ sending ? 'Sending...' : 'Send' }}
            </button>
          </form>

          <div class="footer small">
            Local dev: POSTs go to http://127.0.0.1:8000/chat
          </div>
        </main>

        <aside class="sidebar">
          <h3>Quick tips</h3>
          <div class="hint">
            Simple. Focused. Experimental. A demo environment to test the rhythm
            of conversation.
          </div>
          <div class="small">A glimpse into minimal conversation.</div>
        </aside>
      </div>
    </div>
  `
})
export class AppComponent {
  message = '';
  messages: ChatMessage[] = [];
  sending = false;
  isTyping = false;

  private append(role: ChatMessage['role'], text: string) {
    this.messages.push({ role, text });
    setTimeout(() => this.scrollLog(), 50);
  }

  private scrollLog() {
    const log = document.getElementById('log');
    if (log) log.scrollTop = log.scrollHeight;
  }

  async send(e: Event) {
    e.preventDefault();

    const text = this.message.trim();
    if (!text) return;

    this.append('you', text);
    this.message = '';
    this.sending = true;
    this.isTyping = true;

    try {
      const res = await fetch('http://127.0.0.1:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text })
      });

      const j = await res.json();

      if (res.ok) {
        // simulate a small delay for typing effect
        await new Promise((r) => setTimeout(r, 250));
        this.append('bot', j.reply || JSON.stringify(j));
      } else {
        this.append('bot', 'Error: ' + (j.detail || JSON.stringify(j)));
      }
    } catch (err: any) {
      this.append('bot', 'Network error: ' + (err?.message || String(err)));
    } finally {
      this.isTyping = false;
      this.sending = false;
    }
  }
}
