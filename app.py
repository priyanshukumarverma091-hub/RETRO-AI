from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import logging
import time

from phase3 import Phase3Orchestrator


# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger("retro-ai")


# ============================================================
# FLASK APPLICATION
# ============================================================

app = Flask(__name__)
CORS(app)


# ============================================================
# PHASE 3 INTELLIGENCE ENGINE
# ============================================================

try:
    phase3_engine = Phase3Orchestrator()
    ENGINE_READY = True

except Exception:
    logger.exception(
        "PHASE 3 ERROR: failed to initialize Phase3Orchestrator"
    )

    phase3_engine = None
    ENGINE_READY = False


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():
    return render_template("index.html")


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/api/health")
def health():

    return jsonify({
        "success": True,
        "status": "online" if ENGINE_READY else "offline",
        "brain": "connected" if ENGINE_READY else "disconnected",
        "phase2": "connected" if ENGINE_READY else "disconnected",
        "phase3": "connected" if ENGINE_READY else "disconnected",
        "system": "RETRO-AI"
    })


# ============================================================
# RESULT NORMALIZER
# ============================================================

def normalize_result(result):

    # --------------------------------------------------------
    # Dictionary result
    # --------------------------------------------------------

    if isinstance(result, dict):

        return {
            "final_response": result.get(
                "final_response",
                result.get("response", "")
            ),

            "intent": result.get(
                "intent",
                "GENERAL"
            ),

            "goal": result.get(
                "goal",
                ""
            ),

            "complexity": result.get(
                "complexity",
                0
            ),

            "confidence": result.get(
                "confidence",
                0
            ),

            "agents": result.get(
                "agents",
                []
            ),

            "reasoning": result.get(
                "reasoning",
                []
            )
        }

    # --------------------------------------------------------
    # Object result
    # --------------------------------------------------------

    return {
        "final_response": getattr(
            result,
            "final_response",
            getattr(result, "response", "")
        ),

        "intent": getattr(
            result,
            "intent",
            "GENERAL"
        ),

        "goal": getattr(
            result,
            "goal",
            ""
        ),

        "complexity": getattr(
            result,
            "complexity",
            0
        ),

        "confidence": getattr(
            result,
            "confidence",
            0
        ),

        "agents": getattr(
            result,
            "agents",
            []
        ),

        "reasoning": getattr(
            result,
            "reasoning",
            []
        )
    }


# ============================================================
# CHAT API
# ============================================================

@app.route("/api/chat", methods=["POST"])
def chat():

    data = request.get_json(silent=True) or {}

    message = str(
        data.get("message", "")
    ).strip()


    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if not message:

        return jsonify({
            "success": False,
            "error": "Message cannot be empty."
        }), 400


    # --------------------------------------------------------
    # ENGINE CHECK
    # --------------------------------------------------------

    if not ENGINE_READY:

        return jsonify({
            "success": False,
            "error": "RETRO-AI Phase 3 engine is not available."
        }), 503


    # --------------------------------------------------------
    # PROCESS QUERY
    # --------------------------------------------------------

    try:

        start_time = time.time()

        result = phase3_engine.process(
            message
        )

        total_time = int(
            (time.time() - start_time) * 1000
        )


        # ----------------------------------------------------
        # NORMALIZE
        # ----------------------------------------------------

        normalized = normalize_result(
            result
        )


        # ----------------------------------------------------
        # FINAL RESPONSE
        # ----------------------------------------------------

        final_response = normalized[
            "final_response"
        ]

        if not final_response:

            final_response = (
                "RETRO-AI processed the request "
                "but did not generate a final response."
            )


        # ----------------------------------------------------
        # AGENTS
        # ----------------------------------------------------

        agents = normalized["agents"]

        if agents is None:

            agents = []

        elif not isinstance(agents, list):

            agents = [str(agents)]


        agent_string = ", ".join(
            str(agent)
            for agent in agents
        )


        # ----------------------------------------------------
        # INTENT
        # ----------------------------------------------------

        intent = normalized[
            "intent"
        ]

        if intent is None:

            intent = "GENERAL"


        # ----------------------------------------------------
        # LOG
        # ----------------------------------------------------

        logger.info(
            "Query processed | intent=%s | agents=%s | time=%sms",
            intent,
            agent_string,
            total_time
        )


        # ----------------------------------------------------
        # RESPONSE TO FRONTEND
        # ----------------------------------------------------

        return jsonify({

            "success": True,

            # Main frontend response
            "response": final_response,

            # Also expose final_response
            "final_response": final_response,

            # Agent information
            "agent": agent_string,

            "agents": agents,

            # Brain information
            "intent": intent,

            "goal": normalized[
                "goal"
            ],

            "complexity": normalized[
                "complexity"
            ],

            "confidence": normalized[
                "confidence"
            ],

            "reasoning": normalized[
                "reasoning"
            ],

            # Performance
            "execution_time": total_time,

            # Pipeline
            "pipeline": [
                "Brain",
                "Intent Router",
                "Planner",
                "Specialist Agents",
                "Testing",
                "Reasoning",
                "Critic",
                "Final Synthesis"
            ]
        })


    except Exception as error:

        logger.exception(
            "PHASE 3 CHAT ERROR"
        )

        return jsonify({

            "success": False,

            "error": str(error)

        }), 500


# ============================================================
# SERVER START
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 70)
    print("RETRO-AI MULTI-AGENT SYSTEM")
    print("=" * 70)

    if ENGINE_READY:

        print("BRAIN  : CONNECTED")
        print("PHASE2 : CONNECTED")
        print("PHASE3 : CONNECTED")
        print("AGENTS : READY")

    else:

        print("BRAIN  : ERROR")
        print("PHASE2 : ERROR")
        print("PHASE3 : ERROR")
        print("AGENTS : OFFLINE")

    print()
    print("SERVER : http://127.0.0.1:5000")
    print("=" * 70)
    print()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )