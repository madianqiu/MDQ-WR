import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # 关键设置：强制使用交互式后端
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.optimize import linear_sum_assignment
from v_formation import generate_v_formation
from line_formation import generate_line_formation
from circle_formation import generate_circle_formation


class TimedFormationAnimator:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        self.ax.set_xlim(-20, 20)
        self.ax.set_ylim(-20, 20)
        self.ax.grid(True)
        self.scatter = self.ax.scatter([], [], c='blue', s=50, label='跟随者')
        self.leader = self.ax.scatter([], [], c='red', marker='*', s=200, label='领航机')
        self.ax.legend()

        # 预定义的编队中心位置
        self.centers = [(-15, 0), (0, 0), (15, 0), (0, 15), (0, -15)]

    def get_formation(self, formation_type):
        """获取编队坐标"""
        if formation_type == 1:
            return generate_line_formation()
        elif formation_type == 2:
            return generate_circle_formation()
        elif formation_type == 3:
            return generate_v_formation()
        else:
            raise ValueError("无效的编队类型")

    def hungarian_assign(self, start_pos, end_pos):
        """匈牙利算法路径分配"""
        cost_matrix = np.zeros((len(start_pos), len(end_pos)))
        for i in range(len(start_pos)):
            for j in range(len(end_pos)):
                cost_matrix[i, j] = np.linalg.norm(start_pos[i] - end_pos[j])
        _, col_ind = linear_sum_assignment(cost_matrix)
        return col_ind

    def generate_timed_paths(self, schedule):
        """生成带时间控制的路径"""
        # 按时间排序调度表
        schedule.sort(key=lambda x: x['time'])

        # 初始化路径
        total_frames = schedule[-1]['time'] if schedule else 100
        num_drones = len(self.get_formation(1))  # 假设所有编队无人机数量相同
        paths = np.zeros((num_drones, total_frames, 2))

        current_formation = 1  # 默认起始编队
        current_pos = np.array(self.get_formation(current_formation))
        current_center_idx = 0
        prev_time = 0

        for event in schedule:
            start_time = prev_time
            end_time = event['time']
            duration = end_time - start_time

            # 获取当前和目标编队
            target_formation = event['formation']
            start_form = current_pos
            end_form = np.array(self.get_formation(target_formation))

            # 匈牙利算法分配
            assignment = self.hungarian_assign(current_pos, end_form)
            reordered_end_form = end_form[assignment]

            # 计算中心位置移动
            target_center_idx = event.get('center', current_center_idx)
            start_center = self.centers[current_center_idx]
            end_center = self.centers[target_center_idx]

            # 生成这段路径
            for t in range(start_time, end_time):
                progress = (t - start_time) / duration
                for i in range(num_drones):
                    # 形状变换
                    x = start_form[i][0] * (1 - progress) + reordered_end_form[i][0] * progress
                    y = start_form[i][1] * (1 - progress) + reordered_end_form[i][1] * progress

                    # 编队整体移动
                    x += start_center[0] * (1 - progress) + end_center[0] * progress
                    y += start_center[1] * (1 - progress) + end_center[1] * progress

                    # 添加轻微扰动
                    x += np.random.normal(0, 0.1)
                    y += np.random.normal(0, 0.1)

                    paths[i, t] = [x, y]

            # 更新状态
            current_pos = reordered_end_form
            current_formation = target_formation
            current_center_idx = target_center_idx
            prev_time = end_time

        return paths, schedule

    def animate_schedule(self, schedule):
        """执行定时动画"""
        paths, schedule = self.generate_timed_paths(schedule)

        # 绘制中心位置标记
        for i, center in enumerate(self.centers):
            self.ax.plot(center[0], center[1], 'go', markersize=10)
            self.ax.text(center[0], center[1] + 1, f'C{i}', ha='center')

        def update(frame):
            current_pos = paths[:, frame]
            self.scatter.set_offsets(current_pos[1:])
            self.leader.set_offsets(current_pos[0])

            # 显示当前编队状态
            current_formation = 1
            next_change = "无"
            for event in schedule:
                if frame < event['time']:
                    next_change = f"在帧 {event['time']} 变为 {self.get_type_name(event['formation'])}"
                    break
                current_formation = event['formation']

            self.ax.set_title(
                f"当前编队: {self.get_type_name(current_formation)}\n"
                f"下一变换: {next_change}\n"
                f"进度: {frame + 1}/{len(paths[0])}"
            )
            return self.scatter, self.leader

        ani = FuncAnimation(self.fig, update, frames=len(paths[0]),
                            interval=50, blit=True)
        plt.show()

    def get_type_name(self, type_num):
        names = {1: "一字型", 2: "圆形", 3: "V型"}
        return names.get(type_num, "未知")


def main():
    print("===== 定时编队变换系统 =====")
    print("编队类型: 1=一字型, 2=圆形, 3=V型")
    print("中心位置: 0=左(-15,0), 1=中(0,0), 2=右(15,0), 3=上(0,15), 4=下(0,-15)")
    print("\n输入格式: 时间(帧数) 编队类型 [中心位置]")
    print("示例:")
    print("50 2 1  # 在50帧时变为圆形编队，移动到中心1")
    print("100 3 2 # 在100帧时变为V型编队，移动到中心2")
    print("输入'end'结束输入")

    schedule = []
    while True:
        user_input = input("请输入变换指令: ").strip()
        if user_input.lower() == 'end':
            break

        try:
            parts = user_input.split()
            time = int(parts[0])
            formation = int(parts[1])
            center = int(parts[2]) if len(parts) > 2 else None

            if formation not in [1, 2, 3]:
                raise ValueError("编队类型必须是1-3")

            if center is not None and center not in range(5):
                raise ValueError("中心位置必须是0-4")

            event = {'time': time, 'formation': formation}
            if center is not None:
                event['center'] = center

            schedule.append(event)

        except Exception as e:
            print(f"输入错误: {e}，请重新输入")

    if not schedule:
        print("使用默认调度: 50帧变圆形，100帧变V型")
        schedule = [
            {'time': 50, 'formation': 2, 'center': 1},
            {'time': 100, 'formation': 3, 'center': 2}
        ]

    animator = TimedFormationAnimator()
    animator.animate_schedule(schedule)


if __name__ == "__main__":
    import matplotlib

    matplotlib.use('Qt5Agg')

    main()

# # 复杂变换
# 30 1 0  # 30帧保持一字型但移动到左边
# 60 2 1  # 60帧变圆形到中心
# 90 3 3  # 90帧变V型到上方
# 120 1 2 # 120帧恢复一字型到右边
# end