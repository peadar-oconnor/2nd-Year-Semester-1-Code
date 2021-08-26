class Track:

    def __init__(self, name, artiste, timesplayed=0):
        self.set_name(name)
        self.set_artiste(artiste)
        self.set_timesplayed(timesplayed)

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_artiste(self):
        return self._artiste

    def set_artiste(self, artiste):
        self._artiste = artiste

    def get_timesplayed(self):
        return self._timesplayed

    def set_timesplayed(self, timesplayed):
        # Error check: timesplayed has to be an int because it gets
        #  incremented in the play method. If its not an int it gets set to 0
        if type(timesplayed) == int:
            self._timesplayed = timesplayed
        else:
            timesplayed = 0
            self._timesplayed = timesplayed

    def __str__(self):
        description = ("Name = %s, Artist = %s, Times played = %i" %
                       (self._name, self._artiste, self._timesplayed))
        return description

    def play(self):
        self._timesplayed += 1
        description = ("Name = %s, Artist = %s, Times played = %i" %
                       (self._name, self._artiste, self._timesplayed))
        return description


class DLLNode:
    def __init__(self, item, prevnode, nextnode):
        self._track = item
        self._next = nextnode
        self._prev = prevnode


class PyToonz:
    def __init__(self):
        self._first = None
        self._last = None
        self._current = None
        self._size = 0

    def get_current(self):
        # if playlists empty return none
        if self._size == 0:
            return None
        else:
            return "Current Track: %s" % self._current._track

    def play(self):
        # if playlists empty give an error
        if self._current is None:
            print("Error: No track currently selected.")
        else:
            print("Now Playing: %s" % self._current._track.play())

    def next_track(self):
        # if theres nothing in the playlist then nothing happens
        if self._current is None:
            return None
        # if the current track is the last track: the current track wraps around the list and becomes the first track
        elif self._current._next is None:
            self._current = self._first
        else:
            self._current = self._current._next

    def prev_track(self):
        # if theres nothing in the playlist then nothing happens
        if self._current is None:
            return None
        # if the current track is the first track: the current track wraps around the list and becomes the last track
        if self._current._prev is None:
            self._current = self._last
        else:
            self._current = self._current._prev

    def reset(self):
        self._current = self._first

    def add_track(self, track):
        # new node will always be the last, so nextnode is none
        newnode = DLLNode(track, self._last, None)
        # if the list is empty the new node becomes both the first and current tracks
        if self._first is None:
            self._first = newnode
            self._current = newnode
        # if the list isnt empty then the last track links with the new node
        else:
            self._last._next = newnode
        self._last = newnode
        self._size += 1

    def add_after(self, track):
        # if theres no current track selected then nothing happens
        if self._current is None:
            return None
        # if the current track is the last then the new node is added to the end using the add_track method
        elif self._current._next is None:
            self.add_track(track)
        # adding between two tracks
        else:
            nextNode = self._current._next
            addedTrackPrev = self._current
            addedTrackNext = self._current._next
            newNode = DLLNode(track, addedTrackPrev, addedTrackNext)
            self._current._next = newNode
            nextNode._prev = newNode
            self._size += 1

    def remove_current(self):
        # if you try to remove when nothing is selected (ie when playlist is empty) then nothing happens
        if self._current is None:
            return None
        # when you remove the only track in the playlist the playlist becomes empty
        elif self._current._next is None and self._current._prev is None:
            self._first = None
            self._last = None
            self._current = None
            self._size = 0
        # when the current track is the last in the playlist: previous track becomes last, selected track removed,
        # current track moves to the first
        elif self._current._next is None:
            prevNode = self._current._prev
            prevNode._next = None
            self._last = prevNode
            self._current._prev = None
            self._current = self._first
            self._size -= 1
        # when the current track is the first in the playlist: next track becomes first, selected track removed
        elif self._current._prev is None:
            nextNode = self._current._next
            nextNode._prev = None
            self._first = nextNode
            self._current._next = None
            self._current = self._first
            self._size -= 1
        # other cases when selected track is between two tracks
        else:
            nextNode = self._current._next
            prevNode = self._current._prev
            nextNode._prev = prevNode
            prevNode._next = nextNode
            self._current._next = None
            self._current._prev = None
            self._current = nextNode
            self._size -= 1

    def length(self):
        return self._size

    def __str__(self):
        string = "Playlist:\n"
        # size is 0 when playlists empty
        if self._size == 0:
            return "The Playlist is empty"
        else:
            node_to_print = self._first
            checker = node_to_print._next
            # while its not none then that means theres another track to add
            while checker is not None:
                # checks if the track is the current, adds the arrow if it is
                if node_to_print == self._current:
                    string += ("--> %s \n" % (node_to_print._track.__str__()))
                else:
                    string += ("%s \n" % (node_to_print._track.__str__()))
                # moving along the playlist node by node
                node_to_print = node_to_print._next
                checker = node_to_print._next
            if node_to_print == self._current:
                string += ("--> " + node_to_print._track.__str__())
            else:
                string += node_to_print._track.__str__()
            return string
