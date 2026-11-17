
from diagrams import Diagram, Edge
from diagrams.generic.blank import Blank
from html import escape

def create_node(
    title,
    subtitle="",
    background="#FFFFFF",
    title_size=20,
    subtitle_size=14,
    title_color="#111111",
    subtitle_color="#666666",
    title_bold=True,
    subtitle_bold=False,
    alignment="CENTER",
    width="3.0",
    height="1.5",
):
    """
    Create a Graphviz node with rich text formatting.
    """

    title = escape(title)
    subtitle = escape(subtitle)

    title_format = (
        f'<B>{title}</B>' if title_bold else title
    )

    subtitle_format = (
        f'<B>{subtitle}</B>' if subtitle_bold else subtitle
    )

    html_label = f'''<
        <TABLE BORDER="0"
            CELLBORDER="0"
            CELLSPACING="0"
            CELLPADDING="4">
            <TR>
                <TD ALIGN="CENTER" VALIGN="MIDDLE">
                    <FONT FACE="Arial"
                        POINT-SIZE="{title_size}"
                        COLOR="{title_color}">
                        <B>{title}</B>
                    </FONT>
                </TD>
            </TR>
            <TR>
                <TD ALIGN="CENTER" VALIGN="MIDDLE">
                    <FONT FACE="Arial"
                        POINT-SIZE="{subtitle_size}"
                        COLOR="{subtitle_color}">
                        {subtitle}
                    </FONT>
                </TD>
            </TR>
        </TABLE>
    >'''

    return Blank(
        html_label,
        fillcolor=background,
        width=width,
        height=height,
        shape="box",
        style="rounded,filled",
        color="#DDDDDD",
        penwidth="1.5",
        margin="0.10,0.10",
        labelloc="c",
        labeljust="c",
        fixedsize="true",
)


# --------------------------------------------------
# GitHub Actions CI Pipeline
# --------------------------------------------------

with Diagram(
    "",
    filename="playwright_ci_pipeline",
    outformat="png",
    show=False,
    direction="TB",
    graph_attr={
        "bgcolor": "#FFFFFF",
        "pad": "0.25",
        "nodesep": "0.20",
        "ranksep": "0.65",
        "splines": "ortho",
        "fontname": "Arial",
    },
    edge_attr={
        "color": "#666666",
        "penwidth": "1.8",
        "arrowsize": "0.8",
    },
):

    arrow = Edge(color="#666666", penwidth="1.8")

    # 1. GitHub Actions
    github_actions = create_node(
        title="GitHub Actions CI Pipeline",
        subtitle="Checkout -> Install -> Execute pytest",
        background="#E8EFFC",
        title_size=20,
        subtitle_size=14,
        width="9.0",
        height="1.1",
    )

    # 2. Playwright + pytest
    playwright = create_node(
        title="Playwright + pytest",
        subtitle="Web UI / API / BDD test execution",
        background="#FFFFFF",
        title_size=20,
        subtitle_size=14,
        width="9.0",
        height="1.1",
    )

    github_actions >> arrow >> playwright

    # 3. Parallel report generation
    junit_xml = create_node(
        title="JUnit XML",
        subtitle="GitHub Checks",
        background="#E8F5EA",
        title_size=20,
        subtitle_size=14,
    )

    html_report = create_node(
        title="HTML Report",
        subtitle="pytest-html",
        background="#E8EFFC",
        title_size=20,
        subtitle_size=14,
    )


    trace_zip = create_node(
        title="Trace ZIP",
        subtitle="Debug failures",
        background="#F3E8FA",
        title_size=20,
        subtitle_size=14,
    )

    playwright >> arrow >> [
        junit_xml,
        html_report,
        trace_zip,
    ]

    # 4. TestRail integration
    testrail = create_node(
        title="TestRail Integration",
        subtitle="Update test execution results and link automated test cases",
        background="#E8F5EA",
        title_size=20,
        subtitle_size=14,
        width="9.0",
        height="1.1",
    )

    [
        junit_xml,
        html_report,
        trace_zip,
    ] >> arrow >> testrail


print("Architecture diagram generated successfully!")
