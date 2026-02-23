# final_project/server.py
from __future__ import annotations

from flask import Flask, render_template, request

from EmotionDetection import emotion_detector

# templates/ and static/ are in the repo root (one level above final_project/)
app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static",
    static_url_path="/static",
)


@app.get("/")
def index():
    return render_template("index.html")


# REQUIRED: decorator path must be /emotionDetector
@app.get("/emotionDetector")
def emotion_detector_route():
    text_to_analyze = request.args.get("textToAnalyze", "").strip()
    if not text_to_analyze:
        return "Invalid text! Please try again!", 400

    result = emotion_detector(text_to_analyze)

    anger = result["anger"]
    disgust = result["disgust"]
    fear = result["fear"]
    joy = result["joy"]
    sadness = result["sadness"]
    dominant = result["dominant_emotion"]

    return (
        "For the given statement, the system response is "
        f"'anger': {anger}, 'disgust': {disgust}, 'fear': {fear}, "
        f"'joy': {joy} and 'sadness': {sadness}. "
        f"The dominant emotion is {dominant}."
    )


def main() -> None:
    app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == "__main__":
    main()