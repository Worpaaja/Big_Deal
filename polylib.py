import pygame
import math
import random
 
class GamePolyLine():
    def __init__(self):
        self.lines = []
    def add_line(self,gameline):
        self.lines.append(gameline)
    def draw(self,display,specs):
        for gl in self.lines:
            gl.draw(display,specs)
    def save(self,fname):
        s = ''
        for l in self.lines:
            s += ('%d,%d,%d,%d\n')%(l.p_start[0],l.p_start[1],l.p_end[0],l.p_end[1])
        with open(fname,'w') as fhandle:
            fhandle.write(s)
    def reverse(self):
        self.lines.reverse()
        for igl in range(len(self.lines)):
            self.lines[igl] = GameLine(self.lines[igl].p_end,self.lines[igl].p_start)
 
class GameLine():
    def __init__(self,p_start,p_end):
         self.p_start = p_start
         self.p_end = p_end
         self.len = math.sqrt((p_end[0] - p_start[0])**2 + (p_end[1] - p_start[1])**2)
         self.invec = pygame.math.Vector2(-(p_end[1] - p_start[1]),p_end[0]-p_start[0])
         try:
             self.invec = self.invec / self.invec.magnitude()
         except ZeroDivisionError:
             self.invec = self.invec
         
    def draw(self,display,specs):
        #draw this with specs
        color = specs['color']
        width = specs['width']
        pygame.draw.line(display, color, self.p_start, self.p_end, width)
        
    def move_object_along(self,pos,specs):
        #move the object along the gameline with speed defined in specs
        speed = specs['speed']
        dt = specs['dt']
        t_orig = specs['t']
        dist = speed * dt
        t = t_orig + dist/self.len
        if t > 1.0:
            t = 1.0
        new_pos = (t * (float(self.p_end[0]) - float(self.p_start[0])) + self.p_start[0],
                   t * (float(self.p_end[1]) - float(self.p_start[1])) + self.p_start[1])
        return (new_pos, t)
    def save_str(self):
        return '%d,%d,%d,%d' % (int(self.p_start[0]),int(self.p_start[1]),int(self.p_end[0]),int(self.p_end[1]))
    def recalc_invec(self):
        self.invec = pygame.math.Vector2(-(p_end[1] - p_start[1]),p_end[0]-p_start[0])
        try:
            self.invec = self.invec / self.invec.magnitude()
        except ZeroDivisionError:
            self.invec = self.invec
        
def gameline_from_str(string):
    l = list(map(int,string.split(',')))
    return GameLine((l[0],l[1]),(l[2],l[3]))

def gamepolyline_from_file(fname):
    gpl = GamePolyLine()
    with open(fname) as fhandle:
        lines = fhandle.readlines()
    for l in lines:
        gpl.add_line(gameline_from_str(l))
    return gpl

def dots_from_file(fname):
    li = []
    with open(fname) as fhandle:
        lines = fhandle.readlines()
    for l in lines:
        ls = l.split(',')
        li.append((int(ls[0]),int(ls[1])))
    return li
    
def dots_to_file(fname,li):
    s = ''
    for l in li:
        s += '%d,%d\n' % (l[0],l[1])
    with open(fname,'w') as fhandle:
        fhandle.write(s)
        
        
def check_crossing(gl,pos1,pos2):
    # NOTE: this piece of work is borrowed from other project...
    # this is to check if pos1 and pos2 are on the different sides of 
    # gameline gl
    x1 = gl.p_start[0]
    y1 = gl.p_start[1]
    x2 = gl.p_end[0]
    y2 = gl.p_end[1]
    x3 = pos1[0]
    y3 = pos1[1]
    x4 = pos2[0]
    y4 = pos2[1]
    den = (x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4)
    if abs(den) < 1e-6:
        # denominator is zero: lines are parallel
        return False
    nom_x = (x1*y2 - y1*x2)*(x3 - x4) - (x1 - x2)*(x3*y4 - y3*x4)
    nom_y = (x1*y2 - y1*x2)*(y3 - y4) - (y1 - y2)*(x3*y4 - y3*x4)

    intersect = pygame.math.Vector2(nom_x / den, nom_y / den)
    l1v1 = pygame.math.Vector2(gl.p_start[0],gl.p_start[1])
    l1v2 = pygame.math.Vector2(gl.p_end[0],gl.p_end[1])
    l2v1 = pygame.math.Vector2(pos1[0],pos1[1])
    l2v2 = pygame.math.Vector2(pos2[0],pos2[1])
    if ((intersect - l1v1).dot(l1v2-l1v1) > 0.0
    and (intersect - l2v1).dot(l2v2-l2v1) > 0.0
    and (intersect - l1v2).dot(l1v2-l1v1) < 0.0
    and (intersect - l2v2).dot(l2v2-l2v1) < 0.0):
        # each of these dot products check if the intersection is
        # in the proper direction of each of the segment endpoints
        return True
    else:
        return False
    
class Drawer():
    def __init__(self,pos):
        self.pos = pos
        self.prev_pos = (0,0)
        self.on_border = True
        self.border_idx = 0
        self.border_t = 0.0
        self.dir = (0,0)
        self.icon = pygame.image.load("resources/QuillCrop.png")
        self.icon = pygame.transform.scale(self.icon, (100,100))
        
    def draw(self,display):
        quill_pos = self.pos
        display.blit(self.icon, (quill_pos[0], quill_pos[1] - 100))
#        pygame.draw.circle(display,'red',self.pos,10)

    def return_to_line(self,gl):
        # just find an adequate t...
        n = 100
        maxdist = 1e9
        self.dir = (0,0)
        for i in range(n):
            t = i/n
            new_pos = (t * (float(gl.p_end[0]) - float(gl.p_start[0])) + gl.p_start[0],
                       t * (float(gl.p_end[1]) - float(gl.p_start[1])) + gl.p_start[1])
            dist = math.sqrt((new_pos[0] - self.pos[0])**2 + (new_pos[1] - self.pos[1])**2)
            if dist < maxdist:
                self.border_t = t
                maxdist = dist
                
def check_if_indir(dirr,gl):
    dirvec = pygame.math.Vector2(dirr[0],dirr[1])
    return gl.invec.dot(dirvec) < 0
    
def start_tracing(drawer):
    drawer.on_border = False
    drawer.just_left_border = True
    new_trace = GamePolyLine()
    new_trace.lines.append(GameLine(drawer.pos,drawer.pos))
    return new_trace
    
def tracing_event(drawer,gpl,apl):
    if drawer.on_border and check_if_indir(drawer.dir,gpl.lines[drawer.border_idx]):
        apl = start_tracing(drawer)
    elif not drawer.on_border:
        apl = continue_tracing(drawer,apl)
    return apl
        
def continue_tracing(drawer,apl):
    apl.lines.append(GameLine(drawer.pos,drawer.pos))
    return apl
    
def calc_total_area(gpl):
    #shoelace formula
    summ = 0.0
    for i in range(len(gpl.lines)):
        gl = gpl.lines[i]
        summ += (gl.p_start[1] + gl.p_end[1]) * (gl.p_start[0] - gl.p_end[0])
    A = abs(0.5 * summ)
    return A
    
    #https://www.geeksforgeeks.org/binary-tree-in-python/
class Division():
    def __init__(self):
        self.d1 = None
        self.d2 = None
        self.grains = []
        self.houses = []
        self.area = 0.0
        self.circ_gpl = None

    def encircles_point(self,p):
        max_size = 2000
        crosses = []
        for l in self.circ_gpl.lines:
            crosses.append(0)
            beam_target = (0.5 * (l.p_start[0] + l.p_end[0]), 0.5 * (l.p_start[1] + l.p_end[1]))
            beam_vec = pygame.math.Vector2(beam_target[0] - p[0],beam_target[1] - p[1])
            beam_vec = beam_vec / beam_vec.magnitude()
            beam_end = max_size * beam_vec + pygame.math.Vector2(p[0], p[1])
            p_end = (beam_end[0], beam_end[1])
            for k in self.circ_gpl.lines:
                if check_crossing(k,p,p_end):
                    crosses[-1] += 1
        tally = 0
        for crosamt in crosses:
            if crosamt % 2 == 0:
                # parillinen lukema crossingeja -> indikaattori että ulkona.
                tally -= 1
            else:
                # pariton lukema crossingeja -> sit ollaanki sisällä
                tally += 1
        return tally > 0
    def get_encircling_child(self,p):
        if type(self.d1) != type(None):
            if self.d1.encircles_point(p):
                return self.d1.get_encircling_child(p)
            else:
                return self.d2.get_encircling_child(p)
        else:
            return self
    def house_product(self):
        if type(self.d1) != type(None):
            return self.d1.house_product() * self.d2.house_product()
        else:
            return len(self.houses)
        
    def calc_area(self):
        self.area = calc_total_area(self.circ_gpl)
        
    def house_score(self):
        self.calc_area()
        return (self.houses[0],self.area,len(self.grains))
        
def check_if_ended(globdiv):
    endnum = globdiv.house_product()
    return endnum == 1
            
def find_point_on_gpl(gpl,point):
    # gets the closest point on GamePolyLine 
    n = 100
    maxdist = 1e9
    t = 0.0
    idx = 0
    for igl,gl in enumerate(gpl.lines):
        for i in range(n):
            t_ = i/n
            new_pos = (t_ * (float(gl.p_end[0]) - float(gl.p_start[0])) + gl.p_start[0],
                       t_ * (float(gl.p_end[1]) - float(gl.p_start[1])) + gl.p_start[1])
            dist = math.sqrt((new_pos[0] - point[0])**2 + (new_pos[1] - point[1])**2)
            if dist < maxdist:
                t = t_
                maxdist = dist
                idx = igl
    return (idx,t)
    
def get_next_point_bordercollie_deal(idx1,t1,idx2,t2,gpl):
    if idx1 == idx2 and t1 < t2:
        # they are on the same gameline
        return (idx2,t2)
    else:
        idx = idx1 + 1 if idx1 + 1 < len(gpl.lines) else 0
        t = 0.0
        return (idx,t)
    
def get_point_on_gpl(idx,t,gpl):
    gl = gpl.lines[idx]
    pos = (t * (float(gl.p_end[0]) - float(gl.p_start[0])) + gl.p_start[0],
           t * (float(gl.p_end[1]) - float(gl.p_start[1])) + gl.p_start[1])
    return pos
    
def create_new_division(gpl,deal_lines):

    idx1,t1 = find_point_on_gpl(gpl,deal_lines[-1].lines[0].p_start)
    idx2,t2 = find_point_on_gpl(gpl,deal_lines[-1].lines[-1].p_end)
    
    # tämä kelataan oikein päin
    print(len(gpl.lines))
    print(idx2)
    start_pos2 = get_point_on_gpl(idx2,t2,gpl)
    d2 = GamePolyLine()
    current_pos = start_pos2
    curr_idx = idx2
    curr_t = t2
    print(curr_idx,curr_t)
    while not (curr_t == t1 and curr_idx == idx1):
        curr_idx,curr_t = get_next_point_bordercollie_deal(curr_idx,curr_t,idx1,t1,gpl)
        next_pos = get_point_on_gpl(curr_idx,curr_t,gpl)
        d2.add_line(GameLine(current_pos,next_pos))
        current_pos = next_pos
    for igl,gl in enumerate(deal_lines[-1].lines):
        d2.add_line(gl)
    d1 = GamePolyLine()
    # tämä pitää kelata nurinkurin
    start_pos1 = get_point_on_gpl(idx1,t1,gpl)
    curr_idx = idx1
    curr_t = t1
    while not (curr_t == t2 and curr_idx == idx2):
        curr_idx,curr_t = get_next_point_bordercollie_deal(curr_idx,curr_t,idx2,t2,gpl)
        next_pos = get_point_on_gpl(curr_idx,curr_t,gpl)
        d1.add_line(GameLine(current_pos,next_pos))
        current_pos = next_pos
    deal_lines[-1].reverse()
    for igl,gl in enumerate(deal_lines[-1].lines):
        d1.add_line(gl)
    div1 = Division()
    div1.circ_gpl = d1
    div2 = Division()
    div2.circ_gpl = d2
    return (div1,div2)
        
def get_areas(div,scorelist):
    if type(div.d1) != type(None):
        get_areas(div.d1,scorelist)
        get_areas(div.d2,scorelist)
    else:
        scorelist.append(div.house_score())
        
def score_areas(globdiv):
    tot_houses = len(globdiv.houses)
    globdiv.calc_area()
    total_area = globdiv.area
    scorelist = []
    get_areas(globdiv,scorelist)
    #print(scorelist)
    #for s in scorelist:
    #    print(s[1]/total_area)
    scores = []
    for t in scorelist:
        scores.append((100*t[1] / total_area) * (1 + t[2]))
    return 100 - (max(scores) - min(scores))
    #for i,a in enumerate(areas):
    #    print(i,a[0],a[1],total_area)
    
def divide_houses(pardiv,div1,div2):
    h1 = []
    h2 = []
    for h in pardiv.houses:
        if div1.encircles_point(h):
            h1.append(h)
        else:
            h2.append(h)
    if len(h1) * len(h2) == 0:
        bad_division = True
    else:
        bad_division = False
    return (bad_division,h1,h2)

def divide_grains(pardiv,div1,div2):
    g1 = []
    g2 = []
    for g in pardiv.grains:
        if div1.encircles_point(g):
            g1.append(g)
        else:
            g2.append(g)
    div1.grains = g1
    div2.grains = g2
    
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    screen.fill("purple")
    clock = pygame.time.Clock()
    running = True
    dt = 0
    gpl = GamePolyLine()
    deal_lines = []
    active_line = [None]
    global_div = Division()
    global_div.circ_gpl = gpl
    current_div = global_div
    houses = []
    grains = []
    clicks = [False, False]
    drawer = Drawer((0,0))
    pygame.key.set_repeat()
    draw_speed = 100
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        fname = 'path.pgl'
        fname_house = 'houses.hs'
        fname_grain = 'grain.gr'
        
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
                            print(baddiv,h1,h2)
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
            running = False
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
                    global_div.circ_gpl = gpl
                    clicks[1] = gpl.lines[-1].p_end
                    houses = dots_from_file(fname_house)
                    global_div.houses = houses
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
            if event.type == pygame.MOUSEBUTTONUP:
                if clicks[1]:
                    clicks[0] = clicks[1]
                clicks[1] = pygame.mouse.get_pos()
                if clicks[0]:
                    gl = GameLine(clicks[0],clicks[1])
                    gpl.add_line(gl)
                #print(gpl.lines)
        # flip() the display to put your work on screen
        
        # fill the screen with a color to wipe away anything from last frame
        screen.fill("purple")
        
        #pygame.draw.circle(screen, "red", player_pos, 40)
        gpl.draw(screen,specs={'color':'white','width':1})
        if type(active_line[0]) != type(None):
            active_line[0].draw(screen,specs={'color':'white','width':1})
        for dl in deal_lines:
            dl.draw(screen,specs={'color':'white','width':1})
        for h in houses:
            pygame.draw.circle(screen,'black',h,radius=3)
        for g in grains:
            pygame.draw.circle(screen,'red',g,radius=4)
        drawer.draw(screen)
        pygame.display.flip()

        
        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000
    score_areas(global_div)
    pygame.quit()
        
