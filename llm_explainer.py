import google.generativeai as genai

genai.configure(api_key="AIzaSyABPv9sph7CBrFk2380yUISi_VGqCrHl6w")

model = genai.GenerativeModel("gemini-3-flash-preview")


def explain_strategy(stats_text):

    prompt = f"""
You are an IPL cricket strategy expert.

Based on the statistical insights below:

1. Analyse head-to-head performance
2. Recommend who should bowl or bat
3. Explain strengths & weaknesses
4. Provide tactical match advice
5. Give captaincy strategy

Statistical Data:
{stats_text}

Give detailed but simple cricket explanation.
"""

    response = model.generate_content(prompt)

    return response.text
