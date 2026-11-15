import pygame 
from player import Player #Retrieves player class
from platform1 import Platform
from enemy import Enemy
from level import Level
from HUD import HUD
from mainMenu import MainMenu
from pauseMenu import PauseMenu
from leaderboard import Leaderboard
from settings import Settings
pygame.init() #Initalise pygame library
pygame.mixer.init() #Initialise sound mixer

#Clock
Clock = pygame.time.Clock() #Handles FPS of game

#Dimensions of screen
WIDTH = 1080
HEIGHT = 720

#Creates screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer Game") #Set name of window

#Main menu
titleImg = pygame.image.load("Assets/Free/Menu/Main menu/game title.png").convert_alpha()
startbuttonImg = pygame.image.load("Assets/Free/Menu/Main menu/new game button.png").convert_alpha()
leaderboardbuttonImg = pygame.image.load("Assets/Free/Menu/Main menu/leaderboard button.png").convert_alpha()
settingsbuttonImg = pygame.image.load("Assets/Free/Menu/Main menu/Settings.png").convert_alpha()
backgroundImg = pygame.image.load("Assets/Free/Menu/Main menu/Main menu background.jpg").convert_alpha()
MainMenuScreen = MainMenu(WIDTH, HEIGHT, titleImg, startbuttonImg, leaderboardbuttonImg, settingsbuttonImg, backgroundImg)

#Pause menu
pauseTitleImg = pygame.image.load("Assets/Free/Menu/Pause menu/title.png").convert_alpha()
resumeButtonImg = pygame.image.load("Assets/Free/Menu/Pause menu/resume.png").convert_alpha()
exitButtonImg = pygame.image.load("Assets/Free/Menu/Pause menu/exit.png").convert_alpha()
PauseMenuScreen = PauseMenu(WIDTH, HEIGHT, pauseTitleImg, resumeButtonImg, exitButtonImg, settingsbuttonImg)

#Leaderboard
leaderboardbgImg = pygame.image.load("Assets/Free/Menu/Leaderboard/leaderboardBG.jpg").convert_alpha()
leaderboardTitleImg = pygame.image.load("Assets/Free/Menu/Leaderboard/title.png").convert_alpha()
leaderboardPanelImg = pygame.image.load("Assets/Free/Menu/Leaderboard/panel.png").convert_alpha()
goldMedalImg = pygame.image.load("Assets/Free/Menu/Leaderboard/goldmedal.png").convert_alpha()
silverMedalImg = pygame.image.load("Assets/Free/Menu/Leaderboard/silvermedal.png").convert_alpha()
bronzeMedalImg = pygame.image.load("Assets/Free/Menu/Leaderboard/bronzemedal.png").convert_alpha()
number4 = pygame.image.load("Assets/Free/Menu/Leaderboard/num4.png").convert_alpha()
number5 = pygame.image.load("Assets/Free/Menu/Leaderboard/num5.png").convert_alpha()
number6 = pygame.image.load("Assets/Free/Menu/Leaderboard/num6.png").convert_alpha()
number7 = pygame.image.load("Assets/Free/Menu/Leaderboard/num7.png").convert_alpha()
rowBox = pygame.image.load("Assets/Free/Menu/Leaderboard/rowBox.png").convert_alpha()
levelSelectorImg = pygame.image.load("Assets/Free/Menu/Leaderboard/levelSelect.png").convert_alpha()
LeaderboardScreen = Leaderboard(
    WIDTH, HEIGHT, 
    leaderboardbgImg, leaderboardTitleImg, leaderboardPanelImg,
    goldMedalImg, silverMedalImg, bronzeMedalImg,
    number4, number5, number6, number7,
    rowBox, levelSelectorImg
)

#Settings
settingsBackgroundImg = pygame.image.load("Assets/Free/Menu/Main menu/Main menu background.jpg").convert_alpha()
SettingsScreen = Settings(WIDTH, HEIGHT, settingsBackgroundImg)

#Imports sky background image
background = pygame.image.load("Assets/Free/Background/backgroundSky.jpg").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT)) #Scales image to screen dimensions

#Music
menuMusic = pygame.mixer.Sound("Assets/Free/Sounds/MenuMusic.mp3")
gameMusic = pygame.mixer.Sound("Assets/Free/Sounds/GameMusic.mp3")

#Game state
gameState = "Main menu"
previousState = ""
volume = 50
currentMusic = "menuMusic"

def startGame():
    global level, player, enemies, hud, floor_y
    #Level
    level = Level("Levels/Level1.txt", "Assets/Free/Background/backgroundSky.jpg", size=60, screenHeight=HEIGHT)
    grass_platform_img = pygame.image.load("Assets/Free/Terrain/Grass.png")
    level.SetImage(grass_platform_img)

    #Apply difficulty settings
    cameraSettings = SettingsScreen.getCamSettings()
    level.setDifficulty(cameraSettings["cameraMaxSpeed"], cameraSettings["cameraAcceleration"])

    #HUD
    heart_img = pygame.image.load("Assets/Free/HUD/heart.png").convert_alpha()
    coin_img = pygame.image.load("Assets/Free/HUD/coin.png").convert_alpha()
    pause_img = pygame.image.load("Assets/Free/HUD/pause.png").convert_alpha()
    hud = HUD(WIDTH, HEIGHT, heart_img, coin_img, pause_img)

    #Player
    player_idle = pygame.image.load("Assets/Free/Main Characters/Virtual Guy/Idle_new.png").convert_alpha()
    player_run = pygame.image.load("Assets/Free/Main Characters/Virtual Guy/Run (32x32).png").convert_alpha()
    player_jump = pygame.image.load("Assets/Free/Main Characters/Virtual Guy/Jump (32x32).png").convert_alpha()
    player = Player(WIDTH // 2, level.height - 200, {
    "Idle": {"sheet": player_idle, "frames": 11},
    "run": {"sheet": player_run, "frames": 12},
    "jump": {"sheet": player_jump, "frames": 1}
    })

    #Enemy
    enemy_idle_sheet = pygame.image.load("Assets/Free/Main Characters/Mask Dude/Idle (32x32).png").convert_alpha()
    enemy_move_sheet = pygame.image.load("Assets/Free/Main Characters/Mask Dude/Run (32x32).png")
    enemy1 = Enemy(270, 200, {
        "Idle": {"sheet": enemy_idle_sheet, "frames":  11},
        "Run": {"sheet": enemy_move_sheet, "frames":  12}
    })
    enemies = [enemy1]
    enemy2 = Enemy(270, 700, {
        "Idle": {"sheet": enemy_idle_sheet, "frames":  11},
        "Run": {"sheet": enemy_move_sheet, "frames":  12}
    })
    enemies = [enemy1, enemy2]

    #Screen borders
    floor_y = level.getFloor()

def playMusic(music):
    global currentMusic 
    if currentMusic != music: #Change music if different from selected
        pygame.mixer.stop() #Stops music
        music.play(-1) #Loop forever
        music.set_volume(volume/100) #Set volume from settings
        currentMusic = music #Change music to new selected

#Event handler/ Game loop
run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT: #Enables user to close window
            run = False

        #In main menu
        if gameState == "Main menu":
            action = MainMenuScreen.HandleEvent(event)
            if action == "start game": #Start game button clicked
                startGame()
                gameState = "Playing"
            elif action == "leaderboard": #Leaderboard button clicked
                gameState = "Leaderboard"
            elif action == "settings": #Settings button clicked
                previousState = "Main menu" #Store previous screen
                gameState = "Settings"

        elif gameState == "Leaderboard":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: #Leave leaderboard screen
                    gameState = "Main menu"

        elif gameState == "Playing":

            if hud.checkPause(event): #Check for pause button event 
                gameState = "Paused"

            if event.type == pygame.KEYDOWN: #Checks for jump
                if event.key == pygame.K_SPACE: #Spacebar input
                    if player.sliding:
                        player.slideJump()
                    else:
                        player.jump() #Calls jump procedure from player class

        elif gameState == "Paused":
            action = PauseMenuScreen.HandleEvent(event) #Checks for event type
            if action == "resume": 
                gameState = "Playing"
            elif action == "exit":
                gameState = "Main menu"
            elif action == "settings":
                previousState = "Paused"
                gameState = "Settings"

        elif gameState == "Settings":
            action = SettingsScreen.HandleEvent(event) #Checks for event type
            if action == "return": #Escape was pressed
                gameState = previousState #Change to main menu
            elif action == "difficultyChanged": #Difficulty was changed
                cameraSettings = SettingsScreen.getCamSettings() #Gets dictionary value of current difficulty

    #Main menu screen
    if gameState == "Main menu":
        MainMenuScreen.draw(screen)
        playMusic(menuMusic)#Play music

    #Leaderboard screen (WIP)
    elif gameState == "Leaderboard":
        LeaderboardScreen.draw(screen)
        playMusic(menuMusic) #Play music

    #Gameplay screen
    elif gameState == "Playing":
        #Update enemy, player and HUD
        level.update(player)
        player.update(floor_y, level.platforms)
        for enemy in enemies: 
            enemy.update(player, level.platforms, floor_y)
        hud.update(player.rect.y, level.height)

        #Draw
        level.draw(screen, player, enemies)
        hud.draw(screen)
        playMusic(gameMusic) #Play music

        #print("Jump boost: ", player.wallJumpBoost)
        #print("Friction: ", player.friction)
    
    #Pause screen
    elif gameState == "Paused":
        level.draw(screen, player, enemies) #Draw background for freeze effect
        hud.draw(screen) #Draw background for freeze effect
        PauseMenuScreen.draw(screen)
        playMusic(menuMusic) #Play music

    #Settings screen
    elif gameState == "Settings":
        SettingsScreen.draw(screen)
        volume = SettingsScreen.getVolume() #Get volume from slider
        currentMusic.set_volume(volume / 100) #Set volume to slider

    #print("game state: ",gameState)
    #print(volume)

    pygame.display.update() #Refreshes screen every loop

    Clock.tick(60) #Set to 60 fps

pygame.quit()