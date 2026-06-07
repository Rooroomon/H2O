import pygame
from scripts.slope import Slope
from scripts.electro import Electro_Object
from scripts.power import PowerSource
from scripts.temperature import TemperatureObject

# =========================
# 파일 로드
# =========================
tile_sheet = pygame.image.load("./assets/Sprite/Tile_Sheet.png")
electro_sheet = pygame.image.load("./assets/Sprite/Electronic_Sheet.png")
goal_sprite = pygame.image.load("./assets/Sprite/Goal.png")
start_sprite = pygame.image.load("./assets/Sprite/StartPoint.png")


# =========================
# 스프라이트 설정
# =========================
tiles = []
wires = []
FRAME_W, FRAME_H = 8, 8
COLS = 6
TILE_SIZE = 64

for i in range(30):
    row, col = divmod(i, COLS)
    rect = pygame.Rect(col * FRAME_W, row * FRAME_H, FRAME_W, FRAME_H)
    tiles.append(pygame.transform.scale(tile_sheet.subsurface(rect), (TILE_SIZE, TILE_SIZE)))
    
wires.append(pygame.transform.scale(electro_sheet.subsurface((8, 0, 8, 8)), (TILE_SIZE, TILE_SIZE)))
wires.append(pygame.transform.scale(electro_sheet.subsurface((16, 0, 8, 8)), (TILE_SIZE, TILE_SIZE)))
wires.append(pygame.transform.scale(electro_sheet.subsurface((24, 0, 8, 8)), (TILE_SIZE, TILE_SIZE)))
wires.append(pygame.transform.scale(electro_sheet.subsurface((8, 8, 8, 8)), (TILE_SIZE, TILE_SIZE)))
wires.append(pygame.transform.scale(electro_sheet.subsurface((16, 8, 8, 8)), (TILE_SIZE, TILE_SIZE)))
wires.append(pygame.transform.scale(electro_sheet.subsurface((24, 8, 8, 8)), (TILE_SIZE, TILE_SIZE)))
    
goal_sprite = pygame.transform.scale(goal_sprite, (TILE_SIZE * 3, TILE_SIZE * 5))
start_sprite = pygame.transform.scale(start_sprite, (TILE_SIZE * 2, TILE_SIZE * 5))

#├ : 1, 조명 왼쪽 끝
#→ : 2, 조명 중간
#┤ : 3, 조명 오른쪽 끝
#┬ : 0, 기둥 위쪽 끝
#│ : 6, 기둥 중간
#┴ : 12, 기둥 아래쪽 끝
#┌ : 7, 왼쪽 벽 위쪽 끝
#↑ : 13, 왼쪽 벽
#└ : 19, 왼쪽 벽 아래쪽 끝
#┐ : 9, 오른쪽 벽 위쪽 끝
#↓ : 15, 오른쪽 벽
#┘ : 21, 오른쪽 벽 아래쪽 끝
#← : 18, 바닥
#. : 8, 흰 바탕
#0 : 4, 화면 밖
#' : 24, 발판 단일
#『 : 25, 발판 왼쪽 끝
#= : 26, 발판 중간
#』 : 27, 발판 오른쪽 끝
#S : 개별, 시작점
#G : 개별, 골
#C : X, 클리어 판정 범위
#X : X, 빈칸
## : X, 투명 벽

#특수 오브젝트
#H, C : 온도 오브젝트
#B : 배터리
#D : 빛 감지기
#P : 발판
#┌┐└┘─│ : 전선

MAP1 = [
    "X#├→→→┤├→→→┤├→→→┤├→→→┤├→→→┤├→→→┤#XX",
    "X#↑......┬.........┬.........┬.↓#XX",
    "X#↑......│.........│.........│.↓#XX",
    "X#↑......│.........│.........│.↓#XX",
    "X#↑......│....←←←←←←←←.......│.↓###",
    "S#↑......│....00000000.......│.↓GC#",
    "X#↑......│....00000000.......│.↓CC#",
    "X#↑......┴....00000000.......│.↓CC#",
    "X#↑....←←←←...00000000.......┴.┘CC#",
    "←←←←←←←####←←←00000000←←←←←←←←←←←←#",
]
Special1 = [
    "...................................",
    "...................................",
    ".........................←B........",
    "...................................",
    "...................................",
    "...................................",
    "...................................",
    "...................................",
    "............H......................",
    "...................................",
]

MAP2 = [
    "0├→→→┤├→→→┤├→→→┤├→→→┤0",
]
Special2 = [
    "...................................",
    "...................................",
    "...................................",
    "...................................",
    "...................................",
    "...................................",
    "...................................",
    "...................................",
    "...................................",
    "...................................",]

MAP3 = [
    "0├→→→┤├→→→┤├→→→┤├→→→┤0",
]
Special3 = [
    "...................................",
    "...................................",
    "...................................",
    "...................................",
    "...................................",
    "...................................",
    "...................................",
    "...................................",
    "...................................",
    "...................................",]


Map_List = [MAP1, MAP2, MAP3]

Special_List = [Special1, Special2, Special3]

TILE_INFO = {
    "├": {"index": 1, "solid": "Wall"},
    "→": {"index": 2, "solid": "Wall"},
    "┤": {"index": 3, "solid": "Wall"},
    "0": {"index": 17, "solid": "Wall"},

    "┬": {"index": 0, "solid": "None"},
    "│": {"index": 6, "solid": "None"},
    "┴": {"index": 12, "solid": "None"},

    "┌": {"index": 7, "solid": "None"},
    "↑": {"index": 13, "solid": "None"},
    "└": {"index": 19, "solid": "None"},

    "┐": {"index": 9, "solid": "None"},
    "↓": {"index": 15, "solid": "None"},
    "┘": {"index": 21, "solid": "None"},

    "←": {"index": 18, "solid": "Wall"},
    
    ".": {"index": 8, "solid": "None"},

    "'": {"index": 24, "solid": "Wall"},
    "『": {"index": 25, "solid": "Wall"},
    "=": {"index": 26, "solid": "Wall"},
    "』": {"index": 27, "solid": "Wall"},
    
    "S": {"index": 4, "solid": "None"},
    "G": {"index": 4, "solid": "None"},
    "X": {"index": -1, "solid": "None"},
    "C": {"index": -1, "solid": "None"},
    "#": {"index": -1, "solid": "Wall"},
    
    "1": {"index": 8, "solid": "None"},
    "2": {"index": 8, "solid": "None"},
    "3": {"index": 8, "solid": "None"},
    "4": {"index": 8, "solid": "None"},
    "5": {"index": 8, "solid": "None"},
    "6": {"index": 8, "solid": "None"},
    "7": {"index": 8, "solid": "None"},
    "8": {"index": 8, "solid": "None"},
    "9": {"index": 8, "solid": "None"},
}

def get_wall(index):
    map_data = Map_List[index]
        
    wall_rects = []
    for y, row in enumerate(map_data):
        for x, tile in enumerate(row):
            if TILE_INFO[tile]["solid"] == "Wall":
                wall_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                
    clear_rects = []
    for y, row in enumerate(map_data):
        for x, tile in enumerate(row):
            if tile == "C":
                clear_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                
    return wall_rects, clear_rects

def get_slopePair(target, y, x):
    found_pair = None
        
    # 현재 위치 이후부터 탐색
    for yy in range(y, len(MAP1)):
        start_x = x + 1 if yy == y else 0
        
        for xx in range(start_x, len(MAP1[yy])):
            if MAP1[yy][xx] == target:
                
                if x < xx:
                    xx += 1
                    return Slope(x * 64, y * 64, xx * 64, yy * 64)
                else:
                    x += 1
                    return Slope(xx * 64, yy * 64, x * 64, y * 64)
                    
    return None        
        
    

class TileMap:
    def __init__(self):
        self.map_data = MAP1
        self.special_data = Special1
        self.wall_rects, self.clear_rects = get_wall(0)
        self.wire_index = []

        self.width = len(self.map_data[0])
        self.height = len(self.map_data)
        
    def change_map(self, index):
        self.map_data = Map_List[index]
        self.special_data = Special_List[index]
        self.wall_rects, self.clear_rects = get_wall(0)
        found = 0b0
        slope_List = []
        power_List = []
        temp_List = []
        
        for y, row in enumerate(self.map_data):
            for x, ch in enumerate(row):
                if ch.isdigit() and ch != "0" and found & (0b1<<int(ch)) == 0:   # 1~9 발견
                    
                    found |= (0b1<<int(ch))
                    result = get_slopePair(ch, y, x)
                    
                    if result != None:
                        slope_List.append(result)
                        
        for y, row in enumerate(self.special_data):
            for x, tile in enumerate(row):
                if tile == "B":
                    object = PowerSource(x * TILE_SIZE, y * TILE_SIZE, "battery")
                    self.set_target(object)
                    power_List.append(object)
                elif tile == "D":
                    object = PowerSource(x * TILE_SIZE, y * TILE_SIZE, "detector")
                    self.set_target(object)
                    power_List.append(object)
                elif tile == "P":
                    object = PowerSource(x * TILE_SIZE, y * TILE_SIZE, "plate")
                    self.set_target(object)
                    power_List.append(object)
                elif tile == "H":
                    object = TemperatureObject(x * TILE_SIZE, y * TILE_SIZE, "hot")
                    temp_List.append(object)
                elif tile == "C":
                    object = TemperatureObject(x * TILE_SIZE, y * TILE_SIZE, "cold")
                    temp_List.append(object)
                    
                        
        return slope_List, power_List, temp_List
                    
        

    # 맵 범위 체크
    def in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    # 특정 타일 가져오기
    def get_tile(self, type, x, y):
        x = int(x)
        y = int(y)
        if not self.in_bounds(x, y):
            return None
        
        if type == "map":
            return self.map_data[y][x]
        else:
            return self.special_data[y][x]

    # 벽, 바닥 확인
    def test_solid(self, x, y):
        tile = self.get_tile("map", x, y)

        if tile is None:
            return "None"
        
        return TILE_INFO[tile]["solid"]

    # 타일 -> 픽셀
    def tile_to_world(self, x, y):
        return (
            x * TILE_SIZE,
            y * TILE_SIZE
        )

    # 픽셀 -> 타일
    def world_to_tile(self, px, py):
        return (
            px // TILE_SIZE,
            py // TILE_SIZE
        )
    
    def set_target(self, power): #전력원에서 이어진 오브젝트 탐색
        x = power.rect.x
        y = power.rect.y
        visited = [pygame.math.Vector2((x//TILE_SIZE), (y//TILE_SIZE))]
        now_pos = pygame.math.Vector2((x//TILE_SIZE), (y//TILE_SIZE))
        finding_pos = now_pos + pygame.math.Vector2(0, 1)
        first = now_pos.copy()
        second = now_pos - pygame.math.Vector2(0, 1)

        while(first != second):
            for dir in [pygame.math.Vector2(0, 1), pygame.math.Vector2(1, 0), pygame.math.Vector2(0, -1), pygame.math.Vector2(-1, 0)]:
                finding_pos = now_pos + dir

                if finding_pos in visited:
                    continue
                
                tile = self.get_tile("special", finding_pos.x, finding_pos.y)
                if tile in ["┌", "┐", "└", "┘", "─", "│"]: #이어진 전선 찾음
                    visited.append(finding_pos.copy())
                    now_pos += dir
                    break
                elif tile in ["↑", "→", "↓", "←"]: #선풍기 찾음
                    if tile == "↑":
                        power.target = Electro_Object(finding_pos.x * TILE_SIZE, finding_pos.y * TILE_SIZE, "fan", "up")
                        return
                    elif tile == "→":
                        power.target = Electro_Object(finding_pos.x * TILE_SIZE, finding_pos.y * TILE_SIZE, "fan", "right")
                        return
                    elif tile == "↓":
                        power.target = Electro_Object(finding_pos.x * TILE_SIZE, finding_pos.y * TILE_SIZE, "fan", "down")
                        return
                    elif tile == "←":
                        power.target = Electro_Object(finding_pos.x * TILE_SIZE, finding_pos.y * TILE_SIZE, "fan", "left")
                        return
            second = first.copy()
            first = finding_pos.copy()
    
    
    def draw(self, screen, camera_x, camera_y, SCREEN_W, SCREEN_H):
        # 카메라 기준 화면 시작 위치
        start_x = camera_x - SCREEN_W / 2
        start_y = camera_y - SCREEN_H / 2
    
        # 화면에 보이는 타일 범위 계산
        first_tile_x = (int)(max(0, start_x // TILE_SIZE))
        first_tile_y = (int)(max(0, start_y // TILE_SIZE))
    
        last_tile_x = (int)(min(self.width, (start_x + SCREEN_W) // TILE_SIZE + 2))
        last_tile_y = (int)(min(self.height, (start_y + SCREEN_H) // TILE_SIZE + 2))
    
        # 보이는 타일만 렌더링
        for y in range(first_tile_y, last_tile_y):
            for x in range(first_tile_x, last_tile_x):
                
                tile = self.map_data[y][x]
                special_tile = self.special_data[y][x]
                
                # 월드 좌표
                world_x, world_y = self.tile_to_world(x, y)
    
                # 카메라 적용한 화면 좌표
                screen_x = world_x - start_x
                screen_y = world_y - start_y
                
                map_image = tiles[4]
                wire_image = None
                if tile != None and tiles[TILE_INFO[tile]["index"]] != -1:
                    if tile == "S" or tile == "G": # 시작, 골 지점
                        map_image = start_sprite if tile == "S" else goal_sprite
                    else:
                        map_image = tiles[TILE_INFO[tile]["index"]]
                        
                    screen.blit(map_image, (screen_x, screen_y))
                
                if special_tile != None:
                    if special_tile == "┌":
                        wire_image = wires[0]
                    elif special_tile == "┐":
                        wire_image = wires[1]
                    elif special_tile == "└":
                        wire_image = wires[3]
                    elif special_tile == "┘":
                        wire_image = wires[4]
                    elif special_tile == "─":
                        wire_image = wires[2]
                    elif special_tile == "│":
                        wire_image = wires[5]
                        
                    if wire_image != None:
                        screen.blit(wire_image, (screen_x, screen_y))
                
    
                
    
                
                
        