import pygame
import os

class MusicPlayer:
    def __init__(self, music_dir):
        self.music_dir = music_dir
        self.playlist = [os.path.join(music_dir, f) for f in os.listdir(music_dir) if f.endswith(('.mp3', '.wav'))]
        self.current_index = 0
        self.is_paused = False

    def play(self):
        if self.playlist:
            if self.is_paused:
                pygame.mixer.music.unpause()
                self.is_paused = False
            else:
                pygame.mixer.music.load(self.playlist[self.current_index])
                pygame.mixer.music.play()

    def pause(self):
        pygame.mixer.music.pause()
        self.is_paused = True

    def stop(self):
        pygame.mixer.music.stop()
        self.is_paused = False

    def next(self):
        if self.playlist:
            self.current_index = (self.current_index + 1) % len(self.playlist)
            self.is_paused = False
            self.play()

    def prev(self):
        if self.playlist:
            self.current_index = (self.current_index - 1) % len(self.playlist)
            self.is_paused = False
            self.play()

    def get_current_track(self):
        if self.playlist:
            return os.path.basename(self.playlist[self.current_index])
        return "No tracks found"