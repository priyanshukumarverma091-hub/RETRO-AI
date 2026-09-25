from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import logging
import time
import os

from dotenv import load_dotenv
from phase3 import Phase3Orchestrator

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("retro-ai")

app = Flask(__name__)
CORS(app)

QWEN_API_KEY = os.getenv("QWEN_API_KEY")
QWEN_MODEL = os.getenv("QWEN_MODEL", "qwen-plus")

if QWEN_API_KEY:
    logger.info("QWEN API KEY: CONFIGURED")
    logger.info("QWEN MODEL: %s", QWEN_MODEL)
else:
    logger.warning("QWEN API KEY: NOT CONFIGURED")

try:
    phase3_engine = Phase3Orchestrator()
    ENGINE_READY = True
except Exception:
    logger.exception("PHASE 3 ERROR: failed to initialize Phase3Orchestrator")
    phase3_engine = None
    ENGINE_READY = False


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/health")
def health():
    return jsonify({
        "success": True,
        "status": "online" if ENGINE_READY else "offline",
        "brain": "connected" if ENGINE_READY else "disconnected",
        "phase2": "connected" if ENGINE_READY else "disconnected",
        "phase3": "connected" if ENGINE_READY else "disconnected",
        "qwen": "configured" if QWEN_API_KEY else "not_configured",
        "qwen_model": QWEN_MODEL,
        "system": "RETRO-AI"
    })


def normalize_result(result):
    if isinstance(result, dict):
        return {
            "final_response": result.get(
                "final_response",
                result.get("response", "")
            ),
            "intent": result.get("intent", "GENERAL"),
            "goal": result.get("goal", ""),
            "complexity": result.get("complexity", 0),
            "confidence": result.get("confidence", 0),
            "agents": result.get("agents", []),
            "reasoning": result.get("reasoning", [])
        }

    return {
        "final_response": getattr(
            result, "final_response",
            getattr(result, "response", "")
        ),
        "intent": getattr(result, "intent", "GENERAL"),
        "goal": getattr(result, "goal", ""),
        "complexity": getattr(result, "complexity", 0),
        "confidence": getattr(result, "confidence", 0),
        "agents": getattr(result, "agents", []),
        "reasoning": getattr(result, "reasoning", [])
    }


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()

    if not message:
        return jsonify({
            "success": False,
            "error": "Message cannot be empty."
        }), 400

    if not ENGINE_READY:
        return jsonify({
            "success": False,
            "error": "RETRO-AI Phase 3 engine is not available."
        }), 503

    try:
        start_time = time.time()

        result = phase3_engine.process(message)

        total_time = int((time.time() - start_time) * 1000)

        normalized = normalize_result(result)

        final_response = normalized["final_response"]

        if not final_response:
            final_response = (
                "RETRO-AI processed the request "
                "but did not generate a final response."
            )

        agents = normalized["agents"]

        if agents is None:
            agents = []
        elif not isinstance(agents, list):
            agents = [str(agents)]

        agent_string = ", ".join(str(agent) for agent in agents)

        intent = normalized["intent"] or "GENERAL"

        logger.info(
            "Query processed | intent=%s | agents=%s | qwen=%s | time=%sms",
            intent,
            agent_string,
            "configured" if QWEN_API_KEY else "not_configured",
            total_time
        )

        return jsonify({
            "success": True,
            "response": final_response,
            "final_response": final_response,
            "agent": agent_string,
            "agents": agents,
            "intent": intent,
            "goal": normalized["goal"],
            "complexity": normalized["complexity"],
            "confidence": normalized["confidence"],
            "reasoning": normalized["reasoning"],
            "execution_time": total_time,
            "pipeline": [
                "Brain",
                "Intent Router",
                "Planner",
                "Specialist Agents",
                "Testing",
                "Qwen Reasoning",
                "Critic",
                "Final Synthesis"
            ]
        })

    except Exception as error:
        logger.exception("PHASE 3 CHAT ERROR")
        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


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

    print("QWEN   : " + ("CONFIGURED" if QWEN_API_KEY else "NOT CONFIGURED"))
    print()
    print("SERVER : http://127.0.0.1:5000")
    print("=" * 70)
    print()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
