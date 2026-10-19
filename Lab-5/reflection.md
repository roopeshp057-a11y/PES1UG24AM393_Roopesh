# Lab 5: Static Code Analysis — Reflection

### 1. What is static code analysis?

Static code analysis is a software testing and quality assurance methodology where source code is evaluated and inspected without executing the program. By parsing source files into an Abstract Syntax Tree (AST) and applying specialized rule engines, static analysis identifies syntax errors, adherence to style guidelines (such as PEP 8), potential logical bugs, anti-patterns (such as mutable default arguments), dead code, and security vulnerabilities early in the software development lifecycle (SDLC). Because it does not require running test suites or deploying the program, static code analysis provides rapid, automated feedback to developers, reducing the cost and effort of defect remediation.

---

### 2. What are Pylint, Bandit, and Flake8 used for?

Each of the three static analysis tools targets a distinct dimension of code health:

- **Pylint ("Strict Code Reviewer"):** Pylint evaluates code quality, design structure, and logical consistency. It flags code smells such as dangerous mutable default arguments, unused variables or arguments, missing docstrings, duplicate code, and naming convention violations. It assigns an overall rating out of 10 to measure code health.
- **Bandit ("Security Guard"):** Bandit is a dedicated Static Application Security Testing (SAST) tool tailored for Python. It parses code into an AST to search for known security vulnerabilities and unsafe coding patterns, including command injection (`os.system`), insecure deserialization (`pickle.load`), weak cryptography or pseudo-randomness (`random.choice`), and hardcoded secrets. Findings are categorized by severity (Low, Medium, High) and confidence.
- **Flake8 ("Grammar & Style Checker"):** Flake8 enforces Python's PEP 8 style guide by bundling PyFlakes (syntax and basic errors), pycodestyle (formatting, whitespace, indentation, line lengths), and McCabe (cyclomatic complexity). It ensures consistency, readability, and neat formatting across the codebase.

---

### 3. What issues were identified and fixed?

In `event_manager.py`, several critical, moderate, and stylistic issues were identified and systematically resolved:

1. **Security Vulnerabilities (Bandit):**
   - **Shell Command Injection (High, B605):** `os.system()` was used in `printBadges`, exposing the system to arbitrary shell execution. Replaced with `subprocess.run(["/usr/bin/lp", ...], check=False)` using an argument list rather than a shell string.
   - **Insecure Deserialization (Medium, B301 / B403):** `pickle.load()` was used to restore events. Replaced `pickle` with standard, safe `json` serialization (`json.dump` / `json.load`) with UTF-8 encoding.
   - **Predictable Randomness (Low, B311):** `random.choice()` was used for the lucky draw. Replaced with `secrets.choice()` from Python's standard `secrets` module.

2. **PEP 8 Formatting (Flake8):**
   - Corrected missing whitespace after commas (`"Rooftop",2` $\rightarrow$ `"Rooftop", 2`), missing whitespace around assignment operators (`left=seatsLeft`), missing 2 spaces before inline comments, and ensured two blank lines between top-level functions and invocations. Kept all line lengths within PEP 8 limits ($\le 79$ characters).

3. **Logic Bugs, Code Quality, and Design (Pylint):**
   - **Mutable Default Argument Bug (W0102):** `createEvent` used `guests=[]`, causing all events without an explicit guest list to share a single list object in memory (which caused Alumni Dinner to incorrectly appear full with Tech Meetup attendees). Fixed by setting `guests=None` and instantiating a fresh list inside the function.
   - **Unused Parameter (W0613):** `sortOrder` was declared in `guestReport` but ignored. Implemented proper ordering logic based on `sort_order`.
   - **Naming Conventions (C0103):** Converted all camelCase function and parameter names to PEP 8 standard `snake_case` (`create_event`, `register_guest`, `seats_left`, `event_status`, etc.).
   - **Redundant Control Flow (R1705):** Removed unnecessary `else` after `return` in `event_status`.
   - **Documentation (C0114, C0116):** Added clear, descriptive docstrings for the module and all functions, elevating the Pylint score from 4.64/10 to a perfect 10.00/10.

---

### 4. How does static analysis improve software quality?

Static code analysis significantly enhances software development in multiple ways:

1. **Shift-Left Security & Bug Prevention:** By identifying security risks (such as injection vectors or deserialization flaws) and logical errors (such as shared mutable defaults) during development, flaws are caught before reaching testing or production, dramatically reducing vulnerability windows and fixing costs.
2. **Readability & Maintainability:** Uniform formatting, clean naming conventions, and docstrings ensure that code is self-documenting and accessible to team members, speeding up onboarding and code reviews.
3. **Automated Quality Gates:** Integrating tools like Pylint, Bandit, and Flake8 into CI/CD pipelines ensures objective, repeatable standards that prevent regressions and enforce consistent code health across entire development teams.
4. **Developer Education:** Analysis reports educate developers on modern language idioms, security standards (CWEs), and design best practices, continually raising team engineering standards.
