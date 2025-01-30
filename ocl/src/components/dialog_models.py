from dash import html, dcc
import dash_bootstrap_components as dbc
from src.components.buttons import app_buttons, app_inputs
from src.server.ollama import get_ollama_models
from src.utilities.config import get_chat_history_list


def app_settings_model_dlg():
    """
    Creates a modal dialog for application settings.

    Returns:
        dbc.Modal: The modal dialog component.
    """
    settings = dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Configurations")),
            dbc.ModalBody([update_hostname(), pull_model(), delete_model()]),
        ],
        id="add-modal-card",
        is_open=False,
    )

    return settings

def app_save_chat_dlg():
    """
    Creates a modal dialog for application settings.

    Returns:
        dbc.Modal: The modal dialog component.
    """
    save_chat_dlg = dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Do you want to save current chat?")),
            dbc.Row([
                save_chat()
            ]),
            dbc.Row([
                load_chat()
            ]),
            dbc.Row([
                new_chat()
            ]),
            dbc.Row([], style={"height": "30px"})
        ],
        id="save-chat-card",
        is_open=False,
    )

    return save_chat_dlg


def app_create_model_dlg():
    """
    Create and return a modal dialog for creating a model in the ollama server.

    Returns:
        dbc.Modal: The modal dialog component.
    """
    create_model_dlg = dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Create model to ollama server")),
            dbc.ModalBody(
                [
                    app_inputs(
                        input_id="create-model-name",
                        input_placeholder="Enter name of the model..",
                    ),
                    app_inputs(
                        input_id="create-base-model", input_placeholder="FROM MODEL ..."
                    ),
                    app_inputs(
                        input_id="create-model-temperature",
                        input_placeholder="TEMPERATURE ...",
                    ),
                    app_inputs(
                        input_id="create-modelfile",
                        input_placeholder="SYSTEM MESSAGE ...",
                        class_name="app-input-modelfile",
                    ),
                    app_buttons("btn-create-model", "Create"),
                    html.P(
                        id="create-model-message",
                        children=[
                            html.P(
                                "Note: Enter the valid modelfile script ...",
                                style={"color": "orange", "font-size": ".75em"},
                            )
                        ],
                    ),
                ]
            ),
        ],
        id="create-modal-card",
        is_open=False,
    )

    return create_model_dlg

def pull_model():
    """
    Creates a HTML Div element representing the pull model dialog.

    Returns:
        pull_model (html.Div): The pull model dialog.
    """
    pull_model = html.Div(
        [
            dbc.Row(
                [html.P("Ollama model", className="app-labels")],
                style={"margin-left": "2px"},
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            app_inputs(
                                input_id="add-model",
                                input_placeholder="Enter name of the model..",
                                style={"width": "100%"},
                            )
                        ],
                        width=8,
                    ),
                    dbc.Col([app_buttons("btn-pull-model", "Add")], width=2),
                ]
            ),
            dbc.Row(
                [
                    html.P(
                        id="add-model-message",
                        children=[
                            html.P(
                                "Note: The model name should be the same as the model name in the ollama library.",
                                style={"color": "orange", "font-size": ".75em"},
                            )
                        ],
                    )
                ]
            ),
        ]
    )

    return pull_model


def update_hostname():
    """
    Returns a Div element containing the UI components for updating the hostname of the Ollama server.

    Returns:
        dash_html_components.Div: The Div element containing the UI components.
    """
    pull_model = html.Div(
        [
            dbc.Row(
                [
                    html.P(
                        "host address of ollama server",
                        className="app-labels",
                        style={"width": "12rem"},
                    )
                ],
                style={"margin-left": "2px"},
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            app_inputs(
                                input_id="add-hostname",
                                input_placeholder="Enter ollama server path ...",
                                style={"width": "100%"},
                            )
                        ],
                        width=8,
                    ),
                    dbc.Col([app_buttons("btn-hostname", "Save")], width=2),
                ]
            ),
            dbc.Row(
                [
                    html.P(
                        id="add-hostname-message",
                        children=[
                            html.P(
                                "Note: if ollama server is running locally then update http://localhost:11434 otherwise provide the server path.",
                                style={"color": "orange", "font-size": ".75em"},
                            )
                        ],
                    )
                ]
            ),
        ]
    )

    return pull_model


def delete_model():
    """
    Creates a HTML div element representing the delete model section.

    Returns:
        pull_model (html.Div): The HTML div element representing the delete model section.
    """
    pull_model = html.Div(
        [
            dbc.Row(
                [
                    html.P(
                        "Saved ollama models",
                        className="app-labels",
                        style={"width": "15.5rem"},
                    )
                ],
                style={"margin-left": "15px"},
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Dropdown(
                                id="dropdown-ollama-list-delete",
                                options=get_ollama_models(),
                                className="app-dropdown",
                                style={"margin-left": "2px"},
                            )
                        ],
                        width=8,
                    ),
                    dbc.Col([app_buttons("btn-delete-model", "Delete")], width=2),
                ]
            ),
            dbc.Row(
                [
                    html.P(
                        id="delete-model-message",
                        children=[html.P("", style={"color": "grey"})],
                    )
                ]
            ),
        ]
    )

    return pull_model


def load_chat():
    """
    Creates a HTML div element representing the delete model section.

    Returns:
        pull_model (html.Div): The HTML div element representing the delete model section.
    """
    loadchat = html.Div(
        [
            dbc.Row(
                [
                    html.P(
                        "Saved chats",
                        className="app-labels",
                        style={"width": "15.5rem"},
                    )
                ],
                style={"margin-left": "15px"},
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Dropdown(
                                id="dropdown-saved-chats",
                                options=get_chat_history_list(),
                                className="app-dropdown",
                                style={"margin-left": "2px"},
                            )
                        ],
                        width=8,
                    ),
                    dbc.Col([app_buttons("btn-load-chat", "Load Chat")], width=2),
                ]
            )
        ]
    )

    return loadchat

def save_chat():
    """
    Creates a HTML div element representing the delete model section.

    Returns:
        pull_model (html.Div): The HTML div element representing the delete model section.
    """


    savechat = html.Div(
        [
            dbc.Row([
                dbc.Col([
                    app_inputs(
                        input_id="current-chat-title",
                            input_placeholder="...",
                            style={"width": "100%"}
                    )
                ], width=8),
                dbc.Col([
                    app_buttons("btn-save-chat", "Save Chat"),

                ], width=3)
            ]),
            dbc.Row([
                html.P(
                    id="save-chat-message",
                    children=[
                        html.P(
                            "",
                            style={"color": "orange", "font-size": ".75em"},
                        )
                    ]
                )
            ])
        ]
    )

    return savechat


def new_chat():
    """
    Creates a HTML div element representing the delete model section.

    Returns:
        pull_model (html.Div): The HTML div element representing the delete model section.
    """


    savechat = html.Div(
        [
            dbc.Row([], style={"height": "5px"}),
            dbc.Row([
                dbc.Col([

                ], width=8),
                dbc.Col([
                    app_buttons("btn-create-new-chat", "Start Chat")

                ], width=3)
            ])
        ]
    )

    return savechat



