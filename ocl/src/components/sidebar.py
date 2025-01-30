from dash import html, dcc
import dash_bootstrap_components as dbc
from src.server.ollama import get_ollama_models
from src.components.dialog_models import app_settings_model_dlg, app_create_model_dlg, app_save_chat_dlg
from src.components.buttons import app_buttons


def app_sidebar():
    """
    Generate the sidebar component for the Ollama application.

    Returns:
        dbc.Col: The generated sidebar component.
    """
    sidebar = dbc.Col(
        [
            dbc.Row([], style={"height": "10px"}),
            dbc.Row(
                [
                    html.P(
                        "Ollama models", className="app-labels", style={"width": "8rem"}
                    )
                ],
                style={"margin-left": "18px"},
            ),
            dbc.Row(
                [
                    dcc.Dropdown(
                        id="dropdown-ollama-list",
                        options=get_ollama_models(),
                        className="app-dropdown",
                        style={"margin-left": "4px"},
                    )
                ],
                style={"height": "30px"},
            ),
            dbc.Row([], style={"height": "15px"}),
            dbc.Row(
                [
                    html.Div(
                        [
                            app_buttons(
                                "settings-model-dlg-open",
                                "Settings",
                                style={"width": "9rem"},
                            ),
                            app_settings_model_dlg(),
                        ]
                    )
                ],
                style={"height": "30px", "margin-left": "0px"},
            ),
            dbc.Row([], style={"height": "15px"}),
            dbc.Row(
                [
                    html.Div(
                        [
                            app_buttons(
                                "create-model-dlg-open",
                                "Create Model",
                                style={"width": "9rem"},
                            ),
                            app_create_model_dlg(),
                        ]
                    )
                ],
                style={"height": "30px", "margin-left": "0px"},
            ),
            dbc.Row([], style={"height": "15px"}),
            dbc.Row(
                [
                    html.Div(
                        [
                            app_buttons(
                                "create-chat-dlg-open",
                                "New Chat",
                                style={"width": "9rem"},
                            ),
                            app_save_chat_dlg(),
                        ]
                    )
                ],
                style={"height": "30px", "margin-left": "0px"},
            )

        ],
        width=2,
        className="glass-backdark-sidebar",
        style={"height": "500px"},
    )

    return sidebar
