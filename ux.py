import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import Dash, html, Input, Output, State, callback, dcc
from langchain import OpenAI, ConversationChain
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts.prompt import PromptTemplate
from langchain.embeddings import HuggingFaceEmbeddings

from langchain import FAISS

import base64
from io import BytesIO

# third party
from PIL import Image
from dash import html


def image(path, enc_format="png", **kwargs):
    """
    Converts a PIL (Python Image Library) Image into base64 string for HTML displaying
    :param im: PIL Image object
    :param enc_format: The image format for displaying. If saved the image will have that extension.
    :return: base64 encoding
    """
    image = Image.open(path)
    buff = BytesIO()
    image.save(buff, format=enc_format, **kwargs)
    encoded = base64.b64encode(buff.getvalue()).decode("utf-8")
    return html.Img(
        className="image", src="data:image/png;base64, " + encoded, **kwargs
    )

prompts_list = ["What lessons can we learn from other projects working in ...",
                "Can you give me examples of ...",
                "Can you summarise the lessons from ..."]

external_js = [
    "https://code.jquery.com/jquery-3.4.1.slim.min.js",
    "https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js",
    "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js",
]
lato_font = "https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,100;0,300;0,400;0,700;0,900;1,100;1,300;1,400;1,700;1,900"


chat = OpenAI(temperature=0)   # level of randomness or creativity


template = """I want you to act as an international development artificial intelligence adviser who provides advice to international development professionals. If it isn't clear what characteristics you should looking for to find the most useful documents, I want you to ask the international development professional a series of questions to clarify what they are looking for, for example, location, topic, size of project, budget. Keep asking questions until you are confident you know what characteristics you are looking for. When you return information, include references to where you have obtained this information. All your answers should adhere to the civil service code.
{history}
Human: {input}
AI Assistant:"""

PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)


# model_name = "sentence-transformers/all-mpnet-base-v2"
# hf = HuggingFaceEmbeddings(model_name=model_name)
# db = FAISS.load_local("faiss_index", hf)
# retriever = db.as_retriever(search_kwargs={"k": 4, "fetch_k": 8})


conversation = ConversationChain(prompt=PROMPT,
# conversation = ConversationalRetrievalChain(prompt=PROMPT,
    llm=chat, 
    verbose=True,
    memory=ConversationBufferMemory(),
)


app = Dash(__name__,
           external_stylesheets=[dbc.themes.FLATLY, lato_font],
           external_scripts=external_js,)


app.layout = html.Div([
    html.Div([
              dmc.Title(children=[image("logo.png", **{"width": "65px",
                                                            "height": "60px"}),

                                  "  AI'd Chatbot  ",
                                  image("ukaid.jpeg", enc_format="jpeg", **{"width": "60px",
                                                            "height": "60px"}),])                                  
                                  ],style={'textAlign': 'center',
                                                          "padding": "10px"}),
                                        
        html.Br(),

        dbc.Container(
                    fluid=True,
                    children=[
                        dbc.Row(
                            [
                                dbc.Col(
                                    width=1,
                                ),
                                dbc.Col(
                                    width=10,
                                    children=dbc.Card(
                                        [
                                            dbc.CardHeader(children=[dcc.Markdown("""**Note:** This chatbot is a prototype and is not intended to be used for any official purposes. 
                                            The chatbot is trained on a small sample of publicly available documents and, although some effort has been made to prevent hallucinations, we cannot guarantee the accuracy of the produced content.""")]),
                                            dbc.CardBody([
                                                html.Br(),
                                                html.Div([
                                                dbc.Button(id="prompt_1_button", children=prompts_list[0], value=prompts_list[0]),
                                                dbc.Button(id="prompt_2_button", children=prompts_list[1], value=prompts_list[1]),
                                                dbc.Button(id="prompt_3_button", children=prompts_list[2], value=prompts_list[2]),

                                                ], style={'textAlign': 'center',
                                                          "align-content":"space-between", "width":"100%"}),
                                                html.Br(),
                                                html.Br(),
                                                dbc.InputGroup([
                                                    dbc.Input(id='prompt', value="", placeholder='Your prompt ...', type='text'),
                                                    dbc.Button(id='sendPrompt', children=">", color="success", n_clicks=0),
                                                    ],
                                                ),
                                                html.Br(),
                                                html.P(id='outputHuman', children=""),
                                                html.P(id='outputChatBot', children=""),
                                            ], style={"width":"100%"}),
                                        ],style={"width":"100%"},
                                    )
                                ),
                                dbc.Col(
                                    width=1,
                                ),
                            ]
                        )
                    ]
                ),

    ]
)

@callback(Output(component_id='prompt', component_property='value'),
          Output("prompt_1_button", "n_clicks"),
          Output("prompt_2_button", "n_clicks"),
          Output("prompt_3_button", "n_clicks"),
          Input("prompt_1_button", "n_clicks"),
          State("prompt_1_button", "value"),
          Input("prompt_2_button", "n_clicks"),
          State("prompt_2_button", "value"),
        Input("prompt_3_button", "n_clicks"),
          State("prompt_3_button", "value"),
          prevent_initial_call=True)
def update_prompt(clicks1, value1, clicks2, value2, clicks3, value3):  
    if clicks1>0:
        return value1.strip(), 0, 0, 0
    if clicks2>0:
        return value2.strip(), 0, 0, 0
    if clicks3>0:
        return value3.strip(), 0, 0, 0



@callback(
    Output(component_id='outputHuman', component_property='children'),
    Output(component_id='outputChatBot', component_property='children'),
    Input(component_id='sendPrompt', component_property='n_clicks'),
    State(component_id='prompt', component_property='value')
)
def call_openai_api(n, human_prompt):
    if n==0:
        return "", ""
    else:
        result_ai = conversation.predict(input=human_prompt)

        human_output = f"Human: {human_prompt}"
        chatbot_output = f"ChatBot: {result_ai}"

        return human_output, chatbot_output

if __name__ == '__main__':
    app.run_server(debug=True)