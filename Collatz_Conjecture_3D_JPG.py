import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import os


def generate_spiral_point(n):
    theta = n * np.pi / 7
    r = 0.1 * np.sqrt(n)
    z = n * 0.2
    return (r * np.cos(theta), r * np.sin(theta), z)


def plot_3d_html(max_num, output_file="collatz_3d.html"):
    # 生成所有点
    points = {n: generate_spiral_point(n) for n in range(1, max_num + 1)}

    # 创建散点图
    scatter = go.Scatter3d(
        x=[p[0] for p in points.values()],
        y=[p[1] for p in points.values()],
        z=[p[2] for p in points.values()],
        mode='markers',
        marker=dict(size=1, color='blue'),
        name='Points'
    )

    # 创建连接线
    lines = []
    for n in points:
        # 规则a: n -> 2n
        if 2 * n in points:
            lines.append(go.Scatter3d(
                x=[points[n][0], points[2 * n][0]],
                y=[points[n][1], points[2 * n][1]],
                z=[points[n][2], points[2 * n][2]],
                mode='lines',
                line=dict(color='green', width=1),
                showlegend=False
            ))
        # 规则b: m -> 3m+1
        m = (n - 1) / 3
        if m.is_integer() and (m_int := int(m)) > 0 and m_int in points:
            lines.append(go.Scatter3d(
                x=[points[m_int][0], points[n][0]],
                y=[points[m_int][1], points[n][1]],
                z=[points[m_int][2], points[n][2]],
                mode='lines',
                line=dict(color='red', width=1),
                showlegend=False
            ))

    # 构建图形
    fig = go.Figure([scatter] + lines)
    fig.update_layout(
        scene=dict(
            xaxis=dict(showbackground=False, showticklabels=False),
            yaxis=dict(showbackground=False, showticklabels=False),
            zaxis=dict(showbackground=False, showticklabels=False)
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    fig.write_html(output_file)
    print(f"HTML文件已保存至: {os.path.abspath(output_file)}")


if __name__ == "__main__":
    # 带时间戳的动态路径
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"output/html/collatz_{timestamp}.html"
    plot_3d_html(max_num=2000, output_file=output_path)