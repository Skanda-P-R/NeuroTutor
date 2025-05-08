import ast
from groq_api import send_to_groq

class SymbolicAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.defined_vars = set()      
        self.used_vars = set()         
        self.imports = set()           
        self.used_imports = set()      
        self.functions = set()         
        self.called_functions = set()  
        self.unreachable_code = []     
        self.assigned_but_unused = set() 
        self.function_scope = {}      
        self.current_function = None   

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.add(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module:
            self.imports.add(node.module)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.functions.add(node.name)
        previous_function = self.current_function
        self.current_function = node.name
        self.function_scope[self.current_function] = {
            'defined_vars': set(),
            'used_vars': set(),
            'called_functions': set(),
        }
        self.generic_visit(node)
        self.current_function = previous_function

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if self.current_function:
                self.function_scope[self.current_function]['called_functions'].add(node.func.id)
            self.called_functions.add(node.func.id)
        self.generic_visit(node)

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.defined_vars.add(target.id)
                if self.current_function:
                    self.function_scope[self.current_function]['defined_vars'].add(target.id)
                if isinstance(target.ctx, ast.Store):
                    self.assigned_but_unused.add(target.id)
        self.generic_visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            self.used_vars.add(node.id)
            if self.current_function:
                self.function_scope[self.current_function]['used_vars'].add(node.id)
        self.generic_visit(node)

    def visit_If(self, node):
        if isinstance(node.test, ast.NameConstant):
            if node.test.value is False:
                self.unreachable_code.append(f"Unreachable code after condition {ast.dump(node)}")
        self.generic_visit(node)

    def visit_Return(self, node):
        if self.current_function:
            self.unreachable_code.append(f"Unreachable code after return in function '{self.current_function}'")
        self.generic_visit(node)

    def visit_Break(self, node):
        self.unreachable_code.append(f"Unreachable code after break in loop.")
        self.generic_visit(node)

    def visit_While(self, node):
        if isinstance(node.test, ast.NameConstant) and node.test.value is True:
            self.unreachable_code.append(f"Unreachable code after infinite loop in function '{self.current_function}'")
        self.generic_visit(node)

    def visit_For(self, node):
        if isinstance(node.iter, ast.NameConstant) and node.iter.value is True:
            self.unreachable_code.append(f"Unreachable code after infinite loop in function '{self.current_function}'")
        self.generic_visit(node)

    def analyze(self):
        report = []
        
        undefined_vars = self.used_vars - self.defined_vars - set(dir(__builtins__))
        for var in undefined_vars:
            report.append(f"[ERROR] Undefined variable '{var}' used before definition.")

        unused_imports = self.imports - self.used_vars
        for imp in unused_imports:
            report.append(f"[ERROR] Import '{imp}' is never used.")

        unused_functions = self.functions - self.called_functions
        for func in unused_functions:
            report.append(f"[ERROR] Function '{func}' is defined but never called.")

        for var in self.assigned_but_unused:
            report.append(f"[ERROR] Variable '{var}' is assigned but never used.")

        for uc in self.unreachable_code:
            report.append(f"[ERROR] {uc}")

        for func, scope in self.function_scope.items():
            unused_in_scope = scope['defined_vars'] - scope['used_vars']
            for var in unused_in_scope:
                report.append(f"[ERROR] Variable '{var}' in function '{func}' is defined but never used.")

        return report

def analyze_script(source_code):
    tree = ast.parse(source_code)
    analyzer = SymbolicAnalyzer()
    analyzer.visit(tree)
    issues = analyzer.analyze()
    issues_arr = []
    if issues:
        issues_arr.append("🚨 Issues Found:")
        for issue in issues:
            issues_arr.append(f" - {issue}")
    return issues_arr


def get_debugged_code(issues,source_code):
    return send_to_groq(source_code,issues)