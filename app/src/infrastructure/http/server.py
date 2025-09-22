from fastapi import FastAPI, HTTPException, Request

from pydm import ServiceContainer

from app.src.infrastructure.boot import boot
from app.src.domain.review.result import ReviewResult
from app.src.user_case.on_demand_review import ReviewOnDemandCommandHandler, ReviewOnDemandCommand

app = FastAPI()

@app.post("/on-demand-review")
async def on_demand_review(request: Request):
    try:
        command_handler: ReviewOnDemandCommandHandler = ServiceContainer.get_instance().get_service(
            ReviewOnDemandCommandHandler)

        data = await request.json()
        command: ReviewOnDemandCommand = ReviewOnDemandCommand.from_json(data)

        result: ReviewResult = command_handler.execute(command)

        return {
            "status": "success",
            "issues": result.issues
        }
    except Exception as e:
        print(f"Internal Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Error")

def main():
    print("Starting HTTP POST server on port 8080.")
    boot()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()