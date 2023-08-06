from tkinter import *


class GFG:
    def __init__(self, master=None):
        self.canvas = None
        self.master = master
        self.create()

    def create(self):
        self.canvas = Canvas(self.master)

        def draw_gui():
            def draw_os_panel():
                def _main():
                    self.canvas.create_text(290, 15, fill="black", font=("Arial", 12),
                                            text="Operating System")
                    self.canvas.create_line(0, 30, 700, 30)

                def _data():
                    self.canvas.create_text(35, 40, fill="black", font=("Arial", 10),
                                            text="os name: ")
                    self.canvas.create_text(39, 55, fill="black", font=("Arial", 10),
                                            text="os version: ")
                    self.canvas.create_text(41, 70, fill="black", font=("Arial", 10),
                                            text="linux distro: ")
                    self.canvas.create_text(42, 85, fill="black", font=("Arial", 10),
                                            text="os platform: ")
                    self.canvas.create_text(40, 100, fill="black", font=("Arial", 10),
                                            text="os release: ")
                    self.canvas.create_text(53, 115, fill="black", font=("Arial", 10),
                                            text="os architecture: ")
                    self.canvas.create_text(38, 130, fill="black", font=("Arial", 10),
                                            text="os uptime: ")

                _main()
                _data()

            def draw_cpu_panel():
                def _main():
                    self.canvas.create_line(0, 140, 700, 140)
                    self.canvas.create_text(290, 155, fill="black", font=("Arial", 12),
                                            text="CPU")
                    self.canvas.create_line(0, 170, 700, 170)

                def _data():
                    self.canvas.create_text(38, 180, fill="black", font=("Arial", 10),
                                            text="cpu model: ")
                    self.canvas.create_text(53, 195, fill="black", font=("Arial", 10),
                                            text="cpu clockspeed: ")
                    self.canvas.create_text(54, 210, fill="black", font=("Arial", 10),
                                            text="cpu architecture: ")
                    self.canvas.create_text(72, 225, fill="black", font=("Arial", 10),
                                            text="cpu processor number: ")
                    self.canvas.create_text(38, 240, fill="black", font=("Arial", 10),
                                            text="cpu usage: ")
                    self.canvas.create_text(55, 255, fill="black", font=("Arial", 10),
                                            text="cpu temperature: ")
                    self.canvas.create_text(46, 270, fill="black", font=("Arial", 10),
                                            text="cpu vendor id: ")

                _main()
                _data()

            def draw_gpu_panel():
                def _main():
                    self.canvas.create_line(0, 280, 700, 280)
                    self.canvas.create_text(290, 295, fill="black", font=("Arial", 12),
                                            text="GPU")
                    self.canvas.create_line(0, 310, 700, 310)

                def _data():
                    self.canvas.create_text(38, 320, fill="black", font=("Arial", 10),
                                            text="gpu id: ")
                    self.canvas.create_text(53, 335, fill="black", font=("Arial", 10),
                                            text="gpu name: ")
                    self.canvas.create_text(54, 350, fill="black", font=("Arial", 10),
                                            text="gpu load: ")
                    self.canvas.create_text(72, 365, fill="black", font=("Arial", 10),
                                            text="gpu total memory: ")
                    self.canvas.create_text(38, 380, fill="black", font=("Arial", 10),
                                            text="gpu free memory: ")
                    self.canvas.create_text(55, 395, fill="black", font=("Arial", 10),
                                            text="gpu used memory: ")
                    self.canvas.create_text(46, 410, fill="black", font=("Arial", 10),
                                            text="gpu temperature: ")

                _main()
                _data()

            def draw_ram_panel():
                def _main():
                    self.canvas.create_line(0, 420, 700, 420)
                    self.canvas.create_text(290, 435, fill="black", font=("Arial", 12),
                                            text="RAM")
                    self.canvas.create_line(0, 450, 700, 450)

                def _data():
                    self.canvas.create_text(38, 460, fill="black", font=("Arial", 10),
                                            text="ram total memory: ")
                    self.canvas.create_text(53, 475, fill="black", font=("Arial", 10),
                                            text="ram manufacturer: ")
                    self.canvas.create_text(54, 490, fill="black", font=("Arial", 10),
                                            text="ram serial number: ")
                    self.canvas.create_text(72, 505, fill="black", font=("Arial", 10),
                                            text="ram memory type: ")
                    self.canvas.create_text(38, 520, fill="black", font=("Arial", 10),
                                            text="ram form factor: ")
                    self.canvas.create_text(55, 535, fill="black", font=("Arial", 10),
                                            text="ram clockspeed: ")
                    self.canvas.create_text(46, 550, fill="black", font=("Arial", 10),
                                            text="ram usage: ")

                _main()
                _data()

            def draw_storage_panel():
                def _main():
                    self.canvas.create_line(0, 560, 700, 560)
                    self.canvas.create_text(290, 575, fill="black", font=("Arial", 12),
                                            text="Storage")
                    self.canvas.create_line(0, 590, 700, 590)

                def _data():
                    self.canvas.create_text(38, 600, fill="black", font=("Arial", 10),
                                            text="drive_list: ")
                    self.canvas.create_text(53, 615, fill="black", font=("Arial", 10),
                                            text="total space: ")
                    self.canvas.create_text(54, 630, fill="black", font=("Arial", 10),
                                            text="used_space: ")
                    self.canvas.create_text(72, 645, fill="black", font=("Arial", 10),
                                            text="free space: ")
                    self.canvas.create_text(38, 660, fill="black", font=("Arial", 10),
                                            text="used space percent: ")
                    self.canvas.create_text(55, 675, fill="black", font=("Arial", 10),
                                            text="drive fstype: ")
                    self.canvas.create_text(46, 690, fill="black", font=("Arial", 10),
                                            text="drive mountpoint: ")

                _main()
                _data()

            draw_os_panel()
            draw_cpu_panel()
            draw_gpu_panel()
            draw_ram_panel()
            draw_storage_panel()

        draw_gui()
        self.canvas.pack(fill=BOTH, expand=True)


if __name__ == "__main__":
    root = Tk()
    geeks = GFG(root)
    root.title("pysil system information library gui extension")
    root.geometry("600x700")
    root.resizable(False, False)
    root.mainloop()
