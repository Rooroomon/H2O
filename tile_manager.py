import pygame

# =========================
# 파일 로드
# =========================
tile_sheet = pygame.image.load("./assets/Sprite/Tile_Sheet.png")


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

MAP1 = [
    "0├→→→┤├→→→┤├→→→┤├→→→┤0",
    "0↑..................↓0",
    "0↑..................↓0",
    "0↑..................↓0",
    "0↑..................↓0",
    "0↑..................↓0",
    "0↑.........'........↓0",
    "0↑..................↓0",
    "0└..................┘0",
    "←←←←←←←←←←←←←←←←←←←←←←"
]

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

TILE_INFO = {
    "├": {"index": 1, "solid": "Wall"},
    "→": {"index": 2, "solid": "Wall"},
    "┤": {"index": 3, "solid": "Wall"},
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
}

class TileMap:
    def __init__(self):
        self.map_data = MAP1

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
    
    def draw(self, screen):
        for y, row in enumerate(self.map_data):
            for x, tile in enumerate(row):
                pos = self.tile_to_world(x, y)
                    
                if tile != None:
                    index = TILE_INFO[tile]["index"]
                    screen.blit(tiles[index], pos)