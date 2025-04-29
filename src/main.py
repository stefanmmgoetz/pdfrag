#!/usr/bin/env python

from nicegui import ui, context
import query_pdfs

dud = query_pdfs.main('..', 50, 'What is the purpose of life?')


# def run_user_query(q):
#     ui.chat_message(
#         query_pdfs.main('..', 50, user_query.value),
#         name='Robot', stamp='now',
#         avatar='https://robohash.org/ui'
#     )

def display_response(response):
    ui.chat_message(
            response,
            name='Robot', stamp='now',
            avatar='https://robohash.org/ui'
    )

#ui.textarea().classes('w-full').on('keydown.enter', _enter)

# context.get_client().content.classes('h-[100vh]')  # 1
ui.add_head_html('<style>.q-textarea.flex-grow .q-field__control { height: 100% }</style>')  # 2
user_query = ui.textarea(
    label='Text', placeholder='start typing'
).classes('w-full border flex-grow')
ui.button(
    'Run query!',
    on_click=lambda: display_response(
        query_pdfs.main('..', 50, user_query.value)
    )
)
ui.run(native=True)
