""" Latex labels for Graphviz """
import html
import re
import subprocess
from pylatexenc.latex2text import (
    LatexNodes2Text,
    MacroTextSpec,
    get_default_latex_context_db as get_default_l2t_context_db,
)
from pylatexenc.latexwalker import (
    LatexMacroNode,
    LatexEnvironmentNode,
    LatexWalker,
    get_default_latex_context_db as get_default_walker_context_db,
)
from pylatexenc.macrospec import EnvironmentSpec, MacroSpec

BLACKBOARD_MAP = {"Z": "ℤ", "N": "ℕ", "C": "ℂ", "R": "ℝ", "Q": "ℚ"}


def custom_mathbb(node, l2tobj):
    """ foobar """
    arg_nodes = getattr(
        node.nodeargd, "argnlist", getattr(node.nodeargd, "argnodelist", [])
    )
    arg = l2tobj.nodelist_to_text(arg_nodes)
    return BLACKBOARD_MAP.get(arg, arg)

def custom_frac(node, l2tobj):
    """Converts \frac{num}{den} into a Graphviz HTML Table fraction."""
    arg_nodes = getattr(
        node.nodeargd, "argnlist", getattr(node.nodeargd, "argnodelist", [])
    )
    if len(arg_nodes) < 2:
        return ""

    num_text = l2tobj.nodelist_to_text([arg_nodes[0]])
    den_text = l2tobj.nodelist_to_text([arg_nodes[1]])

    return (
        f"@@@FRACSTART@@@"
        f'<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0" CELLPADDING="1">'
        f'<TR><TD ALIGN="CENTER" CELLPADDING="1">{num_text}</TD></TR>'
        f'<TR><TD BGCOLOR="black" HEIGHT="1"></TD></TR>'
        f'<TR><TD ALIGN="CENTER" CELLPADDING="4">{den_text}</TD></TR>'
        f"</TABLE>"
        f"@@@FRACEND@@@"
    )

EXTRA_WALKER_MACROS = [
    MacroSpec("frac", "{{"),
    MacroSpec("left", "{"),
    MacroSpec("right", "{"),
    MacroSpec("textbf", "{"),
    MacroSpec("cong"),
    MacroSpec("mathbb", "{"),
    MacroSpec("text", "{"),
    MacroSpec("longrightarrow"),
    MacroSpec("Longrightarrow"),
    MacroSpec("iff"),
    MacroSpec("implies"),
    MacroSpec("sim"),
    MacroSpec("approx"),
    MacroSpec("equiv"),
    MacroSpec("lcm"),
    MacroSpec("lbr"),
    MacroSpec("bar", "{"),
    MacroSpec("vspace", "{"),
    MacroSpec("ord"),
    MacroSpec("gcd"),
    MacroSpec("mod"),
    MacroSpec("eq"),
    MacroSpec("neq"),
    MacroSpec("blitza"),
    MacroSpec("triangle"),
    MacroSpec("square"),
    MacroSpec("neg"),
]

walker_ctx = get_default_walker_context_db()
walker_ctx.add_context_category(
    "math-extra", macros=EXTRA_WALKER_MACROS, prepend=True
)
walker_ctx.add_context_category(
    "env-extra", environments=[EnvironmentSpec("cases")], prepend=True
)

l2t_ctx = get_default_l2t_context_db()
l2t_ctx.add_context_category(
    "math-extra-override",
    macros=[
        MacroTextSpec("frac", custom_frac),
        MacroTextSpec("left", '@@@BIGDELIMSTART@@@%(1)s@@@BIGDELIMEND@@@'),
        MacroTextSpec("right", '@@@BIGDELIMSTART@@@%(1)s@@@BIGDELIMEND@@@'),
        MacroTextSpec("textbf", "@@@BOLDSTART@@@%(1)s@@@BOLDEND@@@"),
        MacroTextSpec("cong", " ≅ "),
        MacroTextSpec("mathbb", custom_mathbb),
        MacroTextSpec("text", "%(1)s"),
        MacroTextSpec("vert", "|"),
        MacroTextSpec("longrightarrow", "⟶"),
        MacroTextSpec("Longrightarrow", "⟹"),
        MacroTextSpec("iff", "⇔ "),
        MacroTextSpec("implies", "⇒"),
        MacroTextSpec("sim", "~"),
        MacroTextSpec("approx", "≈"),
        MacroTextSpec("equiv", "≡"),
        MacroTextSpec("Z", "ℤ"),
        MacroTextSpec("N", "ℕ"),
        MacroTextSpec("lcm", "lcm"),
        MacroTextSpec("lbr", "@@@BRLEFT@@@"),
        MacroTextSpec("bar", "@@@BARSTART@@@%(1)s@@@BAREND@@@"),
        MacroTextSpec("vspace", "@@@VSPACESTART@@@%(1)s@@@VSPACEEND@@@"),
        MacroTextSpec("ord", "ord"),
        MacroTextSpec("gcd", "gcd"),
        MacroTextSpec("mod", "mod"),
        MacroTextSpec("eq", "="),
        MacroTextSpec("neq", "≠"),
        MacroTextSpec("blitza", "↯"),
        MacroTextSpec("triangle", "△"),
        MacroTextSpec("square", "□"),
        MacroTextSpec("neg", "¬"),
    ],
    prepend=True,
)


def preprocess_sub_super_scripts(text):
    """Replaces superscripts/subscripts with safe placeholder tags free of underscores."""
    text = re.sub(r"\^\{([^}]+)\}", r"@@@SUPSTART@@@\1@@@SUPEND@@@", text)
    text = re.sub(
        r"\^([a-zA-Z0-9\+\-]|\\iota)", r"@@@SUPSTART@@@\1@@@SUPEND@@@", text
    )
    text = re.sub(r"_\{([^}]+)\}", r"@@@SUBSTART@@@\1@@@SUBEND@@@", text)
    text = re.sub(r"_([a-zA-Z0-9\+\-])", r"@@@SUBSTART@@@\1@@@SUBEND@@@", text)
    return text


def format_right_delim_with_sup(match):
    delim = match.group(1)
    sup_text = match.group(2)
    # Renders parenthesis in large font with superscript exponent attached cleanly
    return f'<FONT POINT-SIZE="18">{delim}</FONT><SUP>{sup_text}</SUP>'

def postprocess_html_tags(text):
    """Converts safe tokens to valid Graphviz HTML labels."""
    text = re.sub(
        r"@@@VSPACESTART@@@(\d+)@@@VSPACEEND@@@",
        r'<BR ALIGN="LEFT"/><FONT POINT-SIZE="\1">&nbsp;</FONT><BR ALIGN="LEFT"/>',
        text,
    )

    # Strip escaping on fraction table structures created by custom_frac
    text = text.replace("&lt;TABLE", "<TABLE").replace("&lt;/TABLE&gt;", "</TABLE>")
    text = text.replace("&lt;TR&gt;", "<TR>").replace("&lt;/TR&gt;", "</TR>")
    text = text.replace("&lt;TD", "<TD").replace("&lt;/TD&gt;", "</TD>")
    text = text.replace('&quot;', '"').replace("&gt;", ">")

    # 1. Match right delimiters followed by superscripts BEFORE replacing @@@SUPSTART@@@
    text = re.sub(
        r"@@@BIGDELIMSTART@@@(.*?)@@@BIGDELIMEND@@@\s*@@@SUPSTART@@@(.*?)\s*@@@SUPEND@@@",
        format_right_delim_with_sup,
        text,
    )

    # 2. Replace all remaining tags
    return (
        text.replace("@@@BOLDSTART@@@", "<B>")
        .replace("@@@BOLDEND@@@", "</B>")
        .replace("@@@SUPSTART@@@", "<SUP>")
        .replace("@@@SUPEND@@@", "</SUP>")
        .replace("@@@SUBSTART@@@", "<SUB>")
        .replace("@@@SUBEND@@@", "</SUB>")
        .replace("@@@BRLEFT@@@", '<BR ALIGN="LEFT"/>')
        .replace("@@@BARSTART@@@", "<O>")
        .replace("@@@BAREND@@@", "</O>")
        .replace("@@@FRACSTART@@@", "")
        .replace("@@@FRACEND@@@", "")
        .replace("@@@BIGDELIMSTART@@@", '<FONT POINT-SIZE="18">')
        .replace("@@@BIGDELIMEND@@@", "</FONT>")
    )

def find_unknown_macro(node, ctx):
    """ foobar """
    if node is None:
        return None
    if isinstance(node, LatexMacroNode):
        if ctx.get_macro_spec(node.macroname) is None:
            return node
        if hasattr(node, "nodeargd") and node.nodeargd:
            arg_list = getattr(
                node.nodeargd,
                "argnlist",
                getattr(node.nodeargd, "argnodelist", []),
            )
            for child in arg_list:
                err_node = find_unknown_macro(child, ctx)
                if err_node:
                    return err_node
    elif hasattr(node, "nodelist") and node.nodelist:
        for child in node.nodelist:
            err_node = find_unknown_macro(child, ctx)
            if err_node:
                return err_node
    return None


def process_cases_environment(env_node, converter, full_latex_str):
    """ foobar """
    rows = [[]]
    for child in env_node.nodelist:
        if isinstance(child, LatexMacroNode) and child.macroname == "\\":
            rows.append([])
        else:
            rows[-1].append(child)

    table_rows = []
    num_rows = len([r for r in rows if r])

    for row_nodes in rows:
        if not row_nodes:
            continue

        first_pos = row_nodes[0].pos
        last_node = row_nodes[-1]
        last_pos = last_node.pos + last_node.len

        row_str = full_latex_str[first_pos:last_pos]

        if "&" in row_str:
            expr_str, cond_str = row_str.split("&", 1)
        else:
            expr_str, cond_str = row_str, ""

        w_expr = LatexWalker(expr_str, latex_context=walker_ctx)
        n_expr, _, _ = w_expr.get_latex_nodes()
        expr = converter.nodelist_to_text(n_expr).strip()

        w_cond = LatexWalker(cond_str, latex_context=walker_ctx)
        n_cond, _, _ = w_cond.get_latex_nodes()
        cond = converter.nodelist_to_text(n_cond).strip()

        expr = postprocess_html_tags(html.escape(expr))
        cond = postprocess_html_tags(html.escape(cond))

        if len(table_rows) == 0:
            table_rows.append(
                f"<TR>"
                f'<TD ROWSPAN="{num_rows}" VALIGN="MIDDLE" ALIGN="RIGHT" BORDER="0">'
                f'<FONT POINT-SIZE="22">&#123;</FONT></TD>'
                f'<TD ALIGN="LEFT" VALIGN="MIDDLE" BORDER="0">{expr}</TD>'
                f'<TD ALIGN="LEFT" VALIGN="MIDDLE" BORDER="0">&nbsp;&nbsp;&nbsp;&nbsp;{cond}</TD>'
                f"</TR>"
            )
        else:
            table_rows.append(
                f"<TR>"
                f'<TD ALIGN="LEFT" VALIGN="MIDDLE" BORDER="0">{expr}</TD>'
                f'<TD ALIGN="LEFT" VALIGN="MIDDLE" BORDER="0">&nbsp;&nbsp;&nbsp;&nbsp;{cond}</TD>'
                f"</TR>"
            )

    return (
        '<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0" CELLPADDING="1">'
        + "".join(table_rows)
        + "</TABLE>"
    )


import html
import re


def latex_to_graphviz_html(latex_str):
    """Converts a LaTeX label string to Graphviz HTML-like label syntax."""
    latex_str = preprocess_sub_super_scripts(latex_str)

    walker = LatexWalker(latex_str, latex_context=walker_ctx)
    nodes, _, _ = walker.get_latex_nodes()

    for node in nodes:
        missing_node = find_unknown_macro(node, l2t_ctx)
        if missing_node:
            raise ValueError(f"Unknown macro \\{missing_node.macroname}")

    converter = LatexNodes2Text(latex_context=l2t_ctx)

    if r"\begin{cases}" in latex_str:
        for node in nodes:
            if (
                isinstance(node, LatexEnvironmentNode)
                and node.environmentname == "cases"
            ):
                cases_table = process_cases_environment(
                    node, converter, latex_str
                )

                prefix_str = latex_str[: node.pos]
                suffix_str = latex_str[node.pos + node.len :]

                if r"\\" in prefix_str:
                    lines = prefix_str.split(r"\\")
                    line1_html = latex_to_graphviz_html(lines[0])[1:-1]
                    line2_html = latex_to_graphviz_html(lines[1])[1:-1]
                    suffix_html = latex_to_graphviz_html(suffix_str)[1:-1]

                    full_html = (
                        '<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0" CELLPADDING="0">'
                        f'<TR><TD BORDER="0" ALIGN="LEFT" COLSPAN="2">{line1_html}</TD></TR>'
                        f'<TR><TD BORDER="0" VALIGN="MIDDLE" ALIGN="LEFT">{line2_html}</TD>'
                        f'<TD BORDER="0" VALIGN="MIDDLE" ALIGN="LEFT">{cases_table}</TD>'
                        f'<TD BORDER="0" VALIGN="MIDDLE" ALIGN="LEFT">{suffix_html}</TD></TR>'
                        "</TABLE>"
                    )
                    return f"<{full_html}>"

                prefix_html = latex_to_graphviz_html(prefix_str)[1:-1]
                suffix_html = latex_to_graphviz_html(suffix_str)[1:-1]

                full_html = (
                    '<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0" CELLPADDING="0"><TR>'
                    f'<TD BORDER="0" VALIGN="MIDDLE">{prefix_html}</TD>'
                    f'<TD BORDER="0" VALIGN="MIDDLE">{cases_table}</TD>'
                    f'<TD BORDER="0" VALIGN="MIDDLE">{suffix_html}</TD>'
                    "</TR></TABLE>"
                )
                return f"<{full_html}>"

    plain_text = converter.nodelist_to_text(nodes)
    escaped_text = html.escape(plain_text)

    # Convert placeholders to Graphviz HTML tags for standard nodes
    html_label_body = postprocess_html_tags(escaped_text)

    # Standardize all line break variations into <ROWBREAK/>
    html_label_body = (
        html_label_body.replace("\\\\", "<ROWBREAK/>")
        .replace("@@@BRLEFT@@@", "<ROWBREAK/>")
        .replace("\n", "<ROWBREAK/>")
        .replace("<BR/>", "<ROWBREAK/>")
    )

    # Process multi-line labels or labels containing inner fraction <TABLE> blocks
    if "<ROWBREAK/>" in html_label_body or (
        "<TABLE" in html_label_body
        and not (html_label_body.startswith("<TABLE") and html_label_body.endswith("</TABLE>"))
    ):
        lines = html_label_body.split("<ROWBREAK/>")
        row_tables = []

        for line in lines:
            if not line.strip():
                continue

            # Split line into alternating non-table text and <TABLE> blocks
            tokens = re.split(r"(<TABLE.*?</TABLE>)", line, flags=re.DOTALL)

            cells = []
            for token in tokens:
                if not token:
                    continue
                if token.startswith("<TABLE"):
                    cells.append(f'<TD VALIGN="MIDDLE" ALIGN="CENTER">{token}</TD>')
                else:
                    match = re.match(
                        r"^(.*?)(<FONT POINT-SIZE=\"\d+\">[^\w\s]</FONT>|<FONT POINT-SIZE=\"\d+\">\)</FONT>|\))<SUP>(.*?)</SUP>(.*)$",
                        token,
                        re.DOTALL,
                    )
                    if match:
                        prefix, delim, sup_val, suffix = match.groups()
                        if prefix:
                            cells.append(f'<TD VALIGN="MIDDLE" ALIGN="LEFT">{prefix}</TD>')

                        cells.append(f'<TD VALIGN="MIDDLE" ALIGN="CENTER">{delim}</TD>')
                        cells.append(f'<TD VALIGN="TOP" ALIGN="LEFT"><FONT POINT-SIZE="10">{sup_val}</FONT></TD>')

                        if suffix:
                            cells.append(f'<TD VALIGN="MIDDLE" ALIGN="LEFT">{suffix}</TD>')
                    else:
                        cells.append(f'<TD VALIGN="MIDDLE" ALIGN="LEFT">{token}</TD>')

            # Wrap each line in an independent nested TABLE to isolate column alignments
            line_table = (
                '<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0" CELLPADDING="0" ALIGN="LEFT">'
                f"<TR>{''.join(cells)}</TR>"
                "</TABLE>"
            )
            row_tables.append(f'<TR><TD ALIGN="LEFT">{line_table}</TD></TR>')

        html_label_body = (
            '<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0" CELLPADDING="0" ALIGN="LEFT">'
            + "".join(row_tables)
            + "</TABLE>"
        )

    return f"<{html_label_body}>"



edge_label = latex_to_graphviz_html(
    r""" 1.1 sol \cdot\ z^2/y^6, \blitza:"""
    r"""\\ 0\neq\left(\frac{x^2z}{y^3}\right)^2"""
    r"""=\left(\frac{z^2}{y^2}\right)^3- \frac{z^2}{y^2}"""
)

edge_label2 = latex_to_graphviz_html(
    r""" a=d, b=0, c=-d, \begin{cases}"""
    r""" f:B_d\to C_d\\g:C_d\to B_d\end{cases}"""
)

edge_label3 = latex_to_graphviz_html(
    r""" \begin{cases}(i)&\implies A_d \neq \emptyset\\"""
    r""" (ii)&\implies B_d \neq \emptyset\\"""
    r""" (iii)&\implies C_d \neq \emptyset\end{cases}"""
)

edge_label4 = latex_to_graphviz_html(
    r""" \begin{cases}"""
    r""" i:A_d\to B_d\\j:B_d\to A_d\end{cases}"""
)

edge_label5 = latex_to_graphviz_html(
    r"""\neg(i)\\d=1"""
)

edge_label6 = latex_to_graphviz_html(
    r"""\neg(iii)\\d=1"""
)

edge_label7 = latex_to_graphviz_html(
    r""" a=1, b=0, c=-1"""
)

edge_label8 = latex_to_graphviz_html(
    r""" (x,y) on elliptic curve\\"""
    r""" \implies\ (\frac{-1}{x},\frac{y}{x^2}) on as well,\\"""
    r""" H(x)=H(-1/x)"""
)

prop_0_13_label = latex_to_graphviz_html(
    r"""\textbf{Prop 0.13 } The area of a right \triangle\\whose sides are integers is not a \square"""
)

prop_1_1_label = latex_to_graphviz_html(
    r"""\textbf{Prop 1.1 } \nexists\ solution (x,y,z) to\vspace{3}"""
    r"""x^4+y^4=z^4 satisfying xyz\neq 0"""
)
def_mul_label = latex_to_graphviz_html(
    r"""\textbf{Def *} Elliptic curve over \mathbb{Q} is equation of form:\vspace{3}"""
    r"""y^2=ax^3+bx^2+cx+d (a,b,c,d\in Q, a\neq 0)\\"""
    r"""where RHS polynomial has no multiple root"""
)

prop_1_2_label = latex_to_graphviz_html(
    r"""\textbf{Prop 1.2 } The only rational solutions\vspace{3}"""
    r"""to y^2=x^3-x are (x,y)=(0,0) and (\pm 1,0)"""
)

lem_1_3_label = latex_to_graphviz_html(
    r"""\textbf{Lem 1.3 } d\in\mathbb{Q}, these are equivalent:\lbr"""
    r"""(i) \exists\ rational number sides \textbf{right }\triangle\ of area d\vspace{3}"""
    r"""(ii) \exists\ 3 \square{{}}s of rational numbers that form\lbr"""
    r""" arithmetic progression of difference d\vspace{3}"""
    r"""(iii) \exists\ rational solution to y^2=x^3-d^2x\lbr"""
    r""" other than (x,y)=(0,0) and (\pm d,0)"""
)

lem_1_4_label = latex_to_graphviz_html(
    r"""\textbf{Lem 1.4} For d\in \mathbb{Q} define:\vspace{3}"""
    r""" A_d=\{(x,y,z)\in \mathbb{Q}\times\mathbb{Q}\times\mathbb{Q}\vert x^2+y^2=z^2,½xy=d\}\vspace{3}"""
    r""" B_d=\{(u,v,w)\in \mathbb{Q}\times\mathbb{Q}\times\mathbb{Q}\vert u^2+d=v^2, v^2+d=w^2\}\vspace{3}"""
    r""" C_d=\{(x,y)\in \mathbb{Q}\times\mathbb{Q}\vert y^2=x^3-d^2x, y\neq 0\}.\vspace{3}"""
    r"""\exists\ bijections between any 2 of A_d, B_d, C_d"""
)

_lem_1_4_label = latex_to_graphviz_html(
        r"""i:(x,y,z)\mapsto \left(\frac{y-x}{2},\frac{z}{2},\frac{x+y}{2}\right)
j:(u,v,w)\mapsto (w-u,w+u,2v)\lbr"""
)

lem_1_5_label = latex_to_graphviz_html(
    r"""\textbf{Lem 1.5} For distinct a,b,c\in \mathbb{Q} define B, \tilde{C} and C\vspace{3}"""
    r""" B=\{(u,v,w)\in \mathbb{Q}\times\mathbb{Q}\times\mathbb{Q}\vert u^2+a=v^2+b=w^2+c\}\vspace{3}"""
    r""" \tilde{C}=\{(x,y)\in \mathbb{Q}\times\mathbb{Q}\vert y^2=(x-a)(x-b)(x-c)\}.\vspace{3}"""
    r""" C=\{(x,y)\in \mathbb{Q}\times\mathbb{Q}\vert y^2=(x-a)(x-b)(x-c), y\neq 0\}.\vspace{3}"""
    r"""(1) \exists\ mutually inverse maps f:B\to C, g:C\to B"""
    r"""\vspace{3} f(u,v,w)=(u^2+a+uv+vw+wu, (u+v)(v+w)(w+u),"""
    r"""\\ g(x,y)=\left(\frac{1}{2y}((x-a)^2-(b-a)(c-a)),\ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \\ \ \ \ \  """
    r"""\\ \frac{1}{2y}((x-b)^2-(a-b)(c-b)), \frac{1}{2y}((x-c)^2-(a-c)(b-c))\right)"""
    r"""\\ (2) \exists\ map h:B\to \tilde{C}, h(u,v,w)=(u^2+a,uvw)"""
)

rem_1_6_label = latex_to_graphviz_html(
    r"""\textbf{Rem 1.6 } h\circ g:C\to \tilde{C} is called multiplication-by-2 map\vspace{3}"""
    r""" for elliptic curve y^2=(x-a)(x-b)(x-c); image of h\circ g is\vspace{3}"""
    r""" \{(x,y)\in \mathbb{Q}\times\mathbb{Q}\vert y^2=(x-a)(x-b)(x-c), x-a, x-b, x-c are {\square}s in \mathbb{Q}\}\vspace{10}"""
    r"""because:\lbr"""
    r"""(x',y')=h(u,v,w) \implies\ x'=u^2+a \implies\ x'-a is \square\ in \mathbb{Q}\vspace{3}"""
    r"""from definition of B (image of g): u^2+a=v^2+b=w^2+c\lbr"""
    r""" x'-b =(v^2+b)-b=v^2 is {\square}\ in \mathbb{Q}\lbr"""
    r""" x'-c =(w^2+c)-c=w^2 is {\square}\ in \mathbb{Q}\lbr"""
)

def_height_label = latex_to_graphviz_html(
    r"""\textbf{Def } For a=\frac{m}{n} with m,n\in \mathbb{N}, (m,n)=1\\"""
    r""" define height H(a):=max(\vert m\vert, \vert n\vert)"""
)

i_label  = latex_to_graphviz_html(
    r"""\textbf{(i) } Let (x_0,y_0) on y^2=x^3-x with y_0\neq 0\vspace{3}"""
    r""" and minimal H(x_0); assume 1<x_0"""
)

ii_label = latex_to_graphviz_html(
    r"""\textbf{(ii) } x_0-1, x_0 and x_0+1 are all squares\\"""
    r""" \implies\ \exists (x_1,y_1)\in C: h\circ g(x_1,y_1)=(x_0,y_0)"""
)

iii_label = latex_to_graphviz_html(
    r"""\textbf{(iii) } H(x_1)<H(x_0), \blitza"""
)

dot_content = f"""digraph G {{
    layout=dot;
    overlap="false";
    sep="+15";
    node [shape=box, fontsize=12, margin="0.15,0.1"];

    labelloc=t
    label="Fermat's last theorem for n=4\n(any field K has been replaced with ℚ)\n\n"

    prop_0_13 [label={prop_0_13_label}];

    prop_1_1 [label={prop_1_1_label}];
    prop_1_2 [label={prop_1_2_label}];
    def_mul [label={def_mul_label}];
    lem_1_3 [label={lem_1_3_label}];
    lem_1_4 [label={lem_1_4_label}];
    _lem_1_4 [label={_lem_1_4_label}];
    lem_1_5 [label={lem_1_5_label}];
    rem_1_6 [label={rem_1_6_label}];
    def_height [label={def_height_label}];
    i [label={i_label}];
    ii [label={ii_label}];
    iii [label={iii_label}];
    join1 [shape=point]
    img [label="" shape=plaintext image="ec.png"]

    {{ rank=same prop_0_13 lem_1_3 prop_1_2 }}
    {{ rank=same lem_1_5 _lem_1_4 }}
    {{ rank=same rem_1_6 join1 }}
    {{ rank=same i img }}

    lem_1_3 -> prop_0_13 [label={edge_label5}]
    prop_0_13 -> lem_1_3 
    def_mul -> lem_1_5 [style=dotted]
    lem_1_3 -> prop_1_2 [label={edge_label6}]
    prop_1_2 -> lem_1_3 
    lem_1_5 -> lem_1_4 [label={edge_label2}]
    lem_1_4 -> lem_1_3 [label={edge_label3}]
    lem_1_5 -> rem_1_6 

    _lem_1_4 -> lem_1_4 [label={edge_label4}];
    _lem_1_4 -> lem_1_5 [style=invis];
    prop_1_2 -> prop_1_1 [label={edge_label}]

    def_height -> i [label={edge_label8} style=dotted]
    rem_1_6 -> join1 [label={edge_label7}]
    i -> join1 -> ii -> iii
    img -> i [style=invis]
}}"""

DOTFILENAME = "graph_unicode.dot"
with open(DOTFILENAME, "w", encoding="utf-8") as f:
    f.write(dot_content)

print("Generated .dot file:\n")
print(dot_content)

subprocess.run(
    ["dot", "-Tpdf", DOTFILENAME, "-o", "Fermat_seminar.pdf"], check=True
)
