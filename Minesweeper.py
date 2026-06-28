# # # music

# 9 * 9    10
# 16 * 16    40
# 30 * 16    99
if __name__ == '__main__':
    import os
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
    import pygame, pygame.locals, sys, webbrowser, random, intervals
    import tkinter as tk
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)

    WIDTH, HEIGHT, TITLE = 1600, 900, 'Minesweeper'

    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    lime = (0, 255, 0)
    blue = (0, 0, 255)
    yellow = (255, 255, 0)
    cyan = (0, 255, 255)
    magenta = (255, 0, 255)
    silver = (192, 192, 192)
    maroon = (128, 0, 0)
    olive = (128, 128, 0)
    navy = (0, 0, 128)
    purple = (128, 0, 128)
    grey = (128, 128, 128)
    teal = (0, 128, 128)
    green = (0, 255, 0)
    violet = (238, 130, 238)

    pygame.init()
    mainwindow = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    FPS = pygame.time.Clock()
    FPS.tick(60)

    explosions = pygame.image.load_animation('explosion.gif')
    # # mainwindow = mainwindow.convert()
    # # mainwindow = mainwindow.convert_alpha()    USELESS
    background, bomb, flag = pygame.image.load('scene.png'), pygame.image.load('bomb.gif'), pygame.image.load('flag.gif')
    flag, bomb = pygame.transform.scale(flag, (50, 50)), pygame.transform.scale(bomb, (50, 50))
    BUTTONS = pygame.sprite.Group()

class texts(pygame.sprite.Sprite):
    def __init__(self, colour, font, size, content, width = 0, height = 0):
        super().__init__()
        self.text_col, self.colour1, self.colour2, self.out_col = colour
        self.ins_col = self.colour1
        self.request = pygame.font.SysFont(font, size)
        self.content = self.request.render(content, True, self.text_col)
        self.size = (width, height)
    def use(self, coordinate, surface):
        self.coordinate = coordinate
        surface.blit(self.content, self.coordinate)
class buttons(texts):
    def __init__(self, coordinate, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.coordinate = coordinate
        self.shape = self.content.get_rect(topleft = self.coordinate)
        self.shape2 = pygame.Surface(self.size)
        self.surface = mainwindow
        self.mine = None
        self.available = True
        self.flag = False
        BUTTONS.add(self)
    def default(self, draw = False):
        self.shape = self.content.get_rect(topleft = self.coordinate)
        if self.shape.collidepoint(pygame.mouse.get_pos()):
            self.ins_col = self.colour2
        else:
            self.ins_col = self.colour1
        if draw:
            pygame.draw.rect(self.surface, self.ins_col, self.shape)
        self.surface.blit(self.content, self.coordinate)
    def rectangle(self, rectangle, width = 0, border_radius = 0):#surface: the interface that you wanna draw on
        #rectangle: a bounding rectangle; a tuple with four elements(x, y, width, height)
        #width: the thickness of the outline; 0 is filled
        pygame.draw.rect(self.surface, self.ins_col, rectangle, 0, border_radius)
        if width:
            pygame.draw.rect(self.surface, self.out_col, rectangle, width, border_radius)
        self.coordinate = (rectangle[0], rectangle[1])
    def circle(self, centre, radius, width = 0):
        pygame.draw.circle(self.surface, self.ins_col, centre, radius, 0)
        if width:
            pygame.draw.circle(self.surface, self.out_col, centre, radius, width)
        self.coordinate = (centre[0] - radius, centre[1] - radius)
    def ellipse(self, rectangle, width = 0):
        pygame.draw.ellipse(self.surface, self.ins_col, rectangle, 0)
        if width:
            pygame.draw.ellipse(self.surface, self.out_col, rectangle, width)
        self.coordinate = (rectangle[0], rectangle[1])
    def polygon(self, points, width = 0):
        pygame.draw.polygon(self.surface, self.ins_col, points, 0)
        if width:
            pygame.draw.polygon(self.surface, self.out_col, points, width)
        self.coordinate = (points[0], points[1])
    def single_line(self, smooth, start_position, end_position, width = 1, blend = 1):
        if smooth:
            pygame.draw.aaline(self.surface, self.ins_col, start_position, end_position, blend)
        else:
            pygame.draw.line(self.surface, self.ins_col, start_position, end_position, width)
        self.coordinate = start_position
    def multiple_connected_lines(self, smooth, closed, points, width = 1, blend = 1):
        #closed: bool value, whether allowed to connect the first and the last point automatically
#         blend: If set to 1 or any non-zero value, the edge pixels of the line will be mixed (blended) with
#         the existing pixels on the screen. This creates the soft, smooth transition that eliminates jagged edges.
#         If set to 0, the line will simply overwrite the background pixels without any blending. In this case, you
#         won't get the intended smooth anti-aliasing effect.
#         In short, unless you have a very specific reason to turn it off, you usually just leave blend at its default value of 1 to enjoy perfectly smooth lines
        if smooth:
            pygame.draw.aalines(self.surface, self.ins_col, closed, points, blend)
        else:
            pygame.draw.lines(self.surface, self.ins_col, closed, points, width = 1)
        self.coordinate = (points[0], points[1])
    def arc(self, rectangle, start_angle, end_angle, width = 1):
        #it's the same as a section of the ellipse,
        #you need provide two angles so that the computer knows how to cut the ellipse
        pygame.draw.arc(self.surface, self.ins_col, rectangle, start_angle, end_angle, width)
        self.coordinate = (rectangle[0], rectangle[1])
class buttons2:
    def __init__(self, whotofollow, whotocall, abg, afg, x, y, reflection):
        self.reflection = reflection
        if self.reflection[0]:
            self.bg, self.fg = 'green', 'olive'
            self.bg2, self.fg2 = 'red', 'maroon'
        else:
            self.bg, self.fg = 'red', 'maroon'
            self.bg2, self.fg2 = 'green', 'olive'
        self.entity = tk.Button(set_window, text = 'open', bg = self.bg, fg = self.fg,
                                command = lambda: whotocall(self), height = 1, 
                                activebackground = abg, activeforeground = afg)
        self.entity.place(x = whotofollow.winfo_x() + whotofollow.winfo_width(), y = whotofollow.winfo_y())
        self.entity.update_idletasks()
        self.entity2 = tk.Button(set_window, text = 'close', bg = self.bg2, fg = self.fg2,
                                 command = lambda: whotocall(self), height = 1)
        self.entity2.place(x = self.entity.winfo_x() + self.entity.winfo_width(), y = self.entity.winfo_y())
    def soundoac(self):
        if self.entity.cget('bg') == 'green':
            self.entity['bg'] = 'red'
            self.entity.configure(fg = 'maroon')
            self.entity2['bg'] = 'green'
            self.entity2.configure(fg = 'olive')
            self.reflection[0] = 0
        elif self.entity.cget('bg') == 'red':
            self.entity['bg'] = 'green'
            self.entity.configure(fg = 'olive')
            self.entity2['bg'] = 'red'
            self.entity2.configure(fg = 'maroon')
            self.reflection[0] = 1

if __name__ == "__main__":
    title = texts((black, black, black, black), 'simhei', 70, TITLE)
    begin = buttons((WIDTH / 2.13, HEIGHT / 2.88), (red, teal, cyan, red), 'verdana', 40, 'Begin')
    instruction = buttons((WIDTH / 2.32, HEIGHT / 2.05), (blue, teal, cyan, blue), 'verdana', 40, 'Instructions')
    setting = buttons((WIDTH / 2.20, HEIGHT / 1.6), (green, teal, cyan, green), 'verdana', 40, 'Settings')
    feedback = buttons((WIDTH / 2.32, HEIGHT / 1.30), (yellow, teal, cyan, yellow), 'verdana', 40, 'Contact Us')

    class operation:
        def __init__(self):
            self.mouse_pressed = [False, False, False]
            self.MUSIC, self.times, self.mines, self.phase, self.count, self.singleframe = [1], 1, [], 0, 0, 1000 / 14
            self.a, self.flags, self.records = 1, 0, {'HARD': [], 'MEDIUM': [], 'EASY': []}
            self.back_alpha = buttons((int(WIDTH / 2.7), int(HEIGHT / 3)), (maroon, lime, magenta, black), 'erasitc',
                                     50, 'Back to Start Menu')
            self.back_beta = buttons((int(WIDTH / 3.1), int(HEIGHT / 2)), (maroon, lime, magenta, black), 'erasitc',
                                    50, 'Back to Difficulty Selection')
            self.back_gamma = buttons((int(WIDTH / 2.5), int(HEIGHT / 1.5)), (maroon, lime, magenta, black), 'erasitc',
                                     50, 'Restart Game')
            self.status = {'welcome': True, 'selection': False, 'in_game': False, 'defeat': False, 'victory': False}
            self.states = {'defeated': False, 'welcoming': False, 'selecting': False, 'gaming': False,
                           'victorious': False}
        def redo(self, method):
            for i in BUTTONS:
                i.kill()
            self.flags = 0
            for j in self.states:
                self.states[j] = False
            self.status[method] = True
        def defeat(self):
            self.states['defeated'], self.status['defeat'] = True, False
            while self.states['defeated']:
                for event in pygame.event.get():
                    if event.type == pygame.locals.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.locals.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            self.mouse_pressed[0] = True
                    else:
                        self.mouse_pressed[0] = False
                mainwindow.fill(red)
                gameover = texts((silver, silver, silver, silver), 'gadugi', HEIGHT // 9, 'GAME OVER')
                gameover.use(((WIDTH - gameover.content.get_width()) / 2, HEIGHT / 7), mainwindow)
                self.back_alpha.default(True)
                self.back_beta.default(True)
                self.back_gamma.default(True)
                if self.mouse_pressed[0]:
                    self.mouse_pressed[0] = False
                    if self.back_alpha.shape.collidepoint(pygame.mouse.get_pos()):
                        self.redo('welcome')
                        break
                    elif self.back_beta.shape.collidepoint(pygame.mouse.get_pos()):
                        self.redo('selection')
                        break
                    elif self.back_gamma.shape.collidepoint(pygame.mouse.get_pos()):
                        self.redo('in_game')
                        break
                pygame.display.update()
        def victory(self):
            self.states['victorious'], self.status['victory'], self.times = True, False, 1
            while self.states['victorious']:
                for event in pygame.event.get():
                    if event.type == pygame.locals.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.locals.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            self.mouse_pressed[0] = True
                    else:
                        self.mouse_pressed[0] = False
                mainwindow.fill(teal)
                success = texts((yellow, yellow, yellow, yellow), 'juiceitc', HEIGHT // 9, 'Success!')
                success.use(((WIDTH - success.content.width) / 2, HEIGHT / 7), mainwindow)
                self.back_alpha.default(True)
                self.back_beta.default(True)
                self.back_gamma.default(True)
                pygame.display.update()
                if self.mouse_pressed[0]:
                    self.mouse_pressed[0] = False
                    if self.back_alpha.shape.collidepoint(pygame.mouse.get_pos()):
                        self.redo('welcome')
                        break
                    elif self.back_beta.shape.collidepoint(pygame.mouse.get_pos()):
                        self.redo('selection')
                        break
                    elif self.back_gamma.shape.collidepoint(pygame.mouse.get_pos()):
                        self.redo('in_game')
                        break
                if self.times == 1:
                    self.records[self.mode].append(self.timecount)
                    vic = tk.Tk()#Toplevel
                    vic.title('record updated')
                    vic.geometry('640x360+640+360')
                    vic.resizable(False, False)
                    congratulations = tk.Label(vic, text = 'Your score has been recorded!', font = ('arial', 20))
                    vic.update_idletasks()
#                     congratulations.place(x = (vic.winfo_width() - congratulations.winfo_reqwidth()) / 2,
#                                           y = vic.winfo_height() / 5)
                    congratulations.place(relx = 0.08, rely = 0.2)
                    tk.Button(vic, text = 'confirm', command = vic.destroy).place(relx = 0.4, rely = 0.6)
                    vic.mainloop()
                    self.times += 1
        def detection(self, mine):
            mine.ins_col = tuple(int(c * 0.5) for c in mine.ins_col)
            mine.rectangle((mine.shape.x, mine.shape.y, self.mine_width, self.mine_height), 1)
            mine.default()
            mine.available = False
            for site in self.around:
                for M in self.mines:
                    if (M.shape.left == mine.shape.x + site[0] and M.mine and
                        mine.shape.y + site[1] in intervals.IntInterval.closed(M.shape.top - 1, M.shape.top + 1)):
                        self.count += 1
            if self.count != 0:
                counter = texts((red, red, red, red), 'arial', self.textsize, f'{self.count}')
                counter.use((mine.shape.left + (mine.shape.width - counter.content.width) / 2,
                                  mine.shape.top), mainwindow)
                self.count = 0
            else:
                for s in self.around:
                    for m in self.mines:
                        if (m.shape.left == mine.shape.x + s[0] and m.available and
                            mine.shape.y + s[1] in intervals.IntInterval.closed(m.shape.top - 1, m.shape.top + 1)):
                            self.detection(m)

        def welcome(self):
            global set_window
            self.status['welcome'], self.states['welcoming'] = False, True
            while self.states['welcoming']:
                phase = 1
                for event in pygame.event.get():
                    if event.type == pygame.locals.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.locals.KEYDOWN:
                        if event.key == pygame.locals.K_p:
                            print(pygame.mouse.get_pos())
                        if event.key == pygame.locals.K_m:
                            print(MUSIC)
                    if event.type == pygame.locals.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            self.mouse_pressed[0] = True
                    else:
                        self.mouse_pressed[0] = False
                mainwindow.blit(background, (0, 0))
                title.use((WIDTH / 2.56, HEIGHT / 7.2), mainwindow)
                begin.default(True)
                instruction.default(True)
                setting.default(True)
                feedback.default(True)
                #if pygame.mouse.get_pressed()[0]:
                if self.mouse_pressed[0] == True:
                    self.mouse_pressed[0] = False
                    if instruction.shape.collidepoint(pygame.mouse.get_pos()):
                        #pygame.Surface((int(WIDTH * 0.8), int(HEIGHT * 0.8)))
                        intro_window = tk.Tk()
                        intro_window.geometry(f'{str(int(WIDTH * 0.8))}x{str(int(HEIGHT * 0.8))}+\
{str(int((1920 - WIDTH * 0.8) / 2))}+{str(int((1080 - HEIGHT * 0.8) / 2))}')
                        intro_window.title("instructions")
                        introduction = tk.Text(intro_window, width = 150, height = 40, font = ('agencyfb', 15))
                        introduction.pack()
                        introduction.insert('1.0', '''                               Welcome to Minesweeper
                              Here are the regulations
            You can choose on of three difficulties: HARD, MEDIUM and EASY
HARD: 30 * 16 board  99 mines    MEDIUM: 16 * 16 board  40 mines
EASY: 9 * 9 board  10 mines

You can press Left Mouse Button to choose one square. If that isn't mine, you will get how many mines around it by the\
number displayed(the nine squares around it). Otherwise your character will die.

You can also press Right Mouse Button to mark a square. The marks limit is the same as the mines count.

There is no time limit.

Have fun!''')
                        intro_window.mainloop()
                    elif feedback.shape.collidepoint(pygame.mouse.get_pos()):
                        webbrowser.open('https://wiki.biligame.com/eft/Escape_from_Tarkov_Wiki/Trivia')
                        #open_new_tab, open_new    new browser window
                    elif setting.shape.collidepoint(pygame.mouse.get_pos()):
                        set_window = tk.Tk()
                        set_window.geometry(f'{str(int(WIDTH * 0.8))}x{str(int(HEIGHT * 0.8))}+\
{str(int((1920 - WIDTH * 0.8) / 2))}+{str(int((1080 - HEIGHT * 0.8) / 2))}')
                        set_window.title('settings')
                        Lsoundoac = tk.Label(set_window, text = 'sound', height = 1)
                        Lsoundoac.place(x = 0, y = 0)
                        Lsoundoac.update_idletasks()
                        Bsoundoac = buttons2(Lsoundoac, buttons2.soundoac, 'white', 'black', 0, 0, self.MUSIC)
                        Lflagcolour = tk.Label(set_window,
                                               text = 'flagcolour').place(x = Lsoundoac.winfo_x(),
                                                                          y = Lsoundoac.winfo_y() +
                                                                          Bsoundoac.entity.winfo_height())
                        set_window.mainloop()
                    elif begin.shape.collidepoint(pygame.mouse.get_pos()):
                        self.redo('selection')
                        break
                pygame.display.flip()      
        def selection(self):
            self.states['selecting'], self.status['selection'] = True, False
            while self.states['selecting']:
                phase = 2
                for event in pygame.event.get():
                    if event.type == pygame.locals.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.locals.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            self.mouse_pressed[0] = True
                    else:
                        self.mouse_pressed[0] = False
                background2 = pygame.image.load('scene2.jpg')
                mainwindow.blit(background2, (0, 0))
                difficulty = texts((navy, navy, navy, navy), 'castellar', 70, 'Difficulty Selection')
                difficulty.use((WIDTH / 4.5, HEIGHT / 5), mainwindow)
                
                hard_button = buttons((WIDTH / 2.15, HEIGHT / 3), (red, navy, olive, red), 'fangsong', 40, 'HARD')
                hard_button.default(True)
                medium_button = buttons((WIDTH / 2.2, HEIGHT / 2), (green, navy, olive, green), 'fangsong', 40,
                                        'MEDIUM')
                medium_button.default(True)
                easy_button = buttons((WIDTH / 2.15, HEIGHT / 1.5), (violet, navy, olive, violet), 'fangsong', 40,
                                      'EASY')
                easy_button.default(True)
                
                try:
                    hard_record = texts((black, black, black, black), 'arial', 40,
                                        f'best: {min(self.records["HARD"])} seconds')
                    hard_record.use((hard_button.shape.right, hard_button.shape.top), mainwindow)
                except:
                    pass
                try:
                    medium_record = texts((black, black, black, black), 'arial', 40,
                                          f'best: {min(self.records["MEDIUM"])} seconds')
                    medium_record.use((medium_button.shape.right, medium_button.shape.top), mainwindow)
                except:
                    pass
                try:
                    easy_record = texts((black, black, black, black), 'arial', 40,
                                        f'best: {min(self.records["EASY"])} seconds')
                    easy_record.use((easy_button.shape.right, easy_button.shape.top), mainwindow)
                except:
                    pass
                
                self.back_alpha.rectangle((WIDTH / 2.65, HEIGHT / 1.1, self.back_alpha.shape.width,
                                           self.back_alpha.shape.height))
                self.back_alpha.default()
                pygame.display.flip()
                if self.mouse_pressed[0]:
                    self.mouse_pressed[0] = False
                    if hard_button.shape.collidepoint(pygame.mouse.get_pos()):
                        self.mode = 'HARD'
                        self.redo('in_game')
                        break
                    elif medium_button.shape.collidepoint(pygame.mouse.get_pos()):
                        self.mode = 'MEDIUM'
                        self.redo('in_game')
                        break
                    elif easy_button.shape.collidepoint(pygame.mouse.get_pos()):
                        self.mode = 'EASY'
                        self.redo('in_game')
                        break
                    elif self.back_alpha.shape.collidepoint(pygame.mouse.get_pos()):
                        self.redo('welcome')
                        break
        def in_game(self):
            time_count, count_begin, firstmoment, self.times2 = 0, False, pygame.time.get_ticks(), 0
            self.status['in_game'], self.states['gaming'], self.times = False, True, 1
            self.mines.clear()
            while self.states['gaming']:
                phase, serial_number = 3, 0
                for event in pygame.event.get():
                    if event.type == pygame.locals.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.locals.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            self.mouse_pressed[0] = True
                        elif event.button == 2:
                            self.mouse_pressed[1] = True
                        elif event.button == 3:
                            self.mouse_pressed[2] = True
                    else:
                        self.mouse_pressed = [False, False, False]
                    if event.type == pygame.locals.KEYDOWN:
                        if event.key == pygame.locals.K_SPACE:
                            print(count_begin)
                if self.times == 1:
                    if self.mode == 'EASY':
                        minesum, x_axis, y_axis = 10, 9, 9
                    elif self.mode == 'HARD':
                        minesum, x_axis, y_axis = 99, 30, 16
                    elif self.mode == 'MEDIUM':
                        minesum, x_axis, y_axis = 40, 16, 16
                    self.mine_width, self.mine_height = WIDTH // 32, HEIGHT // 18
                    self.textsize, self.textlength = int(self.mine_height * 0.86), self.mine_width // 10
                    self.flagsum, self.last_moment, won = minesum, None, False
                    self.around = [(-self.mine_width, -self.mine_height), (0, -self.mine_height),
                                   (+self.mine_width, -self.mine_height), (-self.mine_width, 0),
                                   (+self.mine_width, 0), (-self.mine_width, +self.mine_height),
                                   (0, +self.mine_height), (+self.mine_width, +self.mine_height)]
                    mainwindow.fill(white)
                    for i in range(x_axis * y_axis):
                        x_sequence = serial_number % x_axis
                        y_sequence = serial_number // x_axis
                        x = self.mine_width * x_sequence + (WIDTH - self.mine_width * x_axis) / 2
                        y = self.mine_height * y_sequence
                        mine = buttons((x, y), (white, white, white, black), 'arial', self.textsize,
                                       self.textlength * ' ', self.mine_width, self.mine_height)
                        mine.rectangle((x, y, self.mine_width, self.mine_height), 1)
                        mine.default()
                        self.mines.append(mine)
                        self.times += 1
                        serial_number += 1
                    while minesum > 0:
                        destination = random.choice(self.mines)
                        if destination.mine == None:
                            destination.mine = True
                            minesum -= 1
                    for mine in self.mines:
                        if not mine.mine:
                            mine.mine = False
                
                self.back_alpha.rectangle((WIDTH / 9.5, HEIGHT - self.back_alpha.shape.height,
                                           self.back_alpha.shape.width, self.back_alpha.shape.height))
                self.back_alpha.default()
                self.back_beta.rectangle((WIDTH / 2.65, self.back_alpha.shape.y,
                                          self.back_beta.shape.width, self.back_beta.shape.height))
                self.back_beta.default()
                self.back_gamma.rectangle((WIDTH / 1.35, self.back_beta.shape.y,
                                           self.back_gamma.shape.width, self.back_gamma.shape.height))
                self.back_gamma.default()
                if count_begin:
                    if pygame.time.get_ticks() - firstmoment >= 100:
                        time_count += 0.1
                        firstmoment = pygame.time.get_ticks()
                self.timecount = str(round(time_count, 1))
                if len(self.timecount) <= 3:
                    self.timecount = '0' + self.timecount
                try:
                    pygame.draw.rect(mainwindow, white, (count.coordinate[0], count.coordinate[1],
                                                         count.content.width, count.content.height))
                except:
                    pass
                count = texts((red, red, red, red), 'arial', 40, self.timecount)
                count.use((0, HEIGHT - 46), mainwindow)
                
                for goal in self.mines:
                    if not goal.mine:
                        if not goal.available:
                                won = True
                        else:
                            won = False
                            break
                if won:
                    self.redo('victory')

                if self.mouse_pressed[0]:
                    self.mouse_pressed[0] = False
                    for mine in self.mines:
                        if mine.shape.collidepoint(pygame.mouse.get_pos()):
                            if not self.times2:
                                count_begin = True
                            if mine.mine:
                                first_moment = pygame.time.get_ticks()
                                while True:
                                    if not self.last_moment:
                                        for m in self.mines:
                                            if m.mine:
                                                mainwindow.blit(bomb, (m.shape.x, m.shape.y))
                                                m.available = False
                                        if pygame.time.get_ticks() - first_moment >= 2000:
                                            self.last_moment = pygame.time.get_ticks()
                                    if self.last_moment:
                                        serialframe = int((pygame.time.get_ticks() - self.last_moment) //
                                                          self.singleframe)
                                        if serialframe > len(explosions) - 1:
                                            break
                                        singleimage = pygame.transform.scale(explosions[serialframe][0],
                                                                             (self.mine_height, self.mine_height))
                                        for m in self.mines:
                                            if m.mine:
                                                mainwindow.blit(singleimage,
                                                                (m.shape.left +
                                                                (self.mine_width - singleimage.get_width()) / 2,
                                                                m.shape.top))
                                    pygame.display.update()
                                pygame.display.flip()
                                self.redo('defeat')
                                break
                            elif mine.available:
                                self.detection(mine)
                        elif self.back_alpha.shape.collidepoint(pygame.mouse.get_pos()):
                            self.redo('welcome')
                            break
                        elif self.back_beta.shape.collidepoint(pygame.mouse.get_pos()):
                            self.redo('selection')
                            break
                        elif self.back_gamma.shape.collidepoint(pygame.mouse.get_pos()):
                            self.redo('in_game')
                            break
                    self.times2 += 1
                elif self.mouse_pressed[1]:
                    self.mouse_pressed[1] = False
                    for mine in self.mines:
                        if mine.shape.collidepoint(pygame.mouse.get_pos()):
                            #print(self.mines.index(mine) + 1)
                            print(mine.shape.x, mine.shape.y)
                elif self.mouse_pressed[2]:
                    self.mouse_pressed[2] = False
                    for mine in self.mines:
                        if mine.shape.collidepoint(pygame.mouse.get_pos()):
                            if not mine.flag and self.flags < self.flagsum:
                                mainwindow.blit(flag, ((mine.shape.width - flag.get_width()) / 2 + mine.shape.x, mine.shape.y))
                                mine.flag = True
                                self.flags += 1
                            elif mine.flag:
                                mine.rectangle((mine.shape.x, mine.shape.y, mine.shape.width, mine.shape.height), 1)
                                mine.default()
                                mine.flag = False
                                self.flags -= 1             
                pygame.display.update()
            
    mainloop = operation()
# #     mainloop.status['victory'] = True
    while 1:
        if mainloop.status['welcome']:
            mainloop.welcome()
        elif mainloop.status['selection']:
            mainloop.selection()
        elif mainloop.status['defeat']:
            mainloop.defeat()
        elif mainloop.status['victory']:
            mainloop.victory()
        elif mainloop.status['in_game']:
            mainloop.in_game()