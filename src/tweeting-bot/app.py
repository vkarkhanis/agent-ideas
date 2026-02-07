import gradio as gr
from agent import generate_short_form_tweets, generate_long_form_tweet
from tools.input_validator import validate_subject
from tools.whatsapp_share import whatsapp_share_url

# ---------------- Logic ----------------

def generate_short(subject):
    valid, message = validate_subject(subject)
    if not valid:
        return gr.update(choices=[]), message

    tweets = generate_short_form_tweets(subject)
    return gr.update(choices=tweets, value=None), ""

def generate_long(subject):
    valid, message = validate_subject(subject)
    if not valid:
        return "", message

    return generate_long_form_tweet(subject), ""

def copy_and_open_x(tweet):
    if not tweet:
        return ""
    return gr.HTML("""
    <script>
        navigator.clipboard.writeText(%r);
        window.open("https://x.com/compose/tweet", "_blank");
    </script>
    """ % tweet)

def send_to_whatsapp(tweet):
    if not tweet:
        return ""
    return gr.HTML(
        f'<a href="{whatsapp_share_url(tweet)}" target="_blank">'
        '💬 Send to WhatsApp</a>'
    )

def toggle_generate_buttons(text):
    enabled = bool(text.strip())
    return (
        gr.update(interactive=enabled),
        gr.update(interactive=enabled)
    )

def toggle_short_action_buttons(selected_tweet):
    enabled = bool(selected_tweet)
    return (
        gr.update(interactive=enabled),
        gr.update(interactive=enabled)
    )

def toggle_long_action_buttons(text):
    enabled = bool(text.strip())
    return (
        gr.update(interactive=enabled),
        gr.update(interactive=enabled)
    )

# ---------------- UI ----------------

with gr.Blocks(theme=gr.themes.Soft()) as app:
    gr.Markdown("""
    ## 🧠 Software Engineering Tweet Assistant

    Generate **professional, high-quality tweets** for experienced software engineers.
    """)

    subject = gr.Textbox(
        label="Tweet Topic (Software Engineering only)",
        placeholder="e.g. Tricky Java concurrency interview questions",
        max_lines=4
    )

    error_box = gr.Markdown("", visible=True)

    generate_btn = gr.Button("Generate Short Tweets", interactive=False)
    long_btn = gr.Button("Generate Long Tweet", interactive=False)

    gr.Markdown("### 🔹 Short Tweets (Unverified Account Style)")
    short_tweets = gr.Radio(label="Select a tweet", choices=[])

    short_copy_btn = gr.Button("📋 Copy & Open X", interactive=False)
    short_whatsapp_btn = gr.Button("💬 Send to WhatsApp", interactive=False)

    gr.Markdown("### 🔹 Long Tweet (Verified Account Style)")
    long_tweet = gr.Textbox(lines=6, label="Long-form Tweet")

    long_copy_btn = gr.Button("📋 Copy & Open X", interactive=False)
    long_whatsapp_btn = gr.Button("💬 Send to WhatsApp", interactive=False)

    action_output = gr.HTML()

    subject.change(
        # lambda x: gr.update(interactive=bool(x.strip())),
        toggle_generate_buttons,
        subject,
        outputs=[generate_btn, long_btn]
    )

    short_tweets.change(
        toggle_short_action_buttons,
        short_tweets,
        outputs=[short_copy_btn, short_whatsapp_btn]
    )

    long_tweet.change(
        toggle_long_action_buttons,
        long_tweet,
        outputs=[long_copy_btn, long_whatsapp_btn]
    )

    generate_btn.click(
        generate_short,
        subject,
        outputs=[short_tweets, error_box]
    )

    long_btn.click(
        generate_long,
        subject,
        outputs=[long_tweet, error_box]
    )

    short_copy_btn.click(
        fn=None,
        inputs=short_tweets,
        outputs=None,
        js="""
        (tweet) => {
            if (!tweet) {
                alert("Please select a tweet first.");
                return;
            }
            navigator.clipboard.writeText(tweet);
            window.open("https://x.com/compose/tweet", "_blank");
        }
        """
    )
    short_whatsapp_btn.click(
        fn=None,
        inputs=short_tweets,
        outputs=None,
        js="""
        (tweet) => {
            if (!tweet) {
                alert("Please select a tweet first.");
                return;
            }
            const url =
              "https://wa.me/?text=" + encodeURIComponent(tweet);
            window.open(url, "_blank");
        }
        """
    )

    long_copy_btn.click(
        fn=None,
        inputs=long_tweet,
        outputs=None,
        js="""
        (tweet) => {
            if (!tweet) {
                alert("Please generate a tweet first.");
                return;
            }
            navigator.clipboard.writeText(tweet);
            window.open("https://x.com/compose/tweet", "_blank");
        }
        """
    )
    long_whatsapp_btn.click(
        fn=None,
        inputs=long_tweet,
        outputs=None,
        js="""
        (tweet) => {
            if (!tweet) {
                alert("Please generate a tweet first.");
                return;
            }
            const url =
              "https://wa.me/?text=" + encodeURIComponent(tweet);
            window.open(url, "_blank");
        }
        """
    )

if __name__ == "__main__":
    app.launch(share=True)
