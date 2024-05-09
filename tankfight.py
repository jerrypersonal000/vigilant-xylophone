import streamlit as st
import random
import time

# 设置游戏区域大小
GAME_SIZE = 10

# 初始化位置
player_position = [GAME_SIZE // 2, GAME_SIZE - 1]
enemy_position = [GAME_SIZE // 2, 0]
bullet_position = None
enemy_bullet_position = None

# 游戏状态
game_over = False

def move_player(direction):
    global player_position
    if direction == 'left' and player_position[0] > 0:
        player_position[0] -= 1
    elif direction == 'right' and player_position[0] < GAME_SIZE - 1:
        player_position[0] += 1
    elif direction == 'up' and player_position[1] > 0:
        player_position[1] -= 1
    elif direction == 'down' and player_position[1] < GAME_SIZE - 1:
        player_position[1] += 1

def shoot():
    global bullet_position
    bullet_position = player_position[:]

def move_enemy():
    direction = random.choice(['left', 'right', 'none'])
    if direction == 'left' and enemy_position[0] > 0:
        enemy_position[0] -= 1
    elif direction == 'right' and enemy_position[0] < GAME_SIZE - 1:
        enemy_position[0] += 1

def enemy_shoot():
    global enemy_bullet_position
    if random.random() > 0.8:
        enemy_bullet_position = enemy_position[:]

def update_game():
    global game_over, bullet_position, enemy_bullet_position
    if bullet_position:
        bullet_position[1] -= 1
        if bullet_position[1] < 0:
            bullet_position = None
    if enemy_bullet_position:
        enemy_bullet_position[1] += 1
        if enemy_bullet_position[1] >= GAME_SIZE:
            enemy_bullet_position = None

    if bullet_position and bullet_position == enemy_position:
        st.sidebar.success("You hit the enemy!")
        game_over = True
    if enemy_bullet_position and enemy_bullet_position == player_position:
        st.sidebar.error("You were hit by the enemy!")
        game_over = True

st.sidebar.button("Left", on_click=move_player, args=('left',))
st.sidebar.button("Right", on_click=move_player, args=('right',))
st.sidebar.button("Up", on_click=move_player, args=('up',))
st.sidebar.button("Down", on_click=move_player, args=('down',))
st.sidebar.button("Shoot", on_click=shoot)

while not game_over:
    move_enemy()
    enemy_shoot()
    update_game()
    time.sleep(0.5)  # 控制游戏更新速度

    # 绘制游戏界面
    board = [[" " for _ in range(GAME_SIZE)] for _ in range(GAME_SIZE)]
    board[player_position[1]][player_position[0]] = 'P'
    board[enemy_position[1]][enemy_position[0]] = 'E'
    if bullet_position:
        board[bullet_position[1]][bullet_position[0]] = '*'
    if enemy_bullet_position:
        board[enemy_bullet_position[1]][enemy_bullet_position[0]] = '*'

    st.write("\n".join("".join(row) for row in board))

if game_over:
    st.write("Game Over!")
