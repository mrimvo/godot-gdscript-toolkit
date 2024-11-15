import re
from lark import Tree
from types import MappingProxyType
from typing import List

from .problem import Problem


def lint(parse_tree: Tree, gdscript_code: str,config: MappingProxyType) -> List[Problem]:
    disable = config["disable"]
    checks_to_run_w_tree = [
        (
            "static-type",
            _static_type_check,
        ),
    ]
    problem_clusters = (
        x[1](parse_tree, gdscript_code) if x[0] not in disable else []
        for x in checks_to_run_w_tree
    )
    problems = [problem for cluster in problem_clusters for problem in cluster]
    return problems


def _static_type_check(parse_tree: Tree, code: str) -> List[Problem]:

    # we could use the Tree in the future,
    # but let's keep it simple for now and use the
    # regular expression based approach

    problems = []

    patterns = [
        r"^\s*var\s+\w+\s*=",
        r"^\s*var\s+\w+\s*$",
        r"^\s*func\s+\w+\s*\((\s*\w+\s*=|.*,\s*\w+\s*=)",
        r"^\s*func\s+\w+\s*\((\s*\w+\s*[,\)]|.*,\s*\w+\s*[,\)])",
    ]

    lines = code.splitlines()
    for line_number, line in enumerate(lines):
        for pattern in patterns:
            if re.match(pattern, line):
                problems.append(Problem(
                    name="static-type",
                    description="Untyped expression",
                    line=line_number + 1,
                    column=0,
                ))

    return problems

