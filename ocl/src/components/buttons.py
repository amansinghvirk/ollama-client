from dash import html, dcc
import dash_bootstrap_components as dbc


def app_buttons(btn_id, btn_text, class_name="app-button", style={}):
    buttons = dbc.Button(
        btn_text, id=btn_id, n_clicks=0, className=class_name, style=style
    )

    return buttons


def app_inputs(
    input_id, input_placeholder, input_type="text", class_name="app-input", style={}
):
    """
    Create an input component for the application.

    Parameters:
    - input_id (str): The ID of the input component.
    - input_placeholder (str): The placeholder text for the input component.
    - input_type (str, optional): The type of the input component. Defaults to "text".
    - class_name (str, optional): The CSS class name for the input component. Defaults to "app-input".
    - style (dict, optional): The CSS styles for the input component. Defaults to an empty dictionary.

    Returns:
    - dcc.Input: The input component.

    """
    input = dcc.Input(
        id=input_id,
        type=input_type,
        placeholder=input_placeholder,
        debounce=True,
        className=class_name,
        style=style,
    )

    return input
