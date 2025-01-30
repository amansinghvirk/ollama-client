from dash import html, dcc
import dash_bootstrap_components as dbc


def format_session_response(system_response):
    """
    Formats the system response for a chat session.

    Args:
        system_response (str): The system's response to the user.

    Returns:
        html.P: A formatted response block containing an image and the system's response.
    """
    llm_response_blocks = html.P(
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Img(
                            src="assets/images/agent1333.png",
                            style={"height": "40px", "width": "40px"},
                        )
                    ],
                    width=1,
                    style={"width": "50px"},
                ),
                dbc.Col([dcc.Markdown(system_response)], width=11),
            ]
        ),
        style={"color": "#f7f440", "text-align": "left"},
    )

    return llm_response_blocks


def get_session_chat(session_chat, skip_user=False):
    """
    Generate HTML representation of session chat.

    Args:
        session_chat (dict): The session chat data.

    Returns:
        html.P: HTML paragraph element containing the chat messages.
    """

    chat_message = []
    for chat in session_chat["chat-history"]:

        user_input = chat.get("User")
        llm_response = chat.get("Agent")

        if (user_input.strip() != '') and (user_input[:14] != 'Instruction:::'):
            user_input_blocks = dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Img(
                                src="assets/images/user.png",
                                style={"height": "40px", "width": "40px"},
                            )
                        ],
                        width=1,
                        style={"width": "50px"},
                    ),
                    dbc.Col([dcc.Markdown(user_input)], width=11),
                ]
            )
            chat_message.append(
                html.P(
                    children=user_input_blocks,
                    style={"color": "#68f7e6", "text-align": "left"},
                )
            )

        llm_response_blocks = dbc.Row(
            [
                dbc.Col(
                    [
                        html.Img(
                            src="assets/images/agent1333.png",
                            style={"height": "40px", "width": "40px"},
                        )
                    ],
                    width=1,
                    style={"width": "50px"},
                ),
                dbc.Col([dcc.Markdown(llm_response)], width=11),
            ]
        )


        chat_message.append(
            html.P(
                children=llm_response_blocks,
                style={"color": "#f7f440", "text-align": "left"},
            )
        )

    return html.P(chat_message)

