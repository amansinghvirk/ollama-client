from dash import html, dcc
import dash_bootstrap_components as dbc


def app_navbar():
    """
    Creates and returns the navbar component for the Ollama Chatbot application.

    Returns:
        navbar (dbc.Row): The navbar component.
    """
    navbar = dbc.Row(
        [
            dbc.Col(
                [html.H2("Ollama Chatbot")],
                className="glass-backdark",
                style={"height": "50px", "margin-left": "20px", "margin-right": "20px"},
            )
        ]
    )

    return navbar
