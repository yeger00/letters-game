from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import random
from typing import Optional

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

hebrew_letters = [
    {"letter": "א", "name": "Aleph", "sound": "hebrew_letters/א.mp3"},
    {"letter": "ב", "name": "Bet", "sound": "hebrew_letters/ב.mp3"},
    {"letter": "ג", "name": "Gimel", "sound": "hebrew_letters/ג.mp3"},
    {"letter": "ד", "name": "Dalet", "sound": "hebrew_letters/ד.mp3"},
    {"letter": "ה", "name": "He", "sound": "hebrew_letters/ה.mp3"},
    {"letter": "ו", "name": "Vav", "sound": "hebrew_letters/ו.mp3"},
    {"letter": "ז", "name": "Zayin", "sound": "hebrew_letters/ז.mp3"},
    {"letter": "ח", "name": "Chet", "sound": "hebrew_letters/ח.mp3"},
    {"letter": "ט", "name": "Tet", "sound": "hebrew_letters/ט.mp3"},
    {"letter": "י", "name": "Yod", "sound": "hebrew_letters/י.mp3"},
    {"letter": "כ", "name": "Kaf", "sound": "hebrew_letters/כ.mp3"},
    {"letter": "ך", "name": "Kaf Sofit", "sound": "hebrew_letters/ך.mp3"},
    {"letter": "ל", "name": "Lamed", "sound": "hebrew_letters/ל.mp3"},
    {"letter": "מ", "name": "Mem", "sound": "hebrew_letters/מ.mp3"},
    {"letter": "ם", "name": "Mem Sofit", "sound": "hebrew_letters/ם.mp3"},
    {"letter": "נ", "name": "Nun", "sound": "hebrew_letters/נ.mp3"},
    {"letter": "ן", "name": "Nun Sofit", "sound": "hebrew_letters/ן.mp3"},
    {"letter": "ס", "name": "Samekh", "sound": "hebrew_letters/ס.mp3"},
    {"letter": "ע", "name": "Ayin", "sound": "hebrew_letters/ע.mp3"},
    {"letter": "פ", "name": "Pe", "sound": "hebrew_letters/פ.mp3"},
    {"letter": "ף", "name": "Pe Sofit", "sound": "hebrew_letters/ף.mp3"},
    {"letter": "צ", "name": "Tsadi", "sound": "hebrew_letters/צ.mp3"},
    {"letter": "ץ", "name": "Tsadi Sofit", "sound": "hebrew_letters/ץ.mp3"},
    {"letter": "ק", "name": "Qof", "sound": "hebrew_letters/ק.mp3"},
    {"letter": "ר", "name": "Resh", "sound": "hebrew_letters/ר.mp3"},
    {"letter": "ש", "name": "Shin", "sound": "hebrew_letters/ש.mp3"},
    {"letter": "ת", "name": "Tav", "sound": "hebrew_letters/ת.mp3"},
]

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/mode1", response_class=HTMLResponse)
async def mode1(request: Request, order: str = "random", index: int = 0):
    if order == "alphabetical":
        if index >= len(hebrew_letters) or index < 0:
            index = 0
        letter = hebrew_letters[index]
        next_index = (index + 1) % len(hebrew_letters)
        return templates.TemplateResponse(
            "mode1.html",
            {
                "request": request,
                "letter": letter,
                "order": "alphabetical",
                "next_index": next_index,
            },
        )
    else:  # random
        letter = random.choice(hebrew_letters)
        return templates.TemplateResponse(
            "mode1.html",
            {"request": request, "letter": letter, "order": "random"},
        )

@app.get("/mode2", response_class=HTMLResponse)
async def mode2(request: Request, progress: int = 0):
    letters = random.sample(hebrew_letters, 4)
    correct_letter = random.choice(letters)

    game_html = templates.get_template("mode2.html").render(
        {
            "request": request,
            "letters": letters,
            "correct_letter": correct_letter,
            "progress": progress,
        }
    )

    progress_html = templates.get_template("progress.html").render(
        {"request": request, "progress": progress}
    )

    html = f"""
    {game_html}
    <div id="progress-container" hx-swap-oob="true">{progress_html}</div>
    """
    return HTMLResponse(content=html)

@app.post("/check_answer", response_class=HTMLResponse)
async def check_answer(
    request: Request,
    letter: str = Form(...),
    correct_letter: str = Form(...),
    progress: int = Form(...),
    loop_index: int = Form(...),
):
    if letter == correct_letter:
        new_progress = progress + 1

        progress_bar_html = templates.get_template("progress.html").render(
            {"request": request, "progress": new_progress}
        )

        answered_button_html = templates.get_template(
            "partials/answered_quiz_button.html"
        ).render(
            {
                "request": request,
                "letter_char": letter,
                "is_correct": True,
                "loop_index": loop_index,
            }
        )

        next_button_html = templates.get_template("partials/next_button.html").render(
            {"request": request, "progress": new_progress}
        )

        html = f"""
        {answered_button_html}
        <div id="progress-container" hx-swap-oob="true">{progress_bar_html}</div>
        <div id="next-question-button-container" hx-swap-oob="true">{next_button_html}</div>
        """
        return HTMLResponse(content=html)
    else:
        answered_button_html = templates.get_template(
            "partials/answered_quiz_button.html"
        ).render(
            {
                "request": request,
                "letter_char": letter,
                "is_correct": False,
                "loop_index": loop_index,
            }
        )
        return HTMLResponse(content=answered_button_html) 