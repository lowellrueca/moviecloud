import uvicorn
from app import init_app
from app.config import PORT, HOST


if __name__ == "__main__":
    app = init_app()
    uvicorn.run(app, host=HOST, port=PORT)
