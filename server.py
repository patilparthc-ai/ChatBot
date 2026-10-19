import http.server
import socketserver
import json
import chatbot  # Imports your existing chatbot.py without modifying it

PORT = 8000

class ChatbotHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Endpoint to check if Gemini API mode is ON or OFF
        if self.path == '/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            api_status = "ON" if chatbot.client else "OFF"
            self.wfile.write(json.dumps({"api_mode": api_status}).encode('utf-8'))
        else:
            # Serves index.html and style.css automatically
            super().do_GET()

    def do_POST(self):
        if self.path == '/chat':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            user_text = data.get("message", "").strip()

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            # Replicate the exact exit check from chatbot.py
            if user_text.lower() in ("quit", "exit"):
                response = {
                    "source": "System",
                    "reply": "Bye!",
                    "confidence": 1.0,
                    "ended": True
                }
            else:
                # Call get_reply() directly from your unmodified chatbot.py
                source, reply, conf = chatbot.get_reply(user_text)
                response = {
                    "source": source,
                    "reply": reply,
                    "confidence": round(float(conf), 2),
                    "ended": False
                }

            self.wfile.write(json.dumps(response).encode('utf-8'))

if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), ChatbotHandler) as httpd:
        print(f"✅ Frontend Server started! Open http://localhost:{PORT} in your browser.")
        print("Press Ctrl+C in the terminal to stop the server.")
        httpd.serve_forever()