import PIL
from PIL import Image, ImageDraw
from tkinter import *
import matplotlib.pyplot as plt
import numpy as np


class DoodleInput():
    def __init__(self) -> None:
        width = 300  # canvas width
        height = 300 # canvas height
        center = height//2
        white = (255, 255, 255) # canvas back

        self.drawing_coords = []
        self.coords = None

        self.root = Tk()

        # create a tkinter canvas to draw on
        self.canvas = Canvas(self.root, width=width, height=height, bg='white')
        self.canvas.pack()

        # create an empty PIL image and draw object to draw on
        self.output_image = PIL.Image.new("RGB", (width, height), white)
        self.draw = ImageDraw.Draw(self.output_image)
        self.canvas.pack(expand=YES, fill=BOTH)
        self.canvas.bind("<B1-Motion>", self.paint)

        # add buttons to save or submit the image
        button_save=Button(text="save",command=self.save).pack(side=LEFT)
        button_submit=Button(text="submit",command=self.submit).pack(side=RIGHT)

        self.root.mainloop()

    def save(self):
        coords = np.asarray(self.drawing_coords.copy())
        coords[:,1] = -coords[:,1] + 300
        np.savetxt('draw_coords.csv', coords, delimiter=",")
        return coords
    
    def submit(self):
        coords = np.asarray(self.drawing_coords.copy())
        coords[:,1] = -coords[:,1] + 300
        self.root.destroy()
        self.coords = coords
        return coords

    def paint(self, event):
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        self.drawing_coords.append((x1, y2))
        self.canvas.create_oval(x1, y1, x2, y2, fill="black",width=5)
        self.draw.line([x1, y1, x2, y2],fill="black",width=5)

    def plot(self, coords):
        plt.plot(coords[:,0], coords[:,1])
        plt.show()


if __name__ == "__main__":
    di = DoodleInput()
