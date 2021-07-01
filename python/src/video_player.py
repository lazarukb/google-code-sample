"""A video player class."""

from .video_library import VideoLibrary
from .video_playlist import Playlist

import random


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self.video_playlists = []
        self.selected = None
        self.status = "stopped"

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        unsorted_videos = self._video_library.get_all_videos()
        sorted_videos = sorted(unsorted_videos, key=lambda x: x.title)
        print(f"Here\'s a list of all available videos:")
        for video in sorted_videos:
            if video.flag == "":
                flag_comment = ""
            else:
                flag_comment = "- FLAGGED (reason: " + video.flag + ")"
            tags = ' '.join(map(str, video.tags))
            print(f"  {video.title} ({video.video_id}) [", end='')
            print(f"{tags}] {flag_comment}")

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        all_videos = self._video_library.get_all_videos()
        target = None
        try:
            target = [i for i in all_videos if i.video_id == video_id][0]
        except:
            print(f"Cannot play video: Video does not exist")

        if target is not None:
            if target.flag == "":
                if (self.status == "playing") or (self.status == "paused"):
                    self.stop_video()
                print(f"Playing video: {target.title}")
                self.selected = target
                self.status = "playing"
            else:
                print(f"Cannot play video: Video is currently flagged (reason: {target.flag})")

    def stop_video(self):
        """Stops the current video."""

        if self.status == "stopped":
            print(f"Cannot stop video: No video is currently playing")
        else:
            print(f"Stopping video: {self.selected.title}")
            self.status = "stopped"

    def play_random_video(self):
        """Plays a random video from the video library."""

        all_videos = [ele for ele in self._video_library.get_all_videos() if ele.flag == ""]
        num_videos = len(all_videos)
        if num_videos == 0:
            print(f"No videos available")
        else:
            selected_video = random.randrange(0, num_videos)
            if self.status == "playing":
                self.stop_video()
            self.play_video(all_videos[selected_video].video_id)

    def pause_video(self):
        """Pauses the current video."""

        if self.status == "playing":
            print(f"Pausing video: {self.selected.title}")
            self.status = "paused"
            return
        if self.status == "paused":
            print(f"Video already paused: {self.selected.title}")
            return
        if self.status == "stopped":
            print(f"Cannot pause video: No video is currently playing")
            return

    def continue_video(self):
        """Resumes playing the current video."""

        if self.status == "playing":
            print(f"Cannot continue video: Video is not paused")
            return
        if self.status == "paused":
            print(f"Continuing video: {self.selected.title}")
            self.status = "playing"
            return
        if self.status == "stopped":
            print(f"Cannot continue video: No video is currently playing")
            return

    def show_playing(self):
        """Displays video currently playing."""

        if self.status == "playing":
            video = self.selected
            tags = ' '.join(map(str, video.tags))
            print(f"Currently playing: {video.title} ({video.video_id}) [{tags}]")
            return
        if self.status == "paused":
            video = self.selected
            tags = ' '.join(map(str, video.tags))
            print(f"Currently playing: {video.title} ({video.video_id}) [{tags}] - PAUSED")
            return
        if self.status == "stopped":
            print(f"No video is currently playing")
            return

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.upper() in [(playlist.name.upper()) for playlist in self.video_playlists]:
            print(f"Cannot create playlist: A playlist with the same name already exists")
        else:
            self.video_playlists.append(Playlist(playlist_name))
            print(f"Successfully created new playlist: {playlist_name}")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """

        target_playlist = None
        target_video = None
        all_videos = self._video_library.get_all_videos()

        try:
            target_playlist = \
                [playlist for playlist in self.video_playlists if playlist.name.upper() == playlist_name.upper()][0]
        except:
            print(f"Cannot add video to {playlist_name}: Playlist does not exist")

        if target_playlist is not None:
            try:
                target_video = [vid for vid in all_videos if vid.video_id == video_id][0]
            except:
                print(f"Cannot add video to {playlist_name}: Video does not exist")

        if (target_playlist is not None) and (target_video is not None):
            if target_video.flag == "":
                if video_id not in target_playlist.queue:
                    target_playlist.queue.append(video_id)
                    print(f"Added video to {playlist_name}: {target_video.title}")
                else:
                    print(f"Cannot add video to {playlist_name}: Video already added")
            else:
                print(f"Cannot add video to my_playlist: Video is currently flagged (reason: {target_video.flag})")

    def show_all_playlists(self):
        """Display all playlists."""

        if len(self.video_playlists) == 0:
            print(f"No playlists exist yet")
        else:
            unsorted_playlist_names = [playlist.name for playlist in self.video_playlists]
            sorted_playlists = sorted(unsorted_playlist_names)
            print(f"Showing all playlists:")
            for playlist in sorted_playlists:
                print(f"  {playlist}")

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        target_playlist = None
        all_videos = self._video_library.get_all_videos()

        try:
            target_playlist = \
                [playlist for playlist in self.video_playlists if playlist.name.upper() == playlist_name.upper()][0]
        except:
            print(f"Cannot show playlist {playlist_name}: Playlist does not exist")

        if target_playlist is not None:
            print(f"Showing playlist: {playlist_name}")
            if len(target_playlist.queue) == 0:
                print(f"No videos here yet")
            else:
                for vid in target_playlist.queue:
                    video = [video for video in all_videos if video.video_id == vid][0]
                    if video.flag == "":
                        flag_comment = ""
                    else:
                        flag_comment = "- FLAGGED (reason: " + video.flag + ")"
                    tags = ' '.join(map(str, video.tags))
                    print(f"  {video.title} ({video.video_id}) [", end='')
                    print(f"{tags}] {flag_comment}")

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """

        target_playlist = None
        video = None
        all_videos = self._video_library.get_all_videos()

        try:
            target_playlist = \
                [playlist for playlist in self.video_playlists if playlist.name.upper() == playlist_name.upper()][0]
        except:
            print(f"Cannot remove video from {playlist_name}: Playlist does not exist")

        if target_playlist is not None:
            try:
                video = [video for video in all_videos if video.video_id == video_id][0]
            except:
                print(f"Cannot remove video from {playlist_name}: Video does not exist")

        if (target_playlist is not None) and (video is not None):
            if video_id in target_playlist.queue:
                target_playlist.queue.remove(video_id)
                print(f"Removed video from {playlist_name}: {video.title}")
            else:
                print(f"Cannot remove video from {playlist_name}: Video is not in playlist")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        target_playlist = None

        try:
            target_playlist = \
                [playlist for playlist in self.video_playlists if playlist.name.upper() == playlist_name.upper()][0]
        except:
            print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")

        if target_playlist is not None:
            if len(target_playlist.queue) > 0:
                target_playlist.queue = []
                print(f"Successfully removed all videos from {playlist_name}")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        target_playlist = None

        try:
            target_playlist = \
                [playlist for playlist in self.video_playlists if playlist.name.upper() == playlist_name.upper()][0]
        except:
            print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")

        if target_playlist is not None:
            self.video_playlists.remove(target_playlist)
            print(f"Deleted playlist: {playlist_name}")

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        all_videos = self._video_library.get_all_videos()

        search_hits = []

        try:
            search_hits = [video for video in all_videos if 
                           ((search_term.upper() in video.title.upper()) and (video.flag == ""))]
        except:
            pass

        if len(search_hits) > 0:
            print(f"Here are the results for {search_term}:")
            sorted_hits = sorted(search_hits, key=lambda x: x.title)
            i = 0
            for hit in sorted_hits:
                tags = ' '.join(map(str, hit.tags))
                print(f"{i + 1}) {hit.title} ({hit.video_id}) [{tags}]")
                i += 1
            print(f"Would you like to play any of the above? If yes, specify the number of the video.")
            print(f"If your answer is not a valid number, we will assume it's a no.")
            cin = input("")
            try:
                selection = int(cin)
            except:
                selection = None
            if type(selection) == int:
                if (selection > 0) and (selection <= len(search_hits)):
                    target_video = sorted_hits[selection - 1]
                    self.play_video(target_video.video_id)
        else:
            print(f"No search results for {search_term}")

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        all_videos = self._video_library.get_all_videos()
        search_hits = []

        try:
            search_hits = ([video for video in all_videos if
                           ((video_tag.upper() in [ele.upper() for ele in list(video.tags)]) and (video.flag == ""))])
        except:
            pass

        if len(search_hits) > 0:
            print(f"Here are the results for {video_tag}:")
            sorted_hits = sorted(search_hits, key=lambda x: x.title)
            i = 0
            for hit in sorted_hits:
                tags = ' '.join(map(str, hit.tags))
                print(f"{i + 1}) {hit.title} ({hit.video_id}) [{tags}]")
                i += 1
            print(f"Would you like to play any of the above? If yes, specify the number of the video.")
            print(f"If your answer is not a valid number, we will assume it's a no.")
            cin = input("")
            try:
                selection = int(cin)
            except:
                selection = None
            if type(selection) == int:
                if (selection > 0) and (selection <= len(search_hits)):
                    target_video = sorted_hits[selection - 1]
                    self.play_video(target_video.video_id)
        else:
            print(f"No search results for {video_tag}")

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """

        target_video = None

        if flag_reason == "":
            flag_reason = "Not supplied"
        all_videos = self._video_library.get_all_videos()

        try:
            target_video = [vid for vid in all_videos if vid.video_id == video_id][0]
        except:
            print(f"Cannot flag video: Video does not exist")

        if target_video is not None:

            if target_video.flag == "":
                target_video.flag = flag_reason
                if (self.status != "stopped") and (target_video.title == self.selected.title):
                    self.stop_video()
                print(f"Successfully flagged video: {target_video.title} (reason: {flag_reason})")
            else:
                print(f"Cannot flag video: Video is already flagged")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """

        target_video = None
        all_videos = self._video_library.get_all_videos()

        try:
            target_video = [vid for vid in all_videos if vid.video_id == video_id][0]
        except:
            print(f"Cannot remove flag from video: Video does not exist")

        if target_video is not None:

            if target_video.flag != "":
                target_video.flag = ""
                print(f"Successfully removed flag from video: {target_video.title})")
            else:
                print(f"Cannot remove flag from video: Video is not flagged")
