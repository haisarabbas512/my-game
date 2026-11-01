from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image as KivyImage
from kivy.graphics import Color, Rectangle, Line
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
import random
import os

# Set working directory safely
try:
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
except:
    pass

player_name = "King"
selected_snake_color = (1, 0, 0, 1)  # Default Red
selected_food_color = (0, 1, 0, 1)   # Default Green

# Global Background Sound Manager for Windows 1, 2, and Menu (Arabic Rhythm)
bg_sound = None

def play_bg_music():
    global bg_sound
    if not bg_sound:
        bg_sound = SoundLoader.load('freesound_community-arabic-rythm-74123.mp3')
        if not bg_sound:
            bg_sound = SoundLoader.load('freesound_community-arabic-rythm-74123.wav')
    if bg_sound and not bg_sound.state == 'play':
        bg_sound.loop = True
        bg_sound.play()

def stop_bg_music():
    global bg_sound
    if bg_sound:
        bg_sound.stop()

def play_sound(filename):
    s = SoundLoader.load(filename + '.mp3')
    if not s:
        s = SoundLoader.load(filename + '.wav')
    if s:
        s.play()


# 1. Welcome Screen (Window 1)
class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs)
        play_bg_music()
        layout = FloatLayout()
        
        if os.path.exists('Gemini_Generated_Image_pi8ovqpi8ovqpi8o.jpg'):
            bg = KivyImage(source='Gemini_Generated_Image_pi8ovqpi8ovqpi8o.jpg', pos_hint={'x':0, 'y':0.2}, size_hint=(1, 0.8), allow_stretch=True, keep_ratio=False)
            layout.add_widget(bg)
            
        if os.path.exists('1234567890.png'):
            im2 = KivyImage(source='1234567890.png', pos_hint={'x':0.85, 'y':0.4}, size_hint=(0.15, 0.3))
            im3 = KivyImage(source='1234567890.png', pos_hint={'x':0, 'y':0.4}, size_hint=(0.15, 0.3))
            layout.add_widget(im2)
            layout.add_widget(im3)

        bottom_box = BoxLayout(orientation='vertical', pos_hint={'x':0, 'y':0}, size_hint=(1, 0.25), padding=10, spacing=5)
        
        with bottom_box.canvas.before:
            Color(0, 1, 0, 1)
            self.rect = Rectangle(pos=bottom_box.pos, size=bottom_box.size)
        bottom_box.bind(pos=lambda obj, val: setattr(self.rect, 'pos', val),
                        size=lambda obj, val: setattr(self.rect, 'size', val))

        title_lbl = Label(text="WELCOME TO SNAKE GAME", font_size=28, color=(0, 0.35, 0.35, 1), bold=True)
        
        btn_layout = BoxLayout(size_hint=(1, 0.5), spacing=10)
        enter_btn = Button(text="ENTER", size_hint=(0.3, 1), background_color=(0, 0, 1, 1))
        enter_btn.bind(on_press=self.go_to_name)
        
        btn_layout.add_widget(Label(size_hint=(0.7, 1)))
        btn_layout.add_widget(enter_btn)
        
        bottom_box.add_widget(title_lbl)
        bottom_box.add_widget(btn_layout)
        layout.add_widget(bottom_box)
        
        self.add_widget(layout)
        self._keyboard = None

    def on_enter(self):
        play_bg_music()
        from kivy.core.window import Window
        if not self._keyboard:
            self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
            self._keyboard.bind(on_key_down=self._on_key_down)

    def _keyboard_closed(self):
        if self._keyboard:
            try:
                self._keyboard.unbind(on_key_down=self._on_key_down)
            except:
                pass
            self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'enter':
            play_sound('khoamthanh-dam-566913')
            self.go_to_name(None)
            return True
        return False

    def go_to_name(self, instance):
        play_sound('khoamthanh-dam-566913')
        self._keyboard_closed()
        self.manager.current = 'name_screen'


# 2. Name Input & Color Selection Screen (Window 2)
class NameScreen(Screen):
    def __init__(self, **kwargs):
        super(NameScreen, self).__init__(**kwargs)
        play_bg_music()
        layout = FloatLayout()
        
        with layout.canvas.before:
            Color(0.78, 0.78, 0.78, 1)
            self.rect = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda obj, val: setattr(self.rect, 'pos', val),
                    size=lambda obj, val: setattr(self.rect, 'size', val))

        box = BoxLayout(orientation='vertical', size_hint=(0.7, 0.7), pos_hint={'center_x': 0.5, 'center_y': 0.5}, spacing=10)
        
        lbl = Label(text="Enter your Name:", font_size=22, color=(0, 0, 0, 1), size_hint=(1, 0.15))
        self.text_input = TextInput(text="", font_size=25, multiline=False, size_hint=(1, 0.2))
        
        color_lbl = Label(text="Choose Snake Color:", font_size=18, color=(0, 0, 0, 1), size_hint=(1, 0.1))
        
        snake_btn_box = BoxLayout(size_hint=(1, 0.15), spacing=5)
        self.btn_red = Button(text="Red Snake", background_color=(1, 0, 0, 1))
        self.btn_blue = Button(text="Blue Snake", background_color=(0, 0, 1, 1))
        self.btn_yellow = Button(text="Yellow Snake", background_color=(1, 1, 0, 1))
        
        self.btn_red.bind(on_press=lambda x: self.set_snake_color((1, 0, 0, 1)))
        self.btn_blue.bind(on_press=lambda x: self.set_snake_color((0, 0, 1, 1)))
        self.btn_yellow.bind(on_press=lambda x: self.set_snake_color((1, 1, 0, 1)))
        
        snake_btn_box.add_widget(self.btn_red)
        snake_btn_box.add_widget(self.btn_blue)
        snake_btn_box.add_widget(self.btn_yellow)

        food_lbl = Label(text="Choose Food Color:", font_size=18, color=(0, 0, 0, 1), size_hint=(1, 0.1))
        food_btn_box = BoxLayout(size_hint=(1, 0.15), spacing=5)
        self.btn_fgreen = Button(text="Green Food", background_color=(0, 1, 0, 1))
        self.btn_fpurple = Button(text="Purple Food", background_color=(0.5, 0, 0.5, 1))
        
        self.btn_fgreen.bind(on_press=lambda x: self.set_food_color((0, 1, 0, 1)))
        self.btn_fpurple.bind(on_press=lambda x: self.set_food_color((0.5, 0, 0.5, 1)))
        
        food_btn_box.add_widget(self.btn_fgreen)
        food_btn_box.add_widget(self.btn_fpurple)

        submit_btn = Button(text="Press ENTER / Continue", font_size=20, size_hint=(1, 0.2), background_color=(0, 0.5, 1, 1))
        submit_btn.bind(on_press=self.save_name)
        
        box.add_widget(lbl)
        box.add_widget(self.text_input)
        box.add_widget(color_lbl)
        box.add_widget(snake_btn_box)
        box.add_widget(food_lbl)
        box.add_widget(food_btn_box)
        box.add_widget(submit_btn)
        
        layout.add_widget(box)
        self.add_widget(layout)
        self._keyboard = None

    def set_snake_color(self, col):
        play_sound('khoamthanh-dam-566913')
        global selected_snake_color
        selected_snake_color = col

    def set_food_color(self, col):
        play_sound('khoamthanh-dam-566913')
        global selected_food_color
        selected_food_color = col

    def on_enter(self):
        play_bg_music()
        from kivy.core.window import Window
        if not self._keyboard:
            self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
            self._keyboard.bind(on_key_down=self._on_key_down)

    def _keyboard_closed(self):
        if self._keyboard:
            try:
                self._keyboard.unbind(on_key_down=self._on_key_down)
            except:
                pass
            self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'enter':
            play_sound('khoamthanh-dam-566913')
            self.save_name(None)
            return True
        return False

    def save_name(self, instance):
        play_sound('khoamthanh-dam-566913')
        global player_name
        entered = self.text_input.text.strip()
        if entered == "":
            player_name = "King"
        else:
            player_name = entered
        self._keyboard_closed()
        self.manager.current = 'menu_screen'


# 3. Main Menu Screen (Window 3)
class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        play_bg_music()
        layout = FloatLayout()
        
        with layout.canvas.before:
            Color(0, 0, 0, 1)
            self.rect = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda obj, val: setattr(self.rect, 'pos', val),
                    size=lambda obj, val: setattr(self.rect, 'size', val))

        menu_box = BoxLayout(orientation='vertical', size_hint=(0.5, 0.4), pos_hint={'center_x': 0.5, 'center_y': 0.5}, spacing=20, padding=20)
        
        with menu_box.canvas.before:
            Color(1, 1, 1, 1)
            self.box_rect = Rectangle(pos=menu_box.pos, size=menu_box.size)
        menu_box.bind(pos=lambda obj, val: setattr(self.box_rect, 'pos', val),
                      size=lambda obj, val: setattr(self.box_rect, 'size', val))

        if os.path.exists('—Pngtree—snake illustration_14745105.png'):
            icon = KivyImage(source='—Pngtree—snake illustration_14745105.png', size_hint=(None, None), size=(50, 50))
            menu_box.add_widget(icon)
        
        start_btn = Button(text="Start", font_size=25, color=(0, 0, 1, 1), background_color=(0.8, 0.8, 0.8, 1))
        start_btn.bind(on_press=self.start_game)
        
        quit_btn = Button(text="QUIT", font_size=25, color=(1, 0, 0, 1), background_color=(0.8, 0.8, 0.8, 1))
        quit_btn.bind(on_press=self.quit_app)
        
        menu_box.add_widget(start_btn)
        menu_box.add_widget(quit_btn)
        
        layout.add_widget(menu_box)
        self.add_widget(layout)
        self._keyboard = None

    def on_enter(self):
        play_bg_music()
        from kivy.core.window import Window
        if not self._keyboard:
            self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
            self._keyboard.bind(on_key_down=self._on_key_down)

    def _keyboard_closed(self):
        if self._keyboard:
            try:
                self._keyboard.unbind(on_key_down=self._on_key_down)
            except:
                pass
            self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        key_name = keycode[1]
        if key_name == 'enter':
            play_sound('khoamthanh-dam-566913')
            self.start_game(None)
            return True
        elif key_name == 'backspace':
            play_sound('khoamthanh-dam-566913')
            self.quit_app(None)
            return True
        return False

    def start_game(self, instance):
        play_sound('khoamthanh-dam-566913')
        stop_bg_music()  # Stop background music when game starts
        self._keyboard_closed()
        game_screen = GameScreen(name='game_screen')
        if self.manager.has_screen('game_screen'):
            self.manager.remove_widget(self.manager.get_screen('game_screen'))
        self.manager.add_widget(game_screen)
        self.manager.current = 'game_screen'

    def quit_app(self, instance):
        play_sound('khoamthanh-dam-566913')
        self._keyboard_closed()
        App.get_running_app().stop()


# 4. Main Game Board Screen
class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        stop_bg_music() # Ensure background music is off
        
        root_layout = BoxLayout(orientation='vertical')
        
        self.header_label = Label(text="Score: 0", size_hint=(1, 0.1), font_size=20, color=(1, 1, 0, 1), halign='center', valign='middle')
        self.header_label.bind(size=self.header_label.setter('text_size'))
        root_layout.add_widget(self.header_label)
        
        self.board_layout = FloatLayout(size_hint=(None, None), size=(600, 600), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        
        wrapper_layout = FloatLayout(size_hint=(1, 0.9))
        wrapper_layout.add_widget(self.board_layout)
        root_layout.add_widget(wrapper_layout)
        
        self.add_widget(root_layout)
        
        self.game_over_lbl = None
        self.restart_btn = None
        
        self.score = 0
        self.running = True
        self.score_saved = False
        
        self.head_x = 90
        self.head_y = 90
        self.dx = 30
        self.dy = 0
        self.next_dx = 30
        self.next_dy = 0
        
        self.snake = [(90, 90), (60, 90), (30, 90)]
        self.food_x = random.randrange(0, 570, 30)
        self.food_y = random.randrange(0, 570, 30)

        from kivy.core.window import Window
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)

        self.event_clock = Clock.schedule_interval(self.update_game, 0.15)

    def _keyboard_closed(self):
        if self._keyboard:
            try:
                self._keyboard.unbind(on_key_down=self._on_keyboard_down)
                self._keyboard.unbind(on_key_up=self._on_keyboard_up)
            except:
                pass
            self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if not self.running:
            return True
            
        key_name = keycode[1]
        if key_name == 'down':
            self.change_dir(0, -30)
        elif key_name == 'up':
            self.change_dir(0, 30)
        elif key_name == 'left':
            self.change_dir(-30, 0)
        elif key_name == 'right':
            self.change_dir(30, 0)
        return True

    def _on_keyboard_up(self, keyboard, keycode):
        return True

    def change_dir(self, new_dx, new_dy):
        if new_dx == -30 and self.dx != 30:
            self.next_dx = -30
            self.next_dy = 0
        elif new_dx == 30 and self.dx != -30:
            self.next_dx = 30
            self.next_dy = 0
        elif new_dy == 30 and self.dy != -30:
            self.next_dx = 0
            self.next_dy = 30
        elif new_dy == -30 and self.dy != 30:
            self.next_dx = 0
            self.next_dy = -30

    def spawn_food(self):
        self.food_x = random.randrange(0, 570, 30)
        self.food_y = random.randrange(0, 570, 30)

    def game_over_action(self, collision_type="wall"):
        if not self.running:
            return
        self.running = False
        
        if collision_type == "wall":
            play_sound('khoamthanh-dam-566913')
        elif collision_type == "self":
            play_sound('shidenbeatsmusic-no-luck-too-bad-disappointing-sound-effect-112943')

        if self.score < 200:
            play_sound('alphix-game-over-417465')
        else:
            play_sound('u_ss015dykrt-brass-fanfare-reverberated-146263')

        if not self.score_saved:
            try:
                with open('result.txt', 'a') as f:
                    f.write(f'Final score of {player_name} is {self.score}\n')
            except:
                pass
            self.score_saved = True
        
        if not self.game_over_lbl:
            self.game_over_lbl = Label(text="Game Over", font_size=40, color=(1, 0.2, 0.2, 1), pos_hint={'center_x': 0.5, 'center_y': 0.6})
        if not self.restart_btn:
            self.restart_btn = Button(text="RESTART", font_size=30, size_hint=(None, None), size=(200, 60), pos_hint={'center_x': 0.5, 'center_y': 0.45}, background_color=(1, 0, 0, 1))
            self.restart_btn.bind(on_press=self.restart_game_action)

        if self.game_over_lbl not in self.board_layout.children:
            self.board_layout.add_widget(self.game_over_lbl)
        if self.restart_btn not in self.board_layout.children:
            self.board_layout.add_widget(self.restart_btn)

    def restart_game_action(self, *args):
        play_sound('khoamthanh-dam-566913')
        if self.game_over_lbl and self.game_over_lbl in self.board_layout.children:
            self.board_layout.remove_widget(self.game_over_lbl)
        if self.restart_btn and self.restart_btn in self.board_layout.children:
            self.board_layout.remove_widget(self.restart_btn)

        self.running = True
        self.score = 0
        self.score_saved = False
        self.head_x = 90
        self.head_y = 90
        self.dx = 30
        self.dy = 0
        self.next_dx = 30
        self.next_dy = 0
        self.snake = [(90, 90), (60, 90), (30, 90)]
        self.spawn_food()

    def on_touch_down(self, touch):
        if not self.running:
            return super(GameScreen, self).on_touch_down(touch)
            
        bx, by = self.board_layout.pos
        bw, bh = self.board_layout.size
        
        if bx <= touch.x <= bx + bw and by <= touch.y <= by + bh:
            center_x = bx + bw / 2
            center_y = by + bh / 2
            
            diff_x = touch.x - center_x
            diff_y = touch.y - center_y
            
            if abs(diff_x) > abs(diff_y):
                if diff_x > 0:
                    self.change_dir(30, 0)
                else:
                    self.change_dir(-30, 0)
            else:
                if diff_y > 0:
                    self.change_dir(0, 30)
                else:
                    self.change_dir(0, -30)
                    
        return super(GameScreen, self).on_touch_down(touch)

    def update_game(self, dt):
        if not self.running:
            self.render_graphics()
            return

        self.dx = self.next_dx
        self.dy = self.next_dy

        self.head_x += self.dx
        self.head_y += self.dy
        
        if self.head_x >= 600 or self.head_x < 0 or self.head_y >= 600 or self.head_y < 0:
            self.game_over_action("wall")
            return
            
        new_head = (self.head_x, self.head_y)
        
        if new_head in self.snake:
            self.game_over_action("self")
            return
            
        self.snake.insert(0, new_head)
        
        if abs(self.head_x - self.food_x) < 30 and abs(self.head_y - self.food_y) < 30:
            play_sound('nahtt-eat-323883')
            self.spawn_food()
            self.score += 50
        else:
            self.snake.pop()

        self.header_label.text = f'Score: {self.score} | Hey {player_name} You can do it'
        self.render_graphics()

    def render_graphics(self):
        self.board_layout.canvas.before.clear()
        with self.board_layout.canvas.before:
            Color(0, 0, 0, 1)
            Rectangle(pos=self.board_layout.pos, size=self.board_layout.size)
            
            Color(0.8, 0.8, 0.8, 1)
            Line(rectangle=(self.board_layout.x, self.board_layout.y, self.board_layout.width, self.board_layout.height), width=3)
            
            Color(*selected_food_color)
            Rectangle(pos=(self.board_layout.x + self.food_x, self.board_layout.y + self.food_y), size=(30, 30))
            
            Color(*selected_snake_color)
            for x, y in self.snake:
                Rectangle(pos=(self.board_layout.x + x, self.board_layout.y + y), size=(30, 30))


class SnakeKivyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name='welcome_screen'))
        sm.add_widget(NameScreen(name='name_screen'))
        sm.add_widget(MenuScreen(name='menu_screen'))
        return sm

if __name__ == '__main__':
    SnakeKivyApp().run()