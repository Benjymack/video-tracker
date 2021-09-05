# Imports
try:
    from video_overlay.overlay_canvas import OverlayCanvas
except ImportError:
    from overlay_canvas import OverlayCanvas


# Classes
class OverlayController:
    def __init__(self, video_controller):
        # Create the overlay canvas
        self._overlay_canvas = OverlayCanvas()
        video_controller.add_overlay(self._overlay_canvas, self._mouse_press,
                                     self._mouse_move, self._mouse_release)

    def _mouse_press(self, event):
        print('Overlay press')

    def _mouse_move(self, event):
        print('Overlay move')

    def _mouse_release(self, event):
        print('Overlay release')
