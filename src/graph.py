import json
import os
from typing import Annotated, List, TypedDict

from langchain_google_genai import GoogleGenerativeAI
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field

from prompt import DIRECT_PROMPT


SOLUTIONS = {}
with open("solutions.json", "r") as f:
    SOLUTIONS = json.load(f)


# Define the state of the agent
class AgentState(TypedDict):
    problem_description: str
    code: str
    test_results: str
    reflections: List[str]

# Define the output schema for our solver
class CodeSolution(BaseModel):
    code: str = Field(description="The Python code solution.")

# Define the tools
class ExecuteTests(BaseModel):
    """A tool to execute the generated code against test cases."""
    code: str = Field(description="The code to be executed.")
    test_cases: list = Field(description="A list of (input, expected_output) tuples.")

    def run(self):
        results = []
        for i, (test_input, expected_output) in enumerate(self.test_cases):
            try:
                # A simple and unsafe way to execute code for demonstration.
                # In a real-world scenario, use a secure sandboxed environment.
                local_scope = {}
                exec(self.code, globals(), local_scope)
                result = local_scope['solve'](test_input) # Assuming the function is named 'solve'
                if result == expected_output:
                    results.append(f"Test case {i+1}: Passed")
                else:
                    results.append(f"Test case {i+1}: Failed. Input: {test_input}, Expected: {expected_output}, Got: {result}")
            except Exception as e:
                results.append(f"Test case {i+1}: Error - {e}")
        return "\n".join(results)

# Define the nodes of the graph
def solve(state: AgentState):
    print("---GENERATING SOLUTION---")
    # structured_llm = model.with_structured_output(CodeSolution)
    # prompt = DIRECT_PROMPT.format(problem=state["problem_description"])
    # solution = model.invoke(prompt)

    for solution in SOLUTIONS.values():
        if solution['description'] == state["problem_description"]:
            return {"code": solution['code']}

    return {"code": ""}

# def test(state: AgentState):
#     print("---TESTING SOLUTION---")
#     # Example test cases for a simple problem
#     test_cases = [
#         (2, 4),
#         (3, 9),
#         (-2, 4)
#     ]
#     executor = ExecuteTests(code=state["code"], test_cases=test_cases)
#     test_results = executor.run()
#     return {"test_results": test_results}

# def reflect(state: AgentState):
#     print("---REFLECTING ON FAILURES---")
#     model = ChatAnthropic(model_name="claude-3-opus-20240229", temperature=0)
#     prompt = f"""Your generated code failed some test cases.
# Problem: {state['problem_statement']}
# Code:
# {state['code']}
# Test Results:
# {state['test_results']}

# Provide reflections on why the code might have failed and suggest improvements. Focus on the logic and potential edge cases.
# """
#     reflection = model.invoke(prompt).content
#     new_reflections = state.get('reflections', []) + [reflection]
#     return {"reflections": new_reflections}

# Define the conditional edge
def should_continue(state: AgentState):
    if "Failed" in state["test_results"] or "Error" in state["test_results"]:
        return "reflect"
    else:
        return "end"


model = GoogleGenerativeAI(
    model="gemma-3-12b-it",
    # max_tokens=32,
    temperature=0.1
)

# Build the graph
graph = StateGraph(AgentState)

graph.add_node("solve", solve)
# graph.add_node("test", test)
# graph.add_node("reflect", reflect)

graph.add_edge(START, "solve")
graph.add_edge("solve", END)
# graph.add_edge("solve", "test")
# graph.add_conditional_edges(
#     "test",
#     should_continue,
#     {
#         "reflect": "reflect",
#         "end": END,
#     },
# )
# graph.add_edge("reflect", "solve")

graph = graph.compile()
