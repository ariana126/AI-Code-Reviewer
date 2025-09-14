from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
from dotenv import load_dotenv
from app.src.domain.review.result import ReviewResult
from app.src.domain.review.service.reviewer import Reviewer
from app.src.infrastructure.n8n.sdk import N8nClient, N8nSDK
from app.src.user_case.on_demand_review import ReviewOnDemandCommandHandler, ReviewOnDemandCommand

# TODO: Make use of service registry
load_dotenv()
N8n_BASE_URL = os.getenv("N8N_BASE_URL")
N8N_CODE_REVIEWER_WEBHOOK_PATH: str = os.getenv("N8N_CODE_REVIEWER_WEBHOOK_PATH")


class SimpleHandler(BaseHTTPRequestHandler):
    # TODO: Make use of service registry
    def get_command_handler(self) -> ReviewOnDemandCommandHandler:
        n8n_sdk: N8nSDK = N8nSDK(N8n_BASE_URL)
        n8n_client: N8nClient = N8nClient(n8n_sdk, N8N_CODE_REVIEWER_WEBHOOK_PATH)
        reviewer: Reviewer = Reviewer(n8n_client)
        return ReviewOnDemandCommandHandler(reviewer)

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
            command_handler: ReviewOnDemandCommandHandler = self.get_command_handler()

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
    server = HTTPServer(('0.0.0.0', 8080), SimpleHandler)
    server.serve_forever()

if __name__ == "__main__":
    main()