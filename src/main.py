#!/usr/bin/env python

from nicegui import ui, app
import asyncio
import query_pdfs
import logging

app.native.window_args['text_select'] = True

async def display_response(q, c_size):
    global l_responses, messages
    loop = asyncio.get_running_loop()
    res = await loop.run_in_executor(None, lambda: query_pdfs.main(q, c_size))
    l_responses.insert(0, res)
    messages.clear()
    with messages:
        ui.chat_message(
                l_responses,
                name='Robot', stamp='now',
                avatar='https://robohash.org/ui'
        ).classes('w-full border flex-grow').style('font-size: 20px')

def warmup():
    query_pdfs.global_init('..')
    query_pdfs.main('What is the meaning of life?', 50)

def main():
    ui.add_head_html('<style>.q-textarea.flex-grow .q-field__control { height: 100% }</style>')  # 2
    with prompt:
        user_query = ui.textarea(
            label='User Prompt', placeholder='ask any question from your folder of PDFs'
        ).classes('w-full border flex-grow')
        context_size = ui.number(label='Context size', value=50)
        ui.button(
            'Run query!',
            on_click=lambda: display_response(user_query.value, int(context_size.value))
            
        )
    ui.run(native=True, reload=False)

l_responses = []
prompt = ui.column().classes('w-full h-full')
messages = ui.column().classes('w-full h-full')
logging.getLogger().setLevel(logging.INFO)
logging.info('Warming up...')
app.on_startup(warmup)
logging.info('Starting program!')
main()
