from app.src.infrastructure.boot import boot
from pydm import ServiceContainer
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
from dotenv import load_dotenv
from app.src.domain.review.result import ReviewResult
from app.src.domain.review.service.reviewer import Reviewer
from app.src.infrastructure.n8n.sdk import N8nClient, N8nSDK
from app.src.user_case.on_demand_review import ReviewOnDemandCommandHandler, ReviewOnDemandCommand


class SimpleHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Route handling
        if self.path != "/on-demand-review":
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not Found"}).encode('utf-8'))
            return

        # Read request body
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)

        try:
            command_handler: ReviewOnDemandCommandHandler = ServiceContainer.get_instance().get_service(ReviewOnDemandCommandHandler)

            # Parse JSON payload
            data = json.loads(post_data.decode('utf-8'))
            command: ReviewOnDemandCommand = ReviewOnDemandCommand.from_json(data)
            result: ReviewResult = command_handler.execute(command)

            response = {
                "status": "success",
                "issues": result.issues
            }
            self.send_response(200)
        except json.JSONDecodeError:
            response = {
                "status": "error",
                "message": "Invalid JSON"
            }
            self.send_response(400)
        except Exception:
            response = {
                "status": "error",
                "message": "Internal Error"
            }
            self.send_response(500)

        # Send headers and response
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))

def main():
    print("Starting HTTP POST server on port 8080 at /on-demand-review")
    boot()
    server = HTTPServer(('0.0.0.0', 8080), SimpleHandler)
    server.serve_forever()

if __name__ == "__main__":
    main()