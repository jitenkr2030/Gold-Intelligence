from fastapi import FastAPI, Request


app = FastAPI(
    title="Gold Webhook Test Receiver"
)


@app.post("/webhook")
async def receive_webhook(request: Request):

    payload = await request.json()

    print(
        "WEBHOOK RECEIVED:",
        payload
    )

    return {
        "success": True,
        "received": True,
        "payload": payload
    }
