# Amazing game
import pygame
import random

from polylib import *

class Screens():
    def __init__(self, name, bg_image):
        self.name = name
        self.background = pygame.image.load(bg_image)
        self.background = pygame.transform.scale(self.background, screen.get_size())
        self.level_borders = None
        self.level_grains = None
        self.level_houses = None
        self.is_level = False
        
    def get_image(self):
        return self.background
    
    def load_borders(self, fname):
        self.level_borders = gamepolyline_from_file(fname)
        
    def load_grains(self, fname):
        self.level_grains = dots_from_file(fname)

    def load_houses(self, fname):
        self.level_houses = dots_from_file(fname)
        
    def get_grains(self):
        return self.level_grains

    def get_houses(self):
        return self.level_houses
        
    def setup_level(self, i):
        self.load_borders("levels/level%d.pgl"%i)
        self.load_houses("levels/level%d.hs"%i)
        self.load_grains("levels/level%d.gr"%i)
        self.is_level = True
        
#def draw_quill(x,y, quill_size):
    #Draw quill at location
    #Does rect start at top left
#    quill_rect.update(x,(y-quill_size[1]), 100, 100)
#    screen.blit(quill_scaled, quill_rect)
    

if __name__ == "__main__":
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    screen_width = screen.get_size()[0]
    screen_height = screen.get_size()[1]
    
    clock = pygame.time.Clock()
    running = True
    gameplay_loop = True
    dt = 0
    editor_mode = False
    gpl = GamePolyLine()
    deal_lines = []
    active_line = [None]
    draw_speed = 100
    scores = []
    score = 0

    global_div = Division()
    divisions = []
    
    # define the RGB value for white,
    #  green, blue colour .
    font = pygame.font.Font('resources/times.ttf', 64)
    any_key_font = pygame.font.Font('resources/times.ttf', 24)
    credits = font.render('Thanks for playing', True, 'black')
    credits2 = font.render('Game developed by RentedBlackForge Studios', True, 'black')
    credits3 = font.render('Your final score was:', True, 'black')
    credits_rect = credits.get_rect()
    credits2_rect = credits2.get_rect()
    credits3_rect = credits3.get_rect()
    
    scoretext = font.render('Your score was:', True, 'black')
    score_rect = scoretext.get_rect()
    score_pos = ((((screen_width // 2) - (score_rect.width // 2))),screen_height // 3)

    any_key = any_key_font.render('Press any key to continue', True, 'black')
    instructions = any_key_font.render('Move the quill with arrow keys, press q to quit', True, 'black')
    instructions_rect = instructions.get_rect()
    quit_key = any_key_font.render('Press q key to quit', True, 'black')
    any_key_rect = any_key.get_rect()
    any_key_pos = ((((screen_width // 2) - (any_key_rect.width // 2) + 10)),screen_height - 50)
    
    
    #For saving
    fname = "path.pgl"
    fname_house = "houses.hs"
    fname_grain = "grains.gr"
    
    
    peasant_size=(200,200)
    happy_peasant = pygame.image.load("resources/peasanthappyTP.png")
    happy_peasant_scaled = pygame.transform.scale(happy_peasant, peasant_size)
    neutral_peasant = pygame.image.load("resources/peasantneutralTP.png")
    neutral_peasant_scaled = pygame.transform.scale(happy_peasant, peasant_size)
    angry_peasant = pygame.image.load("resources/peasantangryTP.png")
    angry_peasant_scaled = pygame.transform.scale(angry_peasant, peasant_size)
    peasant_rect = happy_peasant_scaled.get_rect()
    
    grain_img = pygame.image.load("resources/Wheat1.png")
    grain_size = (50,50)
    grain_scaled = pygame.transform.scale(grain_img, grain_size)
    grain_rect = grain_scaled.get_rect()
    
    house_img = pygame.image.load("resources/House1.png")
    house_size = (50,50)
    house_scaled = pygame.transform.scale(house_img, house_size)
    house_rect = house_scaled.get_rect()
    
    
    #backrect = background.get_rect(center=(background.get_height() / 2, background.get_width() / 2))
    #backrect = background.get_rect(center=(500,500))
    backrect = pygame.Rect((0,0),screen.get_size())
    #quill_rect = quill_scaled.get_rect()


    screen.fill("purple")
 #   screen.blit(peasant_happy_scaled, pygame.Rect(600,360,100,100))
      
    screens = []
    screens.append(Screens("welcome", "resources/IntroScreen1.5.png"))
    screens.append(Screens("instructions", "resources/Tutorial1.png"))
    screens.append(Screens("level0", "resources/Level0NoBorder.png"))
    screens.append(Screens("scoreboard", "resources/Background.png"))
    screens.append(Screens("level1", "resources/CatNoBorderNoHouse.png"))
    screens.append(Screens("scoreboard2", "resources/Background.png"))
    screens.append(Screens("level2", "levels/Level2.png"))
    screens.append(Screens("scoreboard3", "resources/Background.png"))
    screens.append(Screens("level3", "levels/Level3.png"))
    screens.append(Screens("scoreboard4", "resources/Background.png"))
    screens.append(Screens("level4", "levels/Level4.png"))
    screens.append(Screens("thankyouscreenandcredits", "resources/Background.png"))
    screen_iterator=0
    screens[2].setup_level(0)
    screens[4].setup_level(1)
    screens[6].setup_level(2)
    screens[8].setup_level(3)
    screens[10].setup_level(4)
    
        
    clicks = [False, False]
    houses = []
    grains = []
    
    screen.fill("black")
    screen.blit(screens[screen_iterator].get_image(), backrect)
    screen.blit(any_key, any_key_pos)
                

    pygame.display.flip()
    
#    quill_pos = (0,0)
    drawer = Drawer((0,0))
    pygame.key.set_repeat()
    
    #Welcome and intro screens
    while running:
        for event in pygame.event.get():    
            if event.type == pygame.KEYDOWN:
                screen_iterator=screen_iterator+1
                if screen_iterator > 1:
                    running = False              
                if event.key == pygame.K_q:
                    pygame.quit()
                
        screen.blit(screens[screen_iterator].get_image(), backrect)
        if screen_iterator == 0:
            screen.blit(any_key, any_key_pos)
        
        pygame.display.flip()
        
    running = True
    gpl = screens[screen_iterator].level_borders
    houses = screens[screen_iterator].get_houses()
    grains = screens[screen_iterator].get_grains()
    gameplay_loop = True
    score = 0
    global_div = Division()
    global_div.circ_gpl = gpl
    current_div = global_div
    global_div.houses = houses
    global_div.grains = grains
    #This should remove old lines
    deal_lines = []

    while running:
        #print("You are not in the game yet")
    #Tähän level infon lataus ja scoreruutu levelin jälkeen
        for event in pygame.event.get():    
            if event.type == pygame.KEYDOWN:
         #       print("you should escape to the game")
                screen_iterator=screen_iterator+1
                gpl = screens[screen_iterator].level_borders
                houses = screens[screen_iterator].get_houses()
                grains = screens[screen_iterator].get_grains()
                gameplay_loop = True
                score = 0    
                global_div = Division()
                global_div.circ_gpl = gpl
                current_div = global_div
                global_div.houses = houses
                global_div.grains = grains
                #This should remove old lines
                deal_lines = []
                #Remove this
                #print(screen_iterator,houses)
                
                
        #This is the game loop
        while gameplay_loop and screens[screen_iterator].is_level:
            
                        
            if len(gpl.lines) > 0 and drawer.on_border:
                curr_line = gpl.lines[drawer.border_idx]
                drawer.pos,drawer.border_t = curr_line.move_object_along(drawer.pos,{'t' : drawer.border_t, 'speed' : draw_speed, 'dt' : dt})
                if drawer.border_t >= 1.0:
                    drawer.border_idx += 1
                    drawer.border_t = 0.0
                    if drawer.border_idx == len(gpl.lines):
                        drawer.border_idx = 0
            if not drawer.on_border:
                
                drawer.prev_pos = drawer.pos
                drawer.pos = (drawer.dir[0] * draw_speed*dt + drawer.pos[0],
                              drawer.dir[1] * draw_speed*dt + drawer.pos[1])
                collided = False
                if not drawer.just_left_border:
                    for igl,gl in enumerate(gpl.lines):
                        if check_crossing(gl,drawer.prev_pos,drawer.pos):
                            collided = True
                            selfcollision = False
                            collide_idx = igl
                    for dl in deal_lines:
                        for gl in dl.lines:
                            if check_crossing(gl,drawer.prev_pos,drawer.pos):
                                collided = True
                                selfcollision = False
                                collide_idx = random.randint(0,len(gpl.lines)-1)
                    for igl in range(len(active_line[0].lines)-2):
                        gl = active_line[0].lines[igl]
                        if check_crossing(gl,drawer.prev_pos,drawer.pos):
                            collided = True
                            selfcollision = True
                            collide_idx = random.randint(0,len(gpl.lines)-1)
                    if collided:
                        drawer.on_border = True
                        drawer.border_idx = collide_idx
                        drawer.return_to_line(gpl.lines[collide_idx])
                        if not selfcollision:
                            deal_lines.append(active_line[0])                    
                            new_divs = create_new_division(current_div.circ_gpl,deal_lines)
                            if type(new_divs) != type(None):
                                baddiv, h1, h2 = divide_houses(current_div,new_divs[0],new_divs[1])
                                #print(baddiv,h1,h2)
                                if not baddiv:
                                    current_div.d1 = new_divs[0]
                                    current_div.d2 = new_divs[1]
                                    current_div.d1.houses = h1
                                    current_div.d2.houses = h2
                                    for idiv,div in enumerate(new_divs):
                                        for h in houses:
                                            if div.encircles_point(h):
                                                print(h," in div ",idiv)
                                else:
                                    deal_lines.pop()
                            else:
                                # it was not a proper line, let's eject it
                                deal_lines.pop()
                        active_line[0] = None
                    
                else:
                    drawer.just_left_border = False
                    current_div = global_div.get_encircling_child(drawer.pos)
                    print(current_div)
                if type(active_line[0]) != type(None):
                    active_line[0].lines[-1].p_end = drawer.pos
            ended = check_if_ended(global_div)
            if ended:
                score = score_areas(global_div)
                scores.append(score)
                gameplay_loop = False
                screen_iterator = screen_iterator + 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and drawer.dir[1] != 1:
                        drawer.dir = (0,-1)
                        active_line[0] = tracing_event(drawer,gpl,active_line[0])
                    if event.key == pygame.K_DOWN and drawer.dir[1] != -1:
                        drawer.dir = (0,1)
                        active_line[0] = tracing_event(drawer,gpl,active_line[0])
                    if event.key == pygame.K_LEFT and drawer.dir[0] != 1:
                        drawer.dir = (-1,0)
                        active_line[0] = tracing_event(drawer,gpl,active_line[0])
                    if event.key == pygame.K_RIGHT and drawer.dir[0] != -1:
                        drawer.dir = (1,0)
                        active_line[0] = tracing_event(drawer,gpl,active_line[0])
                    if event.key == pygame.K_s:
                        gpl.save(fname)
                        dots_to_file(fname_house,houses)
                        dots_to_file(fname_grain,grains)
                    if event.key == pygame.K_l:
                        gpl = gamepolyline_from_file(fname)
                        clicks[1] = gpl.lines[-1].p_end
                        houses = dots_from_file(fname_house)
                        grains = dots_from_file(fname_grain)
                    if event.key == pygame.K_u:
                        gpl.lines.pop()
                        clicks[1] = gpl.lines[-1].p_end
                    if event.key == pygame.K_g:
                        grains.append(pygame.mouse.get_pos())
                        print(global_div.encircles_point(pygame.mouse.get_pos()))
                    if event.key == pygame.K_a:
                        print(calc_total_area(gpl))
                    if event.key == pygame.K_h:
                        houses.append(pygame.mouse.get_pos())
                   #Remove this, or change to editor mode               
                    if event.key == pygame.K_q:
                        screen_iterator = len(screens) + 1
                        gameplay_loop = False
                        running = False
                        
                    if event.key == pygame.K_p:
                        if editor_mode == False:
                            editor_mode = True
                        elif editor_mode == True:
                            editor_mode = False
                                        
                if event.type == pygame.MOUSEBUTTONUP:
                    if clicks[1]:
                        clicks[0] = clicks[1]
                    clicks[1] = pygame.mouse.get_pos()
                    if clicks[0]:
                        gl = GameLine(clicks[0],clicks[1])
                        gpl.add_line(gl)
            #This should contain the end condition
            screen.fill("black")
            screen.blit(screens[screen_iterator].get_image(), backrect)            
            screen.blit(instructions, ((screen_width // 3) - instructions_rect[0], screen_height - 50))
            
            gpl.draw(screen,specs={'color':'red','width':1})
            if type(active_line[0]) != type(None):
                active_line[0].draw(screen,specs={'color':'white','width':3})
            for dl in deal_lines:
                dl.draw(screen,specs={'color':'black','width':3})
            
            for house in houses:
                screen.blit(house_scaled, ((house[0] - 25),(house[1] - 25)), house_rect)
            for grain in grains:
                screen.blit(grain_scaled, ((grain[0]), (grain[1] - 50)), grain_rect)
                #Remove this
                #pygame.draw.circle(screen,'blue',grain,2)
            drawer.draw(screen)
            pygame.display.flip()
            dt = clock.tick(60) / 1000
            #Level loop ends here
            
            #Score screen should be here
        if screens[screen_iterator].is_level == False:
            screen.fill("black")
            screen.blit(screens[3].get_image(), backrect)        
            scorenum = font.render('%d/100'%score, True, 'black')
            screen.blit(scoretext, score_pos)
            screen.blit(scorenum, (screen_width // 2, score_pos[1] + 50))
            screen.blit(any_key, any_key_pos)        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameplay_loop = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        screen_iterator = len(screens) + 1
                        
                if False:
                    if event.key == pygame.K_UP:
                        screen.blit(peasant_happy_scaled, (640,360), peasant_rect)
                    if event.key == pygame.K_DOWN:
                        screen.blit(peasant_angry_scaled, (640,360), peasant_rect)
                    if event.key == pygame.K_LEFT:
                        screen.blit(peasant_neutral_scaled, (640,360), peasant_rect)
                        

                # flip() the display to put your work on screen
    #            gpl.draw(screen,specs={'color':'black','width':1})
    #            draw_quill(quill_pos[0], quill_pos[1], quill_size)
    #            for h in houses:
    #                pygame.draw.circle(screen,'black',h,radius=3)
    #            for g in grains:
    #                pygame.draw.circle(screen,'red',g,radius=4)

            pygame.display.flip()

            # limits FPS to 60
            # dt is delta time in seconds since last frame, used for framerate-
            # independent physics.
        dt = clock.tick(60) / 1000
        if screen_iterator + 1 == (len(screens)):
                while running:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            screen.fill("black")
                            screen.blit(screens[3].get_image(), backrect)
                            screen.blit(credits, ((screen_width // 2) - (credits_rect.width // 2), screen_height // 3 - 75))
                            screen.blit(credits2, ((screen_width // 2) - (credits2_rect.width // 2), screen_height // 3))
                            screen.blit(credits3, ((screen_width // 2) - (credits3_rect.width // 2), screen_height // 3 + 150))
                            #remove this
                            #print(scores)
                            total_score = 0
                            for s in scores:
                                total_score = total_score + s
                                
                            scorenum = font.render('%d'%total_score, True, 'black')
                            screen.blit(scorenum, ((screen_width // 2, ((screen_height // 3) + 225))))
                            
                            screen.blit(quit_key, any_key_pos)
                            pygame.display.flip()
                            #print something like q to quit
                            if event.key == pygame.K_q:
                                running = False
            

    pygame.quit()


