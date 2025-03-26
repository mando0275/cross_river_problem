def solution(S_chicks, S_wolfs, rafts):
    global answer
    max_tried = 1000
    answer = max_tried

    if rafts == 1:
        return "배를 1명만 탈 수 있다면 해결 할 수 없습니다."
    
    if S_chicks < S_wolfs:
        return "시작부터 늑대가 더 많다면 시작하자마자 병아리가 잡아먹힐 겁니다."
    
    movement = {}
    movement[f'{S_chicks}:{S_wolfs}:0:0:start'] = (None, 0)  # 상태 기록

    move(S_chicks, S_wolfs, 0, 0, rafts, "start", 0, movement)

    if answer == max_tried:
        return "정답이 없거나 최대 시도 횟수에 도달했습니다", movement

    # 최단 경로와 이동 횟수 반환
    shortest_path, num_moves = get_shortest_path(movement, f'0:0:{S_chicks}:{S_wolfs}:end')
    return shortest_path, num_moves, movement


def is_possible(animal):
    return animal[0] >= animal[1] or animal[0] == 0


def move(S_chicks, S_wolfs, E_chicks, E_wolfs, rafts, position, count, movement):
    global answer
    
    if S_chicks == 0 and S_wolfs == 0:  # base case: 모든 병아리와 늑대가 끝에 도달
        answer = min(answer, count)
        return

    direction = "end" if position == "start" else "start"
    
    for total in range(rafts, 0, -1):
        for chick in range(total, -1, -1):
            wolf = total - chick
            
            if position == "start":
                if chick > S_chicks or wolf > S_wolfs:
                    continue
                after_move_start = [S_chicks - chick, S_wolfs - wolf]
                after_move_end = [E_chicks + chick, E_wolfs + wolf]
            else:
                if chick > E_chicks or wolf > E_wolfs:
                    continue
                after_move_start = [S_chicks + chick, S_wolfs + wolf]
                after_move_end = [E_chicks - chick, E_wolfs - wolf]
            
            if not (is_possible(after_move_start) and is_possible(after_move_end)):
                continue
            
            after_move_total = f'{after_move_start[0]}:{after_move_start[1]}:{after_move_end[0]}:{after_move_end[1]}:{direction}'
            
            # 더 짧은 경로일 때만 갱신
            if after_move_total not in movement or movement[after_move_total][1] > count + 1:
                movement[after_move_total] = (f'{S_chicks}:{S_wolfs}:{E_chicks}:{E_wolfs}:{position}', count + 1)
                move(after_move_start[0], after_move_start[1], after_move_end[0], after_move_end[1], rafts, direction, count + 1, movement)

#찾은 최단경로를 역으로 진행하여 최단경로의 진행순서 저장
def get_shortest_path(movement, state):
    path = []
    num_moves = -1
    while state:
        path.append(state)
        num_moves += 1
        state = movement[state][0] if state in movement else None
    return list(reversed(path)), num_moves



# 사용자 입력 받기

print ("해당 프로그렘은 파이썬으로 늑대와 병아리 강 건너기 문제를 해결하는 최단의 수를 찾는 알고리즘 입니다. ")
print ("늑대 와 병아리 강 건너기 문제는 늑대와 병아리 들을 안전하게 땟목을 태워 강 반대편으로 보내면 되는 문제입니다. ")
print ("단 늑대의 수가 병아리보다 많을경우 늑대는 병아리를 잡아먹게 되며, 아무것도 태우지 않은체 땟목을 움직일 수는 없습니다. \n")

while True:
    try:
        chick = int(input("초기 병아리의 수를 입력하세요: "))
        wolf = int(input("초기 늑대의 수를 입력하세요: "))
        raft = int(input("땟목에 최대한 태울 수 있는 수를 입력하세요: "))
        break
    except ValueError:
        print("숫자만 입력 가능합니다.")

# 실행 및 결과 출력
shortest_path, num_moves, movement = solution(chick, wolf, raft)
print("최단 경로:  (시작지점 병아리):(시작지점 늑대):(건너편 병아리):(건너편 늑대):땟목위치")
for step in shortest_path:
    print(step)

print(f"\n최단 경로의 이동 횟수: {num_moves}번")
