from nicegui import ui
from typing import List, Dict

def create_intro_page():
    nav_items: List[Dict] = [
        {"name": "Home", "url": "/", "icon": "home"},
        {"name": "Explore", "url": "/explore", "icon": "explore"},
        {"name": "Help", "url": "/help", "icon": "help"}
    ]

    features = [
        {
            "title": "Effective Learning",
            "description": "The SKT legacy has been reignited and T1'll be your 2023 World Champions",
            "icon": "school"
        },
        {
            "title": "Create Activities",
            "description": "They say Busan was Church of Chovy, but what's God to 5 non believers",
            "icon": "groups"
        },
        {
            "title": "Fun Flashcards",
            "description": "It is not LPL versus LCK, it's T1 versus the LPL and I like those odds",
            "icon": "library_books"
        }
    ]

    # Set page background and styles
    ui.query('body').style(
        '''
        background: linear-gradient(135deg, #f0f4ff, #e5e7ff);
        margin: 0;
        padding: 0;
        min-height: 100vh;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        '''
    )

    # Header
    with ui.header().classes('w-full').style('background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(10px);'):
        with ui.row().classes('w-full max-w-7xl mx-auto justify-between items-center p-4'):
            # Logo section
            with ui.row().classes('items-center gap-2'):
                ui.icon('auto_stories').classes('text-3xl text-indigo-600')
                ui.label('MYMY').classes('text-2xl font-bold text-indigo-600')
            
            # Navigation
            with ui.row().classes('space-x-6'):
                for item in nav_items:
                    with ui.row().classes('items-center gap-2 cursor-pointer hover:text-indigo-600 transition-colors duration-200 '):
                        ui.icon(item['icon']).classes('text-indigo-600')
                        ui.link(item['name'], item['url']).classes(
                            'text-gray-700 hover:text-indigo-600 transition-colors duration-200'
                        )
            
            # Call to action button
            #ui.button('Get Started', on_click=lambda: ui.notify('Welcome to MYMY!')).classes(
            #    'bg-indigo text-white hover:bg-indigo-700 px-6'
            #)

    # Hero Section
    with ui.column().classes('max-w-7xl mx-auto px-4 pt-24 pb-16'):
        with ui.column().classes('items-center text-center gap-6'):
            ui.label("We Do Not Just Teach, We Inspire").classes('text-5xl font-bold text-gray-900')
            ui.label(
                'We always make our student satisfy by providing as many convenient as possible'
            ).classes('text-xl text-gray-600 max-w-2xl')
            
            with ui.row().classes('gap-4'):
                ui.button('Log in', on_click=lambda: ui.notify('Starting your learning journey!')).props('rounded').classes(
                    'bg-indigo text-white hover:bg-indigo-700 px-8 py-2'
                )
                ui.button('Sign up', on_click=lambda: ui.notify('Welcome to MYMY!')).props('rounded').classes(
                    'bg-indigo text-white hover:bg-indigo-700 px-8 py-2'
                )

    # Features Section
    with ui.column().classes('max-w-7xl mx-auto px-4 py-16'):
        with ui.grid().classes('grid-cols-1 md:grid-cols-3 gap-8'):
            for feature in features:
                with ui.card().classes('p-6 hover:shadow-lg transition-shadow duration-200'):
                    with ui.column().classes('items-center text-center gap-4'):
                        with ui.element('div').classes('p-3 bg-indigo-50 rounded-lg'):
                            ui.icon(feature['icon']).classes('text-3xl text-indigo-600')
                        ui.label(feature['title']).classes('text-xl font-semibold text-gray-900')
                        ui.label(feature['description']).classes('text-gray-600')

    # Footer
    with ui.footer().classes('w-full bg-white mt-16 py-8'):
        with ui.row().classes('w-full max-w-7xl mx-auto justify-between items-center px-4'):
            ui.label('© 2024 MYMY Learning Platform').classes('text-gray-600')
            #with ui.row().classes('gap-4'):
            #    for item in nav_items:
            #        ui.link(item['name'], item['url']).classes('text-gray-600 hover:text-indigo-600')

if __name__ in {"__main__", "__mp_main__"}:
    create_intro_page()
    ui.run(title='MYMY Learning Platform', favicon='🎓')

