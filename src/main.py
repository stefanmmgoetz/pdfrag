#!/usr/bin/env python

from nicegui import ui, app
from pathlib import Path
import asyncio
import query_pdfs
import logging
import os

app.native.window_args['text_select'] = True

def display_spinner():
    with ui.row():
        ui.image(
            'https://emoji.slack-edge.com/T029PC1PHFX/thinking-spin/b0b51b7b20ec84d5.gif'
        ).classes('w-16')
        ui.label('Thinking...')

def display_message(payload, c_size):
    with ui.chat_message(
        name='PDFRAG',
        stamp=f'Context size: {c_size}',
        avatar='https://emoji.slack-edge.com/T029PC1PHFX/cowboy_fish/b2aafc7878421216.png'
    ).classes('w-full border flex-grow').style('font-size: 20px').props('bg-color=orange-2'):
        with ui.column():
            ui.markdown('### Query')
            ui.label(payload['query'])
        with ui.column():
            ui.markdown('### Response')
            ui.label(payload['response'])
        with ui.column():
            ui.markdown('### Sources')
            for n in range(len(payload['srctext'])):
                with ui.row():
                    # Add the PDF to static files (if local)
                    pdfpath = app.add_static_file(
                        local_file=payload['pdfpath'][n]
                    )
                    # Create a link to the PDF
                    ui.link(
                        payload['srcindex'][n] + ' ' + Path(payload['pdfpath'][n]).name,
                        pdfpath, new_tab=True
                    )
                    ui.label(payload['srctext'][n])

def refresh_chat(c_size, loading=False):
    global l_responses, messages
    messages.clear()
    with messages:
        if loading: display_spinner()
        for response in l_responses:
            display_message(response, c_size)

async def display_response(q, c_size):
    global l_responses
    # loading spinner (such bloat, but it makes the program feel more responsive lol)
    refresh_chat(c_size, loading=True)
    # taking care of the API request
    loop = asyncio.get_running_loop()
    res = await loop.run_in_executor(None, lambda: query_pdfs.main(q, c_size, interactive=False))
    l_responses.insert(0, res)
    refresh_chat(c_size)
    
def warmup():
    query_pdfs.global_init('..')

async def upload_documents():
    with ui.row() as spinboi:
        ui.spinner()
        ui.label('Uploading new documents...')
    loop = asyncio.get_running_loop()
    exit_code = await loop.run_in_executor(
        None, lambda: os.system('../scripts/upload_pdfs.sh')
    )
    logging.info('Refreshing vector database...')
    query_pdfs.global_init('..')
    spinboi.clear()


def main():
    ui.add_head_html('<style>.q-textarea.flex-grow .q-field__control { height: 100% }</style>')  # 2
    with prompt:
        user_query = ui.textarea(
            label='User Prompt',
            placeholder='Ask any question from your folder of PDFs.'
        ).classes('w-full border flex-grow').style('font-size: 20px')
        # user_query.on(
        #     'keydown.enter',
        #     lambda e: display_response(user_query.value, int(context_size.value))
        # )
        context_size = ui.number(
            label='Context size',
            value=50
        ).style('font-size: 20px')
        # context_size.on(
        #     'keydown.enter',
        #     lambda e: display_response(user_query.value, int(context_size.value))
        # )
        ui.button(
            'Upload Documents',
            on_click=upload_documents
        )
        ui.button(
            'Run query!',
            on_click=lambda: display_response(user_query.value, int(context_size.value))
        )
    ui.run(
        native=True,
        reload=False,
        title='PDFRAG'
    )

l_responses = []
prompt = ui.column().classes('w-full h-full')
messages = ui.column().classes('w-full h-full')
logging.getLogger().setLevel(logging.INFO)
logging.info('Warming up...')
app.on_startup(warmup)
logging.info('Starting program!')
main()
