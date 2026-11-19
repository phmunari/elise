import keyword
import os
import re
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk


class NotepadWithLineNumbers:
    C_KEYWORDS = {
        "auto", "break", "case", "char", "const", "continue", "default", "do", "double",
        "else", "enum", "extern", "float", "for", "goto", "if", "inline", "int", "long",
        "register", "restrict", "return", "short", "signed", "sizeof", "static", "struct",
        "switch", "typedef", "union", "unsigned", "void", "volatile", "while",
    }
    JS_KEYWORDS = {
        "break", "case", "catch", "class", "const", "continue", "debugger", "default",
        "delete", "do", "else", "export", "extends", "finally", "for", "function", "if",
        "import", "in", "instanceof", "let", "new", "return", "super", "switch", "this",
        "throw", "try", "typeof", "var", "void", "while", "with", "yield",
    }
    SQL_KEYWORDS = {
        "select", "from", "where", "insert", "update", "delete", "join", "left", "right",
        "inner", "outer", "group", "by", "order", "having", "limit", "offset", "create",
        "table", "alter", "drop", "primary", "key", "foreign", "values", "into", "and",
        "or", "not", "null", "distinct", "as", "on", "union",
    }
    SHELL_KEYWORDS = {
        "if", "then", "else", "elif", "fi", "case", "esac", "for", "while", "until",
        "do", "done", "in", "function", "select", "time", "coproc", "break", "continue",
        "return", "export", "readonly", "local", "declare",
    }
    JAVA_KEYWORDS = {
        "abstract", "assert", "boolean", "break", "byte", "case", "catch", "char", "class", "const",
        "continue", "default", "do", "double", "else", "enum", "extends", "final", "finally", "float",
        "for", "if", "implements", "import", "instanceof", "int", "interface", "long", "native", "new",
        "package", "private", "protected", "public", "return", "short", "static", "strictfp", "super",
        "switch", "synchronized", "this", "throw", "throws", "transient", "try", "void", "volatile", "while",
    }
    CSHARP_KEYWORDS = {
        "abstract", "as", "base", "bool", "break", "byte", "case", "catch", "char", "checked", "class",
        "const", "continue", "decimal", "default", "delegate", "do", "double", "else", "enum", "event",
        "explicit", "extern", "false", "finally", "fixed", "float", "for", "foreach", "goto", "if", "implicit",
        "in", "int", "interface", "internal", "is", "lock", "long", "namespace", "new", "null", "object",
        "operator", "out", "override", "params", "private", "protected", "public", "readonly", "ref", "return",
        "sbyte", "sealed", "short", "sizeof", "stackalloc", "static", "string", "struct", "switch", "this",
        "throw", "true", "try", "typeof", "uint", "ulong", "unchecked", "unsafe", "ushort", "using", "virtual",
        "void", "volatile", "while",
    }
    GO_KEYWORDS = {
        "break", "case", "chan", "const", "continue", "default", "defer", "else", "fallthrough", "for",
        "func", "go", "goto", "if", "import", "interface", "map", "package", "range", "return", "select",
        "struct", "switch", "type", "var",
    }
    RUST_KEYWORDS = {
        "as", "break", "const", "continue", "crate", "else", "enum", "extern", "false", "fn", "for", "if",
        "impl", "in", "let", "loop", "match", "mod", "move", "mut", "pub", "ref", "return", "self", "Self",
        "static", "struct", "super", "trait", "true", "type", "unsafe", "use", "where", "while", "async", "await",
    }
    PHP_KEYWORDS = {
        "abstract", "and", "array", "as", "break", "callable", "case", "catch", "class", "clone", "const",
        "continue", "declare", "default", "do", "echo", "else", "elseif", "empty", "enddeclare", "endfor",
        "endforeach", "endif", "endswitch", "endwhile", "eval", "exit", "extends", "final", "finally", "for",
        "foreach", "function", "global", "if", "implements", "include", "include_once", "instanceof", "insteadof",
        "interface", "isset", "list", "namespace", "new", "or", "print", "private", "protected", "public",
        "require", "require_once", "return", "static", "switch", "throw", "trait", "try", "unset", "use", "var",
        "while", "xor", "yield",
    }
    RUBY_KEYWORDS = {
        "BEGIN", "END", "alias", "and", "begin", "break", "case", "class", "def", "defined?", "do", "else",
        "elsif", "end", "ensure", "false", "for", "if", "in", "module", "next", "nil", "not", "or", "redo",
        "rescue", "retry", "return", "self", "super", "then", "true", "undef", "unless", "until", "when", "while",
        "yield",
    }
    LUA_KEYWORDS = {
        "and", "break", "do", "else", "elseif", "end", "false", "for", "function", "goto", "if", "in", "local",
        "nil", "not", "or", "repeat", "return", "then", "true", "until", "while",
    }
    SWIFT_KEYWORDS = {
        "associatedtype", "class", "deinit", "enum", "extension", "fileprivate", "func", "import", "init", "inout",
        "internal", "let", "open", "operator", "private", "protocol", "public", "static", "struct", "subscript",
        "typealias", "var", "break", "case", "continue", "default", "defer", "do", "else", "fallthrough", "for",
        "guard", "if", "in", "repeat", "return", "switch", "where", "while", "as", "Any", "catch", "false", "is",
        "nil", "rethrows", "super", "self", "Self", "throw", "throws", "true", "try",
    }
    KOTLIN_KEYWORDS = {
        "as", "break", "class", "continue", "do", "else", "false", "for", "fun", "if", "in", "interface", "is",
        "null", "object", "package", "return", "super", "this", "throw", "true", "try", "typealias", "val", "var",
        "when", "while",
    }
    POWERSHELL_KEYWORDS = {
        "function", "param", "if", "else", "elseif", "switch", "foreach", "for", "while", "do", "until", "break",
        "continue", "return", "try", "catch", "finally", "throw", "trap", "class", "enum", "filter", "in",
    }
    BATCH_KEYWORDS = {
        "echo", "set", "setlocal", "endlocal", "if", "else", "for", "in", "do", "goto", "call", "exit", "shift",
        "pause", "title", "cd", "dir", "copy", "move", "del", "ren", "start",
    }
    PY_KEYWORD_PATTERN = re.compile(r"\b(" + "|".join(re.escape(word) for word in keyword.kwlist) + r")\b")
    C_KEYWORD_PATTERN = re.compile(r"\b(" + "|".join(re.escape(word) for word in sorted(C_KEYWORDS)) + r")\b")
    JS_KEYWORD_PATTERN = re.compile(r"\b(" + "|".join(re.escape(word) for word in sorted(JS_KEYWORDS)) + r")\b")
    SQL_KEYWORD_PATTERN = re.compile(
        r"\b(" + "|".join(re.escape(word) for word in sorted(SQL_KEYWORDS)) + r")\b",
        flags=re.IGNORECASE,
    )
    SH_KEYWORD_PATTERN = re.compile(r"\b(" + "|".join(re.escape(word) for word in sorted(SHELL_KEYWORDS)) + r")\b")
    JAVA_KEYWORD_PATTERN = re.compile(r"\b(" + "|".join(re.escape(word) for word in sorted(JAVA_KEYWORDS)) + r")\b")
    CSHARP_KEYWORD_PATTERN = re.compile(r"\b(" + "|".join(re.escape(word) for word in sorted(CSHARP_KEYWORDS)) + r")\b")
    GO_KEYWORD_PATTERN = re.compile(r"\b(" + "|".join(re.escape(word) for word in sorted(GO_KEYWORDS)) + r")\b")
    RUST_KEYWORD_PATTERN = re.compile(r"\b(" + "|".join(re.escape(word) for word in sorted(RUST_KEYWORDS)) + r")\b")
    PHP_KEYWORD_PATTERN = re.compile(r"\b(" + "|".join(re.escape(word) for word in sorted(PHP_KEYWORDS)) + r")\b", flags=re.IGNORECASE)
    RUBY_KEYWORD_PATTERN = re.compile(r"\b(" + "|".join(re.escape(word) for word in sorted(RUBY_KEYWORDS)) + r")\b")
    LUA_KEYWORD_PATTERN = re.compile(r"\b(" + "|".join(re.escape(word) for word in sorted(LUA_KEYWORDS)) + r")\b")
    SWIFT_KEYWORD_PATTERN = re.compile(r"\b(" + "|".join(re.escape(word) for word in sorted(SWIFT_KEYWORDS)) + r")\b")
    KOTLIN_KEYWORD_PATTERN = re.compile(r"\b(" + "|".join(re.escape(word) for word in sorted(KOTLIN_KEYWORDS)) + r")\b")
    POWERSHELL_KEYWORD_PATTERN = re.compile(r"\b(" + "|".join(re.escape(word) for word in sorted(POWERSHELL_KEYWORDS)) + r")\b", flags=re.IGNORECASE)
    BATCH_KEYWORD_PATTERN = re.compile(r"\b(" + "|".join(re.escape(word) for word in sorted(BATCH_KEYWORDS)) + r")\b", flags=re.IGNORECASE)
    PY_STRING_PATTERN = re.compile(r"('([^'\\]|\\.)*'|\"([^\"\\]|\\.)*\")")
    C_STRING_PATTERN = re.compile(r"('([^'\\]|\\.)*'|\"([^\"\\]|\\.)*\")")
    JS_STRING_PATTERN = re.compile(r"('([^'\\]|\\.)*'|\"([^\"\\]|\\.)*\"|`([^`\\]|\\.)*`)")
    SQL_STRING_PATTERN = re.compile(r"('([^']|'')*')")
    SH_STRING_PATTERN = re.compile(r"('([^'\\]|\\.)*'|\"([^\"\\]|\\.)*\")")
    PS_STRING_PATTERN = re.compile(r"('([^'\\]|\\.)*'|\"([^\"\\]|\\.)*\")")
    BATCH_STRING_PATTERN = re.compile(r"\"([^\"\\]|\\.)*\"")
    HTML_STRING_PATTERN = re.compile(r"('([^'\\]|\\.)*'|\"([^\"\\]|\\.)*\")")
    PY_COMMENT_PATTERN = re.compile(r"#.*")
    C_COMMENT_PATTERN = re.compile(r"//.*|/\*[\s\S]*?\*/")
    JS_COMMENT_PATTERN = re.compile(r"//.*|/\*[\s\S]*?\*/")
    SQL_COMMENT_PATTERN = re.compile(r"--.*|/\*[\s\S]*?\*/")
    SH_COMMENT_PATTERN = re.compile(r"#.*")
    PS_COMMENT_PATTERN = re.compile(r"#.*|<#([\s\S]*?)#>")
    BATCH_COMMENT_PATTERN = re.compile(r"(?im)^\s*(rem\b.*|::.*)$")
    HTML_TAG_PATTERN = re.compile(r"</?[a-zA-Z][^>\n]*?>")
    HTML_COMMENT_PATTERN = re.compile(r"<!--[\s\S]*?-->")

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.geometry("1180x760")
        self._app_icon = None
        self._set_window_icon()

        self.theme_mode = tk.StringVar(value="dark")
        self.syntax_mode = tk.StringVar(value="plain")
        self.font_size = tk.IntVar(value=12)

        self.replace_window = None
        self.replace_find_var = tk.StringVar(value="")
        self.replace_with_var = tk.StringVar(value="")
        self.replace_case_sensitive_var = tk.BooleanVar(value=False)

        self.tabs = {}
        self.status_var = tk.StringVar(value="Linha 1, Coluna 1")
        self._refresh_job = None
        self.syntax_max_chars = 300_000
        self.search_highlight_max_chars = 400_000
        self.search_highlight_max_matches = 2000
        self.replace_yield_every = 200

        self._create_menu()
        self._create_layout()
        self._bind_events()
        self._apply_theme()
        self._create_tab()
        self._set_title()
        self._refresh_editor()

    def _set_window_icon(self) -> None:
        base_dir = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_dir, "elise.png")
        if not os.path.exists(icon_path):
            return
        try:
            self._app_icon = tk.PhotoImage(file=icon_path)
            self.root.iconphoto(True, self._app_icon)
        except tk.TclError:
            # Mantem o app funcionando caso o ambiente nao aceite PNG como icone.
            self._app_icon = None

    def _create_menu(self) -> None:
        menu_bar = tk.Menu(self.root)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Nova aba", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Abrir", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Fechar aba", command=self.close_current_tab, accelerator="Ctrl+W")
        file_menu.add_separator()
        file_menu.add_command(label="Salvar", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Salvar como", command=self.save_file_as, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.exit_app)

        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Desfazer", command=self.undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Refazer", command=self.redo, accelerator="Ctrl+Y")
        edit_menu.add_command(label="Selecionar tudo", command=self.select_all, accelerator="Ctrl+A")
        edit_menu.add_separator()
        edit_menu.add_command(label="Buscar", command=self.find_text, accelerator="Ctrl+F")
        edit_menu.add_command(label="Localizar e substituir", command=self.open_replace_dialog, accelerator="Ctrl+H")
        edit_menu.add_command(label="Próxima ocorrência", command=self.find_next, accelerator="F3")

        syntax_menu = tk.Menu(menu_bar, tearoff=0)
        syntax_menu.add_radiobutton(
            label="Texto simples (padrão)",
            value="plain",
            variable=self.syntax_mode,
            command=self._refresh_editor,
        )
        syntax_menu.add_separator()
        syntax_menu.add_radiobutton(label="Automático por extensão", value="auto", variable=self.syntax_mode, command=self._refresh_editor)
        syntax_menu.add_radiobutton(label="Python", value="python", variable=self.syntax_mode, command=self._refresh_editor)
        syntax_menu.add_radiobutton(label="C/C++", value="c", variable=self.syntax_mode, command=self._refresh_editor)
        syntax_menu.add_radiobutton(label="HTML", value="html", variable=self.syntax_mode, command=self._refresh_editor)
        syntax_menu.add_radiobutton(label="JavaScript", value="javascript", variable=self.syntax_mode, command=self._refresh_editor)
        syntax_menu.add_radiobutton(label="SQL", value="sql", variable=self.syntax_mode, command=self._refresh_editor)
        syntax_menu.add_radiobutton(label="Shell Script", value="shell", variable=self.syntax_mode, command=self._refresh_editor)
        syntax_menu.add_radiobutton(label="PowerShell", value="powershell", variable=self.syntax_mode, command=self._refresh_editor)
        syntax_menu.add_radiobutton(label="Batch (CMD/BAT)", value="batch", variable=self.syntax_mode, command=self._refresh_editor)
        syntax_menu.add_radiobutton(label="Java", value="java", variable=self.syntax_mode, command=self._refresh_editor)
        syntax_menu.add_radiobutton(label="PHP", value="php", variable=self.syntax_mode, command=self._refresh_editor)
        syntax_menu.add_radiobutton(label="Ruby", value="ruby", variable=self.syntax_mode, command=self._refresh_editor)
        syntax_menu.add_radiobutton(label="Lua", value="lua", variable=self.syntax_mode, command=self._refresh_editor)
        syntax_menu.add_radiobutton(label="Swift", value="swift", variable=self.syntax_mode, command=self._refresh_editor)
        syntax_menu.add_radiobutton(label="Kotlin", value="kotlin", variable=self.syntax_mode, command=self._refresh_editor)
        syntax_menu.add_radiobutton(label="Rust", value="rust", variable=self.syntax_mode, command=self._refresh_editor)
        syntax_menu.add_radiobutton(label="C#", value="csharp", variable=self.syntax_mode, command=self._refresh_editor)
        syntax_menu.add_radiobutton(label="Golang", value="go", variable=self.syntax_mode, command=self._refresh_editor)

        view_menu = tk.Menu(menu_bar, tearoff=0)
        theme_menu = tk.Menu(view_menu, tearoff=0)
        theme_menu.add_radiobutton(label="Claro", value="light", variable=self.theme_mode, command=self._apply_theme)
        theme_menu.add_radiobutton(label="Escuro", value="dark", variable=self.theme_mode, command=self._apply_theme)

        font_menu = tk.Menu(view_menu, tearoff=0)
        font_menu.add_command(label="Aumentar", command=self.increase_font_size, accelerator="Ctrl++")
        font_menu.add_command(label="Diminuir", command=self.decrease_font_size, accelerator="Ctrl+-")
        font_menu.add_command(label="Definir tamanho...", command=self.set_font_size_dialog)

        view_menu.add_cascade(label="Tema", menu=theme_menu)
        view_menu.add_cascade(label="Tamanho do texto", menu=font_menu)

        menu_bar.add_cascade(label="Arquivo", menu=file_menu)
        menu_bar.add_cascade(label="Editar", menu=edit_menu)
        menu_bar.add_cascade(label="Sintaxe", menu=syntax_menu)
        menu_bar.add_cascade(label="Visual", menu=view_menu)
        self.root.config(menu=menu_bar)

    def _create_layout(self) -> None:
        editor_frame = tk.Frame(self.root)
        editor_frame.pack(fill=tk.BOTH, expand=True)

        self.notebook = ttk.Notebook(editor_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)
        self.notebook.bind("<Button-1>", self._on_notebook_click, add="+")

        status = tk.Label(self.root, textvariable=self.status_var, anchor="w", padx=10, pady=4, relief=tk.SUNKEN, bd=1)
        status.pack(fill=tk.X, side=tk.BOTTOM)
        self.status_label = status

    def _create_tab(self, content: str = "", file_path: str | None = None) -> None:
        frame = tk.Frame(self.notebook)
        container = tk.Frame(frame)
        container.pack(fill=tk.BOTH, expand=True)

        line_numbers = tk.Text(
            container,
            width=5,
            padx=6,
            takefocus=0,
            border=0,
            state="disabled",
            wrap="none",
        )
        line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        text = tk.Text(container, undo=True, maxundo=2000, wrap="word", insertwidth=2)
        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        y_scroll = tk.Scrollbar(container, orient=tk.VERTICAL)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        y_scroll.configure(command=lambda *args, t=text, ln=line_numbers: self._on_scroll(t, ln, *args))
        text.configure(yscrollcommand=lambda *args, sb=y_scroll, ln=line_numbers: self._on_textscroll(sb, ln, *args))
        line_numbers.configure(yscrollcommand=y_scroll.set)

        text.tag_configure("search_match")
        text.tag_configure("syntax_keyword", foreground="#569cd6")
        text.tag_configure("syntax_string", foreground="#ce9178")
        text.tag_configure("syntax_comment", foreground="#6a9955")
        text.tag_configure("syntax_html_tag", foreground="#4ec9b0")

        text.bind("<KeyRelease>", self._on_text_event)
        text.bind("<ButtonRelease-1>", self._on_text_event)
        text.bind("<MouseWheel>", self._on_text_event)
        text.bind("<Button-3>", self._show_context_menu)

        if content:
            text.insert("1.0", content)
        text.edit_modified(False)

        self.notebook.add(frame, text=self._format_tab_label(file_path, False))
        tab_id = str(frame)
        self.tabs[tab_id] = {
            "frame": frame,
            "text": text,
            "line_numbers": line_numbers,
            "file_path": file_path,
            "last_search": "",
            "line_count_cache": 0,
        }

        self.notebook.select(frame)
        self._apply_theme()
        self._refresh_editor()

    def _show_context_menu(self, event) -> str:
        text = event.widget
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Recortar", command=lambda: self._context_action(text, "<<Cut>>"))
        menu.add_command(label="Copiar", command=lambda: self._context_action(text, "<<Copy>>"))
        menu.add_command(label="Colar", command=lambda: self._context_action(text, "<<Paste>>"))
        menu.add_separator()
        menu.add_command(label="Selecionar tudo", command=self.select_all)
        menu.tk_popup(event.x_root, event.y_root)
        return "break"

    def _context_action(self, text: tk.Text, action: str) -> None:
        text.focus_set()
        text.event_generate(action)
        self._refresh_editor()
        self._update_current_tab_label()

    def _bind_events(self) -> None:
        self.root.bind("<Control-n>", lambda event: self.new_file())
        self.root.bind("<Control-o>", lambda event: self.open_file())
        self.root.bind("<Control-w>", lambda event: self.close_current_tab())
        self.root.bind("<Control-s>", lambda event: self.save_file())
        self.root.bind("<Control-S>", lambda event: self.save_file_as())
        self.root.bind("<Control-z>", lambda event: self.undo())
        self.root.bind("<Control-y>", lambda event: self.redo())
        self.root.bind("<Control-a>", lambda event: self.select_all())
        self.root.bind("<Control-f>", lambda event: self.find_text())
        self.root.bind("<Control-h>", lambda event: self.open_replace_dialog())
        self.root.bind("<Control-plus>", lambda event: self.increase_font_size())
        self.root.bind("<Control-equal>", lambda event: self.increase_font_size())
        self.root.bind("<Control-minus>", lambda event: self.decrease_font_size())
        self.root.bind("<F3>", lambda event: self.find_next())

        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)

    def _get_current_tab(self):
        tab_id = self.notebook.select()
        if not tab_id:
            return None
        return self.tabs.get(tab_id)

    def _set_title(self) -> None:
        tab = self._get_current_tab()
        if not tab:
            self.root.title("Elise")
            return
        file_path = tab["file_path"]
        name = os.path.basename(file_path) if file_path else "sem_nome"
        self.root.title(f"Elise - {name}")

    def _format_tab_label(self, file_path: str | None, modified: bool) -> str:
        name = os.path.basename(file_path) if file_path else "sem_nome"
        base = f"* {name}" if modified else name
        return f"{base}  [x]"

    def _update_current_tab_label(self) -> None:
        tab = self._get_current_tab()
        if not tab:
            return
        self.notebook.tab(tab["frame"], text=self._format_tab_label(tab["file_path"], tab["text"].edit_modified()))
        self._set_title()

    def _on_tab_changed(self, event=None):
        self._set_title()
        self._refresh_editor()

    def _on_notebook_click(self, event) -> None:
        try:
            tab_id = self.notebook.index(f"@{event.x},{event.y}")
        except tk.TclError:
            return

        bbox = self.notebook.bbox(tab_id)
        if not bbox:
            return

        tab_x, _, tab_w, _ = bbox
        if event.x >= tab_x + tab_w - 24:
            self.notebook.select(tab_id)
            self.close_current_tab()

    def _on_text_event(self, event=None):
        self._schedule_refresh()
        self._update_current_tab_label()

    def _schedule_refresh(self) -> None:
        if self._refresh_job is not None:
            self.root.after_cancel(self._refresh_job)
        self._refresh_job = self.root.after(60, self._refresh_editor)

    def _on_scroll(self, text: tk.Text, line_numbers: tk.Text, *args):
        text.yview(*args)
        line_numbers.yview(*args)

    def _on_textscroll(self, scrollbar: tk.Scrollbar, line_numbers: tk.Text, *args):
        scrollbar.set(*args)
        if args:
            line_numbers.yview_moveto(args[0])

    def _refresh_editor(self, event=None):
        self._refresh_job = None
        self._update_line_numbers()
        self._highlight_syntax()
        self._update_status_bar()

    def _update_status_bar(self) -> None:
        tab = self._get_current_tab()
        if not tab:
            self.status_var.set("Arquivo: sem_nome | Caminho: (não salvo) | Linha 1, Coluna 1")
            return
        index = tab["text"].index("insert")
        line, col = index.split(".")
        file_path = tab["file_path"]
        file_name = os.path.basename(file_path) if file_path else "sem_nome"
        file_location = file_path if file_path else "(não salvo)"
        self.status_var.set(
            f"Arquivo: {file_name} | Caminho: {file_location} | Linha {line}, Coluna {int(col) + 1}"
        )

    def _text_changed(self) -> bool:
        tab = self._get_current_tab()
        return bool(tab and tab["text"].edit_modified())

    def _confirm_discard_changes(self) -> bool:
        tab = self._get_current_tab()
        if not tab or not tab["text"].edit_modified():
            return True

        response = messagebox.askyesnocancel("Salvar alterações", "Deseja salvar as alterações desta aba?")
        if response is None:
            return False
        if response:
            return self.save_file()
        return True

    def _update_line_numbers(self):
        tab = self._get_current_tab()
        if not tab:
            return

        text = tab["text"]
        line_numbers = tab["line_numbers"]
        total_lines = int(text.index("end-1c").split(".")[0])
        if tab.get("line_count_cache") == total_lines:
            return
        line_text = "\n".join(str(i) for i in range(1, total_lines + 1))

        line_numbers.config(state="normal")
        line_numbers.delete("1.0", tk.END)
        line_numbers.insert("1.0", line_text)
        line_numbers.config(state="disabled")
        tab["line_count_cache"] = total_lines

    def _apply_theme(self) -> None:
        if self.theme_mode.get() == "dark":
            bg_main = "#1e1e1e"
            fg_main = "#d4d4d4"
            bg_lines = "#252526"
            fg_lines = "#858585"
            cursor = "#d4d4d4"
            bg_status = "#161616"
            fg_status = "#bfbfbf"
            search_bg = "#ffd166"
            search_fg = "#111111"
        else:
            bg_main = "#ffffff"
            fg_main = "#1a1a1a"
            bg_lines = "#f3f3f3"
            fg_lines = "#777777"
            cursor = "#1a1a1a"
            bg_status = "#f2f2f2"
            fg_status = "#222222"
            search_bg = "#ffe08a"
            search_fg = "#111111"

        editor_font = ("Consolas", self.font_size.get())
        line_font = ("Consolas", max(8, self.font_size.get() - 1))
        status_font = ("Consolas", max(8, self.font_size.get() - 2))

        self.status_label.configure(bg=bg_status, fg=fg_status)
        self.status_label.configure(font=status_font)

        for tab in self.tabs.values():
            text = tab["text"]
            line_numbers = tab["line_numbers"]
            text.configure(background=bg_main, foreground=fg_main, insertbackground=cursor, font=editor_font)
            line_numbers.configure(background=bg_lines, foreground=fg_lines, font=line_font)
            text.tag_configure("search_match", background=search_bg, foreground=search_fg)

    def _set_font_size(self, new_size: int) -> str:
        clamped = max(8, min(40, int(new_size)))
        self.font_size.set(clamped)
        self._apply_theme()
        self._refresh_editor()
        return "break"

    def increase_font_size(self) -> str:
        return self._set_font_size(self.font_size.get() + 1)

    def decrease_font_size(self) -> str:
        return self._set_font_size(self.font_size.get() - 1)

    def set_font_size_dialog(self) -> str:
        value = simpledialog.askinteger(
            "Tamanho do texto",
            "Digite o tamanho da fonte (8 a 40):",
            parent=self.root,
            minvalue=8,
            maxvalue=40,
            initialvalue=self.font_size.get(),
        )
        if value is not None:
            self._set_font_size(value)
        return "break"

    def _clear_syntax_tags(self, text: tk.Text) -> None:
        for tag in ("syntax_keyword", "syntax_string", "syntax_comment", "syntax_html_tag"):
            text.tag_remove(tag, "1.0", tk.END)

    def _highlight_syntax(self) -> None:
        tab = self._get_current_tab()
        if not tab:
            return

        text = tab["text"]
        content = text.get("1.0", "end-1c")
        mode = self._detect_syntax_mode()

        self._clear_syntax_tags(text)
        if mode == "plain":
            return
        if len(content) > self.syntax_max_chars:
            return

        if mode == "python":
            self._apply_syntax_matches(
                text, content, self.PY_KEYWORD_PATTERN, self.PY_STRING_PATTERN, self.PY_COMMENT_PATTERN
            )
            return

        if mode == "c":
            self._apply_syntax_matches(
                text, content, self.C_KEYWORD_PATTERN, self.C_STRING_PATTERN, self.C_COMMENT_PATTERN
            )
            return

        if mode == "javascript":
            self._apply_syntax_matches(
                text, content, self.JS_KEYWORD_PATTERN, self.JS_STRING_PATTERN, self.JS_COMMENT_PATTERN
            )
            return

        if mode == "sql":
            self._apply_syntax_matches(
                text, content, self.SQL_KEYWORD_PATTERN, self.SQL_STRING_PATTERN, self.SQL_COMMENT_PATTERN
            )
            return

        if mode == "shell":
            self._apply_syntax_matches(
                text, content, self.SH_KEYWORD_PATTERN, self.SH_STRING_PATTERN, self.SH_COMMENT_PATTERN
            )
            return

        if mode == "powershell":
            self._apply_syntax_matches(
                text, content, self.POWERSHELL_KEYWORD_PATTERN, self.PS_STRING_PATTERN, self.PS_COMMENT_PATTERN
            )
            return

        if mode == "batch":
            self._apply_syntax_matches(
                text, content, self.BATCH_KEYWORD_PATTERN, self.BATCH_STRING_PATTERN, self.BATCH_COMMENT_PATTERN
            )
            return

        if mode == "java":
            self._apply_syntax_matches(
                text, content, self.JAVA_KEYWORD_PATTERN, self.C_STRING_PATTERN, self.C_COMMENT_PATTERN
            )
            return

        if mode == "php":
            self._apply_syntax_matches(
                text, content, self.PHP_KEYWORD_PATTERN, self.C_STRING_PATTERN, self.C_COMMENT_PATTERN
            )
            return

        if mode == "ruby":
            self._apply_syntax_matches(
                text, content, self.RUBY_KEYWORD_PATTERN, self.SH_STRING_PATTERN, self.SH_COMMENT_PATTERN
            )
            return

        if mode == "lua":
            self._apply_syntax_matches(
                text, content, self.LUA_KEYWORD_PATTERN, self.SH_STRING_PATTERN, self.SQL_COMMENT_PATTERN
            )
            return

        if mode == "swift":
            self._apply_syntax_matches(
                text, content, self.SWIFT_KEYWORD_PATTERN, self.C_STRING_PATTERN, self.C_COMMENT_PATTERN
            )
            return

        if mode == "kotlin":
            self._apply_syntax_matches(
                text, content, self.KOTLIN_KEYWORD_PATTERN, self.C_STRING_PATTERN, self.C_COMMENT_PATTERN
            )
            return

        if mode == "rust":
            self._apply_syntax_matches(
                text, content, self.RUST_KEYWORD_PATTERN, self.C_STRING_PATTERN, self.C_COMMENT_PATTERN
            )
            return

        if mode == "csharp":
            self._apply_syntax_matches(
                text, content, self.CSHARP_KEYWORD_PATTERN, self.C_STRING_PATTERN, self.C_COMMENT_PATTERN
            )
            return

        if mode == "go":
            self._apply_syntax_matches(
                text, content, self.GO_KEYWORD_PATTERN, self.C_STRING_PATTERN, self.C_COMMENT_PATTERN
            )
            return

        if mode == "html":
            for match in self.HTML_TAG_PATTERN.finditer(content):
                self._tag_range(text, "syntax_html_tag", match.start(), match.end())
            for match in self.HTML_STRING_PATTERN.finditer(content):
                self._tag_range(text, "syntax_string", match.start(), match.end())
            for match in self.HTML_COMMENT_PATTERN.finditer(content):
                self._tag_range(text, "syntax_comment", match.start(), match.end())

    def _apply_syntax_matches(
        self,
        text: tk.Text,
        content: str,
        keyword_pattern: re.Pattern,
        string_pattern: re.Pattern,
        comment_pattern: re.Pattern,
    ) -> None:
        for match in keyword_pattern.finditer(content):
            self._tag_range(text, "syntax_keyword", match.start(), match.end())
        for match in string_pattern.finditer(content):
            self._tag_range(text, "syntax_string", match.start(), match.end())
        for match in comment_pattern.finditer(content):
            self._tag_range(text, "syntax_comment", match.start(), match.end())

    def _detect_syntax_mode(self) -> str:
        selected_mode = self.syntax_mode.get()
        if selected_mode != "auto":
            return selected_mode

        tab = self._get_current_tab()
        if not tab or not tab["file_path"]:
            return "plain"

        ext = os.path.splitext(tab["file_path"])[1].lower()
        if ext == ".py":
            return "python"
        if ext in {".c", ".h", ".cpp", ".hpp"}:
            return "c"
        if ext in {".js", ".mjs", ".cjs"}:
            return "javascript"
        if ext == ".sql":
            return "sql"
        if ext in {".sh", ".bash", ".zsh"}:
            return "shell"
        if ext in {".ps1", ".psm1", ".psd1"}:
            return "powershell"
        if ext in {".bat", ".cmd"}:
            return "batch"
        if ext == ".java":
            return "java"
        if ext == ".php":
            return "php"
        if ext == ".rb":
            return "ruby"
        if ext == ".lua":
            return "lua"
        if ext == ".swift":
            return "swift"
        if ext in {".kt", ".kts"}:
            return "kotlin"
        if ext == ".rs":
            return "rust"
        if ext == ".cs":
            return "csharp"
        if ext == ".go":
            return "go"
        if ext in {".html", ".htm"}:
            return "html"
        return "plain"

    def _tag_range(self, text: tk.Text, tag: str, start: int, end: int) -> None:
        text.tag_add(tag, f"1.0+{start}c", f"1.0+{end}c")

    def undo(self) -> None:
        tab = self._get_current_tab()
        if not tab:
            return
        try:
            tab["text"].edit_undo()
            self._refresh_editor()
            self._update_current_tab_label()
        except tk.TclError:
            pass

    def redo(self) -> None:
        tab = self._get_current_tab()
        if not tab:
            return
        try:
            tab["text"].edit_redo()
            self._refresh_editor()
            self._update_current_tab_label()
        except tk.TclError:
            pass

    def select_all(self) -> str:
        tab = self._get_current_tab()
        if not tab:
            return "break"
        text = tab["text"]
        text.tag_add("sel", "1.0", "end-1c")
        text.mark_set("insert", "end-1c")
        text.see("insert")
        self._update_status_bar()
        return "break"

    def find_text(self) -> None:
        tab = self._get_current_tab()
        if not tab:
            return

        query = simpledialog.askstring("Buscar", "Digite o texto para buscar:", parent=self.root)
        if not query:
            return

        tab["last_search"] = query
        self._highlight_search_matches(query)
        self._focus_next_match("1.0")

    def find_next(self) -> None:
        tab = self._get_current_tab()
        if not tab:
            return
        if not tab["last_search"]:
            self.find_text()
            return

        next_index = tab["text"].index("insert+1c")
        self._focus_next_match(next_index)

    def _highlight_search_matches(self, query: str) -> None:
        tab = self._get_current_tab()
        if not tab:
            return
        text = tab["text"]
        text.tag_remove("search_match", "1.0", tk.END)
        if len(text.get("1.0", "end-1c")) > self.search_highlight_max_chars:
            return

        start = "1.0"
        nocase = not self.replace_case_sensitive_var.get()
        count = 0
        while True:
            pos = text.search(query, start, stopindex=tk.END, nocase=nocase)
            if not pos:
                break
            end = f"{pos}+{len(query)}c"
            text.tag_add("search_match", pos, end)
            start = end
            count += 1
            if count >= self.search_highlight_max_matches:
                break

    def _focus_next_match(self, start_index: str) -> None:
        tab = self._get_current_tab()
        if not tab:
            return

        text = tab["text"]
        query = tab["last_search"]
        nocase = not self.replace_case_sensitive_var.get()

        pos = text.search(query, start_index, stopindex=tk.END, nocase=nocase)
        if not pos:
            pos = text.search(query, "1.0", stopindex=tk.END, nocase=nocase)
            if not pos:
                messagebox.showinfo("Buscar", "Nenhuma ocorrência encontrada.")
                return

        end = f"{pos}+{len(query)}c"
        text.mark_set("insert", end)
        text.see(pos)
        text.tag_remove("sel", "1.0", tk.END)
        text.tag_add("sel", pos, end)
        self._update_status_bar()

    def open_replace_dialog(self) -> str:
        tab = self._get_current_tab()
        if not tab:
            return "break"

        if self.replace_window and self.replace_window.winfo_exists():
            self.replace_window.lift()
            self.replace_window.focus_force()
            return "break"

        self.replace_window = tk.Toplevel(self.root)
        self.replace_window.title("Localizar e substituir")
        self.replace_window.transient(self.root)
        self.replace_window.resizable(False, False)

        if tab["last_search"]:
            self.replace_find_var.set(tab["last_search"])

        frame = tk.Frame(self.replace_window, padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text="Localizar:").grid(row=0, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.replace_find_var, width=38).grid(row=0, column=1, padx=(8, 0), pady=(0, 8))

        tk.Label(frame, text="Substituir por:").grid(row=1, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.replace_with_var, width=38).grid(row=1, column=1, padx=(8, 0), pady=(0, 8))

        tk.Checkbutton(
            frame,
            text="Diferenciar maiúsculas/minúsculas",
            variable=self.replace_case_sensitive_var,
        ).grid(row=2, column=0, columnspan=2, sticky="w", pady=(0, 8))

        actions = tk.Frame(frame)
        actions.grid(row=3, column=0, columnspan=2, sticky="e")
        tk.Button(actions, text="Substituir próximo", command=self.replace_next).pack(side=tk.LEFT, padx=3)
        tk.Button(actions, text="Substituir tudo", command=self.replace_all).pack(side=tk.LEFT, padx=3)
        tk.Button(actions, text="Fechar", command=self._close_replace_dialog).pack(side=tk.LEFT, padx=3)

        self.replace_window.protocol("WM_DELETE_WINDOW", self._close_replace_dialog)
        return "break"

    def _close_replace_dialog(self) -> None:
        if self.replace_window and self.replace_window.winfo_exists():
            self.replace_window.destroy()
        self.replace_window = None

    def replace_next(self) -> None:
        tab = self._get_current_tab()
        if not tab:
            return

        text = tab["text"]
        find_term = self.replace_find_var.get()
        replace_term = self.replace_with_var.get()
        if not find_term:
            messagebox.showinfo("Localizar e substituir", "Informe o texto para localizar.")
            return

        tab["last_search"] = find_term
        start_index = text.index("insert")
        case_sensitive = self.replace_case_sensitive_var.get()
        pos = text.search(find_term, start_index, stopindex=tk.END, nocase=not case_sensitive)
        if not pos:
            pos = text.search(find_term, "1.0", stopindex=tk.END, nocase=not case_sensitive)
            if not pos:
                messagebox.showinfo("Localizar e substituir", "Nenhuma ocorrência encontrada.")
                return

        end = f"{pos}+{len(find_term)}c"
        text.delete(pos, end)
        text.insert(pos, replace_term)
        new_end = f"{pos}+{len(replace_term)}c"
        text.mark_set("insert", new_end)
        text.tag_remove("sel", "1.0", tk.END)
        text.tag_add("sel", pos, new_end)
        text.see(pos)

        self._refresh_editor()
        self._highlight_search_matches(find_term)
        self._update_current_tab_label()

    def replace_all(self) -> None:
        tab = self._get_current_tab()
        if not tab:
            return

        text = tab["text"]
        find_term = self.replace_find_var.get()
        replace_term = self.replace_with_var.get()
        if not find_term:
            messagebox.showinfo("Localizar e substituir", "Informe o texto para localizar.")
            return

        case_sensitive = self.replace_case_sensitive_var.get()
        start = "1.0"
        count = 0

        while True:
            pos = text.search(find_term, start, stopindex=tk.END, nocase=not case_sensitive)
            if not pos:
                break

            end = f"{pos}+{len(find_term)}c"
            text.delete(pos, end)
            text.insert(pos, replace_term)
            start = f"{pos}+{len(replace_term)}c"
            count += 1

            if count % self.replace_yield_every == 0:
                self.root.update_idletasks()

        if count == 0:
            messagebox.showinfo("Localizar e substituir", "Nenhuma ocorrência encontrada.")
            return
        tab["last_search"] = find_term

        self._refresh_editor()
        self._highlight_search_matches(find_term)
        self._update_current_tab_label()
        messagebox.showinfo("Localizar e substituir", f"{count} ocorrência(s) substituída(s).")

    def _open_file_in_new_tab(self, file_path: str) -> None:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
        except OSError as exc:
            messagebox.showerror("Erro", f"Não foi possível abrir o arquivo.\n{exc}")
            return

        self._create_tab(content=content, file_path=file_path)
        tab = self._get_current_tab()
        if tab:
            tab["text"].edit_modified(False)
            self._update_current_tab_label()

    def new_file(self) -> None:
        self._create_tab()

    def open_file(self) -> None:
        file_path = filedialog.askopenfilename(
            title="Abrir arquivo",
            filetypes=[
                (
                    "Arquivos comuns",
                    "*.txt *.py *.c *.h *.cpp *.hpp *.cs *.java *.go *.rs *.kt *.kts *.swift "
                    "*.php *.rb *.lua *.html *.htm *.js *.sql *.sh *.bash *.zsh *.ps1 *.psm1 *.psd1 *.bat *.cmd",
                ),
                ("Todos os arquivos", "*.*"),
            ],
        )
        if file_path:
            self._open_file_in_new_tab(file_path)

    def save_file(self) -> bool:
        tab = self._get_current_tab()
        if not tab:
            return False

        if tab["file_path"] is None:
            return self.save_file_as()

        try:
            with open(tab["file_path"], "w", encoding="utf-8") as file:
                file.write(tab["text"].get("1.0", "end-1c"))
        except OSError as exc:
            messagebox.showerror("Erro", f"Não foi possível salvar o arquivo.\n{exc}")
            return False

        tab["text"].edit_modified(False)
        self._update_current_tab_label()
        return True

    def save_file_as(self) -> bool:
        tab = self._get_current_tab()
        if not tab:
            return False

        file_path = filedialog.asksaveasfilename(
            title="Salvar como",
            defaultextension=".txt",
            filetypes=[
                (
                    "Arquivos comuns",
                    "*.txt *.py *.c *.h *.cpp *.hpp *.cs *.java *.go *.rs *.kt *.kts *.swift "
                    "*.php *.rb *.lua *.html *.htm *.js *.sql *.sh *.bash *.zsh *.ps1 *.psm1 *.psd1 *.bat *.cmd",
                ),
                ("Todos os arquivos", "*.*"),
            ],
        )
        if not file_path:
            return False

        tab["file_path"] = file_path
        return self.save_file()

    def close_current_tab(self) -> str:
        tab = self._get_current_tab()
        if not tab:
            return "break"

        if not self._confirm_discard_changes():
            return "break"

        tab_id = self.notebook.select()
        self.notebook.forget(tab["frame"])
        self.tabs.pop(tab_id, None)

        if not self.tabs:
            self._create_tab()

        self._set_title()
        self._refresh_editor()
        return "break"

    def exit_app(self) -> None:
        for tab_id in list(self.notebook.tabs()):
            if tab_id not in self.tabs:
                continue
            self.notebook.select(tab_id)
            if not self._confirm_discard_changes():
                return
        self.root.destroy()



def main() -> None:
    root = tk.Tk()
    NotepadWithLineNumbers(root)
    root.mainloop()


if __name__ == "__main__":
    main()
