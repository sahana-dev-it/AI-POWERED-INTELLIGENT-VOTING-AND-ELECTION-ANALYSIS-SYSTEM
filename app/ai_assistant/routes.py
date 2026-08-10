# =========================================
# AI ASSISTANT ROUTES
# =========================================

from flask import (
    Blueprint,
    render_template,
    request
)


# =========================================
# AI ASSISTANT BLUEPRINT
# =========================================

ai_assistant = Blueprint(
    "ai_assistant",
    __name__,
    url_prefix="/ai-assistant"
)


# =========================================
# AI ASSISTANT CHAT
# =========================================

@ai_assistant.route(
    "/chat",
    methods=["GET", "POST"]
)
def chat():

    response = None

    if request.method == "POST":

        question = request.form.get(
            "question",
            ""
        ).strip()

        if question:

            # ---------------------------------
            # Temporary response
            # ---------------------------------
            # Actual chatbot logic will be added
            # later.
            # ---------------------------------

            response = (
                "The Election AI Assistant is ready. "
                "AI chatbot functionality will be "
                "connected here."
            )

    return render_template(
        "ai_assistant/chat.html",
        response=response
    )