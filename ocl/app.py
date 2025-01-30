"""
This script initializes and configures a Dash application for the Ollama chat client.
It imports necessary modules and components, sets up the layout, and defines the callbacks.
"""

from dash import Dash, Input, Output, ctx, html, dcc
from dash import html, dcc
import dash_bootstrap_components as dbc
from src.server.ollama import (
    get_llm_response,
    get_ollama_models,
    get_llm_system_response,
    pull_ollama_model,
    create_ollama_model,
    delete_ollama_model,
    save_hostname,
)
from src.utilities.config import get_hostname, setup_chat_history
from src.components import navbar, sidebar
from src.callbacks.app_callbacks import get_callbacks
from src.components.buttons import app_inputs, app_buttons

session_chat = []

app = Dash(
    __name__, title="Ollama chat client", external_stylesheets=[dbc.themes.SOLAR]
)

app_layout = dbc.Container(
    [
        dcc.Store(id="chat-session", storage_type="session"),
        navbar.app_navbar(),
        dbc.Row(
            [
                sidebar.app_sidebar(),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.P(
                                            id="chat-output",
                                            className="card-text",
                                        )
                                    ]
                                ),
                            ],
                            className="app-sessionoutput",
                        ),
                        dbc.Row([
                            dbc.Col([
                                dcc.Textarea(
                                    id="user-input",
                                    value="Enter your message...",
                                    className="app-userinput",
                                )
                            ], width=10),
                            dbc.Col([app_buttons("btn-user-chat", "Chat")], width=2, 
                                    style={"margin-left": "0px","margin-top": "5px", "padding-left": "0px"}),
                        ])
                    ],
                    width=9,
                    className="glass-backdark",
                    style={"height": "500px"},
                ),
            ]
        ),
    ]
)

app.layout = app_layout

setup_chat_history()
get_callbacks(app)


if __name__ == "__main__":
    app.run_server(debug=True)
