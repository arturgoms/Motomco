__author__ = ["Artur Gomes", "github.com/arturgoms"]
import gi
gi.require_version('WebKit2', '4.0')
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
from gi.repository import WebKit2
from threading import Thread

Gtk.rc_parse_string("""style "hide-scrollbar-style"
{
  GtkScrollbar::slider_width = 0
  GtkScrollbar::min-slider-length = 0
  GtkScrollbar::activate_slider = 0
  GtkScrollbar::trough_border = 0
  GtkScrollbar::has-forward-stepper = 0
  GtkScrollbar::has-backward-stepper = 0
  GtkScrollbar::stepper_size = 0
  GtkScrollbar::stepper_spacing = 0
  GtkScrollbar::trough-side-details = 0
  GtkScrollbar::default_border = { 0, 0, 0, 0 }
  GtkScrollbar::default_outside_border = { 0, 0, 0, 0 }
  GtkScrolledWindow::scrollbar-spacing = 0
  GtkScrolledWindow::scrollbar-within-bevel = False
}
widget_class "*Scrollbar" style "hide-scrollbar-style"
widget_class "*ScrolledWindow" style "hide-scrollbar-style"
""")

class  ReloadView:
    def __init__(self):
        import subprocess
        print 'Chamando o servidor'
        subprocess.call("sudo python loader.py &", shell=True)
        window = Gtk.Window()
        window.set_size_request(800, 472)
        window.set_position(Gtk.WindowPosition.CENTER)
        window.set_decorated(False)
        window.set_resizable(False)
        window.set_icon_from_file('/home/pi/Desktop/loader/static/img/logo2.png')
        self.view = WebKit2.WebView()
        window.connect("realize", self.realize_cb)
        self.view.load_uri('http://127.0.0.1:5000')
        window.add(self.view)
        window.show_all()

    def realize_cb(self, widget):
        pixmap = Gtk.gdk.Pixmap(None, 1, 1, 1)
        color = Gtk.gdk.Color()
        cursor = Gtk.gdk.Cursor(pixmap, pixmap, color, color, 0, 0)
        widget.window.set_cursor(cursor)

if __name__ == "__main__":
    ReloadView()
    Gtk.main()

