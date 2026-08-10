# Import Flask tools

from flask import (
    Blueprint,
    render_template,
    request,
    jsonify
)


# ----------------------------------
# Create Chatbot Blueprint
# ----------------------------------

chatbot = Blueprint(
    "chatbot",
    __name__,
    url_prefix="/chatbot"
)


# ==================================
# APPLICATION KNOWLEDGE
# ==================================

def get_response(message):

    message = message.lower().strip()


    # ----------------------------------
    # Greeting
    # ----------------------------------

    if any(word in message for word in [
        "hello",
        "hi",
        "hey"
    ]):

        return (
            "Hello! 👋 I am the Application Assistant. "
            "I can help you understand and use the "
            "Voting and Election Management System."
        )


    # ----------------------------------
    # Create Election
    # ----------------------------------

    if (
        "create election" in message
        or "new election" in message
        or "add election" in message
    ):

        return (
            "To create an election, open Election Management "
            "from the Admin Dashboard and select Create Election. "
            "Enter the election title, description, start date, "
            "start time, end date, end time and election type."
        )


    # ----------------------------------
    # Edit Election
    # ----------------------------------

    if (
        "edit election" in message
        or "update election" in message
    ):

        return (
            "To edit an election, open View Elections from the "
            "Admin Dashboard and select the Edit option for "
            "the required election."
        )


    # ----------------------------------
    # Add Candidate
    # ----------------------------------

    if (
        "add candidate" in message
        or "create candidate" in message
        or "register candidate" in message
    ):

        return (
            "To add a candidate, open Candidate Management "
            "and select Add Candidate. Select the election "
            "and enter the candidate's name, age, gender, "
            "party, education, profession and manifesto."
        )


    # ----------------------------------
    # Edit Candidate
    # ----------------------------------

    if (
        "edit candidate" in message
        or "update candidate" in message
    ):

        return (
            "To edit a candidate, open View Candidates and "
            "select Edit for the candidate you want to update."
        )


    # ----------------------------------
    # Delete Candidate
    # ----------------------------------

    if (
        "delete candidate" in message
        or "remove candidate" in message
    ):

        return (
            "To delete a candidate, open View Candidates "
            "and select Delete for the required candidate."
        )


    # ----------------------------------
    # Position
    # ----------------------------------

    if "position" in message:

        return (
            "Position is used for multiple-position elections. "
            "For a single-position election, a candidate position "
            "is not required."
        )


    # ----------------------------------
    # Voting
    # ----------------------------------

    if (
        "how to vote" in message
        or "how does voting work" in message
        or "vote" in message
    ):

        return (
            "Users can participate in an active election and "
            "cast their vote for a candidate. The system verifies "
            "the user's account and prevents the same user from "
            "voting more than once in the same election."
        )


    # ----------------------------------
    # Vote Twice
    # ----------------------------------

    if (
        "vote twice" in message
        or "multiple votes" in message
        or "vote again" in message
    ):

        return (
            "No. The system is designed to allow one vote per "
            "registered user for each election."
        )


    # ----------------------------------
    # Election Status
    # ----------------------------------

    if (
        "election status" in message
        or "active election" in message
        or "upcoming election" in message
    ):

        return (
            "An election can have different statuses based on "
            "its scheduled start and end time: Upcoming, Active "
            "or Completed."
        )


    # ----------------------------------
    # Results
    # ----------------------------------

    if (
        "result" in message
        or "results" in message
        or "winner" in message
    ):

        return (
            "Election results can be viewed from the Election "
            "Results section of the Admin Dashboard. The results "
            "display candidate vote counts and the final outcome."
        )


    # ----------------------------------
    # Admin Dashboard
    # ----------------------------------

    if (
        "admin dashboard" in message
        or "dashboard" in message
    ):

        return (
            "The Admin Dashboard is the central control area "
            "for managing elections, candidates and official "
            "election results."
        )


    # ----------------------------------
    # Help
    # ----------------------------------

    if (
        "help" in message
        or "what can you do" in message
    ):

        return (
            "I can help you with Elections, Candidates, Voting, "
            "Election Status, Results, the Admin Dashboard and "
            "other features of this application."
        )


    # ----------------------------------
    # Unknown Question
    # ----------------------------------

    return (
        "I'm sorry, I can answer questions only about this "
        "Voting and Election Management System. "
        "Try asking about elections, candidates, voting, "
        "results or the Admin Dashboard."
    )


# ==================================
# CHATBOT PAGE
# ==================================

@chatbot.route("/")
def chatbot_page():

    return render_template(
        "chatbot/chatbot.html"
    )


# ==================================
# CHATBOT RESPONSE
# ==================================

@chatbot.route(
    "/ask",
    methods=["POST"]
)
def ask():

    data = request.get_json()

    message = data.get(
        "message",
        ""
    ).strip()


    if not message:

        return jsonify({
            "response":
                "Please enter a question."
        })


    response = get_response(
        message
    )


    return jsonify({
        "response": response
    })