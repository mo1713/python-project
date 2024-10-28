from nicegui import ui
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
import json
from pathlib import Path
import logging
from datetime import datetime

class Theme(Enum):
    LIGHT = "light"
    DARK = "dark"

@dataclass
class UserSettings:
    theme: Theme
    notifications_enabled: bool
    sidebar_collapsed: bool

    @classmethod
    def default(cls) -> 'UserSettings':
        return cls(
            theme=Theme.LIGHT,
            notifications_enabled=True,
            sidebar_collapsed=False
        )

class DashboardApp:
    def __init__(self):
        self.settings = UserSettings.default()
        
        # Configuration
        self.menu_items: List[Dict] = [
            {"name": "Dictionary", "icon": "school", "url": "/dictionary", "description": "Look up words and definitions"},
            {"name": "Flashcard", "icon": "style", "url": "/flashcard", "description": "Practice with flashcards"},
            {"name": "Reading", "icon": "menu_book", "url": "/reading", "description": "Read and comprehend texts"},
            {"name": "Dictation", "icon": "record_voice_over", "url": "/dictation", "description": "Practice listening and writing"},
            {"name": "Process", "icon": "insights", "url": "/process", "description": "Track your learning progress"}
        ]

        self.nav_items: List[Dict] = [
            {"name": "Home", "url": "/", "icon": "home"},
            {"name": "Explore", "url": "/explore", "icon": "explore"},
            {"name": "Help", "url": "/help", "icon": "help"}
        ]

    def toggle_theme(self):
        self.settings.theme = Theme.DARK if self.settings.theme == Theme.LIGHT else Theme.LIGHT
        ui.notify(f'Switched to {self.settings.theme.value} theme')

    def toggle_sidebar(self):
        self.settings.sidebar_collapsed = not self.settings.sidebar_collapsed
        ui.notify('Toggled sidebar')
    
    def create_layout(self):
        is_dark = self.settings.theme == Theme.DARK

        # Set up the base container with pastel pink background
        ui.query('body').style('''
            margin: 0; 
            padding: 0; 
            min-height: 100vh; 
            background: linear-gradient(135deg, #FFE5EC, #FFE3ED, #FFD9E4);
        ''')

        # Create the main layout container
        with ui.container().classes('h-screen flex flex-col'):
            # Rest of the layout code remains the same
            self.create_top_nav()
        
            with ui.row().classes('flex-1 flex overflow-hidden'):
                with ui.row().classes(f'{"w-64" if not self.settings.sidebar_collapsed else "w-20"} flex-shrink-0 transition-all duration-300'):
                    self.create_sidebar()
            
                with ui.scroll_area().classes('flex-1'):
                    self.create_main_content()
    def create_sidebar(self):
        is_dark = self.settings.theme == Theme.DARK
    
        with ui.column().classes(f'h-full {"bg-gray-900" if is_dark else "bg-white/70"} border-r border-pink-100'):
            # Menu items
            for item in self.menu_items:
                with ui.link(target=item['url']).classes('block'):
                    with ui.row().classes(
                        f"{'px-4 py-3' if not self.settings.sidebar_collapsed else 'p-3'} " +
                        f"{'hover:bg-pink-50' if not is_dark else 'hover:bg-gray-800'} transition-colors"
                    ):
                        ui.icon(item['icon']).classes('text-xl text-pink-500')
                        if not self.settings.sidebar_collapsed:
                            with ui.column().classes('ml-3'):
                                ui.label(item['name']).classes(
                                    'font-medium ' + ('text-white' if is_dark else 'text-gray-700')
                                )
                                ui.label(item['description']).classes('text-xs text-gray-500')
    def create_top_nav(self):
        is_dark = self.settings.theme == Theme.DARK
    
        with ui.header().classes(f'{"bg-gray-900" if is_dark else "bg-white/70"} border-b border-pink-100 px-4 py-2'):
            with ui.row().classes('w-full items-center justify-between'):
                # Left section
                with ui.row().classes('items-center gap-4'):
                    ui.button(icon='menu', color='grey').props('flat').on('click', self.toggle_sidebar)
                    with ui.row().classes('items-center gap-2'):
                        ui.icon('auto_stories').classes('text-2xl text-pink-500')
                        ui.label('MYMY').classes('text-xl font-bold text-pink-500')
            
                # Center section - navigation
                with ui.row().classes('space-x-6'):
                    for item in self.nav_items:
                        with ui.button(color='pink').props('flat').classes('gap-2'):
                            ui.icon(item['icon'])
                            ui.label(item['name'])
            
                # Right section
                with ui.row().classes('items-center gap-4'):
                    ui.input(placeholder='Search...').props('outlined rounded dense').classes('w-48 bg-white/50')
                    ui.button(icon='notifications', color='pink').props('flat')
                    ui.button(
                        icon='dark_mode' if is_dark else 'light_mode',
                        color='pink'
                    ).props('flat').on('click', self.toggle_theme)
                    ui.avatar('User').style('background: linear-gradient(135deg, #FFB6C1, #FFC0CB);')

    def create_main_content(self):
        is_dark = self.settings.theme == Theme.DARK
    
        with ui.container().classes('p-6 max-w-7xl mx-auto'):
            # Welcome section
            with ui.card().classes('mb-6 w-full bg-white/70').props('flat'):
                with ui.row().classes('items-center justify-between p-6'):
                    with ui.column():
                        ui.label('Welcome back, User!').classes(
                            'text-2xl font-bold ' + ('text-white' if is_dark else 'text-gray-800')
                        )
                        ui.label("Here's what's happening with your learning progress").classes('text-gray-500')
                    ui.button('Start Learning', color='pink').props('rounded')

            # Stats grid
            with ui.row().classes('gap-6 mb-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4'):
                stats = [
                    {'label': 'Words Learned', 'value': '1,234', 'icon': 'school', 'trend': '+12%'},
                    {'label': 'Practice Sessions', 'value': '56', 'icon': 'trending_up', 'trend': '+5%'},
                    {'label': 'Study Streak', 'value': '7 days', 'icon': 'local_fire_department', 'trend': '+2 days'},
                    {'label': 'Time Spent', 'value': '48h', 'icon': 'schedule', 'trend': '+3h'}
                ]
            
                for stat in stats:
                    with ui.card().props('flat').classes('h-full bg-white/70'):
                        with ui.column().classes('p-4'):
                            with ui.row().classes('items-center justify-between mb-2'):
                                ui.label(stat['label']).classes('text-gray-500')
                                ui.icon(stat['icon']).classes('text-pink-500')
                            ui.label(stat['value']).classes(
                                'text-2xl font-bold ' + ('text-white' if is_dark else 'text-gray-800')
                            )
                            with ui.row().classes('items-center gap-1'):
                                ui.icon('arrow_upward').classes('text-green-500 text-sm')
                                ui.label(stat['trend']).classes('text-green-500 text-sm')

            # Activity section
            with ui.card().classes('w-full bg-white/70').props('flat'):
                with ui.column().classes('p-6'):
                    with ui.row().classes('items-center justify-between mb-6'):
                        ui.label('Recent Activity').classes(
                            'text-xl font-bold ' + ('text-white' if is_dark else 'text-gray-800')
                        )
                        ui.button('View All', color='pink').props('flat')

def main():
    app = DashboardApp()
    
    @ui.page('/')
    def index():
        app.create_layout()
    
    @ui.page('/{path}')
    def dynamic_page(path: str = ''):
        app.create_layout()
    
    ui.run(
        title='MYMY Learning Platform',
        favicon='🎓',
        dark=app.settings.theme == Theme.DARK,
        viewport='width=device-width, initial-scale=1.0'
    )

if __name__ in {"__main__", "__mp_main__"}:
    main()