# ============================================================
# RETRO-AI : INTELLIGENCE BRAIN
# ============================================================

from dataclasses import dataclass, field
from enum import Enum
from typing import List
import re


# ============================================================
# INTENTS
# ============================================================

class Intent(Enum):
    MACHINE_LEARNING = "machine_learning"
    DATA_ANALYSIS = "data_analysis"
    CODING = "coding"
    RESEARCH = "research"
    REASONING = "reasoning"
    GENERAL = "general"


# ============================================================
# MODES
# ============================================================

VALID_MODES = {
    "general",
    "research",
    "coding",
}


def normalize_mode(mode: str) -> str:
    """
    Normalize user-selected RETRO-AI mode.

    Supported:
        general
        research
        coding

    Invalid values fall back to general.
    """

    value = str(mode or "general").strip().lower()

    if value not in VALID_MODES:
        return "general"

    return value


# ============================================================
# QUERY UNDERSTANDING
# ============================================================

@dataclass
class QueryUnderstanding:

    original_query: str

    # Selected UI / system mode
    mode: str = "general"

    intent: str = Intent.GENERAL.value

    goal: str = ""

    complexity: float = 0.20

    entities: List[str] = field(default_factory=list)

    requirements: List[str] = field(default_factory=list)

    constraints: List[str] = field(default_factory=list)

    capabilities: List[str] = field(default_factory=list)

    needs_tools: bool = False

    needs_multiple_agents: bool = False


# ============================================================
# BRAIN DECISION
# ============================================================

@dataclass
class BrainDecision:

    understanding: QueryUnderstanding

    recommended_agents: List[str]

    reasoning: List[str]

    confidence: float


# ============================================================
# INTELLIGENCE BRAIN
# ============================================================

class IntelligenceBrain:

    def __init__(self):

        # ----------------------------------------------------
        # INTENT SIGNALS
        # ----------------------------------------------------

        self.intent_signals = {

            Intent.MACHINE_LEARNING.value: [

                "machine learning",
                "machine-learning",
                "ml",
                "ml model",
                "machine model",
                "model training",
                "train model",
                "build model",
                "classification",
                "classifier",
                "regression",
                "prediction",
                "predict",
                "neural network",
                "deep learning",
                "cnn",
                "rnn",
                "lstm",
                "transformer",
                "accuracy",
                "precision",
                "recall",
                "f1 score",
                "f1-score",
                "roc-auc",
                "pr-auc",
                "overfitting",
                "underfitting",
                "feature engineering",
                "hyperparameter",
                "model performance",
                "model improvement",
                "improve model",
                "improve accuracy",
                "fraud detection",
                "fraud model",
                "churn model"
            ],

            Intent.DATA_ANALYSIS.value: [

                "dataset",
                "data analysis",
                "analyze data",
                "analyse data",
                "analyze dataset",
                "analyse dataset",
                "eda",
                "csv",
                "dataframe",
                "pandas",
                "statistics",
                "statistical analysis",
                "missing values",
                "outliers",
                "correlation",
                "distribution",
                "data cleaning",
                "data preprocessing"
            ],

            Intent.CODING.value: [

                "code",
                "coding",
                "program",
                "programming",
                "python",
                "javascript",
                "java",
                "c",
                "c++",
                "html",
                "css",
                "function",
                "class",
                "script",
                "debug",
                "debugging",
                "bug",
                "exception",
                "error",
                "implementation",
                "implement",
                "write code",
                "code for",
                "create function",
                "write function",
                "build function",
                "create class",
                "write class",
                "build script",
                "program to",
                "program for"
            ],

            Intent.RESEARCH.value: [

                "research",
                "latest",
                "recent",
                "current",
                "news",
                "find information",
                "search",
                "investigate",
                "study",
                "paper",
                "papers",
                "literature review",
                "research methodology"
            ],

            Intent.REASONING.value: [

                "why",
                "explain",
                "explanation",
                "reason",
                "compare",
                "comparison",
                "difference",
                "versus",
                "vs",
                "pros and cons"
            ]
        }

        # ----------------------------------------------------
        # STRONG CODING SIGNALS
        # ----------------------------------------------------

        self.strong_coding_signals = [

            "write code",
            "write python",
            "write a python",
            "python code",
            "code for",
            "program to",
            "program for",
            "implement",
            "implementation",
            "create function",
            "write function",
            "build function",
            "create class",
            "write class",
            "debug",
            "debugging",
            "fix bug",
            "fix this code",
            "solve this coding problem",
            "coding problem",
            "script to",
            "script for"
        ]

        # ----------------------------------------------------
        # REQUIREMENTS
        # ----------------------------------------------------

        self.requirement_signals = {

            "implementation": [

                "implement",
                "implementation",
                "build",
                "create",
                "develop",
                "write code",
                "code for",
                "program to"
            ],

            "optimization": [

                "optimize",
                "optimization",
                "improve",
                "improvement",
                "increase accuracy",
                "reduce loss",
                "better performance",
                "improve model",
                "improve accuracy"
            ],

            "analysis": [

                "analyze",
                "analyse",
                "analysis",
                "eda",
                "statistics",
                "inspect",
                "dataset",
                "csv",
                "missing values",
                "outliers"
            ],

            "explanation": [

                "explain",
                "explanation",
                "why",
                "how does",
                "what is",
                "describe"
            ],

            "debugging": [

                "debug",
                "debugging",
                "fix bug",
                "error",
                "exception",
                "not working"
            ],

            "research": [

                "research",
                "latest",
                "recent",
                "current",
                "find information",
                "search",
                "paper",
                "literature review"
            ],

            "comparison": [

                "compare",
                "comparison",
                "difference",
                "versus",
                "vs",
                "pros and cons"
            ],

            "prediction": [

                "predict",
                "prediction",
                "forecast"
            ]
        }

        # ----------------------------------------------------
        # KNOWN ENTITIES
        # ----------------------------------------------------

        self.known_entities = [

            "python",
            "javascript",
            "java",
            "c",
            "c++",
            "html",
            "css",

            "tensorflow",
            "pytorch",
            "keras",
            "scikit-learn",
            "sklearn",
            "pandas",
            "numpy",
            "opencv",
            "flask",
            "streamlit",

            "machine learning",
            "deep learning",
            "neural network",
            "cnn",
            "rnn",
            "lstm",
            "transformer",
            "classification",
            "regression",
            "random forest",
            "xgboost",
            "knn",
            "svm",

            "dataset",
            "csv",
            "dataframe",
            "eda",

            "llm",
            "generative ai",
            "genai",
            "rag",
            "embedding",
            "vector database"
        ]

        # ----------------------------------------------------
        # AGENT CAPABILITIES
        # ----------------------------------------------------

        self.agent_capabilities = {

            "ResearchAgent": [
                "research"
            ],

            "CodingAgent": [
                "implementation",
                "debugging"
            ],

            "DataAnalysisAgent": [
                "analysis"
            ],

            "MLAgent": [
                "implementation",
                "optimization",
                "prediction"
            ],

            "ReasoningAgent": [
                "explanation",
                "comparison"
            ],

            "CriticAgent": [
                "verification",
                "quality_control"
            ]
        }

    # ========================================================
    # MAIN THINK
    # ========================================================

    def think(
        self,
        query: str,
        mode: str = "general"
    ) -> BrainDecision:

        mode = normalize_mode(mode)

        understanding = self.understand(
            query,
            mode=mode
        )

        agents = self.select_agents(
            understanding
        )

        reasoning = self.generate_reasoning(
            understanding,
            agents
        )

        confidence = self.calculate_confidence(
            understanding,
            agents
        )

        return BrainDecision(
            understanding=understanding,
            recommended_agents=agents,
            reasoning=reasoning,
            confidence=confidence
        )

    # ========================================================
    # UNDERSTANDING
    # ========================================================

    def understand(
        self,
        query: str,
        mode: str = "general"
    ) -> QueryUnderstanding:

        mode = normalize_mode(mode)

        query = query.strip()

        normalized = query.lower()

        intent = self.detect_intent(
            normalized
        )

        # ----------------------------------------------------
        # MODE-AWARE INTENT
        # ----------------------------------------------------

        # Explicit user mode has priority when the selected
        # mode is research or coding.

        if mode == "research":
            intent = Intent.RESEARCH.value

        elif mode == "coding":
            intent = Intent.CODING.value

        goal = self.extract_goal(
            query
        )

        entities = self.extract_entities(
            normalized
        )

        requirements = self.extract_requirements(
            normalized
        )

        capabilities = self.detect_capabilities(
            normalized
        )

        constraints = self.extract_constraints(
            normalized
        )

        # ----------------------------------------------------
        # MODE CAPABILITIES
        # ----------------------------------------------------

        if mode == "research":

            if Intent.RESEARCH.value not in capabilities:
                capabilities.append(
                    Intent.RESEARCH.value
                )

            if "research" not in requirements:
                requirements.append(
                    "research"
                )

        elif mode == "coding":

            if Intent.CODING.value not in capabilities:
                capabilities.append(
                    Intent.CODING.value
                )

            if "implementation" not in requirements:
                requirements.append(
                    "implementation"
                )

        capabilities = list(
            dict.fromkeys(capabilities)
        )

        requirements = list(
            dict.fromkeys(requirements)
        )

        complexity = self.calculate_complexity(
            normalized,
            requirements,
            capabilities
        )

        needs_tools = self.detect_tool_requirement(
            normalized
        )

        # Research mode normally requires external information.
        if mode == "research":
            needs_tools = True

        domain_capabilities = [

            c for c in capabilities

            if c in {
                Intent.MACHINE_LEARNING.value,
                Intent.DATA_ANALYSIS.value,
                Intent.CODING.value,
                Intent.RESEARCH.value
            }
        ]

        needs_multiple_agents = (

            len(domain_capabilities) >= 2

            or len(requirements) >= 2

            or complexity >= 0.60
        )

        # Mode-specific processing can require multiple stages.
        if mode in {"research", "coding"}:
            needs_multiple_agents = True

        return QueryUnderstanding(

            original_query=query,

            mode=mode,

            intent=intent,

            goal=goal,

            complexity=complexity,

            entities=entities,

            requirements=requirements,

            constraints=constraints,

            capabilities=capabilities,

            needs_tools=needs_tools,

            needs_multiple_agents=needs_multiple_agents
        )

    # ========================================================
    # INTENT DETECTION
    # ========================================================

    def detect_intent(
        self,
        query: str
    ) -> str:

        query = query.lower().strip()

        # ----------------------------------------------------
        # EXPLICIT ML
        # ----------------------------------------------------

        ml_patterns = [

            r"\bml\b",
            r"\bmachine learning\b",
            r"\bmachine-learning\b",
            r"\bml model\b",
            r"\bmachine model\b",
            r"\bmodel training\b",
            r"\btrain model\b",
            r"\bbuild model\b",
            r"\bclassification\b",
            r"\bclassifier\b",
            r"\bregression\b",
            r"\bprediction\b",
            r"\bpredict\b",
            r"\bneural network\b",
            r"\bneural networks\b",
            r"\bdeep learning\b",
            r"\bcnn\b",
            r"\brnn\b",
            r"\blstm\b",
            r"\btransformer\b",
            r"\bfeature engineering\b",
            r"\bhyperparameter\b",
            r"\boverfitting\b",
            r"\bunderfitting\b",
            r"\bmodel performance\b",
            r"\bmodel improvement\b",
            r"\bimprove model\b",
            r"\bimprove accuracy\b",
            r"\bfraud detection\b",
            r"\bfraud model\b",
            r"\bchurn model\b"
        ]

        if any(
            re.search(pattern, query)
            for pattern in ml_patterns
        ):
            return Intent.MACHINE_LEARNING.value

        # ----------------------------------------------------
        # STRONG CODING
        # ----------------------------------------------------

        for signal in self.strong_coding_signals:

            if signal in query:

                return Intent.CODING.value

        # ----------------------------------------------------
        # DATA ANALYSIS
        # ----------------------------------------------------

        data_patterns = [

            r"\bdata analysis\b",
            r"\banalyze data\b",
            r"\banalyse data\b",
            r"\banalyze dataset\b",
            r"\banalyse dataset\b",
            r"\bcsv\b",
            r"\bdataframe\b",
            r"\bpandas\b",
            r"\beda\b",
            r"\bmissing values\b",
            r"\boutliers\b",
            r"\bcorrelation\b",
            r"\bdata cleaning\b",
            r"\bdata preprocessing\b"
        ]

        if any(
            re.search(pattern, query)
            for pattern in data_patterns
        ):
            return Intent.DATA_ANALYSIS.value

        # ----------------------------------------------------
        # RESEARCH
        # ----------------------------------------------------

        research_patterns = [

            r"\bresearch\b",
            r"\blatest\b",
            r"\brecent\b",
            r"\bliterature review\b",
            r"\bresearch paper\b",
            r"\bfind information\b",
            r"\binvestigate\b"
        ]

        if any(
            re.search(pattern, query)
            for pattern in research_patterns
        ):
            return Intent.RESEARCH.value

        # ----------------------------------------------------
        # REASONING
        # ----------------------------------------------------

        reasoning_patterns = [

            r"\bwhy\b",
            r"\bexplain\b",
            r"\bexplanation\b",
            r"\breason\b",
            r"\bcompare\b",
            r"\bcomparison\b",
            r"\bdifference\b",
            r"\bversus\b",
            r"\bvs\b",
            r"\bpros and cons\b"
        ]

        if any(
            re.search(pattern, query)
            for pattern in reasoning_patterns
        ):
            return Intent.REASONING.value

        return Intent.GENERAL.value

    # ========================================================
    # SIGNAL WEIGHT
    # ========================================================

    def signal_weight(
        self,
        signal: str
    ) -> float:

        strong_signals = {

            "machine learning": 3.0,
            "machine-learning": 3.0,
            "ml": 3.0,
            "ml model": 3.0,

            "data analysis": 3.0,

            "deep learning": 3.0,

            "research": 3.0,

            "debug": 2.5,
            "debugging": 2.5,

            "classification": 2.0,
            "regression": 2.0,

            "dataset": 1.5,
            "csv": 1.5,

            "python": 1.5,

            "implementation": 2.0,
            "implement": 2.0,

            "write code": 3.0
        }

        return strong_signals.get(
            signal,
            1.0
        )

    # ========================================================
    # GOAL
    # ========================================================

    def extract_goal(
        self,
        query: str
    ) -> str:

        patterns = [

            r"i want to (.+)",
            r"i need to (.+)",
            r"help me (.+)",
            r"how can i (.+)",
            r"how do i (.+)",
            r"can you (.+)",
            r"please (.+)"
        ]

        normalized = query.lower()

        for pattern in patterns:

            match = re.search(
                pattern,
                normalized
            )

            if match:

                return match.group(1).strip()

        return query.strip()

    # ========================================================
    # ENTITIES
    # ========================================================

    def extract_entities(
        self,
        query: str
    ) -> List[str]:

        entities = []

        for entity in self.known_entities:

            if entity.lower() in query:

                entities.append(entity)

        return list(
            dict.fromkeys(entities)
        )

    # ========================================================
    # REQUIREMENTS
    # ========================================================

    def extract_requirements(
        self,
        query: str
    ) -> List[str]:

        requirements = []

        for requirement, signals in (
            self.requirement_signals.items()
        ):

            for signal in signals:

                if signal in query:

                    requirements.append(
                        requirement
                    )

                    break

        return list(
            dict.fromkeys(requirements)
        )

    # ========================================================
    # CAPABILITIES
    # ========================================================

    def detect_capabilities(
        self,
        query: str
    ) -> List[str]:

        capabilities = []

        # ----------------------------------------------------
        # ML
        # ----------------------------------------------------

        ml_patterns = [

            r"\bml\b",
            r"\bmachine learning\b",
            r"\bmachine-learning\b",
            r"\bml model\b",
            r"\bdeep learning\b",
            r"\bneural network(s)?\b",
            r"\bcnn\b",
            r"\brnn\b",
            r"\blstm\b",
            r"\btransformer\b",
            r"\bclassification\b",
            r"\bregression\b",
            r"\bprediction\b",
            r"\bpredict\b",
            r"\bmodel training\b",
            r"\btrain model\b",
            r"\bbuild model\b",
            r"\bfeature engineering\b",
            r"\bhyperparameter\b"
        ]

        if any(
            re.search(pattern, query)
            for pattern in ml_patterns
        ):

            capabilities.append(
                Intent.MACHINE_LEARNING.value
            )

        # ----------------------------------------------------
        # DATA
        # ----------------------------------------------------

        data_patterns = [

            r"\bdataset\b",
            r"\bdata analysis\b",
            r"\banalyze data\b",
            r"\banalyse data\b",
            r"\banalyze dataset\b",
            r"\banalyse dataset\b",
            r"\bcsv\b",
            r"\bdataframe\b",
            r"\bpandas\b",
            r"\beda\b",
            r"\bstatistics\b",
            r"\bmissing values\b",
            r"\boutliers\b",
            r"\bdata cleaning\b"
        ]

        if any(
            re.search(pattern, query)
            for pattern in data_patterns
        ):

            capabilities.append(
                Intent.DATA_ANALYSIS.value
            )

        # ----------------------------------------------------
        # CODING
        # ----------------------------------------------------

        coding_patterns = [

            r"\bcode\b",
            r"\bcoding\b",
            r"\bprogram\b",
            r"\bprogramming\b",
            r"\bpython\b",
            r"\bjavascript\b",
            r"\bjava\b",
            r"\bfunction\b",
            r"\bclass\b",
            r"\bscript\b",
            r"\bdebug\b",
            r"\bdebugging\b",
            r"\bimplement\b",
            r"\bimplementation\b"
        ]

        if any(
            re.search(pattern, query)
            for pattern in coding_patterns
        ):

            capabilities.append(
                Intent.CODING.value
            )

        # ----------------------------------------------------
        # RESEARCH
        # ----------------------------------------------------

        research_patterns = [

            r"\bresearch\b",
            r"\blatest\b",
            r"\brecent\b",
            r"\bcurrent\b",
            r"\bnews\b",
            r"\bsearch\b",
            r"\bstudy\b",
            r"\bpaper\b",
            r"\bliterature\b"
        ]

        if any(
            re.search(pattern, query)
            for pattern in research_patterns
        ):

            capabilities.append(
                Intent.RESEARCH.value
            )

        # ----------------------------------------------------
        # REASONING
        # ----------------------------------------------------

        reasoning_patterns = [

            r"\bexplain\b",
            r"\bexplanation\b",
            r"\bwhy\b",
            r"\bcompare\b",
            r"\bcomparison\b",
            r"\bdifference\b",
            r"\bversus\b",
            r"\bvs\b",
            r"\bpros and cons\b"
        ]

        if any(
            re.search(pattern, query)
            for pattern in reasoning_patterns
        ):

            capabilities.append(
                Intent.REASONING.value
            )

        return list(
            dict.fromkeys(capabilities)
        )

    # ========================================================
    # CONSTRAINTS
    # ========================================================

    def extract_constraints(
        self,
        query: str
    ) -> List[str]:

        constraints = []

        patterns = [

            r"under\s+\d+",
            r"within\s+\d+",
            r"before\s+\w+",
            r"after\s+\w+",
            r"only\s+\w+",
            r"without\s+\w+",
            r"using\s+\w+"
        ]

        for pattern in patterns:

            matches = re.findall(
                pattern,
                query
            )

            constraints.extend(matches)

        return list(
            dict.fromkeys(constraints)
        )

    # ========================================================
    # COMPLEXITY
    # ========================================================

    def calculate_complexity(
        self,
        query: str,
        requirements: List[str],
        capabilities: List[str]
    ) -> float:

        complexity = 0.20

        if len(query) > 100:
            complexity += 0.10

        if len(query) > 200:
            complexity += 0.10

        complexity += min(
            len(requirements) * 0.08,
            0.20
        )

        complexity += min(
            len(capabilities) * 0.08,
            0.25
        )

        multi_step_words = [

            "and",
            "then",
            "also",
            "after",
            "finally",
            "first",
            "second",
            "step",
            "build",
            "evaluate"
        ]

        for word in multi_step_words:

            if re.search(
                rf"\b{re.escape(word)}\b",
                query
            ):

                complexity += 0.05

        if (
            (
                "machine learning" in query
                or re.search(r"\bml\b", query)
            )
            and (
                "improve" in query
                or "optimize" in query
            )
        ):

            complexity += 0.15

        return min(
            round(complexity, 2),
            1.0
        )

    # ========================================================
    # TOOL REQUIREMENT
    # ========================================================

    def detect_tool_requirement(
        self,
        query: str
    ) -> bool:

        tool_signals = [

            "search",
            "latest",
            "recent",
            "current",
            "news",
            "internet",
            "website",
            "online",
            "file",
            "dataset",
            "csv",
            "calculate"
        ]

        return any(
            signal in query
            for signal in tool_signals
        )

    # ========================================================
    # AGENT SELECTION
    # ========================================================

    def select_agents(
        self,
        understanding: QueryUnderstanding
    ) -> List[str]:

        agents = []

        intent = understanding.intent

        mode = normalize_mode(
            understanding.mode
        )

        # ----------------------------------------------------
        # MODE PRIORITY
        # ----------------------------------------------------

        # Mode does NOT completely replace dynamic routing.
        # It only establishes the primary specialist.

        if mode == "coding":

            agents.append(
                "CodingAgent"
            )

        elif mode == "research":

            agents.append(
                "ResearchAgent"
            )

        # ----------------------------------------------------
        # PRIMARY AGENT FROM INTENT
        # ----------------------------------------------------

        primary_agents = {

            Intent.MACHINE_LEARNING.value:
                "MLAgent",

            Intent.DATA_ANALYSIS.value:
                "DataAnalysisAgent",

            Intent.CODING.value:
                "CodingAgent",

            Intent.RESEARCH.value:
                "ResearchAgent",

            Intent.REASONING.value:
                "ReasoningAgent"
        }

        if intent in primary_agents:

            primary_agent = primary_agents[
                intent
            ]

            if primary_agent not in agents:

                agents.append(
                    primary_agent
                )

        # ----------------------------------------------------
        # DOMAIN CAPABILITY ROUTING
        # ----------------------------------------------------

        capabilities = understanding.capabilities

        if (
            Intent.MACHINE_LEARNING.value
            in capabilities
        ):

            if "MLAgent" not in agents:

                agents.append(
                    "MLAgent"
                )

        if (
            Intent.DATA_ANALYSIS.value
            in capabilities
        ):

            if "DataAnalysisAgent" not in agents:

                agents.append(
                    "DataAnalysisAgent"
                )

        if (
            Intent.CODING.value
            in capabilities
        ):

            if "CodingAgent" not in agents:

                agents.append(
                    "CodingAgent"
                )

        if (
            Intent.RESEARCH.value
            in capabilities
        ):

            if "ResearchAgent" not in agents:

                agents.append(
                    "ResearchAgent"
                )

        # ----------------------------------------------------
        # REQUIREMENT ROUTING
        # ----------------------------------------------------

        requirements = understanding.requirements

        if "implementation" in requirements:

            if "CodingAgent" not in agents:

                agents.append(
                    "CodingAgent"
                )

        if "analysis" in requirements:

            if "DataAnalysisAgent" not in agents:

                agents.append(
                    "DataAnalysisAgent"
                )

        if "research" in requirements:

            if "ResearchAgent" not in agents:

                agents.append(
                    "ResearchAgent"
                )

        if "debugging" in requirements:

            if "CodingAgent" not in agents:

                agents.append(
                    "CodingAgent"
                )

        if "prediction" in requirements:

            if "MLAgent" not in agents:

                agents.append(
                    "MLAgent"
                )

        # ----------------------------------------------------
        # REASONING SUPPORT
        # ----------------------------------------------------

        if (
            "explanation" in requirements
            or "comparison" in requirements
        ):

            if "ReasoningAgent" not in agents:

                agents.append(
                    "ReasoningAgent"
                )

        # ----------------------------------------------------
        # CRITIC
        # ----------------------------------------------------

        if (
            understanding.needs_multiple_agents
            or understanding.complexity >= 0.60
        ):

            if "CriticAgent" not in agents:

                agents.append(
                    "CriticAgent"
                )

        # ----------------------------------------------------
        # MODE-SPECIFIC SUPPORT
        # ----------------------------------------------------

        if mode == "research":

            if "ReasoningAgent" not in agents:

                agents.append(
                    "ReasoningAgent"
                )

        elif mode == "coding":

            # Coding mode benefits from reasoning for
            # implementation decisions and debugging.

            if "ReasoningAgent" not in agents:

                agents.append(
                    "ReasoningAgent"
                )

        # ----------------------------------------------------
        # FALLBACK
        # ----------------------------------------------------

        if not agents:

            agents.append(
                "GeneralAgent"
            )

        return list(
            dict.fromkeys(agents)
        )

    # ========================================================
    # REASONING TRACE
    # ========================================================

    def generate_reasoning(
        self,
        understanding: QueryUnderstanding,
        agents: List[str]
    ) -> List[str]:

        reasoning = []

        reasoning.append(
            f"Selected mode: "
            f"{understanding.mode.upper()}"
        )

        reasoning.append(
            f"Detected intent: "
            f"{understanding.intent}"
        )

        if understanding.goal:

            reasoning.append(
                f"Goal identified: "
                f"{understanding.goal}"
            )

        reasoning.append(
            f"Complexity score: "
            f"{understanding.complexity:.2f}"
        )

        if understanding.capabilities:

            reasoning.append(
                "Capabilities detected: "
                + ", ".join(
                    understanding.capabilities
                )
            )

        if understanding.requirements:

            reasoning.append(
                "Requirements detected: "
                + ", ".join(
                    understanding.requirements
                )
            )

        if understanding.entities:

            reasoning.append(
                "Entities detected: "
                + ", ".join(
                    understanding.entities
                )
            )

        reasoning.append(
            "Selected agents: "
            + ", ".join(agents)
        )

        if understanding.needs_tools:

            reasoning.append(
                "External/tool-assisted processing "
                "may be required."
            )

        if understanding.needs_multiple_agents:

            reasoning.append(
                "Query requires multi-agent processing."
            )

        return reasoning

    # ========================================================
    # CONFIDENCE
    # ========================================================

    def calculate_confidence(
        self,
        understanding: QueryUnderstanding,
        agents: List[str]
    ) -> float:

        confidence = 0.45

        if understanding.intent != Intent.GENERAL.value:

            confidence += 0.15

        if understanding.requirements:

            confidence += 0.08

        if understanding.entities:

            confidence += 0.07

        if understanding.capabilities:

            confidence += 0.08

        if agents:

            confidence += 0.07

        if len(understanding.capabilities) >= 2:

            confidence += 0.05

        return round(
            min(confidence, 0.95),
            2
        )


# ============================================================
# BRAIN TEST
# ============================================================

if __name__ == "__main__":

    brain = IntelligenceBrain()

    # --------------------------------------------------------
    # GENERAL MODE TESTS
    # --------------------------------------------------------

    general_tests = [

        "hello",

        "what is machine learning",

        "explain neural networks",

        "compare TensorFlow and PyTorch",

        "analyze CSV dataset",

        "build a machine learning model using Python"
    ]

    # --------------------------------------------------------
    # RESEARCH MODE TESTS
    # --------------------------------------------------------

    research_tests = [

        "what is artificial intelligence",

        "latest developments in AI",

        "compare recent LLM architectures"
    ]

    # --------------------------------------------------------
    # CODING MODE TESTS
    # --------------------------------------------------------

    coding_tests = [

        "hello",

        "write python code to reverse a string",

        "debug this Python code",

        "create a Flask API"
    ]

    print("\n" + "=" * 70)
    print("RETRO-AI INTELLIGENCE BRAIN TEST")
    print("=" * 70)

    passed = 0
    total = 0

    # --------------------------------------------------------
    # RUN TESTS
    # --------------------------------------------------------

    test_groups = [

        ("GENERAL", general_tests),

        ("RESEARCH", research_tests),

        ("CODING", coding_tests)
    ]

    for mode, queries in test_groups:

        print("\n")
        print("=" * 70)
        print(f"{mode} MODE")
        print("=" * 70)

        for query in queries:

            total += 1

            decision = brain.think(
                query,
                mode=mode.lower()
            )

            understanding = decision.understanding

            print("\nQUERY:")
            print(query)

            print("\nMODE:")
            print(understanding.mode)

            print("\nINTENT:")
            print(understanding.intent)

            print("\nAGENTS:")
            print(decision.recommended_agents)

            print("\nCAPABILITIES:")
            print(
                understanding.capabilities
            )

            print("\nREQUIREMENTS:")
            print(
                understanding.requirements
            )

            print("\nCOMPLEXITY:")
            print(
                understanding.complexity
            )

            print("\nMULTI-AGENT:")
            print(
                understanding.needs_multiple_agents
            )

            print("\nTOOLS:")
            print(
                understanding.needs_tools
            )

            print("\nCONFIDENCE:")
            print(
                decision.confidence
            )

            # ------------------------------------------------
            # BASIC TEST VALIDATION
            # ------------------------------------------------

            valid = bool(
                decision.recommended_agents
            )

            if mode == "RESEARCH":

                valid = (
                    valid
                    and "ResearchAgent"
                    in decision.recommended_agents
                )

            elif mode == "CODING":

                valid = (
                    valid
                    and "CodingAgent"
                    in decision.recommended_agents
                )

            if valid:

                passed += 1
                print("\nSTATUS: PASS")

            else:

                print("\nSTATUS: FAIL")

            print("-" * 70)

    # ========================================================
    # SUMMARY
    # ========================================================

    print("\n" + "=" * 70)
    print("BRAIN TEST SUMMARY")
    print("=" * 70)

    print(f"Passed: {passed}")
    print(f"Total : {total}")

    if passed == total:
        print("STATUS: ALL TESTS PASSED")
    else:
        print("STATUS: SOME TESTS FAILED")

    print("=" * 70)
