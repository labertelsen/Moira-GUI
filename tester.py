import tkinter as tk

window = tk.Tk()
window.state('zoomed')

class DragAndDropArea(tk.Canvas):
    def __init__(self,master, **kwargs):
        tk.Canvas.__init__(self,master, **kwargs)
        self.active = None

        card_I = self.draw_card(300,600, 100,100, 'red1')
        card_II = self.draw_card(600,600, 100,100, 'red2')
        card_III = self.draw_card(400,400, 100,100, 'red3')

        self.bind_tention(card_I,card_III)
        self.bind_tention(card_I,card_II)
        self.bind_tention(card_III,card_II)

        self.bind('<ButtonPress-1>', self.get_item)
        self.bind('<B1-Motion>',self.move_active)
        self.bind('<ButtonRelease-1>', self.set_none)
    def set_none(self,event):
        self.active = None
    def get_item(self,event):
        try:
            item =  self.find_withtag('current')
            self.active = item[0]
        except IndexError:
            print('no item was clicked')
    def move_active(self,event):
        if self.active != None:
            coords = self.coords(self.active)
            width = coords[2] - coords[0] #x2-x1
            height= coords[1] - coords[3] #y1-y2
            position = coords[0],coords[1]#x1,y1

            x1 = event.x - width/2
            y1 = event.y - height/2
            x2 = event.x + width/2
            y2 = event.y + height/2
            
            self.coords(self.active, x1,y1, x2,y2)
            try:
                self.update_tention(self.active)
            except IndexError:
                print('no tentions found')

    def update_tention(self, tag):
        tentions = self.find_withtag(f'card {tag}')
        for tention in tentions:
            bounded_cards = self.gettags(tention)
            card = bounded_cards[0].split()[-1]
            card2= bounded_cards[1].split()[-1]
            x1,y1 = self.get_mid_point(card)
            x2,y2 = self.get_mid_point(card2)
            self.coords(tention, x1,y1, x2,y2)
            self.lower(tention)

    def draw_card(self, x,y, width,height, color):
        x1,y1 = x,y
        x2,y2 = x+width,y+height
        reference = self.create_rectangle(x1,y1,x2,y2,
                                          fill = color)
        return reference
    def bind_tention(self, card, another_card):
        x1,y1 = self.get_mid_point(card)
        x2,y2 = self.get_mid_point(another_card)
        tag_I = f'card {card}'
        tag_II= f'card {another_card}'
        
        reference = self.create_line(x1,y1,x2,y2, fill='green',
                                     tags=(tag_I,tag_II))
        self.lower(reference)

    def get_mid_point(self, card):
        coords = self.coords(card)
        width = coords[2] - coords[0] #x2-x1
        height= coords[1] - coords[3] #y1-y2
        position = coords[0],coords[1]#x1,y1

        mid_x = position[0] + width/2
        mid_y = position[1] - height/2

        return mid_x,mid_y
        
area = DragAndDropArea(window, bg='white')
area.pack(fill='both',expand=1)
window.mainloop()