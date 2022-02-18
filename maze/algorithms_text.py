import time


def move(cur, maze, visited):  # 주변 이동 가능 경로 반환 함수 - 0 / visited == False / 범위 내에
    nlist = []
    dir = [[1, 0], [0, 1], [-1, 0], [0, -1]]  # 아래,오른,위,왼
    for i in range(4):
        row = cur[0]+dir[i][0]
        col = cur[1]+dir[i][1]
        if -1 < row and row < 200 and -1 < col and col < 200:  # 미로 범위 내
            if maze[row][col] == '0':  # 이동 가능 공간
                if visited[row][col] == 0:  # 가지 않았던 곳
                    nlist.append([row, col])
    return nlist


def check(cur, visited):
    nlist = []
    dir = [[1, 0], [0, 1], [-1, 0], [0, -1]]  # 아래,오른,위,왼
    for i in range(4):
        row = cur[0]+dir[i][0]
        col = cur[1]+dir[i][1]
        if -1 < row and row < 200 and -1 < col and col < 200:  # 미로 범위 내
            if visited[row][col] == 1:  # 이동 가능 공간
                nlist.append([row, col])
    return nlist


def way(start, end, visited):  # 최단거리 찾기
    q = [end]
    visited[end[0]][end[1]] = 2
    while True:
        cur = q[0]
        del q[0]
        if cur == start:
            break
        nexts = check(cur, visited)  # 다음 길 찾기
        for i in range(len(nexts)):  # 이동횟수 더하고 큐로 삽입
            visited[nexts[i][0]][nexts[i][1]] = visited[cur[0]][cur[1]] + 1
            q.append(nexts[i])
    answer = visited[start[0]][start[1]] - 2
    return answer


def read(text_num):
    maze = []
    # 미로 읽어오기
    f = open("../maze/{}.txt".format(text_num), "r")
    while True:
        line = f.readline()
        maze.append(list(line)[:-1])  # 마지막 띄어쓰기 빼기
        if line == '':
            break
    f.close()
    start = [0, 1] if maze[0][1] == '0' else [0, 2]  # 입구 좌표
    end = [199, 198] if maze[199][198] == '0' else [199, 197]  # 출구 좌표
    return [maze, start, end]


def dfs(text_num, info):
    maze = info[0]
    start = info[1]
    end = info[2]
    visited = [[0 for i in range(200)]
               for j in range(200)]  # 방문 확인 / 0 미방문, 1 방문

    time_start = time.time()

    # 시작점 방문
    stack = [[start[0], start[1]]]
    visited[start[0]][start[1]] = 1

    # 탐색 알고리즘
    while stack:  # stack이 비기 전까지
        cur = stack[-1]
        if len(move(cur, maze, visited)) == 0:  # 이동 가능 경로 없으면
            del stack[-1]  # 왔던 길 돌아가기
            continue
        next = move(cur, maze, visited)[0]
        visited[next[0]][next[1]] = 1
        stack.append(next)
        if next == end:
            break

    time_end = time.time()
    atime = (time_end - time_start)*1000  # 알고리즘 수행시간
    print(start, end, atime)

    coor = 0  # 탐색한 좌표의 갯수
    for i in range(200):
        coor += visited[i].count(1)
    print('count ', coor)

    # 탐색한 곳 텍스트 파일로
    f = open('test_dfs/maze{}.txt'.format(text_num), 'w')
    for i in range(200):
        for j in range(200):
            f.write(str(visited[i][j]))
        f.write('\n')

    # 최단거리 찾기
    shortest = way(start, end, visited)
    print('shortest ', shortest)

    # 최단거리 텍스트 파일로
    zero = 0
    f = open('test_dfs/maze_shortest{}.txt'.format(text_num), 'w')
    for i in range(200):
        for j in range(200):
            if visited[i][j] == 0:
                #f.write("{0:3d} ".format(a))
                #f.write(" {0:3s}".format(zero))
                f.write(" ■■")
            else:
                f.write(" {0:3d} ".format(visited[i][j]))
        f.write('\n')
    f.close()

    return [text_num, shortest, coor, atime]


def bfs(text_num, info):
    maze = info[0]
    start = info[1]
    end = info[2]
    visited = [[0 for i in range(200)]
               for j in range(200)]  # 방문 확인 / 0 미방문, 1 방문

    time_start = time.time()

    start = [0, 1] if maze[0][1] == '0' else [0, 2]  # 입구 좌표
    end = [199, 198] if maze[199][198] == '0' else [199, 197]  # 출구 좌표
    visited = [[0 for i in range(200)]
               for j in range(200)]  # 방문 확인 / 0 미방문, 1 방문

    # 시작점 방문
    queue = [[start[0], start[1]]]
    visited[start[0]][start[1]] = 1

    # 탐색 알고리즘
    while queue:
        cur = queue[0]
        del queue[0]
        if cur == end:  # 출구 찾음
            break
        nexts = move(cur, maze, visited)
        for i in range(len(nexts)):  # 방문 표시 후 큐로 삽입
            visited[nexts[i][0]][nexts[i][1]] = 1
            queue.append(nexts[i])

    time_end = time.time()
    atime = (time_end - time_start)*1000  # 알고리즘 수행시간
    print(start, end, atime)

    coor = 0  # 탐색한 좌표의 갯수
    for i in range(200):
        coor += visited[i].count(1)
    print('count ', coor)

    # 탐색한 곳 텍스트 파일로
    f = open('test_bfs/maze{}.txt'.format(text_num), 'w')
    for i in range(200):
        for j in range(200):
            f.write(str(visited[i][j]))
        f.write('\n')
    f.close()

    # 최단거리 찾기
    shortest = way(start, end, visited)
    print('shortest ', shortest)

    # 최단거리 텍스트 파일로
    zero = 0
    f = open('test_bfs/maze_shortest{}.txt'.format(text_num), 'w')
    for i in range(200):
        for j in range(200):
            if visited[i][j] == 0:
                #f.write("{0:3d} ".format(a))
                #f.write(" {0:3s}".format(zero))
                f.write(" ■■")
            else:
                f.write(" {0:3d} ".format(visited[i][j]))
        f.write('\n')
    f.close()
    return [text_num, shortest, coor, atime]


def astar(text_num, info):
    maze = info[0]
    start = info[1]
    end = info[2]
    visited = [[0 for i in range(200)]
               for j in range(200)]  # 방문 확인 / 0 미방문, 1 방문

    time_start = time.time()

    start = [0, 1] if maze[0][1] == '0' else [0, 2]  # 입구 좌표
    end = [199, 198] if maze[199][198] == '0' else [199, 197]  # 출구 좌표
    visited = [[0 for i in range(200)]
               for j in range(200)]  # 방문 확인 / 0 미방문, 1 방문

    # 시작점 방문
    o = [start+[0, 0, 0, -1, -1]]
    o_check = [start]
    c_check = []
    c = []  # y좌표, x좌표, F socre, G, H, 부모x, 부모y
    visited[start[0]][start[1]] = 1

    # 탐색 알고리즘
    while True:
        o.sort(key=lambda x: x[2])
        cur = o[0]
        del o[0]
        for i in range(len(o_check)):
            if o_check[i][0] == cur[0] and o_check[i][1] == cur[1]:
                del o_check[i]
                break
        visited[cur[0]][cur[1]] = 1
        c.append(cur)
        c_check.append([cur[0], cur[1]])

        nexts = move(cur, maze, visited)
        for i in range(len(nexts)):
            if nexts[i] not in c_check:
                g = cur[3] + 1
                h = end[0]+end[1]-nexts[i][0]-nexts[i][1]
                next = nexts[i]+[g+h, g, h]+cur
                if nexts[i] not in o_check:
                    o_check.append(nexts[i])
                    o.append(next)
                else:
                    if next[3] < o[o_check.find(nexts[i])][3]:  # 교체하는 경우
                        o[o_check.find(nexts[i])] = next
        if end in c_check:
            break

    time_end = time.time()
    atime = (time_end - time_start)*1000  # 알고리즘 수행시간
    print(start, end, atime)

    coor = 0  # 탐색한 좌표의 갯수
    for i in range(200):
        coor += visited[i].count(1)
    print('count ', coor)

    # 탐색한 곳 텍스트 파일로
    f = open('test_astar/maze{}.txt'.format(text_num), 'w')
    for i in range(200):
        for j in range(200):
            f.write(str(visited[i][j]))
        f.write('\n')
    f.close()

    shortest = way(start, end, visited)
    print('shortest ', shortest)

    # 최단거리 텍스트 파일로
    zero = 0
    f = open('test_astar/maze_shortest{}.txt'.format(text_num), 'w')
    for i in range(200):
        for j in range(200):
            if visited[i][j] == 0:
                #f.write("{0:3d} ".format(a))
                #f.write(" {0:3s}".format(zero))
                f.write(" ■■")
            else:
                f.write(" {0:3d} ".format(visited[i][j]))
        f.write('\n')
    f.close()

    return [text_num, shortest, coor, atime]

# (txt번호(Int16), 출구까지 가장 짧은 이동횟수(Int16), 출구를 찾을때까지 탐색한 좌표의 개수(Int16), 알고리즘 수행시간(Float32, ms))
# 텍스트 번호 / shortest / coor / atime


def main():
    for i in range(1, 6):
        info = read(i)
        print("dfs")
        dfs(i, info)
        print("bfs")
        bfs(i, info)
        print("astar")
        astar(i, info)


if __name__ == "__main__":
    main()
