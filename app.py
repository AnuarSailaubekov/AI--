from flask import Flask, render_template, request
import concurrent.futures
from dotenv import load_dotenv

load_dotenv()

from emotions import analyze_emotion
from recommendations import get_recommendations
from thinking import analyze_thinking
from graph import generate_emotion_graph

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form.get("user_text", "")

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_emotion = executor.submit(analyze_emotion, text)
            future_thinking = executor.submit(analyze_thinking, text)
            future_graph = executor.submit(generate_emotion_graph, text)

            emotion_response = future_emotion.result()
            thinking_analysis = future_thinking.result()
            graph_url = future_graph.result()

        advice, music = get_recommendations(emotion_response)

        return render_template("index.html", 
                               user_text=text, 
                               emotion=emotion_response, 
                               advice=advice, 
                               music=music, 
                               thinking=thinking_analysis, 
                               graph_url=graph_url)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)