import pygame, sys, random

# function tạo sàn
def draw_floor():
	srceen.blit(floor, (floor_x_pos, 350))
	srceen.blit(floor, (floor_x_pos+216, 350))

# function tạo ống
def create_pipe():
	random_pipe_pos = random.choice(pipe_height)
	bottom_pipe = pipe_surface.get_rect(midtop = (250, random_pipe_pos))
	top_pipe = pipe_surface.get_rect(midtop = (250, random_pipe_pos-335))
	return bottom_pipe, top_pipe
def move_pipe(pipes):
	for pipe in pipes:
		pipe.centerx -= 2.50	# -5
	return pipes
def draw_pipe(pipes):
	for pipe in pipes:
		if pipe.bottom >= 300:
			srceen.blit(pipe_surface, pipe)
		else:
			flip_pipe = pygame.transform.flip(pipe_surface, False, True)
			srceen.blit(flip_pipe, pipe)

# func va cham
def check_collision(pipes):
	for pipe in pipes:
		if bird_rect.colliderect(pipe):
			hit_sound.play()
			return False
	if bird_rect.top <= -37.5 or bird_rect.bottom >= 350:
		hit_sound.play()
		return False
	return True

# func xoay bird
def rotate_bird(bird1):
	new_bird = pygame.transform.rotozoom(bird1, bird_movement*3, 1)
	return new_bird

# func đập cánh
def bird_animation():
	new_bird = bird_list[bird_index]
	new_bird_rect = new_bird.get_rect(center = (50, bird_rect.centery))
	return new_bird, new_bird_rect

# func Score
def score_display(game_state):
	if game_state == 'main_game':
		score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
		score_rect = score_surface.get_rect(center = (108, 50))
		srceen.blit(score_surface, score_rect)
	
	if game_state == 'game_over':
		score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
		score_rect = score_surface.get_rect(center = (108, 50))
		srceen.blit(score_surface, score_rect)

		high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
		high_score_rect = high_score_surface.get_rect(center = (108, 335)) # 216, 630
		srceen.blit(high_score_surface, high_score_rect)
def update_score(score, high_score):
	if score > high_score:
		high_score = score
	return high_score

# Khởi tạo ctr
# Chỉnh giá trị âm thanh về thích hợp với pygame, bên trong dấu ngoặc cũng là quy định
pygame.mixer.pre_init(frequency = 44100, size = -16, channels = 2, buffer = 512)

pygame.init()
srceen = pygame.display.set_mode((216, 384)) 	# 432, 768 (màn hình gấp đôi)
clock = pygame.time.Clock()						# FPS
game_font = pygame.font.Font('04B_19.TTF', 20)

# Tạo biến
gravity = 0.125									# Trọng lực
bird_movement = 0
game_active = True
score = 0
high_score = 0

# Tạo BG
bg = pygame.image.load('assets/background-night.png').convert()
# bg = pygame.transform.scale2x(bg) (hình gấp đôi)
# Tùy chỉnh những cái != x2

# Tạp Floor
floor = pygame.image.load('assets/floor.png').convert()
floor_x_pos = 0 	# Tạo biến tọa độ cho sàn

# Tạo Bird
bird_down = pygame.image.load('assets/yellowbird-downflap.png').convert_alpha()
bird_mid = pygame.image.load('assets/yellowbird-midflap.png').convert_alpha()
bird_up = pygame.image.load('assets/yellowbird-upflap.png').convert_alpha()
bird_list = [bird_down, bird_mid, bird_up]
bird_index = 0
bird = bird_list[bird_index]

bird_rect = bird.get_rect(center = (50, 192))

# Tạo timer cho bird
birdFlap = pygame.USEREVENT + 1
pygame.time.set_timer(birdFlap, 200)

# Tạo ống
pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_list = []

# Tạo timer xuất hiện pipe
spawnPipe = pygame.USEREVENT
pygame.time.set_timer(spawnPipe, 2400)
pipe_height = [100, 150, 200, 250]

# Tạo màn hình KT
game_over_surface = pygame.image.load('assets/message.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center = (108, 192))

# Chèn âm thanh
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 1000

# Vẽ Game
while True:
	for event in pygame.event.get():
		# Thoát
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		# Di chuyển
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE and game_active:
				bird_movement = 0
				bird_movement = -4.5	# x2 = -9
				flap_sound.play()

			if event.key == pygame.K_SPACE and game_active == False:
				game_active = True
				pipe_list.clear()
				bird_rect.center = (50, 192)
				bird_movement = 0
				score = 0

		# Tạo ống liên tục
		if event.type == spawnPipe:
			pipe_list.extend(create_pipe())

		# Tạo hiệu ứng đập cánh
		if event.type == birdFlap:
			if bird_index < 2:
				bird_index += 1
			else:
				bird_index = 0

			bird, bird_rect = bird_animation()

	srceen.blit(bg, (0, 0))

	if game_active:
		# Bird
		bird_movement += gravity
		rotated_bird = rotate_bird(bird)
		bird_rect.centery += bird_movement
		srceen.blit(rotated_bird, bird_rect)
		game_active = check_collision(pipe_list)

		# Pipe
		pipe_list = move_pipe(pipe_list)
		draw_pipe(pipe_list)

		# Score
		score += 0.01
		score_display('main_game')
		score_sound_countdown -= 1
		if score_sound_countdown <= 0:
			score_sound.play()
			score_sound_countdown = 1000
	else:
		srceen.blit(game_over_surface, game_over_rect)
		high_score = update_score(score, high_score)
		score_display('game_over')


	# Floor
	floor_x_pos -= 1

	draw_floor()
	# Điều kiện cho floor chạy liên tục
	if floor_x_pos <= -216:
		floor_x_pos = 0

	pygame.display.update()
	clock.tick(120)