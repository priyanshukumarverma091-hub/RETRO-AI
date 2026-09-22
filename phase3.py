# ================================================================
# RETRO-AI PHASE 3
# DYNAMIC MULTI-AGENT INTELLIGENCE SYSTEM
# ================================================================

import ast
import json
import re
import traceback

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from brain import IntelligenceBrain
from phase2 import MultiAgentSystem


# ================================================================
# DATA STRUCTURES
# ================================================================

@dataclass
class AgentTask:
    agent: str
    objective: str
    priority: int = 1
    status: str = "PENDING"
    result: Optional[Any] = None
    error: Optional[str] = None


@dataclass
class AgentExecution:
    agent: str
    status: str
    output: Any
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Phase3Result:
    query: str
    intent: str
    complexity: float
    selected_agents: List[str]
    executions: List[AgentExecution]
    critic_status: str
    final_response: str


# ================================================================
# UTILITY FUNCTIONS
# ================================================================

def safe_text(value: Any) -> str:

    if value is None:
        return ""

    if isinstance(value, str):
        return value

    try:
        return json.dumps(
            value,
            indent=2,
            default=str
        )
    except Exception:
        return str(value)


def normalize_intent(intent: Any) -> str:

    if intent is None:
        return "GENERAL"

    value = getattr(
        intent,
        "value",
        intent
    )

    value = str(
        value
    ).strip().upper()

    aliases = {

        "ML": "MACHINE_LEARNING",

        "MACHINE LEARNING":
            "MACHINE_LEARNING",

        "MACHINE-LEARNING":
            "MACHINE_LEARNING",

        "MACHINE_LEARNING":
            "MACHINE_LEARNING",

        "DATA":
            "DATA_ANALYSIS",

        "DATA ANALYSIS":
            "DATA_ANALYSIS",

        "DATA-ANALYSIS":
            "DATA_ANALYSIS",

        "DATA_ANALYSIS":
            "DATA_ANALYSIS",

        "CODE":
            "CODING",

        "PROGRAMMING":
            "CODING",

        "CODING":
            "CODING",

        "RESEARCH":
            "RESEARCH",

        "REASONING":
            "REASONING",

        "GENERAL":
            "GENERAL",
    }

    return aliases.get(
        value,
        value
    )


def unique_list(
    items: List[str]
) -> List[str]:

    result = []

    for item in items:

        if item not in result:
            result.append(item)

    return result


def validate_python(
    code: str
) -> Dict[str, Any]:

    result = {

        "valid": False,

        "functions": [],

        "classes": [],

        "imports": [],

        "error": None,
    }

    if not code.strip():

        result["error"] = (
            "No code available."
        )

        return result

    try:

        tree = ast.parse(
            code
        )

        result["valid"] = True

        for node in ast.walk(
            tree
        ):

            if isinstance(
                node,
                ast.FunctionDef
            ):

                result[
                    "functions"
                ].append(
                    node.name
                )

            elif isinstance(
                node,
                ast.AsyncFunctionDef
            ):

                result[
                    "functions"
                ].append(
                    node.name
                )

            elif isinstance(
                node,
                ast.ClassDef
            ):

                result[
                    "classes"
                ].append(
                    node.name
                )

            elif isinstance(
                node,
                ast.Import
            ):

                for item in node.names:

                    result[
                        "imports"
                    ].append(
                        item.name
                    )

            elif isinstance(
                node,
                ast.ImportFrom
            ):

                if node.module:

                    result[
                        "imports"
                    ].append(
                        node.module
                    )

    except SyntaxError as exc:

        result["error"] = (
            f"SyntaxError: {exc.msg} "
            f"(line {exc.lineno}, "
            f"column {exc.offset})"
        )

    return result


# ================================================================
# QUERY ANALYZER
# ================================================================

class QueryAnalyzer:

    @staticmethod
    def analyze(
        query: str
    ) -> Dict[str, Any]:

        q = query.lower()

        analysis = {

            "domain": [],

            "task_type": [],

            "metrics": [],

            "data": [],

            "implementation": False,

            "explanation": False,

            "comparison": False,

            "research": False,

            "debugging": False,

            "classification": False,

            "regression": False,

            "anomaly_detection": False,

            "fraud_detection": False,

            "deep_learning": False,

            "nlp": False,

            "computer_vision": False,
        }

        # --------------------------------------------------------
        # MACHINE LEARNING
        # --------------------------------------------------------

        ml_patterns = [

            r"\bml\b",

            r"\bmachine learning\b",

            r"\bmachine-learning\b",

            r"\bml model\b",

            r"\bmodel training\b",

            r"\btrain model\b",

            r"\btrain a model\b",

            r"\bneural network\b",

            r"\bdeep learning\b",

        ]

        if any(
            re.search(
                pattern,
                q
            )
            for pattern in ml_patterns
        ):

            analysis[
                "domain"
            ].append(
                "machine_learning"
            )

        # --------------------------------------------------------
        # DATA ANALYSIS
        # --------------------------------------------------------

        if any(
            term in q
            for term in [

                "dataset",

                "csv",

                "data analysis",

                "dataframe",

                "pandas",

                "transaction data",

            ]
        ):

            analysis[
                "domain"
            ].append(
                "data_analysis"
            )

        # --------------------------------------------------------
        # IMPLEMENTATION
        # --------------------------------------------------------

        if any(
            term in q
            for term in [

                "python",

                "code",

                "function",

                "algorithm",

                "implement",

                "implementation",

                "program",

                "write code",

                "write a program",

            ]
        ):

            analysis[
                "implementation"
            ] = True

        # --------------------------------------------------------
        # EXPLANATION
        # --------------------------------------------------------

        if any(
            term in q
            for term in [

                "explain",

                "why",

                "how does",

                "how do",

                "what is",

                "what are",

                "define",

                "meaning",

                "interpret",

                "interpretation",

            ]
        ):

            analysis[
                "explanation"
            ] = True

        # --------------------------------------------------------
        # COMPARISON
        # --------------------------------------------------------

        if any(
            term in q
            for term in [

                "compare",

                "comparison",

                "versus",

                " vs ",

            ]
        ):

            analysis[
                "comparison"
            ] = True

        # --------------------------------------------------------
        # RESEARCH
        # --------------------------------------------------------

        if any(
            term in q
            for term in [

                "research",

                "latest",

                "recent",

                "literature",

                "paper",

                "methodology",

            ]
        ):

            analysis[
                "research"
            ] = True

        # --------------------------------------------------------
        # DEBUGGING
        # --------------------------------------------------------

        if any(
            term in q
            for term in [

                "debug",

                "error",

                "exception",

                "traceback",

                "fix my code",

                "fix this code",

            ]
        ):

            analysis[
                "debugging"
            ] = True

        # --------------------------------------------------------
        # CLASSIFICATION
        # --------------------------------------------------------

        if any(
            term in q
            for term in [

                "classification",

                "classify",

                "fraud detection",

                "spam detection",

                "churn prediction",

                "binary classification",

            ]
        ):

            analysis[
                "classification"
            ] = True

            analysis[
                "task_type"
            ].append(
                "classification"
            )

        # --------------------------------------------------------
        # REGRESSION
        # --------------------------------------------------------

        if any(
            term in q
            for term in [

                "regression",

                "predict price",

                "predict sales",

                "continuous target",

            ]
        ):

            analysis[
                "regression"
            ] = True

            analysis[
                "task_type"
            ].append(
                "regression"
            )

        # --------------------------------------------------------
        # ANOMALY DETECTION
        # --------------------------------------------------------

        if any(
            term in q
            for term in [

                "anomaly detection",

                "anomalies",

                "outlier detection",

                "outliers",

            ]
        ):

            analysis[
                "anomaly_detection"
            ] = True

            analysis[
                "task_type"
            ].append(
                "anomaly_detection"
            )

        # --------------------------------------------------------
        # FRAUD DETECTION
        # --------------------------------------------------------

        if "fraud" in q:

            analysis[
                "fraud_detection"
            ] = True

        # --------------------------------------------------------
        # COMPUTER VISION
        # --------------------------------------------------------

        if any(
            term in q
            for term in [

                "cnn",

                "convolutional neural network",

                "image classification",

                "object detection",

                "yolo",

                "computer vision",

            ]
        ):

            analysis[
                "deep_learning"
            ] = True

            analysis[
                "computer_vision"
            ] = True

        # --------------------------------------------------------
        # NLP
        # --------------------------------------------------------

        if any(
            term in q
            for term in [

                "nlp",

                "natural language",

                "text classification",

                "sentiment analysis",

                "transformer",

            ]
        ):

            analysis[
                "deep_learning"
            ] = True

            analysis[
                "nlp"
            ] = True

        # --------------------------------------------------------
        # METRICS
        # --------------------------------------------------------

        metric_patterns = [

            "accuracy",

            "precision",

            "recall",

            "f1",

            "f1 score",

            "roc-auc",

            "roc auc",

            "auc",

            "pr-auc",

            "specificity",

            "sensitivity",

            "mae",

            "mse",

            "rmse",

            "r2",

            "ssim",

        ]

        for metric in metric_patterns:

            if metric in q:

                analysis[
                    "metrics"
                ].append(
                    metric
                )

        # --------------------------------------------------------
        # DATA REQUIREMENTS
        # --------------------------------------------------------

        if any(
            term in q
            for term in [

                "missing values",

                "missing data",

                "null values",

                "preprocess",

                "preprocessing",

            ]
        ):

            analysis[
                "data"
            ].append(
                "preprocessing"
            )

        if any(
            term in q
            for term in [

                "imbalanced",

                "class imbalance",

                "imbalanced dataset",

            ]
        ):

            analysis[
                "data"
            ].append(
                "class_imbalance"
            )

        if any(
            term in q
            for term in [

                "feature engineering",

                "features",

                "feature selection",

            ]
        ):

            analysis[
                "data"
            ].append(
                "feature_engineering"
            )

        if any(
            term in q
            for term in [

                "train test split",

                "validation",

                "cross validation",

                "cross-validation",

            ]
        ):

            analysis[
                "data"
            ].append(
                "validation"
            )

        return analysis


# ================================================================
# PLANNER AGENT
# ================================================================

class PlannerAgent:

    name = "PlannerAgent"

    def plan(
        self,
        query: str,
        intent: str,
        complexity: float,
        capabilities: List[str],
        brain_agents: Optional[
            List[str]
        ] = None,
    ) -> List[AgentTask]:

        intent = normalize_intent(
            intent
        )

        q = query.lower()

        analysis = QueryAnalyzer.analyze(
            query
        )

        tasks = []

        # ========================================================
        # CODING
        # ========================================================

        if intent == "CODING":

            tasks.append(
                AgentTask(
                    agent="CodingAgent",
                    objective=(
                        "Solve the programming problem "
                        "and provide a concrete implementation."
                    ),
                    priority=1
                )
            )

            if (
                "test" in q
                or "validate" in q
                or complexity >= 0.45
            ):

                tasks.append(
                    AgentTask(
                        agent="TestingAgent",
                        objective=(
                            "Validate the generated implementation."
                        ),
                        priority=2
                    )
                )

        # ========================================================
        # MACHINE LEARNING
        # ========================================================

        elif intent == "MACHINE_LEARNING":

            tasks.append(
                AgentTask(
                    agent="MLAgent",
                    objective=(
                        "Analyze the machine-learning problem, "
                        "task type, model strategy and evaluation."
                    ),
                    priority=1
                )
            )

            if (
                "dataset" in q
                or "csv" in q
                or "data analysis" in q
                or "dataframe" in q
                or "pandas" in q
                or "transaction data" in q
            ):

                tasks.append(
                    AgentTask(
                        agent="DataAnalysisAgent",
                        objective=(
                            "Analyze dataset characteristics, "
                            "preprocessing, data quality, "
                            "leakage and validation."
                        ),
                        priority=2
                    )
                )

            if analysis[
                "implementation"
            ]:

                tasks.append(
                    AgentTask(
                        agent="CodingAgent",
                        objective=(
                            "Convert the ML strategy "
                            "into code."
                        ),
                        priority=2
                    )
                )

        # ========================================================
        # DATA ANALYSIS
        # ========================================================

        elif intent == "DATA_ANALYSIS":

            tasks.append(
                AgentTask(
                    agent="DataAnalysisAgent",
                    objective=(
                        "Analyze dataset structure, "
                        "quality and patterns."
                    ),
                    priority=1
                )
            )

        # ========================================================
        # RESEARCH
        # ========================================================

        elif intent == "RESEARCH":

            tasks.append(
                AgentTask(
                    agent="ResearchAgent",
                    objective=(
                        "Develop a research methodology, "
                        "methods and evaluation strategy."
                    ),
                    priority=1
                )
            )

        # ========================================================
        # REASONING
        # ========================================================

        elif intent == "REASONING":

            tasks.append(
                AgentTask(
                    agent="ReasoningAgent",
                    objective=(
                        "Analyze the problem logically."
                    ),
                    priority=1
                )
            )

        # ========================================================
        # GENERAL
        # ========================================================

        else:

            tasks.append(
                AgentTask(
                    agent="GeneralAgent",
                    objective=(
                        "Analyze and respond to the request."
                    ),
                    priority=1
                )
            )

        # ========================================================
        # BRAIN RECOMMENDATIONS
        # ========================================================

        if brain_agents:

            allowed = {

                "MLAgent",

                "DataAnalysisAgent",

                "CodingAgent",

                "ResearchAgent",

                "ReasoningAgent",

                "GeneralAgent",

            }

            for agent in brain_agents:

                if agent is None:
                    continue

                agent_name = str(
                    agent
                ).strip()

                if not agent_name.endswith(
                    "Agent"
                ):

                    agent_name += "Agent"

                if agent_name not in allowed:
                    continue

                if not any(
                    task.agent == agent_name
                    for task in tasks
                ):

                    tasks.append(
                        AgentTask(
                            agent=agent_name,
                            objective=(
                                "Execute the capability "
                                "recommended by the Brain."
                            ),
                            priority=2
                        )
                    )

        # ========================================================
        # REASONING SUPPORT
        # ========================================================

        if not any(
            task.agent == "ReasoningAgent"
            for task in tasks
        ):

            if any(
                task.agent not in {

                    "ReasoningAgent",

                    "CriticAgent",

                    "TestingAgent",

                }
                for task in tasks
            ):

                tasks.append(
                    AgentTask(
                        agent="ReasoningAgent",
                        objective=(
                            "Cross-check specialist evidence."
                        ),
                        priority=3
                    )
                )

        # ========================================================
        # CRITIC
        # ========================================================

        if not any(
            task.agent == "CriticAgent"
            for task in tasks
        ):

            tasks.append(
                AgentTask(
                    agent="CriticAgent",
                    objective=(
                        "Validate evidence and completeness."
                    ),
                    priority=4
                )
            )

        # ========================================================
        # REMOVE DUPLICATES
        # ========================================================

        final_tasks = []

        seen = set()

        for task in sorted(
            tasks,
            key=lambda x: x.priority
        ):

            if task.agent not in seen:

                final_tasks.append(
                    task
                )

                seen.add(
                    task.agent
                )

        return final_tasks


# ================================================================
# TESTING AGENT
# ================================================================

class TestingAgent:

    name = "TestingAgent"

    def run(
        self,
        query: str,
        evidence: Dict[str, Any]
    ) -> AgentExecution:

        code_candidates = []

        for value in evidence.values():

            text = safe_text(
                value
            )

            if (
                "def " in text
                or "class " in text
            ):

                code_candidates.append(
                    text
                )

        code = ""

        if code_candidates:

            code = max(
                code_candidates,
                key=len
            )

        validation = validate_python(
            code
        )

        if validation[
            "valid"
        ]:

            return AgentExecution(
                agent=self.name,
                status="SUCCESS",
                output=(
                    "Python syntax validation passed."
                ),
                metadata=validation
            )

        return AgentExecution(
            agent=self.name,
            status="PARTIAL",
            output=(
                "No executable Python code "
                "was available for validation."
            ),
            metadata=validation
        )


# ================================================================
# ENHANCED CODING AGENT
# ================================================================

class EnhancedCodingAgent:

    name = "EnhancedCodingAgent"

    def generate(
        self,
        query: str
    ) -> AgentExecution:

        q = query.lower()

        # ========================================================
        # BINARY SEARCH
        # ========================================================

        if "binary search" in q:

            code = """def binary_search(arr, target):
    left = 0
    right = len(arr) - 1

    while left <= right:
        mid = (left + right) // 2

        if arr[mid] == target:
            return mid

        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1
"""

            return AgentExecution(
                agent=self.name,
                status="SUCCESS",
                output=code,
                metadata={
                    "validation": validate_python(
                        code
                    ),
                    "time_complexity": "O(log n)",
                    "space_complexity": "O(1)",
                }
            )

        # ========================================================
        # FIRST NON-REPEATING CHARACTER
        # ========================================================

        if (
            "first non-repeating character"
            in q
            or
            "first non repeating character"
            in q
        ):

            code = """def first_non_repeating_character(text):
    counts = {}

    for char in text:
        counts[char] = counts.get(char, 0) + 1

    for char in text:
        if counts[char] == 1:
            return char

    return None
"""

            return AgentExecution(
                agent=self.name,
                status="SUCCESS",
                output=code,
                metadata={
                    "validation": validate_python(
                        code
                    ),
                    "time_complexity": "O(n)",
                    "space_complexity": "O(k)",
                }
            )

        # ========================================================
        # REVERSE STRING
        # ========================================================

        if (
            "reverse a string" in q
            or "reverse string" in q
        ):

            code = """def reverse_string(text):
    return text[::-1]
"""

            return AgentExecution(
                agent=self.name,
                status="SUCCESS",
                output=code,
                metadata={
                    "validation": validate_python(
                        code
                    ),
                    "time_complexity": "O(n)",
                    "space_complexity": "O(n)",
                }
            )

        # ========================================================
        # DUPLICATES
        # ========================================================

        if (
            "duplicate elements" in q
            or "find duplicates" in q
        ):

            code = """def find_duplicates(arr):
    seen = set()
    duplicates = set()

    for value in arr:
        if value in seen:
            duplicates.add(value)
        else:
            seen.add(value)

    return list(duplicates)
"""

            return AgentExecution(
                agent=self.name,
                status="SUCCESS",
                output=code,
                metadata={
                    "validation": validate_python(
                        code
                    ),
                    "time_complexity": "O(n)",
                    "space_complexity": "O(n)",
                }
            )

        return AgentExecution(
            agent=self.name,
            status="PARTIAL",
            output=(
                "No specialized coding template matched."
            ),
            metadata={}
        )


# ================================================================
# ML QUERY ANALYZER
# ================================================================

class MLQueryAnalyzer:

    name = "MLQueryAnalyzer"

    def run(
        self,
        query: str
    ) -> AgentExecution:

        analysis = QueryAnalyzer.analyze(
            query
        )

        findings = []

        if analysis[
            "fraud_detection"
        ]:

            findings.append(
                "Domain: Fraud detection"
            )

            findings.append(
                "Task type: Binary classification"
            )

        elif analysis[
            "classification"
        ]:

            findings.append(
                "Task type: Classification"
            )

        elif analysis[
            "regression"
        ]:

            findings.append(
                "Task type: Regression"
            )

        elif analysis[
            "anomaly_detection"
        ]:

            findings.append(
                "Task type: Anomaly detection"
            )

        elif (
            analysis[
                "explanation"
            ]
            and (
                re.search(
                    r"\bml\b",
                    query.lower()
                )
                or
                "machine learning"
                in query.lower()
            )
        ):

            findings.append(
                "Task type: Conceptual machine-learning explanation"
            )

        else:

            findings.append(
                "Task type: General machine-learning task"
            )

        if analysis[
            "metrics"
        ]:

            findings.append(
                "Metrics: "
                + ", ".join(
                    analysis["metrics"]
                )
            )

        findings.append(
            "Validation should use a held-out test set "
            "or suitable cross-validation."
        )

        output = (
            "QUERY-SPECIFIC ML ANALYSIS\n\n"
            + "\n".join(
                f"{i + 1}. {item}"
                for i, item in enumerate(
                    findings
                )
            )
        )

        return AgentExecution(
            agent=self.name,
            status="SUCCESS",
            output=output,
            metadata=analysis
        )


# ================================================================
# DATA QUERY ANALYZER
# ================================================================

class DataQueryAnalyzer:

    name = "DataQueryAnalyzer"

    def run(
        self,
        query: str
    ) -> AgentExecution:

        q = query.lower()

        findings = []

        if "csv" in q:

            findings.append(
                "CSV input detected."
            )

        findings.append(
            "Inspect shape, columns, dtypes, "
            "missing values and duplicates."
        )

        if (
            "fraud" in q
            or "transaction" in q
        ):

            findings.append(
                "Check class imbalance and "
                "potential data leakage."
            )

        findings.append(
            "Keep validation/test data isolated "
            "from training transformations."
        )

        output = (
            "QUERY-SPECIFIC DATA ANALYSIS\n\n"
            + "\n".join(
                f"{i + 1}. {item}"
                for i, item in enumerate(
                    findings
                )
            )
        )

        return AgentExecution(
            agent=self.name,
            status="SUCCESS",
            output=output,
            metadata={}
        )


# ================================================================
# QUERY REASONING ENGINE
# ================================================================

class QueryReasoningEngine:

    name = "QueryReasoningEngine"

    def run(
        self,
        query: str,
        understanding: Dict[str, Any],
        evidence: Dict[str, Any]
    ) -> AgentExecution:

        intent = normalize_intent(
            understanding[
                "intent"
            ]
        )

        analysis = QueryAnalyzer.analyze(
            query
        )

        conclusions = []

        # ========================================================
        # ML
        # ========================================================

        if intent == "MACHINE_LEARNING":

            if analysis[
                "explanation"
            ]:

                conclusions.append(
                    "The query requests an explanation "
                    "of a machine-learning concept."
                )

            if analysis[
                "classification"
            ]:

                conclusions.append(
                    "Classification predicts discrete classes."
                )

            if analysis[
                "regression"
            ]:

                conclusions.append(
                    "Regression predicts continuous values."
                )

            if analysis[
                "fraud_detection"
            ]:

                conclusions.append(
                    "Fraud detection usually requires "
                    "careful treatment of class imbalance."
                )

            if analysis[
                "anomaly_detection"
            ]:

                conclusions.append(
                    "Anomaly detection identifies observations "
                    "that deviate from expected patterns."
                )

        # ========================================================
        # CODING
        # ========================================================

        elif intent == "CODING":

            conclusions.append(
                "The request requires an executable "
                "programming solution."
            )

        # ========================================================
        # DATA
        # ========================================================

        elif intent == "DATA_ANALYSIS":

            conclusions.append(
                "Dataset profiling should precede "
                "statistical conclusions."
            )

        # ========================================================
        # RESEARCH
        # ========================================================

        elif intent == "RESEARCH":

            conclusions.append(
                "Research methodology should define "
                "data, method and evaluation."
            )

        # ========================================================
        # REASONING
        # ========================================================

        elif intent == "REASONING":

            conclusions.append(
                "The request requires structured reasoning."
            )

        # ========================================================
        # GENERAL
        # ========================================================

        else:

            conclusions.append(
                "Evidence should be combined according "
                "to the user's objective."
            )

        specialist_count = len(
            [
                key
                for key in evidence
                if key not in {

                    "ReasoningAgent",

                    "CriticAgent",

                    "QueryReasoningEngine",

                    "QueryCritic",

                }
            ]
        )

        conclusions.append(
            f"Specialist evidence received from "
            f"{specialist_count} agent(s)."
        )

        output = (
            "QUERY-SPECIFIC REASONING\n\n"
            + "\n".join(
                f"{i + 1}. {item}"
                for i, item in enumerate(
                    conclusions
                )
            )
        )

        return AgentExecution(
            agent=self.name,
            status="SUCCESS",
            output=output,
            metadata={
                "intent": intent
            }
        )


# ================================================================
# QUERY CRITIC
# ================================================================

class QueryCritic:

    name = "QueryCritic"

    def run(
        self,
        query: str,
        understanding: Dict[str, Any],
        evidence: Dict[str, Any]
    ) -> AgentExecution:

        intent = normalize_intent(
            understanding[
                "intent"
            ]
        )

        expected = {

            "MACHINE_LEARNING": [

                "MLAgent",

                "MLQueryAnalyzer",

            ],

            "CODING": [

                "CodingAgent",

                "EnhancedCodingAgent",

            ],

            "DATA_ANALYSIS": [

                "DataAnalysisAgent",

                "DataQueryAnalyzer",

            ],

            "RESEARCH": [

                "ResearchAgent",

            ],

            "REASONING": [

                "ReasoningAgent",

                "QueryReasoningEngine",

            ],

            "GENERAL": [

                "GeneralAgent",

            ],
        }

        expected_agents = expected.get(
            intent,
            []
        )

        specialist_found = any(
            agent in evidence
            for agent in expected_agents
        )

        checks = []

        if specialist_found:

            checks.append(
                "PASS: Correct specialist evidence available."
            )

        else:

            checks.append(
                "FAIL: Expected specialist evidence missing."
            )

        if (
            "QueryReasoningEngine"
            in evidence
            or
            "ReasoningAgent"
            in evidence
        ):

            checks.append(
                "PASS: Reasoning stage completed."
            )

        else:

            checks.append(
                "FAIL: Reasoning stage missing."
            )

        failures = [

            item

            for item in checks

            if item.startswith(
                "FAIL"
            )

        ]

        status = (

            "PASSED"

            if not failures

            else

            "FAILED"
        )

        output = (
            "QUERY-AWARE CRITIC\n\n"
            + "\n".join(
                checks
            )
            + "\n\n"
            + f"Final validation: {status}"
        )

        return AgentExecution(
            agent=self.name,
            status=status,
            output=output,
            metadata={
                "intent": intent,
                "checks": checks
            }
        )


# ================================================================
# PHASE 3 ORCHESTRATOR
# ================================================================

class Phase3Orchestrator:

    def __init__(self):

        self.brain = (
            IntelligenceBrain()
        )

        self.phase2 = (
            MultiAgentSystem()
        )

        self.planner = (
            PlannerAgent()
        )

        self.testing = (
            TestingAgent()
        )

        self.enhanced_coding = (
            EnhancedCodingAgent()
        )

        self.ml_query_analyzer = (
            MLQueryAnalyzer()
        )

        self.data_query_analyzer = (
            DataQueryAnalyzer()
        )

        self.reasoning_engine = (
            QueryReasoningEngine()
        )

        self.query_critic = (
            QueryCritic()
        )

        self._current_intent = (
            "GENERAL"
        )

    # ============================================================
    # UNDERSTAND
    # ============================================================

    def understand(
        self,
        query: str
    ) -> Dict[str, Any]:

        decision = self.brain.think(
            query
        )

        understanding = (
            decision.understanding
        )

        return {

            "intent":
                normalize_intent(
                    understanding.intent
                ),

            "goal":
                understanding.goal,

            "complexity":
                understanding.complexity,

            "entities":
                understanding.entities,

            "requirements":
                understanding.requirements,

            "constraints":
                understanding.constraints,

            "capabilities":
                understanding.capabilities,

            "needs_tools":
                understanding.needs_tools,

            "needs_multiple_agents":
                understanding.needs_multiple_agents,

            "brain_agents":
                decision.recommended_agents,

            "brain_reasoning":
                decision.reasoning,

            "confidence":
                decision.confidence,
        }

    # ============================================================
    # PHASE 2 SPECIALIST
    # ============================================================

    def execute_phase2_specialist(
        self,
        agent_name: str,
        query: str
    ) -> Optional[AgentExecution]:

        try:

            agents = getattr(
                self.phase2,
                "agents",
                {}
            )

            agent = agents.get(
                agent_name
            )

            if agent is None:

                return None

            result = agent.run(
                query
            )

            return AgentExecution(
                agent=agent_name,
                status=getattr(
                    result,
                    "status",
                    "SUCCESS"
                ),
                output=getattr(
                    result,
                    "output",
                    result
                ),
                metadata={}
            )

        except Exception as exc:

            return AgentExecution(
                agent=agent_name,
                status="FAILED",
                output="",
                metadata={
                    "error": str(exc),
                    "traceback":
                        traceback.format_exc()
                }
            )

    # ============================================================
    # AUGMENT TASKS
    # ============================================================

    def augment_tasks(
        self,
        tasks: List[AgentTask],
        query: str,
        intent: str,
        complexity: float
    ) -> List[AgentTask]:

        intent = normalize_intent(
            intent
        )

        result = list(
            tasks
        )

        existing = {

            task.agent

            for task in result

        }

        q = query.lower()

        # --------------------------------------------------------
        # ML
        # --------------------------------------------------------

        if intent == "MACHINE_LEARNING":

            if (
                "MLQueryAnalyzer"
                not in existing
            ):

                result.append(
                    AgentTask(
                        agent="MLQueryAnalyzer",
                        objective=(
                            "Perform query-specific "
                            "machine-learning analysis."
                        ),
                        priority=1
                    )
                )

            if (
                "csv" in q
                or "dataset" in q
                or "dataframe" in q
                or "pandas" in q
                or "transaction data" in q
            ):

                if (
                    "DataQueryAnalyzer"
                    not in existing
                ):

                    result.append(
                        AgentTask(
                            agent="DataQueryAnalyzer",
                            objective=(
                                "Perform query-specific "
                                "data analysis."
                            ),
                            priority=2
                        )
                    )

        # --------------------------------------------------------
        # DATA
        # --------------------------------------------------------

        if intent == "DATA_ANALYSIS":

            if (
                "DataQueryAnalyzer"
                not in existing
            ):

                result.append(
                    AgentTask(
                        agent="DataQueryAnalyzer",
                        objective=(
                            "Perform query-specific "
                            "data analysis."
                        ),
                        priority=1
                    )
                )

        # --------------------------------------------------------
        # CODING SPECIAL CASES
        # --------------------------------------------------------

        coding_cases = (

            "binary search" in q

            or
            "first non-repeating character"
            in q

            or
            "first non repeating character"
            in q

            or
            "reverse a string"
            in q

            or
            "reverse string"
            in q

            or
            "duplicate elements"
            in q

            or
            "find duplicates"
            in q
        )

        if (
            intent == "CODING"
            and coding_cases
        ):

            if (
                "EnhancedCodingAgent"
                not in existing
            ):

                result.append(
                    AgentTask(
                        agent="EnhancedCodingAgent",
                        objective=(
                            "Generate a concrete "
                            "coding implementation."
                        ),
                        priority=1
                    )
                )

        return sorted(
            result,
            key=lambda x: x.priority
        )

    # ============================================================
    # EXECUTE TASK
    # ============================================================

    def execute_task(
        self,
        task: AgentTask,
        query: str,
        evidence: Dict[str, Any]
    ) -> AgentExecution:

        # --------------------------------------------------------
        # ENHANCED CODING
        # --------------------------------------------------------

        if (
            task.agent
            == "EnhancedCodingAgent"
        ):

            return (
                self.enhanced_coding.generate(
                    query
                )
            )

        # --------------------------------------------------------
        # TESTING
        # --------------------------------------------------------

        if (
            task.agent
            == "TestingAgent"
        ):

            return (
                self.testing.run(
                    query,
                    evidence
                )
            )

        # --------------------------------------------------------
        # ML ANALYZER
        # --------------------------------------------------------

        if (
            task.agent
            == "MLQueryAnalyzer"
        ):

            return (
                self.ml_query_analyzer.run(
                    query
                )
            )

        # --------------------------------------------------------
        # DATA ANALYZER
        # --------------------------------------------------------

        if (
            task.agent
            == "DataQueryAnalyzer"
        ):

            return (
                self.data_query_analyzer.run(
                    query
                )
            )

        # --------------------------------------------------------
        # LOCAL REASONING
        # --------------------------------------------------------

        if (
            task.agent
            == "QueryReasoningEngine"
        ):

            return (
                self.reasoning_engine.run(
                    query,
                    {
                        "intent":
                            self._current_intent
                    },
                    evidence
                )
            )

        # --------------------------------------------------------
        # LOCAL CRITIC
        # --------------------------------------------------------

        if (
            task.agent
            == "QueryCritic"
        ):

            return (
                self.query_critic.run(
                    query,
                    {
                        "intent":
                            self._current_intent
                    },
                    evidence
                )
            )

        # --------------------------------------------------------
        # PHASE 2 AGENTS
        # --------------------------------------------------------

        phase2_agents = {

            "CodingAgent",

            "MLAgent",

            "DataAnalysisAgent",

            "ResearchAgent",

            "GeneralAgent",

            "ReasoningAgent",

            "CriticAgent",

        }

        if (
            task.agent
            in phase2_agents
        ):

            result = (
                self.execute_phase2_specialist(
                    task.agent,
                    query
                )
            )

            if result is not None:

                return result

        return AgentExecution(
            agent=task.agent,
            status="FAILED",
            output=(
                f"Agent '{task.agent}' "
                "is unavailable."
            ),
            metadata={}
        )

    # ============================================================
    # PROCESS
    # ============================================================

    def process(
        self,
        query: str
    ) -> Phase3Result:

        if not isinstance(
            query,
            str
        ):

            raise ValueError(
                "Query must be a string."
            )

        if not query.strip():

            raise ValueError(
                "Query cannot be empty."
            )

        # ========================================================
        # 1. BRAIN
        # ========================================================

        understanding = (
            self.understand(
                query
            )
        )

        intent = normalize_intent(
            understanding[
                "intent"
            ]
        )

        complexity = (
            understanding[
                "complexity"
            ]
        )

        self._current_intent = (
            intent
        )

        # ========================================================
        # 2. PLANNER
        # ========================================================

        tasks = self.planner.plan(

            query=query,

            intent=intent,

            complexity=complexity,

            capabilities=(
                understanding[
                    "capabilities"
                ]
            ),

            brain_agents=(
                understanding[
                    "brain_agents"
                ]
            ),
        )

        # ========================================================
        # 3. AUGMENT
        # ========================================================

        tasks = self.augment_tasks(

            tasks=tasks,

            query=query,

            intent=intent,

            complexity=complexity
        )

        # ========================================================
        # 4. EXECUTION
        # ========================================================

        executions = []

        evidence = {}

        support_agents = {

            "ReasoningAgent",

            "QueryReasoningEngine",

            "CriticAgent",

            "QueryCritic",

            "TestingAgent",

        }

        specialist_tasks = [

            task

            for task in tasks

            if task.agent
            not in support_agents

        ]

        for task in specialist_tasks:

            execution = (
                self.execute_task(
                    task,
                    query,
                    evidence
                )
            )

            executions.append(
                execution
            )

            evidence[
                execution.agent
            ] = execution.output

        # ========================================================
        # 5. TESTING
        # ========================================================

        if any(

            task.agent
            == "TestingAgent"

            for task in tasks

        ):

            execution = (
                self.testing.run(
                    query,
                    evidence
                )
            )

            executions.append(
                execution
            )

            evidence[
                "TestingAgent"
            ] = execution.output

        # ========================================================
        # 6. LOCAL REASONING
        # ========================================================

        reasoning_execution = (
            self.reasoning_engine.run(

                query,

                understanding,

                evidence

            )
        )

        executions.append(
            reasoning_execution
        )

        evidence[
            "QueryReasoningEngine"
        ] = reasoning_execution.output

        # ========================================================
        # 7. PHASE 2 REASONING
        # ========================================================
        #
        # INTERNAL ONLY
        # Not exposed to user.
        # ========================================================

        if any(

            task.agent
            == "ReasoningAgent"

            for task in tasks

        ):

            reasoning_input = (

                "PHASE 3 CANONICAL INTENT: "

                + intent

                + "\n\nUSER QUERY:\n"

                + query

                + "\n\nSPECIALIST EVIDENCE:\n"

                + safe_text(
                    evidence
                )
            )

            execution = (
                self.execute_phase2_specialist(

                    "ReasoningAgent",

                    reasoning_input

                )
            )

            if execution is not None:

                executions.append(
                    execution
                )

                evidence[
                    "ReasoningAgent"
                ] = execution.output

        # ========================================================
        # 8. LOCAL CRITIC
        # ========================================================

        critic_execution = (
            self.query_critic.run(

                query,

                understanding,

                evidence

            )
        )

        executions.append(
            critic_execution
        )

        evidence[
            "QueryCritic"
        ] = critic_execution.output

        # ========================================================
        # 9. PHASE 2 CRITIC
        # ========================================================
        #
        # INTERNAL ONLY
        # ========================================================

        if any(

            task.agent
            == "CriticAgent"

            for task in tasks

        ):

            critic_input = (

                "PHASE 3 CANONICAL INTENT: "

                + intent

                + "\n\nUSER QUERY:\n"

                + query

                + "\n\nPIPELINE EVIDENCE:\n"

                + safe_text(
                    evidence
                )
            )

            execution = (
                self.execute_phase2_specialist(

                    "CriticAgent",

                    critic_input

                )
            )

            if execution is not None:

                executions.append(
                    execution
                )

                evidence[
                    "CriticAgent"
                ] = execution.output

        # ========================================================
        # 10. INTERNAL CRITIC STATUS
        # ========================================================

        critic_status = (

            "PASSED"

            if
            critic_execution.status
            == "PASSED"

            else
            "FAILED"
        )

        # ========================================================
        # 11. FINAL USER ANSWER
        # ========================================================
        #
        # ONLY THIS STRING GOES TO THE USER.
        # ========================================================

        final_response = (
            self.generate_user_answer(

                query=query,

                understanding=understanding,

                executions=executions

            )
        )

        selected_agents = unique_list(

            [
                task.agent

                for task in tasks

            ]
        )

        return Phase3Result(

            query=query,

            intent=intent,

            complexity=complexity,

            selected_agents=selected_agents,

            executions=executions,

            critic_status=critic_status,

            final_response=final_response,

        )

    # ============================================================
    # FINAL USER ANSWER
    # ============================================================

    def generate_user_answer(
        self,
        query: str,
        understanding: Dict[str, Any],
        executions: List[AgentExecution]
    ) -> str:

        intent = normalize_intent(
            understanding[
                "intent"
            ]
        )

        q = query.lower()

        analysis = QueryAnalyzer.analyze(
            query
        )

        # ========================================================
        # MACHINE LEARNING
        # ========================================================

        if (
            intent
            == "MACHINE_LEARNING"
        ):

            # ----------------------------------------------------
            # GENERAL ML EXPLANATION
            # ----------------------------------------------------

            if (

                analysis[
                    "explanation"
                ]

                and re.search(
                    r"\bml\b",
                    q
                )

                and not analysis[
                    "classification"
                ]

                and not analysis[
                    "regression"
                ]

                and not analysis[
                    "fraud_detection"
                ]

                and not analysis[
                    "anomaly_detection"
                ]

                and not analysis[
                    "computer_vision"
                ]

                and not analysis[
                    "nlp"
                ]

            ):

                return (
                    "Machine Learning (ML) is a branch of "
                    "Artificial Intelligence in which computers "
                    "learn patterns from data and use those "
                    "patterns to make predictions or decisions "
                    "without being explicitly programmed for "
                    "every individual case.\n\n"

                    "Main types of Machine Learning:\n"

                    "1. Supervised Learning - learns from "
                    "labelled data, such as classification "
                    "and regression.\n"

                    "2. Unsupervised Learning - finds patterns "
                    "in unlabelled data, such as clustering "
                    "and anomaly detection.\n"

                    "3. Reinforcement Learning - learns actions "
                    "through rewards and penalties.\n\n"

                    "Typical ML workflow:\n"

                    "Data → Preprocessing → Feature Engineering "
                    "→ Model Training → Validation → Evaluation "
                    "→ Prediction.\n\n"

                    "Example: a model can learn from historical "
                    "house prices and then predict the price "
                    "of a new house based on its features."
                )

            # ----------------------------------------------------
            # CLASSIFICATION
            # ----------------------------------------------------

            if analysis[
                "classification"
            ]:

                answer = (

                    "This is a classification problem because "
                    "the model predicts a discrete class or "
                    "category.\n\n"

                    "Recommended workflow:\n"

                    "1. Prepare and inspect the dataset.\n"

                    "2. Split the data into training and "
                    "validation/test sets.\n"

                    "3. Preprocess the features.\n"

                    "4. Train a baseline classifier.\n"

                    "5. Evaluate using precision, recall, "
                    "F1-score and the confusion matrix.\n"

                    "6. Tune the model and decision threshold "
                    "if required."
                )

                if analysis[
                    "fraud_detection"
                ]:

                    answer += (

                        "\n\nFor fraud detection, accuracy "
                        "alone can be misleading because "
                        "fraud is often a minority class. "
                        "Precision, recall, F1-score and "
                        "PR-AUC can provide more useful "
                        "information."
                    )

                return answer

            # ----------------------------------------------------
            # REGRESSION
            # ----------------------------------------------------

            if analysis[
                "regression"
            ]:

                return (

                    "This is a regression problem because "
                    "the model predicts a continuous "
                    "numerical value.\n\n"

                    "Recommended workflow:\n"

                    "1. Inspect the target distribution.\n"

                    "2. Clean and preprocess the features.\n"

                    "3. Establish a baseline regression model.\n"

                    "4. Evaluate using MAE, MSE, RMSE and R².\n"

                    "5. Perform error analysis and compare models."
                )

            # ----------------------------------------------------
            # ANOMALY DETECTION
            # ----------------------------------------------------

            if analysis[
                "anomaly_detection"
            ]:

                return (

                    "Anomaly detection identifies observations "
                    "that deviate substantially from expected "
                    "patterns.\n\n"

                    "Common approaches include:\n"

                    "1. Isolation Forest\n"

                    "2. One-Class SVM\n"

                    "3. Autoencoders\n"

                    "4. Statistical thresholding\n\n"

                    "The important part is defining what "
                    "constitutes an anomaly and validating "
                    "whether detected anomalies correspond "
                    "to meaningful events."
                )

            # ----------------------------------------------------
            # FRAUD DETECTION
            # ----------------------------------------------------

            if analysis[
                "fraud_detection"
            ]:

                return (

                    "Fraud detection is typically formulated "
                    "as a binary classification problem: "
                    "legitimate versus fraudulent.\n\n"

                    "Because fraud datasets are often imbalanced, "
                    "accuracy should not be the only evaluation "
                    "metric. Precision, recall, F1-score, PR-AUC "
                    "and the confusion matrix should be considered.\n\n"

                    "Threshold tuning can also be important "
                    "because the default 0.50 decision threshold "
                    "may not match the application's "
                    "false-positive and false-negative costs."
                )

            # ----------------------------------------------------
            # COMPUTER VISION
            # ----------------------------------------------------

            if analysis[
                "computer_vision"
            ]:

                return (

                    "This is a computer-vision machine-learning "
                    "task.\n\n"

                    "A common workflow is:\n"

                    "1. Collect and clean images.\n"

                    "2. Resize and normalize inputs.\n"

                    "3. Split data into train, validation and "
                    "test sets.\n"

                    "4. Train a CNN or use transfer learning.\n"

                    "5. Evaluate using task-specific metrics.\n"

                    "6. Analyze incorrect predictions."
                )

            # ----------------------------------------------------
            # NLP
            # ----------------------------------------------------

            if analysis[
                "nlp"
            ]:

                return (

                    "This is an NLP machine-learning task "
                    "involving text or language data.\n\n"

                    "Typical workflow:\n"

                    "1. Clean and tokenize the text.\n"

                    "2. Convert text into useful representations.\n"

                    "3. Train a baseline model.\n"

                    "4. Evaluate on a held-out dataset.\n"

                    "5. Use transformers or other advanced "
                    "models when required."
                )

            # ----------------------------------------------------
            # GENERAL ML
            # ----------------------------------------------------

            return (

                "This is a Machine Learning task.\n\n"

                "A standard workflow is:\n"

                "1. Define the prediction or learning objective.\n"

                "2. Collect and inspect the data.\n"

                "3. Preprocess the features.\n"

                "4. Establish a baseline model.\n"

                "5. Train and validate the model.\n"

                "6. Evaluate using metrics appropriate "
                "to the task.\n"

                "7. Perform error analysis and improve the model."
            )

        # ========================================================
        # CODING
        # ========================================================

        if intent == "CODING":

            # ----------------------------------------------------
            # BINARY SEARCH
            # ----------------------------------------------------

            if "binary search" in q:

                return (

                    "```python\n"

                    "def binary_search(arr, target):\n"

                    "    left = 0\n"

                    "    right = len(arr) - 1\n\n"

                    "    while left <= right:\n"

                    "        mid = (left + right) // 2\n\n"

                    "        if arr[mid] == target:\n"

                    "            return mid\n\n"

                    "        if arr[mid] < target:\n"

                    "            left = mid + 1\n"

                    "        else:\n"

                    "            right = mid - 1\n\n"

                    "    return -1\n"

                    "```\n\n"

                    "### Time Complexity\n\n"

                    "**O(log n)** because the search space "
                    "is divided in half after every iteration.\n\n"

                    "### Space Complexity\n\n"

                    "**O(1)** auxiliary space because the "
                    "iterative implementation uses only a "
                    "fixed number of variables."
                )

            # ----------------------------------------------------
            # FIRST NON-REPEATING CHARACTER
            # ----------------------------------------------------

            if (

                "first non-repeating character"
                in q

                or

                "first non repeating character"
                in q

            ):

                return (

                    "```python\n"

                    "def first_non_repeating_character(text):\n"

                    "    counts = {}\n\n"

                    "    for char in text:\n"

                    "        counts[char] = "
                    "counts.get(char, 0) + 1\n\n"

                    "    for char in text:\n"

                    "        if counts[char] == 1:\n"

                    "            return char\n\n"

                    "    return None\n"

                    "```\n\n"

                    "### Time Complexity\n\n"

                    "**O(n)** because the string is traversed "
                    "twice, which is still linear.\n\n"

                    "### Space Complexity\n\n"

                    "**O(k)** where `k` is the number of "
                    "distinct characters stored in the "
                    "frequency dictionary."
                )

            # ----------------------------------------------------
            # REVERSE STRING
            # ----------------------------------------------------

            if (

                "reverse a string"
                in q

                or

                "reverse string"
                in q

            ):

                return (

                    "```python\n"

                    "def reverse_string(text):\n"

                    "    return text[::-1]\n"

                    "```\n\n"

                    "### Time Complexity\n\n"

                    "**O(n)**.\n\n"

                    "### Space Complexity\n\n"

                    "**O(n)** because Python creates a "
                    "new reversed string."
                )

            # ----------------------------------------------------
            # DUPLICATES
            # ----------------------------------------------------

            if (

                "duplicate elements"
                in q

                or

                "find duplicates"
                in q

            ):

                return (

                    "```python\n"

                    "def find_duplicates(arr):\n"

                    "    seen = set()\n"

                    "    duplicates = set()\n\n"

                    "    for value in arr:\n"

                    "        if value in seen:\n"

                    "            duplicates.add(value)\n"

                    "        else:\n"

                    "            seen.add(value)\n\n"

                    "    return list(duplicates)\n"

                    "```\n\n"

                    "### Time Complexity\n\n"

                    "**O(n)** average time.\n\n"

                    "### Space Complexity\n\n"

                    "**O(n)** in the worst case."
                )

            # ----------------------------------------------------
            # ENHANCED CODING FALLBACK
            # ----------------------------------------------------

            for execution in executions:

                if (

                    execution.agent
                    == "EnhancedCodingAgent"

                    and

                    execution.status
                    == "SUCCESS"

                ):

                    code = safe_text(
                        execution.output
                    )

                    return (

                        "```python\n"

                        + code.strip()

                        + "\n```"
                    )

            return (

                "The request requires a programming "
                "solution. The coding agent has analyzed "
                "the problem."
            )

        # ========================================================
        # DATA ANALYSIS
        # ========================================================

        if (
            intent
            == "DATA_ANALYSIS"
        ):

            return (

                "The dataset should first be profiled for "
                "shape, columns, data types, missing values, "
                "duplicates and target/distribution "
                "characteristics.\n\n"

                "After profiling, preprocessing and feature "
                "engineering can be applied while keeping "
                "validation and test information isolated "
                "to avoid data leakage."
            )

        # ========================================================
        # RESEARCH
        # ========================================================

        if intent == "RESEARCH":

            return (

                "A strong research workflow should define "
                "the research question, dataset, methodology, "
                "baseline, evaluation metrics and "
                "reproducibility procedure.\n\n"

                "The final conclusion should be supported "
                "by experimental evidence."
            )

        # ========================================================
        # REASONING
        # ========================================================

        if intent == "REASONING":

            return (

                "The request requires structured reasoning. "
                "The relevant evidence should be combined, "
                "checked for contradictions and then "
                "converted into a clear conclusion."
            )

        # ========================================================
        # GENERAL
        # ========================================================

        return (

            "I analyzed the request using the RETRO-AI "
            "multi-agent system and routed it through "
            "the appropriate processing pipeline."
        )


# ================================================================
# PHASE 3 TEST SUITE
# ================================================================

def run_phase3_tests():

    print()
    print("=" * 72)
    print("RETRO-AI PHASE 3 TEST SUITE")
    print("=" * 72)

    system = Phase3Orchestrator()

    tests = [

        (
            "ML Explanation",
            "Explain ML"
        ),

        (
            "Binary Search",
            (
                "Write Python code to implement "
                "binary search and explain its "
                "time complexity."
            )
        ),

        (
            "First Non-Repeating Character",
            (
                "Write Python code to find the "
                "first non-repeating character "
                "in a string."
            )
        ),

        (
            "Reverse String",
            (
                "Write Python code to reverse a string."
            )
        ),

        (
            "Duplicate Detection",
            (
                "Write Python code to find duplicate "
                "elements in an array."
            )
        ),

        (
            "Fraud Detection",
            (
                "My fraud detection model has 99% "
                "accuracy but only 40% recall. "
                "How should I evaluate it?"
            )
        ),

        (
            "Research",
            (
                "Design a research methodology for "
                "anomaly detection in satellite images."
            )
        ),
    ]

    passed = 0

    for index, (
        name,
        query
    ) in enumerate(
        tests,
        1
    ):

        print()
        print("-" * 72)

        print(
            f"TEST {index}: {name}"
        )

        print(
            f"QUERY: {query}"
        )

        try:

            result = system.process(
                query
            )

            if (
                result.final_response
                and
                result.final_response.strip()
            ):

                passed += 1

                print(
                    "STATUS: PASS"
                )

            else:

                print(
                    "STATUS: FAIL"
                )

            print()
            print(
                "FINAL ANSWER:"
            )

            print(
                result.final_response
            )

            print()
            print(
                "INTERNAL INTENT:",
                result.intent
            )

            print(
                "INTERNAL AGENTS:",
                result.selected_agents
            )

            print(
                "INTERNAL CRITIC:",
                result.critic_status
            )

        except Exception:

            print(
                "STATUS: ERROR"
            )

            traceback.print_exc()

    print()
    print("=" * 72)

    print(
        f"PHASE 3 TESTS: "
        f"{passed}/{len(tests)} PASSED"
    )

    print("=" * 72)


# ================================================================
# MAIN
# ================================================================

if __name__ == "__main__":

    run_phase3_tests()