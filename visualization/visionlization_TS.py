# Energy saving
# 1. visualization for representing B/S on/off code
# In the right above box, the on/off action is represented and the action is from EsActions.txt
# - EsActions,txt : timestamp,cellId,hoAllowed
# 1-1 : ExActions numpy array is created : [time_index, cellid, on/off policy] # 0 on, 1off
# 1-2 : BsState numpy array is created from bsState.txt
# - (simulation_time, current_time (os_time), cellid, handover 허용 여부 (true, false))
# sim time 만 이용 할 것
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.cm import tab10  # 색상 10개까지 확장

# output of fileInfo
# ues도 빠아내야지
def fileInfo(forder_path, bs_index = np.array([1,2,3,4,5,6,7,8]), debug = True):
    # To Do 공통파일로 변경
    bsstatefile_path = forder_path+"TsActions.txt"
    with open(bsstatefile_path, "r") as f:
        lines = f.readlines()

    data_lines = lines[1:] # 데이터 라인 추출 (헤더 제외)
    timestamps = [float(line.split(",")[0]) for line in data_lines] # timestamp 값만 추출
    unique_ts = sorted(set(timestamps)) # 고유 timestamp → 인덱스 매핑 만들기

    time_index = np.array(unique_ts) # numpy 배열로 변환

    len_ts = len(time_index)
    len_bs = len(bs_index)

    timestamp_to_index = {ts: idx for idx, ts in enumerate(time_index)}
    cellid_to_index = {cid: idx for idx, cid in enumerate(bs_index)}

    # 결과 출력 (원하면 저장도 가능)
    if debug == True:
        print(f"time_index numpy array: {time_index}")
        print(f"cellids numpy array: {bs_index}")
        print(f"time_index numpy array: {timestamp_to_index}")
        print(f"cellids numpy array: {cellid_to_index}")

    return len_ts, len_bs, time_index, timestamp_to_index, cellid_to_index


# File 설명
def bs_actionInfo(forder_path, len_ts, n_ue, timestamp_to_index):
    # create Actions numpy
    Actions =np.ones ((len_ts,n_ue))*-1
    esfile_path = forder_path+"TsActions.txt"
    with open(esfile_path, "r") as f:
        lines = f.readlines()
    data_lines = lines[1:] # 데이터 라인 추출 (헤더 제외)
    ## 수정 할 것 (절대 시간을 0으로 코드 수정 필요)
    timestamps = [int(line.split(",")[0]) for line in data_lines] # timestamp 값만 추출
    ueids = [int(line.split(",")[1]) for line in data_lines] # cellids 값만 추출
    cellids = [int(line.split(",")[2]) for line in data_lines] # cellid 값만 추출

    for ts, uid, cid in zip(timestamps, ueids, cellids):
        t_idx = timestamp_to_index[ts]
        uidx = uid-1
        Actions[t_idx,uidx] = int(cid)

    cellUEstate =np.ones ((len_ts, n_ue))*-1
    cellstate_path = forder_path+"CellIdStats.txt"
    with open(cellstate_path, "r") as f:
        lines = f.readlines()

    timestamps = []
    for i in range(len(lines)):
        time_value = float(lines[i].split(" ")[0])
        for j in range (len_ts):
            if 0.1*j <= time_value < 0.1*(j+1):
                timestamps.append(round(0.1 * (j + 1), 3))
    ueids = [int(line.split(" ")[1]) for line in lines] # ueids 값만 추출
    cellids = [int(line.split(" ")[2]) for line in lines] # ueids 값만 추출


    for ts, cid, ueid in zip(timestamps, cellids, ueids):
        ts_i = int(1000*ts)
        t_idx = timestamp_to_index[ts_i]
        #cellid_idx = cellid_to_index[cid]
        cellUEstate[t_idx, ueid-1] = int(cid)
    for t_idx in range(1,len_ts):
        for ueid in range(n_ue):
            if cellUEstate[t_idx, ueid] == -1:
                cellUEstate[t_idx, ueid] = cellUEstate[t_idx-1, ueid]

    return Actions, cellUEstate


# 단말의 possition 만들기
def PossInfo (forder_path, len_ts,n_ue,len_bs, cellid_to_index):
    gnbPoss_path = forder_path + "enbs.txt"
    gnbPosses = np.ones((len_bs, 2)) * -1  # Adjusted size
    with open(gnbPoss_path, "r") as f:
        for line in f:
            parts = line.strip().split()
            cellid = int(parts[2].strip('"'))
            xy_str = parts[4]  # e.g., "2000,2000"
            x_str, y_str = xy_str.split(",")
            x = float(x_str)
            y = float(y_str)
            c_idx = cellid_to_index[cellid]
            gnbPosses[c_idx, 0] = x
            gnbPosses[c_idx, 1] = y


    uePoss_path = forder_path+"ue_trace.txt"
    uePosses = np.ones ((len_ts, n_ue,2))*-1 # Adjusted size

    with open(uePoss_path, "r") as f:
        lines = f.readlines()

    timestamps = [float(line.split(",")[0]) for line in lines] # timestamp 값만 추출
    ueids = [int(line.split(",")[1]) for line in lines] # cellids 값만 추출
    x_posses = [float(line.split(",")[2]) for line in lines] #x
    y_posses = [float(line.split(",")[3]) for line in lines] #x

    for ts, ueid, x,y in zip(timestamps, ueids, x_posses,y_posses):
        ts_i = int(ts*1000)
        t_idx = timestamp_to_index[ts_i]
        uePosses[t_idx, ueid-1,0] = x
        uePosses[t_idx, ueid-1,1] = y
    return uePosses, gnbPosses



def plot_ts_state(ts_idx,time_index, Actions, gnbPosses, uePosses,cellUEstate, ax= None):
    colors = [tab10(i) for i in range(10)]

    if ax == None:
        fig, ax = plt.subplots(figsize=(8, 8))
    else:
        ax.clear()

    action = Actions[ts_idx] ## ue 별 handoder
    for (ue_idx, bs_idx) in enumerate(Actions[ts_idx]):
        if bs_idx == -1 and ts_idx > 0:
            Actions[ts_idx, ue_idx] = Actions[ts_idx-1, ue_idx]

    print (f"action {Actions[ts_idx]}")
    if ts_idx == 0:
        previous_action = [-1]*14  ## 초기 상태
    else:
        previous_action =Actions[ts_idx-1]
    ue_bs_state = cellUEstate [ts_idx]

    box_text = (
        f"Previous Action :  = {', '.join(map(str, previous_action))}\n"
        f"Current Action :  = {', '.join(map(str, action))}\n"
        f"Current Ue State :  = {', '.join(map(str, ue_bs_state))}"

    )

    props = dict(boxstyle='round', facecolor='white', edgecolor='black', alpha=0.9)
    ax.text(0.01, 1.02, box_text, transform=ax.transAxes, fontsize=10,
            verticalalignment='bottom', bbox=props)

    for bs_idx, (x, y) in enumerate(gnbPosses):
        color = colors[bs_idx % len(colors)]
        if bs_idx == 0:
            ax.scatter(x, y, marker='*', color=color, s=500, label='eNB')
        else:
            ax.scatter(x, y, marker='o', color=color, s=150,
                           label='gNB')
            # gNB 안에 index 텍스트
            ax.text(x, y, str(bs_idx + 1), color='white',
                    fontsize=9, ha='center', va='center', fontweight='bold')

    uePosses_ts = uePosses[ts_idx]
    if uePosses_ts is not None:
        for i, (ux, uy) in enumerate(uePosses_ts):
            ue_state = cellUEstate[ts_idx, i]
            cellid = int(ue_state)
            color = colors[cellid-1 % len(colors)]
            ax.scatter(ux, uy, marker='^', color=color, s=50, label='UE' if i == 0 else "")
            ax.text(ux, uy + 50, f"UE{i + 1}", color=color, ha='center', fontsize=9)

    if ts_idx == 0:
        ax.set_title(f"Step {ts_idx} : 0 ~ {time_index[ts_idx]} second ", fontsize=11, pad=20, loc='right')
    else:
        ax.set_title(f"Step {ts_idx} : {time_index[ts_idx-1]} ~ {time_index[ts_idx]} second ", fontsize=11, pad=20, loc='right')

    legend_elements = [
        Line2D([0], [0], marker='*', color=colors[0], label='eNB',
               markerfacecolor=colors[0], markersize=15),
        Line2D([0], [0], marker='o', color='black', label='gNB',
               markerfacecolor='black', markersize=10),
        Line2D([0], [0], marker='^', color='green', label='UE',
               markerfacecolor='black', markersize=10)
    ]
    ax.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1, 0.5))

    all_x = gnbPosses[:, 0].tolist()
    all_y = gnbPosses[:, 1].tolist()
    margin_x = (max(all_x) - min(all_x)) * 0.2
    margin_y = (max(all_y) - min(all_y)) * 0.2
    ax.set_xlim(min(all_x) - margin_x, max(all_x) + margin_x)
    ax.set_ylim(min(all_y) - margin_y, max(all_y) + margin_y)

    ax.set_xlabel("X", fontsize=12)
    ax.set_ylabel("Y", fontsize=12)
    ax.grid(True)
    ax.set_aspect('equal')
    plt.tight_layout()
    plt.subplots_adjust(right=0.8)
    plt.show()

#################################################################################

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib
import time
n_ue = 14
forder_path = "ts_sample/"
len_ts, len_bs, time_index, timestamp_to_index, cellid_to_index = fileInfo(forder_path)
TsActions, cellUEstate = bs_actionInfo(forder_path, len_ts, n_ue, timestamp_to_index)
uePosses, gnbPosses = PossInfo (forder_path, len_ts,n_ue,len_bs,cellid_to_index)

fig, ax = plt.subplots(figsize=(8, 8))

# 프레임 업데이트 함수 정의
'''
def update(ts_idx):
    ax.clear()
    plot_ts_state(ts_idx=ts_idx, time_index=time_index, EsActions=EsActions,
                  bsStates=bsStates, gnbPosses=gnbPosses,
                  uePosses=uePosses, cellUEstate=cellUEstate, ax=ax)
# 애니메이션 생성
ani = FuncAnimation(fig, update, frames=len_ts, interval=1000)

# GIF로 저장
ani.save('oran_simulation.gif', writer='pillow', fps=1)
ani.save("oran_simulation.mp4", writer='ffmpeg', fps=1)
'''
for ts_idx in range(len_ts):
    plot_ts_state(ts_idx=ts_idx, time_index=time_index, Actions=TsActions,
                  gnbPosses=gnbPosses, uePosses= uePosses, cellUEstate=cellUEstate)
    plt.show()
    time.sleep(2)
