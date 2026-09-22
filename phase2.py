# ============================================================
# RETRO-AI PHASE 2
# MULTI-AGENT INTELLIGENCE SYSTEM
# ============================================================

import ast
import json
import re
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple


# ============================================================
# OPTIONAL INTELLIGENCE BRAIN
# ============================================================

try:
    from brain import IntelligenceBrain
except Exception:
    IntelligenceBrain = None


# ============================================================
# RESULT OBJECT
# ============================================================

@dataclass
class AgentResult:
    agent_name: str
    intent: str
    success: bool
    output: str
    metadata: Dict[str, Any]


# ============================================================
# BASE AGENT
# ============================================================

class BaseAgent:

    def __init__(self, name: str):
        self.name = name

    def run(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResult:
        raise NotImplementedError


# ============================================================
# HELPERS
# ============================================================

def normalize_intent(intent: str) -> str:

    value = str(intent).strip().lower()

    mapping = {
        "ml": "MACHINE_LEARNING",
        "machine learning": "MACHINE_LEARNING",
        "machine_learning": "MACHINE_LEARNING",
        "machine-learning": "MACHINE_LEARNING",
        "machinelearning": "MACHINE_LEARNING",

        "coding": "CODING",
        "code": "CODING",
        "programming": "CODING",

        "data analysis": "DATA_ANALYSIS",
        "data_analysis": "DATA_ANALYSIS",
        "data-analysis": "DATA_ANALYSIS",
        "dataanalysis": "DATA_ANALYSIS",

        "research": "RESEARCH",

        "general": "GENERAL",
        "chat": "GENERAL",
    }

    return mapping.get(value, value.upper())


def normalize_agent_name(name: str) -> str:

    value = str(name).strip().lower()

    mapping = {
        "ml": "MLAgent",
        "mlagent": "MLAgent",
        "machine_learning": "MLAgent",
        "machinelearning": "MLAgent",

        "coding": "CodingAgent",
        "codingagent": "CodingAgent",
        "code": "CodingAgent",

        "data_analysis": "DataAnalysisAgent",
        "dataanalysis": "DataAnalysisAgent",
        "dataanalysisagent": "DataAnalysisAgent",

        "research": "ResearchAgent",
        "researchagent": "ResearchAgent",

        "reasoning": "ReasoningAgent",
        "reasoningagent": "ReasoningAgent",

        "critic": "CriticAgent",
        "criticagent": "CriticAgent",

        "general": "GeneralAgent",
        "generalagent": "GeneralAgent",
    }

    return mapping.get(value, name)


def validate_python_code(code: str) -> Dict[str, Any]:

    result = {
        "valid": False,
        "error": None,
        "functions": [],
        "classes": [],
        "imports": [],
    }

    try:

        tree = ast.parse(code)

        result["valid"] = True

        for node in ast.walk(tree):

            if isinstance(
                node,
                (ast.FunctionDef, ast.AsyncFunctionDef)
            ):
                result["functions"].append(node.name)

            elif isinstance(node, ast.ClassDef):
                result["classes"].append(node.name)

            elif isinstance(node, ast.Import):

                for alias in node.names:
                    result["imports"].append(alias.name)

            elif isinstance(node, ast.ImportFrom):

                if node.module:
                    result["imports"].append(node.module)

    except SyntaxError as exc:

        result["error"] = (
            f"{exc.msg} "
            f"at line {exc.lineno}, column {exc.offset}"
        )

    except Exception as exc:

        result["error"] = str(exc)

    return result


# ============================================================
# MACHINE LEARNING AGENT
# ============================================================

class MLAgent(BaseAgent):

    def __init__(self):
        super().__init__("MLAgent")

    def run(
        self,
        query: str,
        context=None
    ) -> AgentResult:

        q = query.lower()

        output = []

        output.append("MACHINE LEARNING AGENT")
        output.append("=" * 45)

        # ----------------------------------------------------
        # FRAUD / IMBALANCED CLASSIFICATION
        # ----------------------------------------------------

        if (
            "fraud" in q
            or "imbalance" in q
            or "imbalanced" in q
        ):

            output.append(
                "\nProblem type:"
            )

            output.append(
                "Binary classification with possible severe class imbalance."
            )

            output.append(
                "\nRecommended evaluation metrics:"
            )

            output.append(
                "1. Precision"
            )

            output.append(
                "2. Recall"
            )

            output.append(
                "3. F1-score"
            )

            output.append(
                "4. ROC-AUC"
            )

            output.append(
                "5. PR-AUC"
            )

            output.append(
                "6. Confusion Matrix"
            )

            output.append(
                "\nEvaluation reasoning:"
            )

            output.append(
                "Accuracy alone can be misleading when fraudulent "
                "transactions represent a small fraction of all transactions."
            )

            output.append(
                "Recall measures how many actual fraud cases are detected."
            )

            output.append(
                "Precision measures how many transactions predicted as "
                "fraud are actually fraudulent."
            )

            output.append(
                "PR-AUC is particularly informative when the positive "
                "class is rare."
            )

            output.append(
                "\nRecommended workflow:"
            )

            output.append(
                "1. Split data using stratification."
            )

            output.append(
                "2. Prevent data leakage."
            )

            output.append(
                "3. Establish a baseline."
            )

            output.append(
                "4. Evaluate precision, recall and F1."
            )

            output.append(
                "5. Inspect ROC-AUC and PR-AUC."
            )

            output.append(
                "6. Tune the decision threshold."
            )

            output.append(
                "7. Analyze the confusion matrix."
            )

            output.append(
                "8. Validate on untouched test data."
            )

        # ----------------------------------------------------
        # OVERFITTING
        # ----------------------------------------------------

        elif (
            "overfit" in q
            or "overfitting" in q
        ):

            output.append(
                "Problem type: Model generalization / overfitting."
            )

            output.append(
                "\nDiagnostic steps:"
            )

            output.append(
                "1. Compare training and validation loss."
            )

            output.append(
                "2. Compare training and validation metrics."
            )

            output.append(
                "3. Measure the generalization gap."
            )

            output.append(
                "4. Inspect model complexity."
            )

            output.append(
                "5. Check dataset size and quality."
            )

            output.append(
                "\nPossible interventions:"
            )

            output.append(
                "- Dropout"
            )

            output.append(
                "- L1/L2 regularization"
            )

            output.append(
                "- Early stopping"
            )

            output.append(
                "- Data augmentation"
            )

            output.append(
                "- Smaller architecture"
            )

            output.append(
                "- More representative data"
            )

        # ----------------------------------------------------
        # GENERAL ML
        # ----------------------------------------------------

        else:

            output.append(
                "Problem type: General machine-learning task."
            )

            output.append(
                "\nRecommended workflow:"
            )

            output.append(
                "1. Define target."
            )

            output.append(
                "2. Inspect dataset."
            )

            output.append(
                "3. Preprocess features."
            )

            output.append(
                "4. Establish baseline."
            )

            output.append(
                "5. Train model."
            )

            output.append(
                "6. Validate model."
            )

            output.append(
                "7. Perform error analysis."
            )

            output.append(
                "8. Evaluate on held-out test data."
            )

        return AgentResult(
            agent_name=self.name,
            intent="MACHINE_LEARNING",
            success=True,
            output="\n".join(output),
            metadata={
                "domain": "machine_learning",
                "fraud_related": (
                    "fraud" in q
                    or "imbalance" in q
                    or "imbalanced" in q
                ),
            },
        )


# ============================================================
# CODING AGENT
# ============================================================

class CodingAgent(BaseAgent):

    def __init__(self):
        super().__init__("CodingAgent")

    def generate_code(
        self,
        query: str
    ) -> Tuple[str, str]:

        q = query.lower()

        if "prime" in q:

            return (
'''def is_prime(n):
    if n < 2:
        return False

    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False

    return True
''',
                "Checks divisibility up to sqrt(n), "
                "giving O(sqrt(n)) time complexity."
            )

        if "duplicate" in q:

            return (
'''def find_duplicates(items):
    seen = set()
    duplicates = set()

    for item in items:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)

    return list(duplicates)
''',
                "Uses a set for efficient membership checks "
                "with average O(n) time complexity."
            )

        if "second largest" in q:

            return (
'''def second_largest(numbers):
    unique_numbers = set(numbers)

    if len(unique_numbers) < 2:
        raise ValueError(
            "At least two distinct values are required."
        )

    unique_numbers.remove(max(unique_numbers))

    return max(unique_numbers)
''',
                "Finds the second-largest distinct value."
            )

        if "factorial" in q:

            return (
'''def factorial(n):
    if n < 0:
        raise ValueError(
            "Factorial is undefined for negative numbers."
        )

    result = 1

    for i in range(2, n + 1):
        result *= i

    return result
''',
                "Iterative factorial with O(n) time "
                "and O(1) auxiliary space."
            )

        if "fibonacci" in q:

            return (
'''def fibonacci(n):
    if n < 0:
        raise ValueError(
            "n must be non-negative."
        )

    a, b = 0, 1

    for _ in range(n):
        a, b = b, a + b

    return a
''',
                "Iterative Fibonacci implementation with O(n) time."
            )

        if "palindrome" in q:

            return (
'''def is_palindrome(text):
    normalized = ''.join(
        char.lower()
        for char in text
        if char.isalnum()
    )

    return normalized == normalized[::-1]
''',
                "Normalizes input and compares it with its reverse."
            )

        if "csv" in q:

            return (
'''import csv

def read_csv_file(file_path):
    with open(
        file_path,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        return list(reader)
''',
                "Uses csv.DictReader to return CSV rows as dictionaries."
            )

        return (
'''def solution():
    """
    Implement the requested logic here.
    """
    pass
''',
            "A generic Python solution template was generated "
            "because no specific algorithm was identified."
        )

    def run(
        self,
        query: str,
        context=None
    ) -> AgentResult:

        code, explanation = self.generate_code(query)

        validation = validate_python_code(code)

        output = []

        output.append("CODING AGENT")
        output.append("=" * 45)

        output.append(
            "\nIMPLEMENTATION"
        )

        output.append(
            "-" * 45
        )

        output.append(
            "```python"
        )

        output.append(code)

        output.append(
            "```"
        )

        output.append(
            "\nANALYSIS"
        )

        output.append(
            "-" * 45
        )

        output.append(
            explanation
        )

        output.append(
            "\nVALIDATION"
        )

        output.append(
            "-" * 45
        )

        if validation["valid"]:

            output.append(
                "Syntax test: PASSED"
            )

            if validation["functions"]:

                output.append(
                    "Functions detected: "
                    + ", ".join(
                        validation["functions"]
                    )
                )

            if validation["imports"]:

                output.append(
                    "Imports detected: "
                    + ", ".join(
                        validation["imports"]
                    )
                )

        else:

            output.append(
                "Syntax test: FAILED"
            )

            output.append(
                f"Error: {validation['error']}"
            )

        return AgentResult(
            agent_name=self.name,
            intent="CODING",
            success=validation["valid"],
            output="\n".join(output),
            metadata={
                "syntax_valid": validation["valid"],
                "functions": validation["functions"],
                "imports": validation["imports"],
                "code": code,
            },
        )


# ============================================================
# DATA ANALYSIS AGENT
# ============================================================

class DataAnalysisAgent(BaseAgent):

    def __init__(self):
        super().__init__("DataAnalysisAgent")

    def run(
        self,
        query: str,
        context=None
    ) -> AgentResult:

        output = [
            "DATA ANALYSIS AGENT",
            "=" * 45,
            "",
            "Recommended analysis pipeline:",
            "1. Load the dataset.",
            "2. Inspect shape, columns and data types.",
            "3. Detect missing values.",
            "4. Identify duplicates.",
            "5. Inspect numerical distributions.",
            "6. Inspect categorical variables.",
            "7. Analyze correlations.",
            "8. Detect potential outliers.",
            "9. Perform feature engineering if required.",
            "10. Generate conclusions from actual observations.",
        ]

        if "csv" in query.lower():

            output.extend([
                "",
                "CSV-specific recommendation:",
                "Use pandas.read_csv() and validate "
                "column types before analysis.",
            ])

        return AgentResult(
            agent_name=self.name,
            intent="DATA_ANALYSIS",
            success=True,
            output="\n".join(output),
            metadata={
                "workflow_complete": True
            },
        )


# ============================================================
# RESEARCH AGENT
# ============================================================

class ResearchAgent(BaseAgent):

    def __init__(self):
        super().__init__("ResearchAgent")

    def run(
        self,
        query: str,
        context=None
    ) -> AgentResult:

        output = [
            "RESEARCH AGENT",
            "=" * 45,
            "",
            "Research workflow:",
            "1. Define the research question.",
            "2. Identify relevant concepts.",
            "3. Identify candidate methodologies.",
            "4. Compare evidence and assumptions.",
            "5. Identify limitations.",
            "6. Formulate a testable conclusion.",
            "",
            "Source status:",
            "This Phase-2 configuration does not perform live web search.",
            "External claims therefore require a connected "
            "source-retrieval layer for verification.",
        ]

        return AgentResult(
            agent_name=self.name,
            intent="RESEARCH",
            success=True,
            output="\n".join(output),
            metadata={
                "live_search": False
            },
        )


# ============================================================
# GENERAL AGENT
# ============================================================

class GeneralAgent(BaseAgent):

    def __init__(self):
        super().__init__("GeneralAgent")

    def run(
        self,
        query: str,
        context=None
    ) -> AgentResult:

        output = (
            "GENERAL AGENT\n"
            "=============================================\n\n"
            f"User request received:\n{query}\n\n"
            "No specialized domain workflow was detected."
        )

        return AgentResult(
            agent_name=self.name,
            intent="GENERAL",
            success=True,
            output=output,
            metadata={},
        )


# ============================================================
# REASONING AGENT
# ============================================================

class ReasoningAgent(BaseAgent):

    def __init__(self):
        super().__init__("ReasoningAgent")

    def run(
        self,
        query: str,
        context=None
    ) -> AgentResult:

        context = context or {}

        intent = normalize_intent(
            context.get("intent", "GENERAL")
        )

        results = context.get(
            "agent_results",
            []
        )

        findings = []

        # ----------------------------------------------------
        # MACHINE LEARNING REASONING
        # ----------------------------------------------------

        if intent == "MACHINE_LEARNING":

            ml_result = next(
                (
                    r for r in results
                    if r.agent_name == "MLAgent"
                ),
                None,
            )

            if ml_result:

                q = query.lower()

                if (
                    "fraud" in q
                    or "imbalance" in q
                    or "imbalanced" in q
                ):

                    findings.extend([
                        "The task is a classification-evaluation problem "
                        "with potential class imbalance.",
                        "Accuracy alone may hide poor detection of the "
                        "minority fraud class.",
                        "Precision and recall should be evaluated together "
                        "because false positives and false negatives have "
                        "different operational consequences.",
                        "PR-AUC is useful when fraudulent transactions "
                        "are rare.",
                        "The decision threshold should be evaluated "
                        "instead of assuming 0.5 is optimal.",
                        "Final performance should be measured on an "
                        "untouched test set after model and threshold selection.",
                    ])

                elif (
                    "overfit" in q
                    or "overfitting" in q
                ):

                    findings.extend([
                        "The central issue is model generalization.",
                        "Training and validation behavior should be compared "
                        "before selecting a remedy.",
                        "A large train-validation gap can indicate overfitting.",
                        "Regularization, early stopping, augmentation, "
                        "or reduced model complexity can then be evaluated.",
                    ])

                else:

                    findings.extend([
                        "The ML specialist identified a complete "
                        "model-development workflow.",
                        "Validation and held-out testing are required "
                        "before interpreting model performance.",
                    ])

        # ----------------------------------------------------
        # CODING REASONING
        # ----------------------------------------------------

        elif intent == "CODING":

            coding_result = next(
                (
                    r for r in results
                    if r.agent_name == "CodingAgent"
                ),
                None,
            )

            if coding_result:

                metadata = coding_result.metadata

                if metadata.get("syntax_valid"):

                    findings.append(
                        "The generated implementation passed "
                        "Python AST syntax validation."
                    )

                else:

                    findings.append(
                        "The generated implementation failed "
                        "Python AST syntax validation."
                    )

                functions = metadata.get(
                    "functions",
                    []
                )

                if functions:

                    findings.append(
                        "Detected function(s): "
                        + ", ".join(functions)
                        + "."
                    )

                code = metadata.get(
                    "code",
                    ""
                )

                if "set(" in code:

                    findings.append(
                        "A set-based structure is used for efficient "
                        "membership or uniqueness operations."
                    )

                if "sqrt" in code:

                    findings.append(
                        "The prime-number implementation limits "
                        "divisibility checks using the square-root bound."
                    )

                if "DictReader" in code:

                    findings.append(
                        "CSV rows are represented using column-aware "
                        "dictionary records."
                    )

                findings.append(
                    "Edge cases should still be tested before production use."
                )

        # ----------------------------------------------------
        # DATA ANALYSIS REASONING
        # ----------------------------------------------------

        elif intent == "DATA_ANALYSIS":

            findings.extend([
                "The data-analysis workflow begins with structural "
                "inspection before statistical interpretation.",
                "Missing values, duplicates and incorrect data types "
                "should be checked before modeling or visualization.",
                "Actual numerical conclusions require the dataset itself.",
            ])

            if "csv" in query.lower():

                findings.append(
                    "For CSV data, parsing and column-type validation "
                    "should occur before downstream analysis."
                )

        # ----------------------------------------------------
        # RESEARCH REASONING
        # ----------------------------------------------------

        elif intent == "RESEARCH":

            findings.extend([
                "The workflow separates the research question, "
                "methodology, evidence and limitations.",
                "The current configuration does not verify live external sources.",
                "External factual claims should therefore be checked "
                "through a source-retrieval mechanism.",
            ])

        # ----------------------------------------------------
        # GENERAL
        # ----------------------------------------------------

        else:

            successful_agents = [
                r.agent_name
                for r in results
                if r.success
            ]

            if successful_agents:

                findings.append(
                    "Successfully executed agent(s): "
                    + ", ".join(successful_agents)
                    + "."
                )

            findings.append(
                "No specialized reasoning strategy was required."
            )

        output = []

        output.append("REASONING AGENT")
        output.append("=" * 45)

        output.append(
            f"\nIntent analyzed: {intent}"
        )

        output.append(
            "\nEvidence received:"
        )

        for result in results:

            output.append(
                f"- {result.agent_name}: "
                f"{'SUCCESS' if result.success else 'FAILED'}"
            )

        output.append(
            "\nREASONING FINDINGS"
        )

        output.append(
            "-" * 45
        )

        for index, finding in enumerate(
            findings,
            1
        ):

            output.append(
                f"{index}. {finding}"
            )

        output.append(
            "\nCONCLUSION"
        )

        output.append(
            "-" * 45
        )

        if findings:

            output.append(
                "The specialist evidence was analyzed according "
                "to the detected task type."
            )

        else:

            output.append(
                "Insufficient specialist evidence was available."
            )

        return AgentResult(
            agent_name=self.name,
            intent="REASONING",
            success=bool(findings),
            output="\n".join(output),
            metadata={
                "finding_count": len(findings),
                "analyzed_intent": intent,
            },
        )


# ============================================================
# CRITIC AGENT
# ============================================================

class CriticAgent(BaseAgent):

    def __init__(self):
        super().__init__("CriticAgent")

    def run(
        self,
        query: str,
        context=None
    ) -> AgentResult:

        context = context or {}

        results = context.get(
            "agent_results",
            []
        )

        reasoning = context.get(
            "reasoning_result"
        )

        intent = normalize_intent(
            context.get(
                "intent",
                "GENERAL"
            )
        )

        checks = []

        # ----------------------------------------------------
        # EXPECTED SPECIALIST
        # ----------------------------------------------------

        expected_agents = {
            "MACHINE_LEARNING": "MLAgent",
            "CODING": "CodingAgent",
            "DATA_ANALYSIS": "DataAnalysisAgent",
            "RESEARCH": "ResearchAgent",
            "GENERAL": "GeneralAgent",
        }

        expected_agent = expected_agents.get(
            intent,
            "GeneralAgent"
        )

        executed_agents = [
            r.agent_name
            for r in results
        ]

        if expected_agent in executed_agents:

            checks.append(
                (
                    True,
                    f"Intent '{intent}' correctly routed "
                    f"to {expected_agent}."
                )
            )

        else:

            checks.append(
                (
                    False,
                    f"Intent '{intent}' expected "
                    f"{expected_agent}, but executed: "
                    + (
                        ", ".join(executed_agents)
                        if executed_agents
                        else "none"
                    )
                )
            )

        # ----------------------------------------------------
        # SPECIALIST EXECUTION
        # ----------------------------------------------------

        if results:

            checks.append(
                (
                    True,
                    "At least one specialist agent executed."
                )
            )

        else:

            checks.append(
                (
                    False,
                    "No specialist agent executed."
                )
            )

        # ----------------------------------------------------
        # FAILED AGENTS
        # ----------------------------------------------------

        failed_agents = [
            r.agent_name
            for r in results
            if not r.success
        ]

        if not failed_agents:

            checks.append(
                (
                    True,
                    "No specialist agent reported execution failure."
                )
            )

        else:

            checks.append(
                (
                    False,
                    "Failed agent(s): "
                    + ", ".join(failed_agents)
                )
            )

        # ----------------------------------------------------
        # OUTPUT EXISTENCE
        # ----------------------------------------------------

        if any(
            r.output.strip()
            for r in results
        ):

            checks.append(
                (
                    True,
                    "Specialist agents produced usable evidence."
                )
            )

        else:

            checks.append(
                (
                    False,
                    "Specialist agents produced empty output."
                )
            )

        # ----------------------------------------------------
        # REASONING
        # ----------------------------------------------------

        if reasoning and reasoning.success:

            checks.append(
                (
                    True,
                    "Reasoning layer produced task-specific findings."
                )
            )

        else:

            checks.append(
                (
                    False,
                    "Reasoning layer did not produce usable findings."
                )
            )

        # ----------------------------------------------------
        # CODING VALIDATION
        # ----------------------------------------------------

        for result in results:

            if result.agent_name == "CodingAgent":

                if result.metadata.get(
                    "syntax_valid",
                    False
                ):

                    checks.append(
                        (
                            True,
                            "Generated Python code passed AST validation."
                        )
                    )

                else:

                    checks.append(
                        (
                            False,
                            "Generated Python code failed AST validation."
                        )
                    )

        # ----------------------------------------------------
        # REASONING QUALITY
        # ----------------------------------------------------

        if reasoning:

            reasoning_text = reasoning.output.lower()

            generic_markers = [
                "identify relevant evidence.",
                "compare specialist outputs.",
                "detect contradictions or missing information.",
                "infer the most likely explanation.",
                "appropriate next action.",
            ]

            generic_count = sum(
                marker in reasoning_text
                for marker in generic_markers
            )

            if generic_count >= 3:

                checks.append(
                    (
                        False,
                        "Reasoning output is overly generic."
                    )
                )

            else:

                checks.append(
                    (
                        True,
                        "Reasoning output contains "
                        "task-specific analysis."
                    )
                )

        # ----------------------------------------------------
        # FINAL STATUS
        # ----------------------------------------------------

        passed = sum(
            1
            for status, _ in checks
            if status
        )

        total = len(checks)

        overall_success = (
            total > 0
            and passed == total
        )

        output = []

        output.append("CRITIC AGENT")
        output.append("=" * 45)

        output.append(
            f"\nChecks passed: {passed}/{total}"
        )

        output.append(
            "\nVALIDATION RESULTS"
        )

        output.append(
            "-" * 45
        )

        for index, (
            status,
            message
        ) in enumerate(
            checks,
            1
        ):

            output.append(
                f"{index}. "
                f"{'PASS' if status else 'FAIL'} - "
                f"{message}"
            )

        output.append(
            "\nFINAL STATUS"
        )

        output.append(
            "-" * 45
        )

        output.append(
            "PASSED"
            if overall_success
            else
            "NEEDS REVIEW"
        )

        return AgentResult(
            agent_name=self.name,
            intent="CRITIC",
            success=overall_success,
            output="\n".join(output),
            metadata={
                "passed": passed,
                "total": total,
                "checks": checks,
            },
        )


# ============================================================
# MULTI-AGENT SYSTEM
# ============================================================

class MultiAgentSystem:

    def __init__(self):

        self.agents = {
            "MLAgent": MLAgent(),
            "CodingAgent": CodingAgent(),
            "DataAnalysisAgent": DataAnalysisAgent(),
            "ResearchAgent": ResearchAgent(),
            "ReasoningAgent": ReasoningAgent(),
            "CriticAgent": CriticAgent(),
            "GeneralAgent": GeneralAgent(),
        }

        self.brain = None

        if IntelligenceBrain is not None:

            try:
                self.brain = IntelligenceBrain()

            except Exception:

                self.brain = None

    # ========================================================
    # INTENT DETECTION
    # ========================================================

    def detect_intent(
        self,
        query: str
    ) -> str:

        q = query.lower().strip()

        # ----------------------------------------------------
        # MACHINE LEARNING
        # ----------------------------------------------------

        ml_keywords = [

            "machine learning",
            "machine-learning",

            "deep learning",

            "neural network",
            "neural networks",

            "cnn",
            "rnn",
            "lstm",
            "transformer",

            "classification",
            "classifier",

            "regression",

            "model evaluation",
            "evaluate model",
            "evaluate a model",
            "model performance",

            "overfit",
            "overfitting",

            "fraud",
            "fraud detection",
            "fraud detection model",

            "anomaly detection",

            "imbalance",
            "imbalanced",
            "class imbalance",
            "imbalanced dataset",

            "roc",
            "roc-auc",
            "auc",
            "pr-auc",

            "precision",
            "recall",
            "f1",
            "f1-score",

            "accuracy",
            "confusion matrix",

            "train model",
            "training model",
            "trained model",
            "predictive model",
        ]

        # ----------------------------------------------------
        # DATA ANALYSIS
        # ----------------------------------------------------

        data_keywords = [

            "data analysis",
            "analyze data",
            "analyse data",

            "csv dataset",
            "csv file",

            "dataframe",
            "pandas",

            "missing values",
            "outliers",
            "correlation",

            "exploratory data analysis",
            "eda",
        ]

        # ----------------------------------------------------
        # RESEARCH
        # ----------------------------------------------------

        research_keywords = [

            "research paper",
            "research workflow",
            "research",

            "literature review",
            "methodology",

            "academic paper",
            "academic",

            "research study",
        ]

        # ----------------------------------------------------
        # CODING
        # ----------------------------------------------------

        coding_keywords = [

            "write code",
            "python code",
            "code for",

            "program",
            "programming",

            "function",
            "algorithm",
            "implement",

            "debug",
            "script",

            "prime number",
            "palindrome",
            "factorial",
            "fibonacci",

            "duplicate",
            "second largest",
        ]

        # ML first.
        if any(
            keyword in q
            for keyword in ml_keywords
        ):

            return "MACHINE_LEARNING"

        if any(
            keyword in q
            for keyword in data_keywords
        ):

            return "DATA_ANALYSIS"

        if any(
            keyword in q
            for keyword in research_keywords
        ):

            return "RESEARCH"

        if any(
            keyword in q
            for keyword in coding_keywords
        ):

            return "CODING"

        return "GENERAL"

    # ========================================================
    # BRAIN ROUTING
    # ========================================================

    def brain_route(
        self,
        query: str
    ) -> Tuple[str, List[str]]:

        fallback_intent = self.detect_intent(
            query
        )

        if self.brain is None:

            return (
                fallback_intent,
                []
            )

        try:

            result = None

            methods = [
                "analyze",
                "route",
                "process",
                "get_intent",
            ]

            for method_name in methods:

                method = getattr(
                    self.brain,
                    method_name,
                    None
                )

                if callable(method):

                    try:

                        result = method(
                            query
                        )

                        break

                    except Exception:

                        continue

            if result is None:

                return (
                    fallback_intent,
                    []
                )

            # ------------------------------------------------
            # DICTIONARY
            # ------------------------------------------------

            if isinstance(
                result,
                dict
            ):

                intent = result.get(
                    "intent",
                    result.get(
                        "task_type",
                        fallback_intent
                    )
                )

                agents = result.get(
                    "agents",
                    result.get(
                        "selected_agents",
                        result.get(
                            "recommended_agents",
                            []
                        )
                    )
                )

                if isinstance(
                    agents,
                    str
                ):

                    agents = [
                        agents
                    ]

                return (
                    normalize_intent(
                        intent
                    ),
                    [
                        normalize_agent_name(
                            agent
                        )
                        for agent in agents
                    ]
                )

            # ------------------------------------------------
            # STRING
            # ------------------------------------------------

            if isinstance(
                result,
                str
            ):

                text = result.lower()

                if (
                    "fraud" in query.lower()
                    or "machine learning" in text
                    or (
                        "machine" in text
                        and "learning" in text
                    )
                ):

                    return (
                        "MACHINE_LEARNING",
                        []
                    )

                if "data analysis" in text:

                    return (
                        "DATA_ANALYSIS",
                        []
                    )

                if "research" in text:

                    return (
                        "RESEARCH",
                        []
                    )

                if "coding" in text:

                    return (
                        "CODING",
                        []
                    )

        except Exception:
            pass

        return (
            fallback_intent,
            []
        )

    # ========================================================
    # AGENT SELECTION
    # ========================================================

    def select_agents(
        self,
        intent: str,
        brain_agents: Optional[List[str]] = None
    ) -> List[str]:

        intent = normalize_intent(
            intent
        )

        selected = []

        if brain_agents:

            for name in brain_agents:

                normalized = normalize_agent_name(
                    name
                )

                if normalized in self.agents:

                    selected.append(
                        normalized
                    )

        mapping = {
            "MACHINE_LEARNING": "MLAgent",
            "CODING": "CodingAgent",
            "DATA_ANALYSIS": "DataAnalysisAgent",
            "RESEARCH": "ResearchAgent",
            "GENERAL": "GeneralAgent",
        }

        specialist = mapping.get(
            intent,
            "GeneralAgent"
        )

        if specialist not in selected:

            selected.insert(
                0,
                specialist
            )

        if "ReasoningAgent" not in selected:

            selected.append(
                "ReasoningAgent"
            )

        final_agents = []

        for agent in selected:

            if agent not in final_agents:

                final_agents.append(
                    agent
                )

        return final_agents

    # ========================================================
    # EXECUTE SPECIALISTS
    # ========================================================

    def execute_specialists(
        self,
        query: str,
        selected_agents: List[str],
        intent: str
    ) -> List[AgentResult]:

        results = []

        for agent_name in selected_agents:

            if agent_name in (
                "ReasoningAgent",
                "CriticAgent"
            ):
                continue

            agent = self.agents.get(
                agent_name
            )

            if agent is None:
                continue

            try:

                result = agent.run(
                    query,
                    {
                        "intent": intent
                    }
                )

            except Exception as exc:

                result = AgentResult(
                    agent_name=agent_name,
                    intent=intent,
                    success=False,
                    output=(
                        f"Agent execution error: {exc}"
                    ),
                    metadata={
                        "error": str(exc)
                    },
                )

            results.append(
                result
            )

        return results

    # ========================================================
    # FINAL RESPONSE
    # ========================================================

    def synthesize_final_response(
        self,
        query: str,
        intent: str,
        specialists: List[AgentResult],
        reasoning: AgentResult,
        critic: AgentResult
    ) -> str:

        output = []

        output.append(
            "RETRO-AI FINAL RESPONSE"
        )

        output.append(
            "=" * 60
        )

        output.append(
            f"\nDetected intent: {intent}"
        )

        output.append(
            "\nSPECIALIST FINDINGS"
        )

        output.append(
            "-" * 60
        )

        for result in specialists:

            output.append(
                f"\n[{result.agent_name}]"
            )

            output.append(
                result.output
            )

        output.append(
            "\nREASONING"
        )

        output.append(
            "-" * 60
        )

        output.append(
            reasoning.output
        )

        output.append(
            "\nCRITIC VALIDATION"
        )

        output.append(
            "-" * 60
        )

        status = (
            "PASSED"
            if critic.success
            else
            "NEEDS REVIEW"
        )

        output.append(
            f"System validation: {status}"
        )

        output.append(
            f"Validation checks: "
            f"{critic.metadata.get('passed', 0)}/"
            f"{critic.metadata.get('total', 0)}"
        )

        output.append(
            "\nSYSTEM PIPELINE"
        )

        output.append(
            "-" * 60
        )

        output.append(
            "Query → Brain → Intent Router → "
            "Specialist → Reasoning → Critic → Final Response"
        )

        return "\n".join(
            output
        )

    # ========================================================
    # MAIN PROCESS
    # ========================================================

    def process(
        self,
        query: str
    ) -> Dict[str, Any]:

        start = time.perf_counter()

        # ----------------------------------------------------
        # ROUTING
        # ----------------------------------------------------

        intent, brain_agents = self.brain_route(
            query
        )

        intent = normalize_intent(
            intent
        )

        # ----------------------------------------------------
        # SAFETY OVERRIDE
        # ----------------------------------------------------
        # Certain explicit domain terms should never fall
        # through to GENERAL because the Brain returned
        # an incomplete/incorrect classification.

        fallback_intent = self.detect_intent(
            query
        )

        if fallback_intent != "GENERAL":

            intent = fallback_intent

        # ----------------------------------------------------
        # AGENT SELECTION
        # ----------------------------------------------------

        selected_agents = self.select_agents(
            intent,
            brain_agents
        )

        # ----------------------------------------------------
        # SPECIALISTS
        # ----------------------------------------------------

        specialist_results = (
            self.execute_specialists(
                query,
                selected_agents,
                intent
            )
        )

        # ----------------------------------------------------
        # REASONING
        # ----------------------------------------------------

        reasoning_agent = self.agents[
            "ReasoningAgent"
        ]

        reasoning_result = reasoning_agent.run(
            query,
            {
                "intent": intent,
                "agent_results": specialist_results,
            }
        )

        # ----------------------------------------------------
        # CRITIC
        # ----------------------------------------------------

        critic_agent = self.agents[
            "CriticAgent"
        ]

        critic_result = critic_agent.run(
            query,
            {
                "intent": intent,
                "agent_results": specialist_results,
                "reasoning_result": reasoning_result,
            }
        )

        # ----------------------------------------------------
        # FINAL
        # ----------------------------------------------------

        final_response = (
            self.synthesize_final_response(
                query,
                intent,
                specialist_results,
                reasoning_result,
                critic_result
            )
        )

        elapsed = (
            time.perf_counter() - start
        ) * 1000

        return {
            "query": query,
            "intent": intent,

            "selected_agents":
                selected_agents,

            "specialist_results": [
                {
                    "agent": r.agent_name,
                    "intent": r.intent,
                    "success": r.success,
                    "output": r.output,
                    "metadata": r.metadata,
                }
                for r in specialist_results
            ],

            "reasoning": {
                "agent":
                    reasoning_result.agent_name,
                "success":
                    reasoning_result.success,
                "output":
                    reasoning_result.output,
                "metadata":
                    reasoning_result.metadata,
            },

            "critic": {
                "agent":
                    critic_result.agent_name,
                "success":
                    critic_result.success,
                "output":
                    critic_result.output,
                "metadata":
                    critic_result.metadata,
            },

            "final_response":
                final_response,

            "execution_time_ms":
                round(elapsed, 2),
        }

    # ========================================================
    # SIMPLE RUN
    # ========================================================

    def run(
        self,
        query: str
    ) -> str:

        return self.process(
            query
        )["final_response"]


# ============================================================
# TEST SUITE
# ============================================================

def run_tests():

    print()
    print("=" * 70)
    print("RETRO-AI PHASE 2 TEST SUITE")
    print("=" * 70)

    system = MultiAgentSystem()

    test_queries = [

        "Write Python code to check whether a number is prime.",

        "Write Python code to find duplicates in a list.",

        "Write Python code to find the second largest number.",

        "Write Python code for factorial.",

        "Write Python code for Fibonacci.",

        "Write Python code to check a palindrome.",

        "Write Python code to read a CSV file.",

        "How can I reduce overfitting in a neural network?",

        "How should I evaluate a fraud detection model?",

        "How should I analyze a CSV dataset?",

        "Explain a research workflow for an AI project.",
    ]

    passed = 0
    failed = 0

    for index, query in enumerate(
        test_queries,
        start=1
    ):

        print()
        print("-" * 70)

        print(
            f"TEST {index}/{len(test_queries)}"
        )

        print(
            "-" * 70
        )

        print(
            f"QUERY: {query}"
        )

        try:

            result = system.process(
                query
            )

            print(
                f"\nINTENT: "
                f"{result['intent']}"
            )

            print(
                "SELECTED AGENTS: "
                + ", ".join(
                    result[
                        "selected_agents"
                    ]
                )
            )

            print(
                "\nFINAL RESPONSE:"
            )

            print(
                result[
                    "final_response"
                ]
            )

            critic_success = result[
                "critic"
            ][
                "success"
            ]

            if critic_success:

                passed += 1

                print(
                    "\nTEST STATUS: PASSED"
                )

            else:

                failed += 1

                print(
                    "\nTEST STATUS: FAILED"
                )

            print(
                f"\nExecution time: "
                f"{result['execution_time_ms']} ms"
            )

        except Exception as exc:

            failed += 1

            print(
                "\nTEST STATUS: FAILED"
            )

            print(
                f"ERROR: {exc}"
            )

    print()
    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)

    print(
        f"Passed: {passed}"
    )

    print(
        f"Failed: {failed}"
    )

    print(
        f"Total: {len(test_queries)}"
    )

    print(
        "=" * 70
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    run_tests()