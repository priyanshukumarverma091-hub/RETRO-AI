import os
from openai import OpenAI


class LLMReasoner:
    VALID_MODES = {"general", "research", "coding"}

    def __init__(self):
        self.api_key = os.getenv("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")

        if not self.api_key:
            print("LLM Reasoner: OPENROUTER API KEY NOT FOUND")
            self.client = None
        else:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url="https://openrouter.ai/api/v1",
            )
            print("LLM Reasoner: OPENROUTER READY")

        self.model = os.getenv(
            "QWEN_MODEL",
            "qwen/qwen3-8b"
        )

        print(f"LLM Reasoner: MODEL = {self.model}")

    def normalize_mode(self, mode):
        mode = str(mode or "general").strip().lower()

        if mode not in self.VALID_MODES:
            return "general"

        return mode

    def get_mode_instruction(self, mode):
        mode = self.normalize_mode(mode)

        if mode == "research":
            return (
                "You are operating in RESEARCH mode. "
                "Focus on factual analysis, evidence, comparison, "
                "structured reasoning, and clearly distinguish known "
                "information from uncertainty. "
                "Do not fabricate sources or facts."
            )

        if mode == "coding":
            return (
                "You are operating in CODING mode. "
                "Focus on correct, practical, maintainable software solutions. "
                "When code is requested, provide usable code with necessary "
                "explanations. Consider errors, edge cases, dependencies, "
                "and integration with the existing system."
            )

        return (
            "You are operating in GENERAL mode. "
            "Answer naturally, clearly, and directly. "
            "Adapt the explanation to the user's question."
        )

    def generate(
        self,
        query,
        agent_outputs,
        mode="general"
    ):
        mode = self.normalize_mode(mode)

        if not agent_outputs:
            return "I could not generate an answer."

        # Fallback if OpenRouter is unavailable
        if self.client is None:
            return str(agent_outputs[0][1]).strip()

        context = "\n\n".join(
            f"Agent: {agent}\nOutput: {output}"
            for agent, output in agent_outputs
        )

        mode_instruction = self.get_mode_instruction(mode)

        system_prompt = (
            "You are the final reasoning engine of RETRO-AI.\n\n"

            f"SELECTED MODE: {mode.upper()}\n\n"

            f"{mode_instruction}\n\n"

            "General rules:\n"
            "- Answer the user's question clearly and naturally.\n"
            "- Use agent outputs as supporting context.\n"
            "- Do not mention internal agents unless the user asks.\n"
            "- Do not expose internal pipeline details unnecessarily.\n"
            "- Do not invent unsupported information.\n"
            "- If the available evidence is insufficient, say so.\n"
            "- Follow the user's requested format when possible.\n"
        )

        user_prompt = (
            f"RETRO-AI MODE:\n"
            f"{mode.upper()}\n\n"

            f"USER QUERY:\n"
            f"{query}\n\n"

            f"AGENT OUTPUTS:\n"
            f"{context}\n\n"

            "Using the selected mode and the available agent outputs, "
            "provide the final answer to the user."
        )

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    },
                ],
                temperature=0.3,
            )

            if not response.choices:
                return str(agent_outputs[0][1]).strip()

            answer = response.choices[0].message.content

            if answer:
                return answer.strip()

        except Exception as e:
            print(
                f"OpenRouter Reasoning Error: {e}"
            )

        return str(agent_outputs[0][1]).strip()
