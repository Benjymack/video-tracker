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

        self._overlay_items = (
            self._overlay_canvas.get_reference_axes(),
        )

    def _find_items_containing(self, pos):
        for item in self._overlay_items:
            if item.sceneBoundingRect().isEmpty() or \
                    item.sceneBoundingRect().contains(pos):
                yield item

    def _mouse_press(self, event):
        for item in self._find_items_containing(event.scenePos()):
            item.mouse_press(event)

    def _mouse_move(self, event):
        for item in self._find_items_containing(event.scenePos()):
            item.mouse_move(event)

    def _mouse_release(self, event):
        for item in self._find_items_containing(event.scenePos()):
            item.mouse_release(event)
