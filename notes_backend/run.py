from app import app

if __name__ == "__main__":
    # Run on port 3001 for the preview environment, accessible externally.
    app.run(host="0.0.0.0", port=3001)
