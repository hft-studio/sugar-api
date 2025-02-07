import uvicorn

if __name__ == "__main__":
    uvicorn.run("sugar_api.api:app", host="0.0.0.0", port=5000, workers=4)
