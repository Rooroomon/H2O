import pygame

# =========================
# 파일 로드
# =========================
tile_sheet = pygame.image.load("./assets/Sprite/Tile_Sheet.png")
Goal_Sprite = pygame.image.load("./assets/Sprite/Goal.png")
Start_Sprite = pygame.image.load("./assets/Sprite/StartPoint.png")


# =========================
# 스프라이트 설정
# =========================
tiles = []
FRAME_W, FRAME_H = 8, 8
COLS = 6
TILE_SIZE = 64

for i in range(30):
    row, col = divmod(i, COLS)
    rect = pygame.Rect(col * FRAME_W, row * FRAME_H, FRAME_W, FRAME_H)
    tiles.append(pygame.transform.scale(tile_sheet.subsurface(rect), (TILE_SIZE, TILE_SIZE)))
    
Goal_Sprite = pygame.transform.scale(Goal_Sprite, (TILE_SIZE * 3, TILE_SIZE * 5))
Start_Sprite = pygame.transform.scale(Start_Sprite, (TILE_SIZE * 2, TILE_SIZE * 5))

MAP1 = [
    "X0├→→→┤├→→→┤├→→→┤├→→→┤0XX",
    "X0↑..................↓0XX",
    "X0↑..................↓0XX",
    "X0↑..................↓0XX",
    "X0↑..................↓000",
    "S#↑..................↓GX0",
    "X#↑.........'........↓XX0",
    "X#↑..................↓XX0",
    "X#↑..................┘XX0",
    "←←←←←←←←←←←←←←←←←←←←←←←←0"
]

MAP2 = [
    "0├→→→┤├→→→┤├→→→┤├→→→┤0",
]

MAP3 = [
    "0├→→→┤├→→→┤├→→→┤├→→→┤0",
]

Map_List = [MAP1, MAP2, MAP3]

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
#X : 빈칸
## : 투명 배리어

TILE_INFO = {
    "├": {"index": 1, "solid": "Roof"},
    "→": {"index": 2, "solid": "Roof"},
    "┤": {"index": 3, "solid": "Roof"},
    "0": {"index": 17, "solid": "Wall"},

    "┬": {"index": 0, "solid": "None"},
    "┃": {"index": 6, "solid": "None"},
    "┴": {"index": 12, "solid": "None"},

    "┌": {"index": 7, "solid": "None"},
    "↑": {"index": 13, "solid": "None"},
    "└": {"index": 19, "solid": "None"},

    "┐": {"index": 9, "solid": "None"},
    "↓": {"index": 15, "solid": "None"},
    "┘": {"index": 21, "solid": "None"},

    "←": {"index": 18, "solid": "Ground"},

    ".": {"index": 8, "solid": "None"},

    "'": {"index": 24, "solid": "Ground"},
    "『": {"index": 25, "solid": "Ground"},
    "=": {"index": 26, "solid": "Ground"},
    "』": {"index": 27, "solid": "Ground"},
    
    "S": {"index": 4, "solid": "None"},
    "G": {"index": 4, "solid": "None"},
    "X": {"index": 4, "solid": "None"},
    "#": {"index": 4, "solid": "Wall"},
}

def get_wall(index):
    map_data = Map_List[index]
        
    wall_rects = []
    for y, row in enumerate(map_data):
        for x, tile in enumerate(row):
            if TILE_INFO[tile]["solid"] == "Wall":
                wall_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    
    ground_rects = []
    for y, row in enumerate(map_data):
        for x, tile in enumerate(row):
            if TILE_INFO[tile]["solid"] == "Ground":
                ground_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                
    roof_rects = []
    for y, row in enumerate(map_data):
        for x, tile in enumerate(row):
            if TILE_INFO[tile]["solid"] == "Roof":
                roof_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                
    return wall_rects, ground_rects, roof_rects

class TileMap:
    def __init__(self):
        self.map_data = MAP1
        self.wall_rects, self.ground_rects, self.roof_rects = get_wall(0)

        self.width = len(self.map_data[0])
        self.height = len(self.map_data)
        
        #경사 생성
        #for i in range(0, 10):
        #    text = str(i)
        #    for y, row in enumerate(self.map_data):
        #        for x, tile in enumerate(row):
        #            if get_tile(x, y) == text:
        
    

    # 맵 범위 체크
    def in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    # 특정 타일 가져오기
    def get_tile(self, x, y):
        if not self.in_bounds(x, y):
            return None

        return self.map_data[y][x]

    # 벽, 바닥 확인
    def test_solid(self, x, y):
        tile = self.get_tile(x, y)

        if tile is None:
            return "None"
        
        return TILE_INFO[tile]["solid"]
    
    # 목표지점인지
    def is_goal(self, x, y):
        return self.get_tile(x, y) == "G"

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
    
                if tile is None or tile == "X" or tile == "#":
                    continue
                
                image = tiles[4]
                if tile == "S" or tile == "G":
                    image = Start_Sprite if tile == "S" else Goal_Sprite
                else:
                    image = tiles[TILE_INFO[tile]["index"]]
    
                # 월드 좌표
                world_x, world_y = self.tile_to_world(x, y)
    
                # 카메라 적용한 화면 좌표
                screen_x = world_x - start_x
                screen_y = world_y - start_y
    
                screen.blit(image, (screen_x, screen_y))
                
        