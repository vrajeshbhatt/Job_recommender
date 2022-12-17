from pathlib import Path
import uuid
import os

import dash_uploader as du
import dash
from dash import html
from dash.dependencies import Input, Output, State


# # Configure Dash to recognize the URL of the container
# user = os.environ.get("DOMINO_PROJECT_OWNER")
# project = os.environ.get("DOMINO_PROJECT_NAME")
# runid = os.environ.get("DOMINO_RUN_ID")
# runurl = '/' + user + '/' + project + '/r/notebookSession/'+ runid + '/'

app = dash.Dash()


# UPLOAD_FOLDER_ROOT = r"/mnt/dash"
du.configure_upload(app, 'upload_files')

def get_upload_component(id):
    return du.Upload(
    id=id,
    max_file_size=1800, # 1800 Mb
    filetypes=['csv', 'zip','pdf'],
    upload_id=uuid.uuid1(), # Unique session id
)


# get_app_layout is a function
# This way we can use unique session id's as upload_id's
app.layout = html.Div(
[
    html.H1('Demo'),    
    html.Div(
    [
    get_upload_component(id='dash-uploader'),
    html.Div(id='callback-output'),
    ],
style={ # wrapper div style
'textAlign': 'center',
'width': '600px',
'padding': '10px',
'display': 'inline-block'
}),
],
style={
'textAlign': 'center',
},
)


@du.callback(
output=Output('callback-output', 'children'),
id='dash-uploader',
)
def get_a_list(filenames):
    return html.Ul([html.Li(filenames)])


if __name__ == '__main__':
    app.run_server(debug=True)