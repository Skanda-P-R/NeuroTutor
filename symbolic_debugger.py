import ast
from groq_api_debug import send_to_groq
from tree_sitter_language_pack import get_language, get_parser

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
    issues_arr = []

    try:
        tree = ast.parse(source_code)
        analyzer = SymbolicAnalyzer()
        analyzer.visit(tree)
        issues = analyzer.analyze()

        if issues:
            issues_arr.append("🚨 Issues Found:")
            for issue in issues:
                issues_arr.append(f" - {issue}")

    except SyntaxError as e:
        issues_arr.append("🚨 Syntax Error:")
        issues_arr.append(f" - {e.msg} at line {e.lineno}, column {e.offset}")
        issues_arr.append(f" - Line: {e.text.strip()}" if e.text else "")

    return issues_arr

def get_debugged_code(issues,source_code):
    return send_to_groq(source_code,issues)

cpp_language = get_language("cpp")
parser = get_parser("cpp")

class CppSymbolicAnalyzer:
    def __init__(self):
        self.builtin_vars = set([
            "std", "cout", "endl", "string", "vector", "map", "auto", "size_t",
            "Calculator", "main", "do_math"
        ])
        self.global_defined = set()
        self.used_vars = {}
        self.functions = {}
        self.called_functions = set()
        self.unreachable_code = []
        self.assigned_but_unused = {}

        self.current_function = None
        self.function_scope = {}

    def analyze(self, source_code):
        tree = parser.parse(source_code.encode())
        root = tree.root_node

        self.collect_functions(root)

        self.analyze_node(root)

        report = []

        undefined_vars = set(self.used_vars) - self.global_defined - self.builtin_vars
        for var in undefined_vars:
            node = self.used_vars[var]
            line = node.start_point[0] + 1
            report.append(f"[ERROR] Line {line}: Undefined variable '{var}' used before definition.")

        unused_functions = set(self.functions) - self.called_functions
        for func in unused_functions:
            node = self.functions[func]
            line = node.start_point[0] + 1
            report.append(f"[ERROR] Line {line}: Function '{func}' is defined but never called.")

        for var, node in self.assigned_but_unused.items():
            if var not in self.used_vars:
                line = node.start_point[0] + 1
                report.append(f"[ERROR] Line {line}: Variable '{var}' is assigned but never used.")

        for func, scope in self.function_scope.items():
            unused_in_scope = set(scope['defined_vars']) - set(scope['used_vars'])
            for var in unused_in_scope:
                node = scope['defined_vars'][var]
                line = node.start_point[0] + 1
                report.append(f"[ERROR] Line {line}: Variable '{var}' in function '{func}' is defined but never used.")

        for msg, line in self.unreachable_code:
            report.append(f"[ERROR] Line {line}: {msg}")

        return report

    def collect_functions(self, node):
        if node.type == "function_definition":
            func_name = None
            for child in node.children:
                if child.type == "declarator":
                    for dchild in child.children:
                        if dchild.type == "identifier":
                            func_name = self.get_node_text(dchild)
                            self.functions[func_name] = node
                            break
            if func_name:
                self.function_scope[func_name] = {
                    'defined_vars': {},
                    'used_vars': {},
                    'called_functions': set(),
                }
        for child in node.children:
            self.collect_functions(child)

    def analyze_node(self, node):
        method = getattr(self, f"handle_{node.type}", self.generic_handle)
        method(node)

    def generic_handle(self, node):
        for child in node.children:
            self.analyze_node(child)

    def handle_function_definition(self, node):
        func_name = None
        for child in node.children:
            if child.type == "declarator":
                for dchild in child.children:
                    if dchild.type == "identifier":
                        func_name = self.get_node_text(dchild)
                        break

        if func_name:
            self.current_function = func_name
            for child in node.children:
                self.analyze_node(child)
            self.current_function = None
        else:
            self.generic_handle(node)


    def handle_parameter_list(self, node):
        func_name = self.current_function
        if not func_name:
            return
        for param in node.children:
            if param.type == "parameter_declaration":
                for child in param.children:
                    if child.type == "identifier":
                        var_name = self.get_node_text(child)
                        self.function_scope[func_name]['defined_vars'][var_name] = child


    def handle_call_expression(self, node):
        if node.children and node.children[0].type == "identifier":
            func_called = self.get_node_text(node.children[0])
            self.called_functions.add(func_called)
            if self.current_function:
                self.function_scope[self.current_function]['called_functions'].add(func_called)
        self.generic_handle(node)

    def handle_identifier(self, node):
        var_name = self.get_node_text(node)
        parent = node.parent

        if parent:
            if parent.type in ("init_declarator", "parameter_declaration", "declaration"):
                if self.current_function:
                    self.function_scope[self.current_function]['defined_vars'][var_name] = node
                else:
                    self.global_defined.add(var_name)
                self.assigned_but_unused[var_name] = node
            else:
                self.used_vars[var_name] = node
                if self.current_function:
                    self.function_scope[self.current_function]['used_vars'][var_name] = node


    def handle_return_statement(self, node):
        if self.current_function:
            pass
        self.generic_handle(node)

    def handle_compound_statement(self, node):
        found_return = False
        reported_unreachable_lines = set()
        for child in node.children:
            if found_return:
                line = child.start_point[0] + 1
                if line not in reported_unreachable_lines:
                    self.unreachable_code.append(("Unreachable code detected after return statement.", line))
                    reported_unreachable_lines.add(line)
            if child.type == "return_statement":
                found_return = True
            self.analyze_node(child)

    def handle_for_statement(self, node):
        for child in node.children:
            if child.type == "init_statement":
                self.handle_init_statement(child)
            else:
                self.analyze_node(child)

    def handle_init_statement(self, node):
        for child in node.children:
            if child.type in ("declaration", "init_declarator"):
                self.handle_init_declarator(child)
            else:
                self.analyze_node(child)

    def handle_init_declarator(self, node):
        for child in node.children:
            if child.type == "identifier":
                var_name = self.get_node_text(child)
                if self.current_function:
                    self.function_scope[self.current_function]['defined_vars'][var_name] = child
                else:
                    self.global_defined.add(var_name)
            else:
                self.analyze_node(child)

    def handle_range_for_statement(self, node):
        for child in node.children:
            if child.type in ("declaration", "init_declarator"):
                self.handle_init_declarator(child)
            else:
                self.analyze_node(child)

    def get_node_text(self, node):
        return bytes(node.text).decode('utf-8')

def analyze_script_cpp(source_code):
    analyzer = CppSymbolicAnalyzer()
    issues = analyzer.analyze(source_code)
    issues_arr = []
    if issues:
        issues_arr.append("🚨 Issues Found:")
        for issue in issues:
            issues_arr.append(f" - {issue}")
    return issues_arr

def get_debugged_code_cpp(errors,code):
    return send_to_groq(code,errors)