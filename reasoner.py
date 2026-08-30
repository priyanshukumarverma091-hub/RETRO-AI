# -*- coding: utf-8 -*-

class LLMReasoner:

    def __init__(self):
        print("LLM Reasoner: RULE-BASED FALLBACK READY")

    def generate(self, query, agent_outputs):

        if not agent_outputs:
            return "I could not generate an answer."

        primary = agent_outputs[0][1]

        return primary.strip()