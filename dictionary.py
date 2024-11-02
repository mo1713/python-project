import requests
from nicegui import ui

class DictionaryApp:
    def __init__(self):
        self.api_url = "https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        self.albums = {}  # Store flashcard albums
        self.setup_ui()

    def get_word_info(self, word):
        result = requests.get(self.api_url.format(word=word))
        return result.json()

    def search_word(self):
        word = self.input_word.value.strip()
        
        # Clear previous results
        if hasattr(self, 'result_container'):
            self.result_container.clear()
        
        with self.result_container:
            if not word:
                ui.label('Please enter a word to search').classes('text-red-500')
                return

            try:
                with ui.spinner('circle').classes('text-blue-500'):
                    data = self.get_word_info(word)
                
                if isinstance(data, list) and len(data) > 0:
                    word_data = data[0]
                    phonetic = word_data.get('phonetic', 'No phonetic available')
                    meanings = word_data.get('meanings', [])

                    # Word and Phonetic
                    with ui.card().classes('w-full'):
                        with ui.row().classes('items-center gap-4'):
                            ui.label(word).classes('text-2xl font-bold')
                            ui.label(phonetic).classes('text-gray-500')

                    # Meanings
                    with ui.card().classes('w-full mt-4'):
                        for i, meaning in enumerate(meanings):
                            part_of_speech = meaning.get('partOfSpeech', '')
                            definitions = meaning.get('definitions', [])
                            
                            # Add separator if not the first meaning
                            if i > 0:
                                ui.separator().classes('my-4')
                            
                            ui.label(part_of_speech.capitalize()).classes('text-lg font-semibold mb-2')
                            
                            for j, definition in enumerate(definitions, 1):
                                with ui.row().classes('ml-4 mb-2'):
                                    ui.label(f"{j}.").classes('mr-2')
                                    with ui.column().classes('gap-1'):
                                        ui.label(definition.get('definition', '')).classes('text-gray-700')
                                        if example := definition.get('example'):
                                            ui.label(f"Example: {example}").classes('text-gray-500 text-sm ml-4')

                    # Flashcard Creation Card
                    with ui.card().classes('w-full mt-4 p-4'):
                        ui.label('Create Flashcard Album').classes('text-lg font-semibold mb-2')
                        
                        # Album creation section
                        with ui.row().classes('w-full gap-2 mb-4'):
                            self.new_album_input = ui.input(label='New Flashcard Album Name') \
                                .classes('flex-grow')
                            ui.button('Create', 
                                     on_click=lambda: self.create_album(self.new_album_input.value)) \
                                .props('rounded').classes('bg-indigo text-white')
                        
                        # Add to existing album section
                        with ui.row().classes('w-full gap-2 items-center'):
                            if self.albums:
                                self.album_select = ui.select(
                                    options=list(self.albums.keys()),
                                    label='Select Existing Flashcard Album'
                                ).classes('flex-grow')
                                
                                ui.button('Add to Flashcard Album', 
                                        on_click=lambda: self.add_to_flashcard(word_data)) \
                                    .props('rounded').classes('bg-indigo text-white')
                            else:
                                ui.label('Create an flashcard album above to add flashcards') \
                                    .classes('text-gray-500')

                else:
                    ui.label(f"No information found for word: '{word}'") \
                        .classes('text-red-500')

            except Exception as e:
                ui.label(f"Error: {str(e)}").classes('text-red-500')

    def add_to_flashcard(self, word_data):
        if not hasattr(self, 'album_select') or not self.album_select.value:
            ui.notify("Please select an flashcard album before adding a word", type='warning')
            return
        
        album_name = self.album_select.value
        word = word_data['word']
        definitions = []
        for meaning in word_data.get('meanings', []):
            for definition in meaning.get('definitions', []):
                definitions.append({
                    'definition': definition.get('definition', ''),
                    'example': definition.get('example', ''),
                    'part_of_speech': meaning.get('partOfSpeech', '')
                })
        
        if album_name not in self.albums:
            self.albums[album_name] = []
            
        # Check if word already exists in the album
        if any(card['word'] == word for card in self.albums[album_name]):
            ui.notify(f"'{word}' already exists in flashcard album '{album_name}'", type='warning')
            return
            
        self.albums[album_name].append({
            "word": word,
            "definitions": definitions,
            "phonetic": word_data.get('phonetic', '')
        })
        
        ui.notify(f"Added '{word}' to fashcard album '{album_name}'", type='success')

    def create_album(self, album_name):
        album_name = album_name.strip()
        if not album_name:
            ui.notify("Please enter an flashcard album name", type='warning')
            return
            
        if album_name in self.albums:
            ui.notify("Flashcard album already exists", type='warning')
            return
            
        self.albums[album_name] = []
        self.update_album_selects()
        self.new_album_input.value = ''  # Clear the input
        ui.notify(f"Created new flashcard album: {album_name}", type='success')

    def update_album_selects(self):
        if hasattr(self, 'album_select'):
            self.album_select.options = list(self.albums.keys())
            self.album_select.update()
    
    def setup_ui(self):
        # Style the body
        ui.query('body').style('background: linear-gradient(135deg, #f0f4ff, #e5e7ff)')

        with ui.row().classes('width: 144%; height: 80px; padding: 20px;'):
            with ui.card().classes('w-full max-w-3xl'):
                ui.icon('school').classes('text-3xl text-indigo-600')
                ui.label('DICTIONARY').classes('text-2xl font-bold text-indigo-600')
                
                # Search section
                with ui.row().classes('w-full gap-2 items-center'):
                    self.input_word = ui.input(label='Search word') \
                        .classes('flex-grow')
                    self.input_word.on('keypress.enter', self.search_word)
                    
                    ui.button('Search', on_click=self.search_word) \
                        .props('rounded').classes('bg-indigo text-white')
                
                # Results container
                self.result_container = ui.column().classes('w-full mt-4 gap-4')

def main():
    app = DictionaryApp()
    ui.run(title='Dictionary', favicon='🎓')

if __name__ in {"__main__", "__mp_main__"}:
    main()