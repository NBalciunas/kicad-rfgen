import pcbnew
import wx
import os
from .microstrip_patch_inset_gen import generate_microstrip_inset_patch
from .microstrip_patch_coaxial_gen import generate_microstrip_coaxial_patch
from .microstrip_patch_gen_legacy import generate_microstrip_patch_legacy
from .wilkinson_gen import generate_wilkinson


class RFgen(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "RFgen"
        self.category = "RF tools"
        self.description = "Generate PCB antennas"
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(os.path.dirname(__file__), "assets/icon.png")

    def Run(self):
        RFgenUI(wx.Window.FindFocus()).Show()


class RFgenUI(wx.Frame):
    def __init__(self, frame):
        style = wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)
        super().__init__(parent=None, title="RFgen", size=(360, 830), style=style)

        self._frame = frame

        icon_path = os.path.join(os.path.dirname(__file__), "assets/icon.png")
        icon = wx.Icon(icon_path, wx.BITMAP_TYPE_PNG)
        self.SetIcon(icon)

        self.panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Choice
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(wx.StaticText(self.panel, label="generate"), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=10)
        self.gen_choice = wx.Choice(self.panel, choices=["Microstrip Patch Antenna (Inset Feed)", "Microstrip Patch Antenna (Coaxial Feed)", "Microstrip Patch Antenna (Legacy)", "Wilkinson Power Divider"])
        self.gen_choice.SetSelection(0)
        hbox.Add(self.gen_choice, proportion=1, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=10)
        vbox.Add(hbox, flag=wx.EXPAND)
        self.gen_choice.Bind(wx.EVT_CHOICE, self.on_choice)

        self.dynamic_box = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.dynamic_box, flag=wx.EXPAND | wx.ALL, border=5)

        # Enter
        enter_btn = wx.Button(self.panel, label="Generate")
        vbox.Add(enter_btn, flag=wx.ALL | wx.CENTER, border=10)
        enter_btn.Bind(wx.EVT_BUTTON, self.on_enter)

        self.panel.SetSizer(vbox)

        self.update_fields("Microstrip Patch Antenna (Inset Feed)")

    def on_choice(self, event):
        choice = self.gen_choice.GetStringSelection()
        self.update_fields(choice)

    def update_fields(self, choice):
        self.dynamic_box.Clear(True)

        self.img = None
        self.footprint_name_input = None
        self.ground_check_input = None
        self.mask_check_input = None

        self.patch_length_input = None
        self.patch_width_input = None
        self.ground_length_input = None
        self.ground_width_input = None

        self.feed_length_input = None  # Legacy
        self.feed_width_input = None
        self.inset_gap_input = None
        self.inset_distance_input = None

        self.feed_offset_x_input = None
        self.feed_offset_y_input = None
        self.pad_radius_input = None
        self.hole_radius_input = None
        self.clearance_radius_input = None

        self.input_length_input = None
        self.input_width_input = None
        self.output_length_input = None
        self.output_width_input = None
        self.arc_radius_input = None
        self.arc_width_input = None

        match choice:
            case "Microstrip Patch Antenna (Inset Feed)":
                self.img = add_image(self.panel, self.dynamic_box, "assets/microstrip-patch-antenna.png", size=(270, 270))
                self.footprint_name_input = add_field(self.panel, self.dynamic_box, "footprint name", "PATCH_ANTENNA", width=160)
                self.patch_length_input = add_field(self.panel, self.dynamic_box, "Patch Length (Lp)", "11.6", width=80, unit="mm")
                self.patch_width_input = add_field(self.panel, self.dynamic_box, "Patch Width (Wp)", "16.3", width=80, unit="mm")
                self.ground_length_input = add_field(self.panel, self.dynamic_box, "Ground Length (Lg)", "21.2", width=80, unit="mm")
                self.ground_width_input = add_field(self.panel, self.dynamic_box, "Ground Width (Wg)", "25.9", width=80,unit="mm")
                self.feed_width_input = add_field(self.panel, self.dynamic_box, "Feed Width (Wf)", "2.8", width=80, unit="mm")
                self.inset_gap_input = add_field(self.panel, self.dynamic_box, "Inset Gap (X0)", "0.5", width=80, unit="mm")
                self.inset_distance_input = add_field(self.panel, self.dynamic_box, "Inset Distance (Y0)", "3.9", width=80, unit="mm")
                self.ground_check_input = add_checkbox(self.panel, self.dynamic_box, "Include ground plane", default=True)
                self.mask_check_input = add_checkbox(self.panel, self.dynamic_box, "Remove solder mask", default=True)
            case "Microstrip Patch Antenna (Coaxial Feed)":
                self.img = add_image(self.panel, self.dynamic_box, "assets/microstrip-patch-antenna.png", size=(270, 270))
                self.footprint_name_input = add_field(self.panel, self.dynamic_box, "footprint name", "PATCH_ANTENNA", width=160)
                self.patch_length_input = add_field(self.panel, self.dynamic_box, "Patch Length (Lp)", "11.6", width=80, unit="mm")
                self.patch_width_input = add_field(self.panel, self.dynamic_box, "Patch Width (Wp)", "16.3", width=80, unit="mm")
                self.ground_length_input = add_field(self.panel, self.dynamic_box, "Ground Length (Lg)", "21.2", width=80, unit="mm")
                self.ground_width_input = add_field(self.panel, self.dynamic_box, "Ground Width (Wg)", "25.9", width=80, unit="mm")
                self.feed_offset_x_input = add_field(self.panel, self.dynamic_box, "Feed Offset X (Xf)", "0", width=80, unit="mm")
                self.feed_offset_y_input = add_field(self.panel, self.dynamic_box, "Feed Offset Y (Yf)", "2.9", width=80, unit="mm")
                self.pad_radius_input = add_field(self.panel, self.dynamic_box, "Pad Radius (Rp)", "1.4", width=80, unit="mm")
                self.hole_radius_input = add_field(self.panel, self.dynamic_box, "Hole Radius (Rt)", "0.65", width=80, unit="mm")
                self.clearance_radius_input = add_field(self.panel, self.dynamic_box, "Clearance Radius (Rc)", "2.5", width=80, unit="mm")
                self.ground_check_input = add_checkbox(self.panel, self.dynamic_box, "Include ground plane", default=True)
                self.mask_check_input = add_checkbox(self.panel, self.dynamic_box, "Remove solder mask", default=True)
            case "Microstrip Patch Antenna (Legacy)":
                self.img = add_image(self.panel, self.dynamic_box, "assets/microstrip-patch-antenna.png", size=(270, 270))
                self.footprint_name_input = add_field(self.panel, self.dynamic_box, "footprint name", "PATCH_ANTENNA", width=160)
                self.patch_length_input = add_field(self.panel, self.dynamic_box, "Patch Length (Lp)", "11.6", width=80, unit="mm")
                self.patch_width_input = add_field(self.panel, self.dynamic_box, "Patch Width (Wp)", "16.3", width=80, unit="mm")
                self.feed_length_input = add_field(self.panel, self.dynamic_box, "Feed Length (Lf)", "4.8", width=80, unit="mm")
                self.feed_width_input = add_field(self.panel, self.dynamic_box, "Feed Width (Wf)", "2.8", width=80, unit="mm")
                self.inset_gap_input = add_field(self.panel, self.dynamic_box, "Inset Gap (X0)", "0.5", width=80, unit="mm")
                self.inset_distance_input = add_field(self.panel, self.dynamic_box, "Inset Distance (Y0)", "3.9", width=80, unit="mm")
                self.ground_check_input = add_checkbox(self.panel, self.dynamic_box, "Include ground plane", default=True)
                self.mask_check_input = add_checkbox(self.panel, self.dynamic_box, "Remove solder mask", default=True)
            case "Wilkinson Power Divider":
                self.img = add_image(self.panel, self.dynamic_box, "assets/wilkinson-power-divider.png", size=(270, 270))
                self.footprint_name_input = add_field(self.panel, self.dynamic_box, "footprint name", "WILKINSON", width=160)
                self.input_length_input = add_field(self.panel, self.dynamic_box, "Input Length (L0)", "1.9", width=80, unit="mm")
                self.input_width_input = add_field(self.panel, self.dynamic_box, "Input Width (W0)", "2.8", width=80, unit="mm")
                self.output_length_input = add_field(self.panel, self.dynamic_box, "Output Length (L1)", "3.4", width=80, unit="mm")
                self.output_width_input = add_field(self.panel, self.dynamic_box, "Output Width (W1)", "1.7", width=80, unit="mm")
                self.arc_radius_input = add_field(self.panel, self.dynamic_box, "Arc Radius (R)", "2.2", width=80, unit="mm")
                self.arc_width_input = add_field(self.panel, self.dynamic_box, "Arc Width (W2)", "1.7", width=80, unit="mm")
                self.ground_check_input = add_checkbox(self.panel, self.dynamic_box, "Include ground plane", default=True)
                self.mask_check_input = add_checkbox(self.panel, self.dynamic_box, "Expose pads for isolation resistor", default=True)
            case _:
                wx.MessageBox("Something went wrong...", "Error")

        self.panel.Layout()

    def on_enter(self, event):
        footprint_name = self.footprint_name_input.GetValue()
        gen_choice = self.gen_choice.GetStringSelection()
        match gen_choice:
            case "Microstrip Patch Antenna (Inset Feed)":
                self.Destroy()
                patch_length = float(self.patch_length_input.GetValue())
                patch_width = float(self.patch_width_input.GetValue())
                ground_length = float(self.ground_length_input.GetValue())
                ground_width = float(self.ground_width_input.GetValue())
                feed_width = float(self.feed_width_input.GetValue())
                inset_gap = float(self.inset_gap_input.GetValue())
                inset_distance = float(self.inset_distance_input.GetValue())
                ground_check = bool(self.ground_check_input.GetValue())
                mask_check = bool(self.mask_check_input.GetValue())
                footprint = generate_microstrip_inset_patch(footprint_name, patch_length=patch_length, patch_width=patch_width, ground_length=ground_length, ground_width=ground_width, feed_width=feed_width, inset_gap=inset_gap, inset_distance=inset_distance, ground_check=ground_check, mask_check=mask_check)
                self.spawn_footprint(footprint)
            case "Microstrip Patch Antenna (Coaxial Feed)":
                self.Destroy()
                patch_length = float(self.patch_length_input.GetValue())
                patch_width = float(self.patch_width_input.GetValue())
                ground_length = float(self.ground_length_input.GetValue())
                ground_width = float(self.ground_width_input.GetValue())
                feed_offset_x = float(self.feed_offset_x_input.GetValue())
                feed_offset_y = float(self.feed_offset_y_input.GetValue())
                pad_radius = float(self.pad_radius_input.GetValue())
                hole_radius = float(self.hole_radius_input.GetValue())
                clearance_radius = float(self.clearance_radius_input.GetValue())
                ground_check = bool(self.ground_check_input.GetValue())
                mask_check = bool(self.mask_check_input.GetValue())
                footprint = generate_microstrip_coaxial_patch(footprint_name, patch_length=patch_length, patch_width=patch_width, ground_length=ground_length, ground_width=ground_width, feed_offset_x=feed_offset_x, feed_offset_y=feed_offset_y, pad_radius=pad_radius, hole_radius=hole_radius, clearance_radius=clearance_radius, ground_check=ground_check, mask_check=mask_check)
                self.spawn_footprint(footprint)
            case "Microstrip Patch Antenna (Legacy)":
                self.Destroy()
                patch_length = float(self.patch_length_input.GetValue())
                patch_width = float(self.patch_width_input.GetValue())
                feed_length = float(self.feed_length_input.GetValue())
                feed_width = float(self.feed_width_input.GetValue())
                inset_gap = float(self.inset_gap_input.GetValue())
                inset_distance = float(self.inset_distance_input.GetValue())
                ground_check = bool(self.ground_check_input.GetValue())
                mask_check = bool(self.mask_check_input.GetValue())
                footprint = generate_microstrip_patch_legacy(footprint_name, patch_length=patch_length, patch_width=patch_width, feed_length=feed_length, feed_width=feed_width, inset_gap=inset_gap, inset_distance=inset_distance, ground_check=ground_check, mask_check=mask_check)
                self.spawn_footprint(footprint)
            case "Wilkinson Power Divider":
                self.Destroy()
                input_length = float(self.input_length_input.GetValue())
                input_width = float(self.input_width_input.GetValue())
                output_length = float(self.output_length_input.GetValue())
                output_width = float(self.output_width_input.GetValue())
                arc_radius = float(self.arc_radius_input.GetValue())
                arc_width = float(self.arc_width_input.GetValue())
                ground_check = bool(self.ground_check_input.GetValue())
                mask_check = bool(self.mask_check_input.GetValue())
                footprint = generate_wilkinson(footprint_name, input_length=input_length, input_width=input_width, output_length=output_length, output_width=output_width, arc_radius=arc_radius, arc_width=arc_width, ground_check=ground_check, mask_check=mask_check)
                self.spawn_footprint(footprint)
            case _:
                wx.MessageBox("Something went wrong...", "Error")

    def spawn_footprint(self, input_footprint):
        clipboard = wx.Clipboard.Get()
        if clipboard.Open():
            clipboard.SetData(wx.TextDataObject(input_footprint))
            clipboard.Close()

            evt_esc = wx.KeyEvent(wx.wxEVT_CHAR_HOOK)
            evt_esc.SetKeyCode(wx.WXK_ESCAPE)
            evt_esc.SetControlDown(True)
            wx.PostEvent(self._frame, evt_esc)

            evt_paste = wx.KeyEvent(wx.wxEVT_CHAR_HOOK)
            evt_paste.SetKeyCode(ord('V'))
            evt_paste.SetControlDown(True)
            wx.PostEvent(self._frame, evt_paste)


def add_field(panel, vbox, label, default="", width=80, unit=None):
    hbox = wx.BoxSizer(wx.HORIZONTAL)
    hbox.Add(wx.StaticText(panel, label=label, size=(130, -1)), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)
    ctrl = wx.TextCtrl(panel, value=str(default), size=(width, -1))
    hbox.Add(ctrl, flag=wx.ALL | wx.CENTER, border=5)

    if unit:
        hbox.Add(wx.StaticText(panel, label=unit), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)

    vbox.Add(hbox, flag=wx.EXPAND)
    return ctrl

def add_image(panel, vbox, filename, size=None):
    base = os.path.dirname(__file__)
    path = os.path.join(base, filename)
    img = wx.Image(path, type=wx.BITMAP_TYPE_ANY)

    if size:
        img = img.Scale(size[0], size[1], quality=wx.IMAGE_QUALITY_HIGH)

    bmp = wx.Bitmap(img)
    ctrl = wx.StaticBitmap(panel, bitmap=bmp)
    vbox.Add(ctrl, flag=wx.ALL | wx.CENTER, border=5)
    return ctrl


def add_checkbox(panel, vbox, label, default=False):
    hbox = wx.BoxSizer(wx.HORIZONTAL)
    ctrl = wx.CheckBox(panel, label=label)
    ctrl.SetValue(default)
    hbox.Add(ctrl, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)
    vbox.Add(hbox, flag=wx.ALL)
    return ctrl


RFgen().register()
