from dash import Dash, Input, Output, ctx, html
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from src.utilities.config import get_chat_history_list, load_chat

from src.server.ollama import (
    get_llm_response,
    get_ollama_models,
    get_llm_system_response,
    pull_ollama_model,
    create_ollama_model,
    delete_ollama_model,
    save_hostname,
)
from src.server.langchain_ollama import get_langchain_llm_response, get_session_chat_title
from src.utilities.config import get_hostname, save_chat_history
from src.processing.chat import get_session_chat, format_session_response


def get_callbacks(app):
    """
    Returns the callbacks for the given app.

    Parameters:
    - app: The Dash app object.

    Returns:
    - A list of callbacks.

    """

    @app.callback(
        Output("chat-output", "children"),
        Output("chat-session", "data"),
        Output("user-input", "value"),
        [Input("dropdown-ollama-list", "value"), 
         Input("btn-user-chat", "n_clicks"),
         Input("btn-create-new-chat", "n_clicks"),
         Input("btn-load-chat", "n_clicks")],
        State("user-input", "value"),
        State("chat-session", "data"),
        State("dropdown-saved-chats", "value"),
        prevent_initial_call=True
    )
    def get_system_message(sel_model, chat_click, newchat_click, loadchat_click, user_input, data, chat_list):
        return get_system_message_callback(sel_model, chat_click, newchat_click, loadchat_click, user_input, data, chat_list)

    @app.callback(
        Output("add-model-message", "children"),
        Output("add-hostname-message", "children"),
        Output("create-model-message", "children"),
        Output("dropdown-ollama-list", "options"),
        Output("dropdown-ollama-list-delete", "options"),
        Input("add-model", "value"),
        Input("add-hostname", "value"),
        Input("btn-delete-model", "n_clicks"),
        Input("btn-create-model", "n_clicks"),
        State("dropdown-ollama-list-delete", "value"),
        State("create-model-name", "value"),
        State("create-base-model", "value"),
        State("create-model-temperature", "value"),
        State("create-modelfile", "value"),
        prevent_initial_call=True,
    )
    def configuration(
        model_name,
        ollama_server_path,
        delete_n_click,
        create_n_click,
        model_to_delete,
        create_model_name,
        base_model,
        model_temperature,
        modelfile,
    ):
        return configuration_callback(
            model_name,
            ollama_server_path,
            delete_n_click,
            create_n_click,
            model_to_delete,
            create_model_name,
            base_model,
            model_temperature,
            modelfile,
        )

    @app.callback(
        Output("add-modal-card", "is_open"),
        Output("add-hostname", "value"),
        [Input("settings-model-dlg-open", "n_clicks")],
        [State("add-modal-card", "is_open")],
    )
    def toggle_modal(n1, is_open):
        hostserver = get_hostname()
        if n1:
            return not is_open, hostserver
        return is_open, hostserver

    @app.callback(
        Output("create-modal-card", "is_open"),
        [Input("create-model-dlg-open", "n_clicks")],
        [State("create-modal-card", "is_open")],
    )
    def toggle_create_modal(n1, is_open):
        if n1:
            return not is_open
        return is_open
    
    @app.callback(
        Output("save-chat-message", "children"),
        Output("dropdown-saved-chats", "options"),
        [Input("btn-save-chat", "n_clicks")],
        State("current-chat-title", "value"),
        State("chat-session", "data"),
        State("dropdown-ollama-list", "value")
    )
    def save_current_chat_to_file(n_click, chat_filename, memory_data, model):
        if n_click:
            if save_chat_history(model, memory_data, chat_filename):
                return "Chat saved!", get_chat_history_list()
            return "Chat not saved!", get_chat_history_list()
        return "", get_chat_history_list()
    
    @app.callback(
        Output("save-chat-card", "is_open"),
        Output("current-chat-title", "value"),
        [Input("create-chat-dlg-open", "n_clicks")],
        State("save-chat-card", "is_open"),
        State("dropdown-ollama-list", "value"), 
        State("chat-session", "data")
    )
    def toggle_save_chat_modal(n1, is_open, model, memory_data):
        chat_title = ""
        if n1:
            
            if (model is not None) and (memory_data is not None):
                print(11)
                chat_title = get_session_chat_title(model, memory_data)
            return not is_open, chat_title
        
        print(2)
        if (model is not None) and (memory_data is not None):
            print(21)
            chat_title = get_session_chat_title(model, memory_data)
            print(chat_title)
        return is_open, chat_title


def get_system_message_callback(sel_model, chat_click, newchat_click, loadchat_click, user_input, memory_data, chat_list):
    """
    Callback function to get the system message for the chat window.

    Args:
        sel_model (str): The selected model.
        user_input (str): The user's input message.
        data (dict): The data dictionary containing chat history.

    Returns:
        tuple: A tuple containing the chat window message and updated data dictionary.
    """

    triggered_id = ctx.triggered_id
    print(triggered_id)

    if triggered_id == "dropdown-ollama-list":
        return format_session_response(get_llm_system_response(model=sel_model)), None, ""
    if triggered_id == "btn-create-new-chat":
        if memory_data is not None:
            memory_data = None
        if sel_model is None:
            return "Select a model", None, user_input
        return format_session_response(get_llm_system_response(model=sel_model)), None, ""
    if triggered_id == "btn-load-chat":
        if sel_model is None:
            return "Select a model", None, user_input
        chat_history, chat_title, chat_type, chat_model = load_chat(chat_list)

        if chat_history is not None:
            memory_data = dict()
            memory_data["chat-history"] = chat_history
            memory_data = get_langchain_llm_response(
                model=sel_model, 
                user_message="Instruction::: Sumarize the previous conversation and ask for the user input to proceed further...", 
                memory_data=memory_data
            )
            chat_window_message = get_session_chat(memory_data)

            return chat_window_message, memory_data, ""
        return format_session_response(get_llm_system_response(model=sel_model)), None, ""

    elif triggered_id == "btn-user-chat":
        chat_window_message = ""
        if chat_click:
            if sel_model is None:
                return "Select a model", None, user_input

            if (
                (user_input is None)
                | (user_input == "Enter your message...")
            ):
                return format_session_response(get_llm_system_response(model=sel_model)), None, ""
            
            if memory_data is None:
                memory_data = dict()
                memory_data["chat-history"] = []

            memory_data = get_langchain_llm_response(
                model=sel_model, 
                user_message=user_input, 
                memory_data=memory_data
            )
            chat_window_message = get_session_chat(memory_data)

            return chat_window_message, memory_data, ""
        return chat_window_message, memory_data, ""


def add_model_callback(
    model_name,
    default_message_add_model,
    default_message_add_hostname,
    default_message_create_model,
):
    """
    Callback function for adding a model.

    Args:
        model_name (str): The name of the model.
        default_message_add_model (str): The default message for adding a model.
        default_message_add_hostname (str): The default message for adding a hostname.
        default_message_create_model (str): The default message for creating a model.

    Returns:
        tuple: A tuple containing the following elements:
            - message (str): The message indicating the result of the operation.
            - default_message_add_hostname (str): The default message for adding a hostname.
            - default_message_create_model (str): The default message for creating a model.
            - ollama_models_before (list): The list of Ollama models before the operation.
            - ollama_models_after (list): The list of Ollama models after the operation.
    """
    if (
        (model_name == "Enter name of the model..")
        or (model_name is None)
        or (model_name == "")
    ):
        message = default_message_add_model
        return (
            message,
            default_message_add_hostname,
            default_message_create_model,
            get_ollama_models(),
            get_ollama_models(),
        )

    if pull_ollama_model(model_name):
        message = html.P(
            "Model added to the ollama server.",
            style={"color": "green", "font-size": ".75em"},
        )
        return (
            message,
            default_message_add_hostname,
            default_message_create_model,
            get_ollama_models(),
            get_ollama_models(),
        )

    message = html.P(
        "Model note found in the ollama library.",
        style={"color": "red", "font-size": ".75em"},
    )
    return (
        message,
        default_message_add_hostname,
        default_message_create_model,
        get_ollama_models(),
        get_ollama_models(),
    )


def add_hostname_callback(
    ollama_server_path,
    default_message_add_model,
    default_message_add_hostname,
    default_message_create_model,
):
    """
    Callback function for adding a hostname.

    Args:
        ollama_server_path (str): The path to the Ollama server.
        default_message_add_model (str): The default message for adding a model.
        default_message_add_hostname (str): The default message for adding a hostname.
        default_message_create_model (str): The default message for creating a model.

    Returns:
        tuple: A tuple containing the following elements:
            - default_message_add_model (str): The default message for adding a model.
            - message (str or html.P): The message indicating the result of the operation.
            - default_message_create_model (str): The default message for creating a model.
            - ollama_models_before (list): The list of Ollama models before the operation.
            - ollama_models_after (list): The list of Ollama models after the operation.
    """
    if (
        (ollama_server_path == "Enter ollama server path ...")
        or (ollama_server_path is None)
        or (ollama_server_path == "")
    ):
        message = default_message_add_hostname
        return (
            default_message_add_model,
            message,
            default_message_create_model,
            get_ollama_models(),
            get_ollama_models(),
        )

    if save_hostname(ollama_server_path):
        message = html.P(
            "Connection tested and saved successfully ...",
            style={"color": "green", "font-size": ".75em"},
        )
        return (
            default_message_add_model,
            message,
            default_message_create_model,
            get_ollama_models(),
            get_ollama_models(),
        )

    message = html.P(
        "Server connection failed ...", style={"color": "red", "font-size": ".75em"}
    )
    return (
        default_message_add_model,
        message,
        default_message_create_model,
        get_ollama_models(),
        get_ollama_models(),
    )


def delete_model_callback(
    delete_n_click,
    model_to_delete,
    default_message_add_model,
    default_message_add_hostname,
    default_message_create_model,
):
    """
    Callback function for deleting a model.

    Args:
        delete_n_click (bool): Indicates whether the delete button was clicked.
        model_to_delete (str): The model to be deleted.
        default_message_add_model (str): Default message for adding a model.
        default_message_add_hostname (str): Default message for adding a hostname.
        default_message_create_model (str): Default message for creating a model.

    Returns:
        tuple: A tuple containing the updated default messages, and the updated list of models.
    """
    if delete_n_click:
        if delete_ollama_model(model_to_delete):
            message = html.P(
                "Model deleted successfully ...",
                style={"color": "green", "font-size": ".75em"},
            )
            return (
                default_message_add_model,
                default_message_add_hostname,
                default_message_create_model,
                get_ollama_models(),
                get_ollama_models(),
            )

        message = html.P(
            "Error in model deletion.", style={"color": "red", "font-size": ".75em"}
        )
        return (
            default_message_add_model,
            default_message_add_hostname,
            default_message_create_model,
            get_ollama_models(),
            get_ollama_models(),
        )
    return (
        default_message_add_model,
        default_message_add_hostname,
        default_message_create_model,
        get_ollama_models(),
        get_ollama_models(),
    )


def create_model_callback(
    create_n_click,
    create_model_name,
    base_model,
    model_temperature,
    modelfile,
    default_message_add_model,
    default_message_add_hostname,
    default_message_create_model,
):
    """
    Callback function for creating a model.

    Args:
        create_n_click (bool): Indicates whether the create button was clicked.
        create_model_name (str): The name of the model to be created.
        base_model (str): The base model to use for creating the new model.
        model_temperature (float): The temperature to be used for the new model.
        modelfile (str): The file path of the model file.
        default_message_add_model (str): The default message for adding a model.
        default_message_add_hostname (str): The default message for adding a hostname.
        default_message_create_model (str): The default message for creating a model.

    Returns:
        tuple: A tuple containing the following elements:
            - default_message_add_model (str): The default message for adding a model.
            - default_message_add_hostname (str): The default message for adding a hostname.
            - message (str or html.P): The message indicating the result of the model creation.
            - get_ollama_models (function): A function that returns the list of ollama models.
            - get_ollama_models (function): A function that returns the list of ollama models.
    """
    if create_n_click:
        if (
            (create_model_name == "FROM MODEL ...")
            or (create_model_name is None)
            or (create_model_name == "")
        ):
            message = default_message_create_model
            return (
                default_message_add_model,
                default_message_add_hostname,
                message,
                get_ollama_models(),
                get_ollama_models(),
            )

        model_file = (
            f"FROM {base_model}\n TEMPERATE {model_temperature}\n SYSTEM {modelfile}"
        )

        if create_ollama_model(create_model_name, model_file):
            message = html.P(
                "Model added to the ollama server.",
                style={"color": "green", "font-size": ".75em"},
            )
            return (
                default_message_add_model,
                default_message_add_hostname,
                message,
                get_ollama_models(),
                get_ollama_models(),
            )

        message = html.P("Error in model creation.", style={"color": "red"})
        return (
            default_message_add_model,
            default_message_add_hostname,
            message,
            get_ollama_models(),
            get_ollama_models(),
        )

    message = html.P(
        "Note: Enter the valid modelfile script ...",
        style={"color": "orange", "font-size": ".75em"},
    )
    return (
        default_message_add_model,
        default_message_add_hostname,
        message,
        get_ollama_models(),
        get_ollama_models(),
    )


def configuration_callback(
    model_name,
    ollama_server_path,
    delete_n_click,
    create_n_click,
    model_to_delete,
    create_model_name,
    base_model,
    model_temperature,
    modelfile,
):
    """
    Callback function for handling configuration changes.

    Args:
        model_name (str): The name of the model.
        ollama_server_path (str): The path to the ollama server.
        delete_n_click (int): The number of times the delete button has been clicked.
        create_n_click (int): The number of times the create button has been clicked.
        model_to_delete (str): The name of the model to delete.
        create_model_name (str): The name of the model to create.
        base_model (str): The base model to use for creating a new model.
        model_temperature (float): The temperature value for the model.
        modelfile (str): The script for the model.

    Returns:
        The result of the corresponding callback function based on the triggered_id.

    """
    default_message_add_model = html.P(
        "Note: The model name should be the same as the model name in the ollama library.",
        style={"color": "orange", "font-size": ".75em"},
    )
    default_message_add_hostname = html.P(
        "Note: if ollama server is running locally then update http://localhost:11434 otherwise provide the server path.",
        style={"color": "orange", "font-size": ".75em"},
    )
    default_message_create_model = html.P(
        "Note: Enter the valid modelfile script ...",
        style={"color": "orange", "font-size": ".75em"},
    )

    triggered_id = ctx.triggered_id

    if triggered_id == "add-model":
        return add_model_callback(
            model_name,
            default_message_add_model,
            default_message_add_hostname,
            default_message_create_model,
        )

    elif triggered_id == "add-hostname":
        return add_hostname_callback(
            ollama_server_path,
            default_message_add_model,
            default_message_add_hostname,
            default_message_create_model,
        )

    elif triggered_id == "btn-delete-model":
        return delete_model_callback(
            delete_n_click,
            model_to_delete,
            default_message_add_model,
            default_message_add_hostname,
            default_message_create_model,
        )
    elif triggered_id == "btn-create-model":
        return create_model_callback(
            create_n_click,
            create_model_name,
            base_model,
            model_temperature,
            modelfile,
            default_message_add_model,
            default_message_add_hostname,
            default_message_create_model,
        )
