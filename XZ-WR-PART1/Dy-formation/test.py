from v_formation import generate_v_formation
from line_formation import generate_line_formation
from circle_formation import generate_circle_formation
import matplotlib.pyplot as plt


def plot_formation(positions, title):
    """可视化函数"""
    x_coords = [pos[0] for pos in positions]
    y_coords = [pos[1] for pos in positions]
    plt.figure(figsize=(8, 8))
    plt.scatter(x_coords[1:], y_coords[1:], c='blue', label='Followers')
    plt.scatter(x_coords[0], y_coords[0], c='red', marker='*', s=200, label='Leader')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.axis('equal')
    plt.show()


def main():
    print("===== 集群编队生成器 =====")
    print("请选择编队类型：")
    print("1. 人形编队（V字形）")
    print("2. 一字形编队")
    print("3. 圆形编队")
    print("4. 退出程序")

    while True:
        choice = input("\n请输入选项(1-4): ").strip()

        if choice == '1':
            positions = generate_v_formation()
            plot_formation(positions, "V-Shaped Formation (N=25)")
        elif choice == '2':
            positions = generate_line_formation()
            plot_formation(positions, "Line Formation (N=25)")
        elif choice == '3':
            positions = generate_circle_formation()
            plot_formation(positions, "Circle Formation (N=25)")
        elif choice == '4':
            print("程序已退出")
            break
        else:
            print("无效输入，请重新选择！")


if __name__ == "__main__":
    main()