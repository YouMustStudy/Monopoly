from pico2d import*
from main_state import CENTER
from game_framework import frame_time
import game_framework
import building_state
import main_state

class Player:
    def __init__(self, x, y, shape):
        self.index=3 #현 위치
        self.x = x
        self.y = y
        self.money=4000 #총자산
        self.cash=4000 #현자산
        self.image = None
        if shape == 'p':
            self.image = load_image('.\\character\\pig.png')
        elif shape == 's':
            self.image = load_image('.\\character\\skeleton.png')
        self.status = IdleState
        self.frame = 0
        self.move = 0
        self.round = 1 #몇바퀴 돌았는지 | 업그레이드 가능한 건물 종류

    def draw(self):
        self.status.draw(self)

    def update(self):
        self.status.do(self)

    def rotate(self, theta):
        theta=math.radians(theta)
        self.x-=CENTER[0]
        self.y-=CENTER[1]
        tmp_x, tmp_y = self.x, self.y
        self.x=tmp_x*math.cos(theta) - tmp_y*math.sin(theta)
        self.y=tmp_x*math.sin(theta) + tmp_y*math.cos(theta)
        self.x+=CENTER[0]
        self.y+=CENTER[1]

    def change_state(self, state):
        self.status.exit(self)
        self.status = state
        self.status.enter(self)

class IdleState:
    @staticmethod
    def enter(player):
        player.frame = 0
    @staticmethod
    def exit(player):
        pass
    @staticmethod
    def do(player):
        if player.move > 0:
            player.change_state(RunState)
    @staticmethod
    def draw(player):
        player.image.clip_draw(player.frame * 20, 0, 20, 20, player.x, player.y)
class RunState:
    @staticmethod
    def enter(player):
        player.frame = 0
    @staticmethod
    def exit(player):
        pass
    @staticmethod
    def do(player):
        player.frame = (player.frame+1) % 2
        player.x += game_framework.frame_time * 70 * 3
        player.x = clamp(main_state.MAP[player.index].x, player.x, main_state.MAP[player.index+1].x)
        if player.x == main_state.MAP[player.index+1].x:
            player.index = (player.index + 1) % 28
            player.move -= 1
            #월급 시스템 추가
            if(player.index == 0):
                player.cash += 600
                player.money += 600
            if main_state.MAP[player.index].theta > 0:
                player.change_state(SpinState)
            elif player.move == 0:
                player.change_state(IdleState)
                #도착 후 이벤트 처리
                if(player.index % 7 == 0): #큰타일 - 특수이벤트
                    pass
                elif(player.index == 9 or player.index == 24): #찬스카드
                    pass
                elif(main_state.MAP[player.index].owner == -1 or main_state.MAP[player.index].owner == main_state.PLAYER_TURN): #땅주인이 없거나 본인이 주인이면
                    game_framework.push_state(building_state) #건설상태로 분기


    @staticmethod
    def draw(player):
        player.image.clip_draw(player.frame * 20 + 20, 0, 20, 20, player.x, player.y)
class SpinState:
    @staticmethod
    def enter(player):
        player.frame = 0
    @staticmethod
    def exit(player):
        pass
    @staticmethod
    def do(player):
        player.frame = (player.frame+1) % 2
        if main_state.MAP[player.index].theta > 0:
            theta = min(main_state.MAP[player.index].theta, 180 * game_framework.frame_time)
            player.rotate(-theta)
            main_state.rotate_map(-theta)
            print(main_state.MAP[player.index].theta)
        else:
            main_state.fix_map()
            player.change_state(IdleState)

    @staticmethod
    def draw(player):
        player.image.clip_draw(player.frame * 20 + 20, 0, 20, 20, player.x, player.y)