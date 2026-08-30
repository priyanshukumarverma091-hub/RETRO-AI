
from flask import Flask, render_template, request, jsonify
import mysql.connector
import time

from phase2 import MultiAgentSystem


# ============================================================
# FLASK APPLICATION
# ============================================================

app = Flask(__name__)


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "RetroAI@123"
DB_NAME = "multi_agent_db"


# ============================================================
# MULTI-AGENT ENGINE
# ============================================================

try:
    multi_agent = MultiAgentSystem()
    ENGINE_READY = True
except Exception as error:
    print("PHASE 2 ERROR:", error)
    multi_agent = None
    ENGINE_READY = False


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():

    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )


# ============================================================
# CREATE CHAT SESSION
# ============================================================

def create_session(title):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO chat_sessions
            (title)
            VALUES (%s)
            """,
            (title,)
        )

        connection.commit()

        return cursor.lastrowid

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ============================================================
# SAVE MESSAGE
# ============================================================

def save_message(
    session_id,
    role,
    content,
    agent=None
):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO messages
            (
                session_id,
                role,
                content,
                agent
            )
            VALUES (%s, %s, %s, %s)
            """,
            (
                session_id,
                role,
                content,
                agent
            )
        )

        connection.commit()

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ============================================================
# SAVE AGENT LOG
# ============================================================

def save_agent_log(
    session_id,
    agent_name,
    task,
    result,
    status,
    execution_time
):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO agent_logs
            (
                session_id,
                agent_name,
                task,
                result,
                status,
                execution_time_ms
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                session_id,
                agent_name,
                task,
                result,
                status,
                execution_time
            )
        )

        connection.commit()

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/api/health")
def health():

    connection = None

    try:

        connection = get_connection()

        database_status = "connected"

        engine_status = (
            "connected"
            if ENGINE_READY
            else "disconnected"
        )

        return jsonify({

            "success": True,

            "status": "online",

            "database": database_status,

            "brain": engine_status,

            "phase2": engine_status,

            "system": "RETRO-AI"

        })

    except Exception as error:

        return jsonify({

            "success": False,

            "status": "offline",

            "database": "disconnected",

            "brain": "unknown",

            "phase2": "unknown",

            "error": str(error)

        }), 500

    finally:

        if connection:
            connection.close()


# ============================================================
# CHAT API
# ============================================================

@app.route(
    "/api/chat",
    methods=["POST"]
)
def chat():

    data = request.get_json(
        silent=True
    ) or {}

    message = str(
        data.get(
            "message",
            ""
        )
    ).strip()

    session_id = data.get(
        "session_id"
    )

    # --------------------------------------------------------
    # VALIDATE MESSAGE
    # --------------------------------------------------------

    if not message:

        return jsonify({

            "success": False,

            "error":
                "Message cannot be empty."

        }), 400

    # --------------------------------------------------------
    # CHECK ENGINE
    # --------------------------------------------------------

    if not ENGINE_READY:

        return jsonify({

            "success": False,

            "error":
                "RETRO-AI engine is not available."

        }), 503

    try:

        # ----------------------------------------------------
        # CREATE SESSION IF REQUIRED
        # ----------------------------------------------------

        if not session_id:

            session_id = create_session(
                message[:50]
            )

        else:

            session_id = int(
                session_id
            )

        # ----------------------------------------------------
        # SAVE USER MESSAGE
        # ----------------------------------------------------

        save_message(
            session_id,
            "user",
            message
        )

        # ----------------------------------------------------
        # EXECUTE MULTI-AGENT ENGINE
        # ----------------------------------------------------

        start_time = time.time()

        result = multi_agent.execute(
            message
        )

        total_time = int(
            (time.time() - start_time)
            * 1000
        )

        # ----------------------------------------------------
        # FINAL RESPONSE
        # ----------------------------------------------------

        final_response = result.get(
            "final_response",
            ""
        )

        if not final_response:

            final_response = (
                "RETRO-AI could not generate "
                "a final response."
            )

        # ----------------------------------------------------
        # AGENTS
        # ----------------------------------------------------

        agents = result.get(
            "agents",
            []
        )

        agent_string = ", ".join(
            agents
        )

        # ----------------------------------------------------
        # SAVE AI RESPONSE
        # ----------------------------------------------------

        save_message(
            session_id,
            "ai",
            final_response,
            agent_string
        )

        # ----------------------------------------------------
        # SAVE AGENT EXECUTION LOGS
        # ----------------------------------------------------

        for agent_result in result.get(
            "results",
            []
        ):

            save_agent_log(

                session_id,

                agent_result.agent_name,

                message,

                agent_result.output,

                agent_result.status,

                agent_result.execution_time_ms
            )

        # ----------------------------------------------------
        # RETURN RESPONSE
        # ----------------------------------------------------

        return jsonify({

            "success": True,

            "session_id": session_id,

            "response": final_response,

            "agent": agent_string,

            "agents": agents,

            "intent": result.get(
                "intent",
                "GENERAL"
            ),

            "goal": result.get(
                "goal",
                message
            ),

            "complexity": result.get(
                "complexity",
                0
            ),

            "confidence": result.get(
                "confidence",
                0
            ),

            "execution_time":
                total_time

        })

    except ValueError as error:

        return jsonify({

            "success": False,

            "error":
                "Invalid session ID."

        }), 400

    except Exception as error:

        print()
        print("CHAT ERROR:")
        print(error)
        print()

        return jsonify({

            "success": False,

            "error":
                str(error)

        }), 500


# ============================================================
# GET ALL SESSIONS
# ============================================================

@app.route(
    "/api/sessions",
    methods=["GET"]
)
def get_sessions():

    connection = None
    cursor = None

    try:

        connection = get_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT
                id,
                title,
                created_at,
                updated_at
            FROM chat_sessions
            ORDER BY updated_at DESC
            """
        )

        sessions = cursor.fetchall()

        return jsonify({

            "success": True,

            "sessions": sessions

        })

    except Exception as error:

        return jsonify({

            "success": False,

            "error":
                str(error)

        }), 500

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ============================================================
# GET CONVERSATION
# ============================================================

@app.route(
    "/api/conversations/<int:session_id>",
    methods=["GET"]
)
def get_conversation(
    session_id
):

    connection = None
    cursor = None

    try:

        connection = get_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT
                id,
                role,
                content,
                agent,
                created_at
            FROM messages
            WHERE session_id = %s
            ORDER BY id ASC
            """,
            (session_id,)
        )

        messages = cursor.fetchall()

        return jsonify({

            "success": True,

            "session_id":
                session_id,

            "messages":
                messages

        })

    except Exception as error:

        return jsonify({

            "success": False,

            "error":
                str(error)

        }), 500

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ============================================================
# SERVER START
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 70)
    print("RETRO-AI MULTI-AGENT SYSTEM")
    print("=" * 70)

    # --------------------------------------------------------
    # MYSQL CHECK
    # --------------------------------------------------------

    try:

        connection = get_connection()

        connection.close()

        print("MYSQL  : CONNECTED")

    except Exception as error:

        print("MYSQL  : ERROR")
        print(error)

    # --------------------------------------------------------
    # ENGINE CHECK
    # --------------------------------------------------------

    if ENGINE_READY:

        print("BRAIN  : CONNECTED")
        print("PHASE2 : CONNECTED")
        print("AGENTS : READY")

    else:

        print("BRAIN  : ERROR")
        print("PHASE2 : ERROR")
        print("AGENTS : OFFLINE")

    print()
    print(
        "SERVER : http://127.0.0.1:5000"
    )

    print("=" * 70)
    print()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )

