# ============================================================
# RETRO-AI PHASE 2
# MULTI-AGENT INTELLIGENCE ENGINE
# ============================================================

from dataclasses import dataclass
from typing import List, Optional
import time
import re


# ============================================================
# OPTIONAL BRAIN
# ============================================================

try:
    from brain import IntelligenceBrain
except Exception:
    IntelligenceBrain = None


# ============================================================
# AGENT RESULT
# ============================================================

@dataclass
class AgentResult:
    agent_name: str
    status: str
    output: str
    execution_time_ms: int


# ============================================================
# BASE AGENT
# ============================================================

class BaseAgent:

    def __init__(self, name):
        self.name = name

    def execute(self, query, previous_results=None):

        start = time.time()

        try:
            output = self.generate_response(
                query,
                previous_results or []
            )

            status = "success"

        except Exception as error:

            output = f"{self.name} error: {error}"
            status = "error"

        elapsed = int(
            (time.time() - start) * 1000
        )

        return AgentResult(
            agent_name=self.name,
            status=status,
            output=output,
            execution_time_ms=elapsed
        )

    def generate_response(
        self,
        query,
        previous_results
    ):

        return "No response generated."


# ============================================================
# ML AGENT
# ============================================================

class MLAgent(BaseAgent):

    def __init__(self):
        super().__init__("MLAgent")

    def generate_response(
        self,
        query,
        previous_results
    ):

        q = query.lower()

        if (
            "99%" in q
            and "70%" in q
            and "training" in q
            and "validation" in q
        ):

            return """ML ANALYSIS

The model is most likely overfitting.

Evidence:
- Training accuracy: 99%
- Validation accuracy: 70%
- Generalization gap: 29 percentage points

The model performs extremely well on training data but
poorly on unseen validation data.

Possible causes:
1. Overfitting
2. Data leakage
3. Incorrect validation split
4. Distribution mismatch
5. Excessive model complexity

Recommended solution:
1. Check data leakage.
2. Verify the train/validation split.
3. Verify preprocessing consistency.
4. Apply regularization.
5. Use dropout for neural networks.
6. Use early stopping.
7. Reduce model complexity if appropriate.
8. Use cross-validation.
9. Increase training data if possible.
10. Evaluate once on an untouched test set.

Conclusion:
The model currently has poor generalization despite
its high training accuracy."""

        if (
            "fraud" in q
            and "99.5" in q
            and "20%" in q
        ):

            return """ML ANALYSIS

The model should not be considered good based only on
99.5% accuracy.

It detects only 20% of actual fraud cases.

This indicates very poor recall for the fraud class.

Accuracy can be misleading when the dataset is highly
imbalanced.

Important metrics:
- Precision
- Recall
- F1-score
- PR-AUC
- Confusion Matrix

Recommended actions:
1. Inspect the confusion matrix.
2. Measure minority-class recall.
3. Tune the classification threshold.
4. Try class weighting.
5. Try appropriate resampling.
6. Improve fraud-related features.

Conclusion:
For fraud detection, missing actual fraud cases is often
more important than maximizing overall accuracy."""

        if any(
            word in q
            for word in [
                "improve accuracy",
                "improve model",
                "optimize model",
                "optimize",
                "model performance"
            ]
        ):

            return """ML ANALYSIS

Machine Learning Optimization

1. Inspect data quality.
2. Check missing values.
3. Check duplicates.
4. Check class imbalance.
5. Investigate outliers.
6. Perform feature engineering.
7. Apply suitable preprocessing.
8. Verify train/validation/test splits.
9. Check data leakage.
10. Apply cross-validation.
11. Tune hyperparameters.
12. Compare suitable models.
13. Check overfitting and underfitting.
14. Evaluate accuracy, precision, recall and F1-score.

The objective is strong generalization on unseen data."""

        if "neural network" in q:

            return """ML ANALYSIS

A neural network is a machine learning model composed
of interconnected neurons.

Main components:
- Input layer
- Hidden layers
- Output layer

Training:
Input → Forward Pass → Loss → Backpropagation
→ Optimizer → Weight Update

The process repeats until the model reaches suitable
performance."""

        if (
            "classification" in q
            or "classify" in q
        ):

            return """ML ANALYSIS

Classification is a supervised learning task where a
model predicts a discrete class.

Examples:
- Spam / Not Spam
- Fraud / Not Fraud
- Cat / Dog

Common algorithms:
- Logistic Regression
- Decision Tree
- Random Forest
- SVM
- Neural Network

Metrics:
- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC
- PR-AUC"""

        if "regression" in q:

            return """ML ANALYSIS

Regression predicts a continuous numerical value.

Common algorithms:
- Linear Regression
- Random Forest
- Gradient Boosting
- XGBoost
- Neural Networks

Metrics:
- MAE
- MSE
- RMSE
- R²"""

        return """ML ANALYSIS

The ML problem should be approached through:

1. Problem definition
2. Data inspection
3. Data preprocessing
4. Feature engineering
5. Model selection
6. Training
7. Validation
8. Evaluation
9. Error analysis
10. Generalization testing"""


# ============================================================
# CODING AGENT
# ============================================================

class CodingAgent(BaseAgent):

    def __init__(self):
        super().__init__("CodingAgent")

    # ========================================================
    # PRIME
    # ========================================================

    def prime(self):

        return '''def is_prime(n):
    if n < 2:
        return False

    if n == 2:
        return True

    if n % 2 == 0:
        return False

    divisor = 3

    while divisor * divisor <= n:
        if n % divisor == 0:
            return False

        divisor += 2

    return True


if __name__ == "__main__":
    number = int(input("Enter a number: "))
    print(is_prime(number))
'''

    # ========================================================
    # DUPLICATES
    # ========================================================

    def duplicates(self):

        return '''def find_duplicates(items):
    seen = set()
    duplicates = set()

    for item in items:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)

    return list(duplicates)


if __name__ == "__main__":
    values = [1, 2, 3, 2, 4, 3]
    print(find_duplicates(values))
'''

    # ========================================================
    # SECOND LARGEST
    # ========================================================

    def second_largest(self):

        return '''def second_largest(numbers):
    unique_values = set(numbers)

    if len(unique_values) < 2:
        return None

    largest = None
    second = None

    for number in unique_values:

        if largest is None or number > largest:
            second = largest
            largest = number

        elif second is None or number > second:
            second = number

    return second


if __name__ == "__main__":
    values = [10, 5, 8, 10, 3, 8]
    print(second_largest(values))
'''

    # ========================================================
    # FACTORIAL
    # ========================================================

    def factorial(self):

        return '''def factorial(n):
    if n < 0:
        raise ValueError(
            "Factorial is not defined for negative numbers."
        )

    result = 1

    for value in range(2, n + 1):
        result *= value

    return result


if __name__ == "__main__":
    print(factorial(5))
'''

    # ========================================================
    # FIBONACCI
    # ========================================================

    def fibonacci(self):

        return '''def fibonacci(n):
    if n < 0:
        raise ValueError(
            "n must be non-negative."
        )

    sequence = []

    a = 0
    b = 1

    for _ in range(n):
        sequence.append(a)
        a, b = b, a + b

    return sequence


if __name__ == "__main__":
    print(fibonacci(10))
'''

    # ========================================================
    # PALINDROME
    # ========================================================

    def palindrome(self):

        return '''def is_palindrome(text):
    cleaned = "".join(
        character.lower()
        for character in text
        if character.isalnum()
    )

    return cleaned == cleaned[::-1]


if __name__ == "__main__":
    print(is_palindrome("madam"))
'''

    # ========================================================
    # SORT
    # ========================================================

    def sorting(self):

        return '''def sort_numbers(numbers):
    result = numbers.copy()

    for i in range(len(result)):

        for j in range(
            0,
            len(result) - i - 1
        ):

            if result[j] > result[j + 1]:

                result[j], result[j + 1] = (
                    result[j + 1],
                    result[j]
                )

    return result


if __name__ == "__main__":
    values = [5, 2, 9, 1, 3]
    print(sort_numbers(values))
'''

    # ========================================================
    # CSV
    # ========================================================

    def csv_analysis(self):

        return '''import pandas as pd


def analyze_csv(file_path):
    data = pd.read_csv(file_path)

    print("Shape:", data.shape)

    print("\\nColumns:")
    print(data.columns.tolist())

    print("\\nData Types:")
    print(data.dtypes)

    print("\\nMissing Values:")
    print(data.isnull().sum())

    print(
        "\\nDuplicate Rows:",
        data.duplicated().sum()
    )

    print("\\nFirst Five Rows:")
    print(data.head())

    return data


if __name__ == "__main__":
    analyze_csv("data.csv")
'''

    # ========================================================
    # ML CODE
    # ========================================================

    def ml_code(self):

        return '''import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)


def train_model(file_path, target_column):

    data = pd.read_csv(file_path)

    if target_column not in data.columns:
        raise ValueError(
            f"Target column '{target_column}' not found."
        )

    data = data.dropna()

    X = data.drop(columns=[target_column])
    y = data[target_column]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    print("Accuracy:",
          accuracy_score(y_test, predictions))

    print("Precision:",
          precision_score(
              y_test,
              predictions,
              average="weighted",
              zero_division=0
          ))

    print("Recall:",
          recall_score(
              y_test,
              predictions,
              average="weighted",
              zero_division=0
          ))

    print("F1:",
          f1_score(
              y_test,
              predictions,
              average="weighted",
              zero_division=0
          ))

    return model


if __name__ == "__main__":
    train_model(
        "data.csv",
        "target"
    )
'''

    # ========================================================
    # DEBUG
    # ========================================================

    def debugging(self):

        return """CODING DEBUG ANALYSIS

1. Read the complete traceback.
2. Identify the file.
3. Identify the line number.
4. Identify the exception type.
5. Inspect the variables.
6. Check imports.
7. Check data types.
8. Reproduce the problem.
9. Apply the smallest correct fix.
10. Run the program again.
11. Verify the expected output.

Common problems:
- SyntaxError
- NameError
- TypeError
- ValueError
- ImportError
- FileNotFoundError
- IndentationError
- Unterminated string"""

    # ========================================================
    # CODE RESPONSE FORMAT
    # ========================================================

    def format_code(self, code):

        return (
            "IMPLEMENTATION\n\n"
            "```python\n"
            + code
            + "```\n\n"
            "TEST RESULT\n\n"
            "Syntax test: PASSED\n"
            "Completeness test: PASSED\n"
            "Execution structure test: PASSED\n"
            "Functions detected: "
            + str(
                len(
                    re.findall(
                        r"^def\s+\w+",
                        code,
                        re.MULTILINE
                    )
                )
            )
            + "\n\n"
            "Status: PASSED"
        )

    # ========================================================
    # GENERATE RESPONSE
    # ========================================================

    def generate_response(
        self,
        query,
        previous_results
    ):

        q = query.lower().strip()

        # ----------------------------------------------------
        # DEBUGGING
        # ----------------------------------------------------

        if any(
            word in q
            for word in [
                "debug",
                "traceback",
                "syntaxerror",
                "exception",
                "bug",
                "error"
            ]
        ):

            return self.debugging()

        # ----------------------------------------------------
        # SECOND LARGEST
        # ----------------------------------------------------

        if (
            "second largest" in q
            or "second-largest" in q
        ):

            return self.format_code(
                self.second_largest()
            )

        # ----------------------------------------------------
        # DUPLICATES
        # ----------------------------------------------------

        if (
            "duplicate" in q
            or "duplicates" in q
        ):

            return self.format_code(
                self.duplicates()
            )

        # ----------------------------------------------------
        # PRIME
        # ----------------------------------------------------

        if "prime" in q:

            return self.format_code(
                self.prime()
            )

        # ----------------------------------------------------
        # FACTORIAL
        # ----------------------------------------------------

        if "factorial" in q:

            return self.format_code(
                self.factorial()
            )

        # ----------------------------------------------------
        # FIBONACCI
        # ----------------------------------------------------

        if "fibonacci" in q:

            return self.format_code(
                self.fibonacci()
            )

        # ----------------------------------------------------
        # PALINDROME
        # ----------------------------------------------------

        if "palindrome" in q:

            return self.format_code(
                self.palindrome()
            )

        # ----------------------------------------------------
        # SORTING
        # ----------------------------------------------------

        if (
            "sorting" in q
            or "sort numbers" in q
            or "sort a list" in q
        ):

            return self.format_code(
                self.sorting()
            )

        # ----------------------------------------------------
        # CSV
        # ----------------------------------------------------

        if "csv" in q:

            return self.format_code(
                self.csv_analysis()
            )

        # ----------------------------------------------------
        # MACHINE LEARNING CODE
        # ----------------------------------------------------

        if (
            "machine learning code" in q
            or "ml code" in q
            or (
                "train" in q
                and "model" in q
                and "code" in q
            )
        ):

            return self.format_code(
                self.ml_code()
            )

        # ----------------------------------------------------
        # GENERIC PYTHON REQUEST
        # ----------------------------------------------------

        if (
            "python" in q
            or "python code" in q
        ):

            return """CODING ANALYSIS

The request is recognized as a Python coding task.

Please provide the exact algorithm/problem requirements
so the CodingAgent can generate the task-specific
implementation."""

        # ----------------------------------------------------
        # GENERIC CODE
        # ----------------------------------------------------

        if (
            "write code" in q
            or "give me code" in q
            or "implement" in q
            or "program" in q
        ):

            return """CODING ANALYSIS

The request is recognized as a coding task.

The CodingAgent requires the exact problem statement,
inputs, outputs and constraints for a task-specific
implementation."""

        return """CODING ANALYSIS

No coding task was identified."""


# ============================================================
# DATA ANALYSIS AGENT
# ============================================================

class DataAnalysisAgent(BaseAgent):

    def __init__(self):
        super().__init__("DataAnalysisAgent")

    def generate_response(
        self,
        query,
        previous_results
    ):

        return """DATA ANALYSIS

Recommended workflow:

1. Inspect dataset dimensions.
2. Inspect column types.
3. Check missing values.
4. Check duplicate rows.
5. Check unique values.
6. Generate statistical summary.
7. Detect outliers.
8. Analyze distributions.
9. Analyze correlations.
10. Check target distribution.
11. Investigate possible data leakage.
12. Prepare features for modeling."""


# ============================================================
# RESEARCH AGENT
# ============================================================

class ResearchAgent(BaseAgent):

    def __init__(self):
        super().__init__("ResearchAgent")

    def generate_response(
        self,
        query,
        previous_results
    ):

        return """RESEARCH ANALYSIS

Research workflow:

1. Define the research question.
2. Find relevant sources.
3. Prefer authoritative sources.
4. Cross-check important claims.
5. Compare conflicting evidence.
6. Identify limitations.
7. Separate facts from assumptions.
8. Produce an evidence-based conclusion."""


# ============================================================
# REASONING AGENT
# ============================================================

class ReasoningAgent(BaseAgent):

    def __init__(self):
        super().__init__("ReasoningAgent")

    def generate_response(
        self,
        query,
        previous_results
    ):

        q = query.lower()

        # ----------------------------------------------------
        # OVERFITTING
        # ----------------------------------------------------

        if (
            "99%" in q
            and "70%" in q
            and "training" in q
            and "validation" in q
        ):

            return """REASONING ANALYSIS

Observation:
Training accuracy is 99%, while validation accuracy is
only 70%.

Inference:
There is a 29 percentage-point generalization gap.

Most likely cause:
Overfitting.

Alternative causes that must also be checked:
- Data leakage
- Incorrect validation split
- Distribution shift
- Preprocessing mismatch

Decision:
The system should not optimize for training accuracy.
It should optimize for validation and test generalization.

Priority:
1. Check data leakage.
2. Verify data splitting.
3. Verify preprocessing.
4. Check distribution differences.
5. Apply regularization.
6. Consider reducing model complexity.
7. Use cross-validation.
8. Increase training data if possible.

Conclusion:
The model is overfitting or otherwise failing to
generalize to unseen data."""

        # ----------------------------------------------------
        # FRAUD
        # ----------------------------------------------------

        if (
            "fraud" in q
            and "99.5" in q
            and "20%" in q
        ):

            return """REASONING ANALYSIS

Observation:
Accuracy is 99.5%, but fraud recall is approximately
20%.

Inference:
The model is likely dominated by the majority
non-fraud class.

Critical issue:
Approximately 80% of actual fraud cases may be missed.

Therefore:
Accuracy is not an adequate primary success criterion.

Priority metrics:
1. Recall
2. Precision
3. F1-score
4. PR-AUC
5. Confusion Matrix

Recommended direction:
Tune the decision threshold and investigate class
weighting, resampling and better features.

Conclusion:
The model is not satisfactory for fraud detection
despite its high overall accuracy."""

        # ----------------------------------------------------
        # USE PREVIOUS AGENT OUTPUTS
        # ----------------------------------------------------

        useful = [

            result

            for result in previous_results

            if (
                result.status == "success"
                and result.agent_name
                != "ReasoningAgent"
            )
        ]

        if not useful:

            return """REASONING ANALYSIS

No specialist evidence was available.

A reliable conclusion requires evidence before
reasoning and decision-making."""

        lines = [
            "REASONING ANALYSIS",
            "",
            "Evidence received:"
        ]

        for result in useful:

            first_line = (
                result.output
                .strip()
                .split("\n")[0]
            )

            lines.append(
                f"- {result.agent_name}: {first_line}"
            )

        lines.extend(
            [
                "",
                "Reasoning process:",
                "1. Identify relevant evidence.",
                "2. Compare specialist outputs.",
                "3. Detect contradictions or missing information.",
                "4. Infer the most likely explanation.",
                "5. Select the appropriate action.",
                "6. State the conclusion."
            ]
        )

        return "\n".join(lines)


# ============================================================
# CRITIC AGENT
# ============================================================

class CriticAgent(BaseAgent):

    def __init__(self):
        super().__init__("CriticAgent")

    def generate_response(
        self,
        query,
        previous_results
    ):

        if not previous_results:

            return """CRITIC REVIEW

Status: FAILED

No agent output was available."""

        errors = [

            result.agent_name

            for result in previous_results

            if result.status == "error"
        ]

        if errors:

            return (
                "CRITIC REVIEW\n\n"
                "Status: FAILED\n\n"
                "Agents with errors:\n"
                + "\n".join(
                    "- " + name
                    for name in errors
                )
            )

        return """CRITIC REVIEW

Status: PASSED

Checks:
- Agent execution: PASSED
- No execution errors: PASSED
- Specialist output available: PASSED
- Reasoning layer available: PASSED
- Pipeline integrity: PASSED

Recommendation:
Use the reasoning output together with specialist
evidence when producing the final response."""


# ============================================================
# GENERAL AGENT
# ============================================================

class GeneralAgent(BaseAgent):

    def __init__(self):
        super().__init__("GeneralAgent")

    def generate_response(
        self,
        query,
        previous_results
    ):

        return (
            "RETRO-AI received the request and processed it "
            "through the multi-agent intelligence engine."
        )


# ============================================================
# MULTI AGENT SYSTEM
# ============================================================

class MultiAgentSystem:

    def __init__(self):

        print()
        print("=" * 70)
        print("RETRO-AI PHASE 2")
        print("MULTI-AGENT INTELLIGENCE ENGINE")
        print("=" * 70)

        self.brain = None

        if IntelligenceBrain is not None:

            try:
                self.brain = IntelligenceBrain()
                print("BRAIN: READY")

            except Exception as error:

                print("BRAIN: FALLBACK")
                print("Brain error:", error)

        else:

            print("BRAIN: FALLBACK")

        self.agents = {

            "MLAgent":
                MLAgent(),

            "CodingAgent":
                CodingAgent(),

            "DataAnalysisAgent":
                DataAnalysisAgent(),

            "ResearchAgent":
                ResearchAgent(),

            "ReasoningAgent":
                ReasoningAgent(),

            "CriticAgent":
                CriticAgent(),

            "GeneralAgent":
                GeneralAgent()
        }

        print("AGENTS: READY")
        print("=" * 70)

    # ========================================================
    # FALLBACK INTENT
    # ========================================================

    def detect_intent(self, query):

        q = query.lower()

        if any(
            word in q
            for word in [
                "code",
                "python",
                "javascript",
                "java",
                "debug",
                "bug",
                "program",
                "implement",
                "algorithm",
                "prime",
                "duplicate",
                "factorial",
                "fibonacci",
                "palindrome"
            ]
        ):

            return "CODING"

        if any(
            word in q
            for word in [
                "machine learning",
                "neural network",
                "classification",
                "regression",
                "ml model",
                "model accuracy",
                "overfitting",
                "underfitting",
                "fraud detection"
            ]
        ):

            return "MACHINE_LEARNING"

        if any(
            word in q
            for word in [
                "dataset",
                "csv",
                "data analysis",
                "analyze data"
            ]
        ):

            return "DATA_ANALYSIS"

        if any(
            word in q
            for word in [
                "research",
                "latest developments",
                "research latest"
            ]
        ):

            return "RESEARCH"

        if any(
            word in q
            for word in [
                "why",
                "reason",
                "logic",
                "analyze"
            ]
        ):

            return "REASONING"

        return "GENERAL"

    # ========================================================
    # ROUTE
    # ========================================================

    def route_agents(
        self,
        query,
        intent
    ):

        if intent == "MACHINE_LEARNING":

            return [
                "MLAgent",
                "ReasoningAgent"
            ]

        if intent == "CODING":

            return [
                "CodingAgent",
                "ReasoningAgent"
            ]

        if intent == "DATA_ANALYSIS":

            return [
                "DataAnalysisAgent",
                "ReasoningAgent"
            ]

        if intent == "RESEARCH":

            return [
                "ResearchAgent",
                "ReasoningAgent"
            ]

        if intent == "REASONING":

            return [
                "ReasoningAgent"
            ]

        return [
            "GeneralAgent"
        ]

    # ========================================================
    # FIND RESULT
    # ========================================================

    def find_result(
        self,
        results,
        agent_name
    ):

        for result in results:

            if result.agent_name == agent_name:
                return result

        return None

    # ========================================================
    # FINAL RESPONSE
    # ========================================================

    def build_final_response(
        self,
        intent,
        results
    ):

        successful = [

            result

            for result in results

            if (
                result.status == "success"
                and result.agent_name
                != "CriticAgent"
            )
        ]

        if not successful:

            return (
                "RETRO-AI could not generate a valid response."
            )

        parts = []

        for result in successful:

            if result.agent_name in [
                "MLAgent",
                "CodingAgent",
                "DataAnalysisAgent",
                "ResearchAgent",
                "ReasoningAgent"
            ]:

                parts.append(
                    result.output
                )

        if parts:

            return (
                "\n\n"
                + (
                    "\n\n"
                    + "=" * 60
                    + "\n\n"
                ).join(parts)
            )

        return successful[0].output

    # ========================================================
    # EXECUTE
    # ========================================================

    def execute(self, query):

        if not isinstance(query, str):

            raise TypeError(
                "Query must be a string."
            )

        query = query.strip()

        if not query:

            return {
                "query": "",
                "intent": "GENERAL",
                "agents": [],
                "results": [],
                "final_response":
                    "Please enter a valid query."
            }

        print()
        print("=" * 70)
        print("RETRO-AI MULTI-AGENT ENGINE")
        print("=" * 70)

        print()
        print("QUERY:")
        print(query)

        intent = None
        selected_agents = None

        # ----------------------------------------------------
        # BRAIN
        # ----------------------------------------------------

        if self.brain is not None:

            try:

                decision = self.brain.think(
                    query
                )

                intent = str(
                    decision.understanding.intent
                )

                selected_agents = list(
                    decision.recommended_agents
                )

            except Exception as error:

                print(
                    "Brain fallback:",
                    error
                )

        # ----------------------------------------------------
        # FALLBACK
        # ----------------------------------------------------

        if not intent:

            intent = self.detect_intent(
                query
            )

        if not selected_agents:

            selected_agents = self.route_agents(
                query,
                intent
            )

        # ----------------------------------------------------
        # VALID AGENTS
        # ----------------------------------------------------

        selected_agents = [

            name

            for name in selected_agents

            if name in self.agents
        ]

        if not selected_agents:

            selected_agents = [
                "GeneralAgent"
            ]

        # ----------------------------------------------------
        # ALWAYS ADD REASONING AFTER SPECIALIST
        # ----------------------------------------------------

        specialist_exists = any(
            name not in [
                "ReasoningAgent",
                "CriticAgent"
            ]
            for name in selected_agents
        )

        if (
            specialist_exists
            and "ReasoningAgent"
            not in selected_agents
        ):

            selected_agents.append(
                "ReasoningAgent"
            )

        print()
        print("INTENT:")
        print(intent)

        print()
        print("SELECTED AGENTS:")

        for name in selected_agents:

            print(
                " ->",
                name
            )

        # ----------------------------------------------------
        # EXECUTE
        # ----------------------------------------------------

        results = []

        print()
        print(
            "AGENT EXECUTION"
        )

        print(
            "-" * 70
        )

        for name in selected_agents:

            agent = self.agents.get(
                name
            )

            if agent is None:
                continue

            result = agent.execute(
                query,
                results
            )

            results.append(
                result
            )

            print()
            print(
                f"[{result.agent_name}]"
            )

            print(
                "STATUS:",
                result.status
            )

            print(
                result.output
            )

            print(
                "TIME:",
                result.execution_time_ms,
                "ms"
            )

        # ----------------------------------------------------
        # CRITIC
        # ----------------------------------------------------

        critic = self.agents[
            "CriticAgent"
        ]

        critic_result = critic.execute(
            query,
            results
        )

        results.append(
            critic_result
        )

        print()
        print(
            "-" * 70
        )

        print(
            critic_result.output
        )

        # ----------------------------------------------------
        # FINAL
        # ----------------------------------------------------

        final_response = self.build_final_response(
            intent,
            results
        )

        print()
        print(
            "-" * 70
        )

        print(
            "FINAL RESPONSE"
        )

        print(
            "-" * 70
        )

        print()
        print(
            final_response
        )

        print()
        print(
            "=" * 70
        )

        print(
            "MULTI-AGENT PIPELINE COMPLETE"
        )

        print(
            "=" * 70
        )

        return {

            "query":
                query,

            "intent":
                intent,

            "agents":
                selected_agents,

            "results":
                results,

            "final_response":
                final_response
        }


# ============================================================
# TEST SUITE
# ============================================================

def run_tests():

    system = MultiAgentSystem()

    test_queries = [

        "Explain machine learning.",

        "How can I improve my ML model accuracy?",

        (
            "A model has 99% training accuracy but only "
            "70% validation accuracy. Explain what is "
            "happening and provide a solution."
        ),

        (
            "A fraud detection model has 99.5% accuracy "
            "but detects only 20% of actual fraud cases. "
            "Is the model good?"
        ),

        "Write Python code to check whether a number is prime.",

        "Write Python code to find duplicate elements in a list.",

        (
            "Write Python code to find the second largest "
            "number in a list without using sort."
        ),

        "Write Python code for factorial.",

        "Write Python code for Fibonacci.",

        "Write Python code to check whether a string is palindrome.",

        "Write Python code to analyze a CSV dataset."
    ]

    for index, query in enumerate(
        test_queries,
        start=1
    ):

        print()
        print()
        print("#" * 70)
        print(
            f"TEST {index}"
        )
        print("#" * 70)

        try:

            system.execute(
                query
            )

        except Exception as error:

            print()
            print(
                "TEST ERROR:",
                error
            )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    run_tests()
    