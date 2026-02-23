"""Flask server for the EmotionDetection application.

Routes:
- GET /                : serves the UI (templates/index.html)
- GET /emotionDetector : returns formatted emotion analysis text
"""

from __future__ import annotations

from pathlib import Path

from flask import Flask, render_template, request

from EmotionDetection import emotion_detector

REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATES_DIR = REPO_ROOT / "templates"
STATIC_DIR = REPO_ROOT / "static"

app = Flask(
    __name__,
    template_folder=str(TEMPLATES_DIR),
    static_folder=str(STATIC_DIR),
    static_url_path="/static",
)


@app.get("/")
def index() -> str:
    """Serve the application UI."""
    return render_template("index.html")


@app.get("/emotionDetector")
def emotion_detector_route() -> str:
    """Analyze query text and return a formatted response string."""
    text_to_analyze = request.args.get("textToAnalyze", "").strip()

    if not text_to_analyze:
        return "Invalid text! Please try again!"

    result = emotion_detector(text_to_analyze)
    dominant = result.get("dominant_emotion")
    if dominant is None:
        return "Invalid text! Please try again!"

    return (
        "For the given statement, the system response is "
        f"'anger': {result['anger']}, 'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, 'joy': {result['joy']} and "
        f"'sadness': {result['sadness']}. "
        f"The dominant emotion is {dominant}."
    )


def main() -> None:
    """Run the Flask development server on localhost:5000."""
    app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == "__main__":
    main()