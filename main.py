# bot.py
import uvicorn

# Run the application with Uvicorn
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=9001, reload=True)