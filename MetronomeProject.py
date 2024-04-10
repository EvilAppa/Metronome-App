import tkinter as tk  # Import tkinter for GUI
from pygame import mixer  # Import mixer from pygame for sound handling

class MetronomeApp:
    def __init__(self, master):
        self.master = master  # Save reference to the Tkinter root window
        self.master.title("Metronome App")  # Set window title

        # Variables
        self.is_running = False  # Bool - Metronome is active or not
        self.bpm = 60  # Sets a default BPM
        self.volume = 50  # Sets a default volume
        self.selected_sound = "Click"  # Sets a default sound
        self.sound_interval = 60000 / self.bpm  # Calculates sound interval based on BPM

        self.load_sounds()  # Initialize sound mixer
        self.create_widgets()  # Create GUI widgets

    def load_sounds(self):
        mixer.init()  # Initialize sound mixer
        # Load sound files and create a dictionary mapping sound names to sound objects
        self.sounds = {
            "Click": mixer.Sound("Click1.wav"),
            "Tick": mixer.Sound("Click2.wav")
        }

    def create_widgets(self):
        # Create Start/Stop button
        self.start_stop_button = tk.Button(self.master, text="Start", command=self.toggle_metronome)
        self.start_stop_button.pack()

        # Create BPM label and input field - validates if input is valid (integer between 1 and 240)
        self.bpm_label = tk.Label(self.master, text="BPM:")
        self.bpm_label.pack()
        vcmd = (self.master.register(self.validate_bpm), '%P')  # Register validation function
        self.bpm_entry = tk.Entry(self.master, validate="key", validatecommand=vcmd)
        self.bpm_entry.insert(0, str(self.bpm))  # Set default BPM value
        self.bpm_entry.pack()

        # Create sound selection option menu
        self.sound_option_menu = tk.OptionMenu(self.master, tk.StringVar(), *self.sounds.keys(), command=self.update_sound)
        self.sound_option_menu.pack()

        # Create volume control slider
        self.volume_scale = tk.Scale(self.master, from_=100, to=0, orient="vertical", label="Volume",
                                      command=self.update_volume)
        self.volume_scale.set(self.volume)  # Set default volume
        self.volume_scale.pack()

        

        # Add hotkey functionality (Spacebar toggles metronome)
        self.master.bind("<KeyPress-space>", self.toggle_metronome)
    
    def validate_bpm(self, new_value):
        if new_value == "":  # Allow empty string (deletion)
            return True
        try:
            value = int(new_value)
            return 1 <= value <= 240  # Check if value is within range
        except ValueError:
            return False  # Reject non-integer input

    def toggle_metronome(self, event=None):
        if self.is_running:  # If metronome is running, stop it
            self.is_running = False
            self.start_stop_button.config(text="Start")  # Change button text to "Start"
            mixer.music.stop()  # Stop playing the sound
        else:  # If metronome is stopped, start it
            self.is_running = True
            self.start_stop_button.config(text="Stop")  # Change button text to "Stop"
            new_bpm = int(self.bpm_entry.get())  # Get the new BPM from entry field
            self.update_bpm(new_bpm)  # Update BPM and sound interval
            self.play_sound()  # Play sound immediately
            self.master.after(1000, self.reactivate_button)  # Disable button temporarily
            if not event:  # If the event is not from button press, schedule the next sound immediately
                self.master.after(0, self.play_sound_loop)

    def update_bpm(self, new_bpm):
        self.bpm = new_bpm  # Update BPM
        self.sound_interval = 60000 / self.bpm  # Recalculate sound interval



    def reactivate_button(self):
        self.start_stop_button.config(state="normal")  # Enable the button

    def play_sound_loop(self):
        if self.is_running:  # If metronome is running, play the sound and schedule the next one
            self.play_sound()
            self.master.after(int(self.sound_interval), self.play_sound_loop)

    def play_sound(self):
        sound = self.sounds[self.selected_sound]  # Get selected sound
        sound.set_volume(self.volume / 100)  # Set volume level
        sound.play()  # Play the sound

    def update_volume(self, value):
        self.volume = int(value)  # Update volume level when slider value changes

    def update_sound(self, selected_sound):
        self.selected_sound = selected_sound  # Update selected sound

def main():
    root = tk.Tk()  # Create Tkinter root window
    app = MetronomeApp(root)  # Create MetronomeApp instance
    root.mainloop()  # Enter Tkinter event loop

if __name__ == "__main__":
    main()  # Run the application if the script is executed directly
