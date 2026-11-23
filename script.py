import tkinter as tk
import math

class ProjectionViewer:
    def __init__(self, width=800, height=600):
        self.root = tk.Tk()
        self.root.title("Проекции платоновых тел")

        self.width = width
        self.height = height

        main_container = tk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(main_container, width=width, height=height, bg='white')
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        control_panel = tk.Frame(main_container, width=300, bg='lightgray')
        control_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        control_panel.pack_propagate(False)

        tk.Label(control_panel, text="Управление", font=('Arial', 14, 'bold'),
                 bg='lightgray').pack(pady=10)

        frame_figure = tk.LabelFrame(control_panel, text="Выбор фигуры",
                                     padx=10, pady=10, bg='lightgray')
        frame_figure.pack(fill=tk.X, padx=10, pady=5)

        self.body_var = tk.StringVar(value="tetrahedron")

        tk.Radiobutton(frame_figure, text="Тетраэдр", variable=self.body_var,
                       value="tetrahedron", command=self.update_view,
                       bg='lightgray', font=('Arial', 11)).pack(anchor=tk.W, pady=5)

        tk.Radiobutton(frame_figure, text="Додекаэдр", variable=self.body_var,
                       value="dodecahedron", command=self.update_view,
                       bg='lightgray', font=('Arial', 11)).pack(anchor=tk.W, pady=5)

        info_frame = tk.Frame(frame_figure, bg='lightgray')
        info_frame.pack(fill=tk.X, pady=5)
        tk.Label(info_frame, text="Тетраэдр: 4 вершины, 6 рёбер",
                 bg='lightgray', font=('Arial', 9), fg='darkblue').pack(anchor=tk.W)
        tk.Label(info_frame, text="Додекаэдр: 20 вершин, 30 рёбер",
                 bg='lightgray', font=('Arial', 9), fg='darkblue').pack(anchor=tk.W)

        frame_projection = tk.LabelFrame(control_panel, text="Тип проекции",
                                         padx=10, pady=10, bg='lightgray')
        frame_projection.pack(fill=tk.X, padx=10, pady=10)

        self.projection_var = tk.StringVar(value="orthographic")

        tk.Radiobutton(frame_projection, text="Ортогональная проекция",
                       variable=self.projection_var, value="orthographic",
                       command=self.update_view, bg='lightgray',
                       font=('Arial', 11)).pack(anchor=tk.W, pady=5)

        tk.Radiobutton(frame_projection, text="Центральная проекция",
                       variable=self.projection_var, value="perspective",
                       command=self.update_view, bg='lightgray',
                       font=('Arial', 11)).pack(anchor=tk.W, pady=5)

        param_frame = tk.Frame(frame_projection, bg='lightgray')
        param_frame.pack(fill=tk.X, pady=10)

        tk.Label(param_frame, text="Расстояние до плоскости (d):",
                 bg='lightgray', font=('Arial', 10)).pack(anchor=tk.W)

        scale_frame = tk.Frame(param_frame, bg='lightgray')
        scale_frame.pack(fill=tk.X, pady=5)

        tk.Label(scale_frame, text="1", bg='lightgray').pack(side=tk.LEFT)
        self.d_var = tk.DoubleVar(value=4.0)
        self.d_scale = tk.Scale(scale_frame, from_=1.0, to=15.0, resolution=0.5,
                                orient=tk.HORIZONTAL, variable=self.d_var,
                                command=lambda x: self.update_view(),
                                length=180, bg='lightgray',
                                highlightbackground='lightgray')
        self.d_scale.pack(side=tk.LEFT, padx=5)
        tk.Label(scale_frame, text="15", bg='lightgray').pack(side=tk.LEFT)

        self.d_label = tk.Label(param_frame, text=f"d = {self.d_var.get():.1f}",
                                bg='lightgray', font=('Arial', 10, 'bold'))
        self.d_label.pack()

        frame_rotation = tk.LabelFrame(control_panel, text="Вращение",
                                       padx=10, pady=10, bg='lightgray')
        frame_rotation.pack(fill=tk.X, padx=10, pady=10)

        rotation_grid = tk.Frame(frame_rotation, bg='lightgray')
        rotation_grid.pack()

        axes = ['X', 'Y', 'Z']
        for i, axis in enumerate(axes):
            tk.Label(rotation_grid, text=f"Ось {axis}:", bg='lightgray',
                     font=('Arial', 10)).grid(row=i, column=0, padx=5, pady=5, sticky=tk.W)
            tk.Button(rotation_grid, text="+",
                      command=lambda a=axis.lower(): self.rotate(a + '+'),
                      width=3, font=('Arial', 10, 'bold')).grid(row=i, column=1, padx=2)
            tk.Button(rotation_grid, text="-",
                      command=lambda a=axis.lower(): self.rotate(a + '-'),
                      width=3, font=('Arial', 10, 'bold')).grid(row=i, column=2, padx=2)

        tk.Button(frame_rotation, text="Сбросить вращение",
                  command=self.reset_rotation, font=('Arial', 11),
                  bg='orange', activebackground='darkorange').pack(pady=10)

        self.angle_label = tk.Label(frame_rotation, text="Углы: X=0°, Y=0°, Z=0°",
                                    bg='lightgray', font=('Arial', 10))
        self.angle_label.pack(pady=5)

        frame_view = tk.LabelFrame(control_panel, text="Настройки вида",
                                   padx=10, pady=10, bg='lightgray')
        frame_view.pack(fill=tk.X, padx=10, pady=10)

        self.scale_var = tk.DoubleVar(value=120.0)
        tk.Scale(frame_view, from_=50, to=250, resolution=5,
                 orient=tk.HORIZONTAL, variable=self.scale_var,
                 command=lambda x: self.update_view(),
                 length=200, bg='lightgray',
                 highlightbackground='lightgray').pack(fill=tk.X, pady=5)

        self.show_axes_var = tk.BooleanVar(value=True)
        tk.Checkbutton(frame_view, text="Показывать оси координат",
                       variable=self.show_axes_var, command=self.update_view,
                       bg='lightgray', font=('Arial', 10)).pack(anchor=tk.W, pady=5)

        info_panel = tk.Frame(control_panel, bg='lightgray', height=60)
        info_panel.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        info_panel.pack_propagate(False)

        tk.Label(info_panel, text="Лабораторная работа №11",
                 bg='lightgray', font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        tk.Label(info_panel, text="Проективные преобразования",
                 bg='lightgray', font=('Arial', 9)).pack(anchor=tk.W)
        tk.Label(info_panel, text="Вариант 10: Тетраэдр и Додекаэдр",
                 bg='lightgray', font=('Arial', 9)).pack(anchor=tk.W)

        self.rotation_x = 0
        self.rotation_y = 0
        self.rotation_z = 0

        self.define_bodies()

        self.update_view()

        self.root.bind('<Configure>', self.on_window_resize)

    def define_bodies(self):

        self.tetrahedron_vertices = [
            [1, 1, 1],
            [-1, -1, 1],
            [-1, 1, -1],
            [1, -1, -1]
        ]
        norm = math.sqrt(3)
        self.tetrahedron_vertices = [
            [v[0] / norm, v[1] / norm, v[2] / norm]
            for v in self.tetrahedron_vertices
        ]

        self.tetrahedron_edges = [
            (0, 1), (0, 2), (0, 3),
            (1, 2), (1, 3),
            (2, 3)
        ]

        phi = (1 + math.sqrt(5)) / 2
        inv_phi = 1 / phi
        a = 1.0

        verts = []
        for sx in (-1, 1):
            for sy in (-1, 1):
                for sz in (-1, 1):
                    verts.append([sx * a, sy * a, sz * a])
        for sy in (-1, 1):
            for sz in (-1, 1):
                verts.append([0, sy * inv_phi, sz * phi])
        for sx in (-1, 1):
            for sy in (-1, 1):
                verts.append([sx * inv_phi, sy * phi, 0])
        for sx in (-1, 1):
            for sz in (-1, 1):
                verts.append([sx * phi, 0, sz * inv_phi])

        radius = math.sqrt(1 + 1 + 1)
        self.dodecahedron_vertices = [
            [v[0] / radius, v[1] / radius, v[2] / radius]
            for v in verts
        ]

        n = len(self.dodecahedron_vertices)
        dists = {}
        for i in range(n):
            for j in range(i + 1, n):
                vi = self.dodecahedron_vertices[i]
                vj = self.dodecahedron_vertices[j]
                d = math.sqrt(sum((vi[k] - vj[k]) ** 2 for k in range(3)))
                dists[(i, j)] = d

        edge_len = min(d for d in dists.values() if d > 1e-6)

        self.dodecahedron_edges = []
        for (i, j), d in dists.items():
            if abs(d - edge_len) < 1e-4:
                self.dodecahedron_edges.append((i, j))

    def rotate_point(self, point, angle_x, angle_y, angle_z):
        x, y, z = point

        cz, sz = math.cos(angle_z), math.sin(angle_z)
        x1 = x * cz - y * sz
        y1 = x * sz + y * cz
        z1 = z

        cy, sy = math.cos(angle_y), math.sin(angle_y)
        x2 = x1 * cy + z1 * sy
        y2 = y1
        z2 = -x1 * sy + z1 * cy

        cx, sx = math.cos(angle_x), math.sin(angle_x)
        x3 = x2
        y3 = y2 * cx - z2 * sx
        z3 = y2 * sx + z2 * cx

        return [x3, y3, z3]

    def orthographic_projection(self, point):
        scale = self.scale_var.get()
        ox, oy = self.width / 2, self.height / 2
        return point[0] * scale + ox, -point[1] * scale + oy

    def perspective_projection(self, point):
        d = self.d_var.get()
        z_offset = 3.0
        z_eff = point[2] + z_offset

        if abs(z_eff) < 1e-6:
            xp, yp = point[0], point[1]
        else:
            factor = d / z_eff
            xp = point[0] * factor
            yp = point[1] * factor

        scale = self.scale_var.get()
        ox, oy = self.width / 2, self.height / 2
        return xp * scale + ox, -yp * scale + oy

    def rotate(self, direction):
        step = math.pi / 18  # 10°
        axis, sign = direction[0], direction[1]
        if axis == 'x':
            self.rotation_x += step if sign == '+' else -step
        elif axis == 'y':
            self.rotation_y += step if sign == '+' else -step
        elif axis == 'z':
            self.rotation_z += step if sign == '+' else -step
        self.update_view()

    def reset_rotation(self):
        self.rotation_x = self.rotation_y = self.rotation_z = 0
        self.update_view()

    def on_window_resize(self, event):
        if event.widget == self.root:
            new_w = event.width - 320
            new_h = event.height
            if new_w > 0 and new_h > 0:
                self.width, self.height = new_w, new_h
                self.canvas.config(width=new_w, height=new_h)
                self.update_view()

    def update_view(self):
        self.canvas.delete("all")

        self.d_label.config(text=f"d = {self.d_var.get():.1f}")

        ax = round(math.degrees(self.rotation_x) % 360, 1)
        ay = round(math.degrees(self.rotation_y) % 360, 1)
        az = round(math.degrees(self.rotation_z) % 360, 1)
        self.angle_label.config(text=f"Углы: X={ax}°, Y={ay}°, Z={az}°")

        if self.body_var.get() == "tetrahedron":
            vertices = self.tetrahedron_vertices
            edges = self.tetrahedron_edges
            body_name = "ТЕТРАЭДР"
            color = 'purple'
        else:
            vertices = self.dodecahedron_vertices
            edges = self.dodecahedron_edges
            body_name = "ДОДЕКАЭДР"
            color = 'darkgreen'

        rotated = [
            self.rotate_point(v, self.rotation_x, self.rotation_y, self.rotation_z)
            for v in vertices
        ]

        if self.projection_var.get() == "orthographic":
            projected = [self.orthographic_projection(v) for v in rotated]
        else:
            projected = [self.perspective_projection(v) for v in rotated]

        for (i, j) in edges:
            x1, y1 = projected[i]
            x2, y2 = projected[j]
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2)

        for (x, y) in projected:
            self.canvas.create_oval(x - 4, y - 4, x + 4, y + 4,
                                    fill='red', outline='darkred')

        proj_type = "ОРТОГОНАЛЬНАЯ" if self.projection_var.get() == "orthographic" \
                    else "ЦЕНТРАЛЬНАЯ"
        title = f"{body_name} - {proj_type} ПРОЕКЦИЯ"
        if self.projection_var.get() == "perspective":
            title += f" (d={self.d_var.get():.1f})"
        self.canvas.create_text(20, 20, text=title, anchor=tk.NW,
                                fill='black', font=('Arial', 11, 'bold'))

        if self.show_axes_var.get():
            self.draw_coordinate_axes(rotated)

        self.canvas.create_oval(self.width / 2 - 3, self.height / 2 - 3,
                                self.width / 2 + 3, self.height / 2 + 3,
                                fill='black', outline='black')

    def draw_coordinate_axes(self, vertices):
        cx = sum(v[0] for v in vertices) / len(vertices)
        cy = sum(v[1] for v in vertices) / len(vertices)
        cz = sum(v[2] for v in vertices) / len(vertices)
        center = [cx, cy, cz]

        axes_pts = [
            [cx + 0.9, cy, cz],
            [cx, cy + 0.9, cz],
            [cx, cy, cz + 0.9],
        ]

        if self.projection_var.get() == "orthographic":
            c_proj = self.orthographic_projection(center)
            a_proj = [self.orthographic_projection(p) for p in axes_pts]
        else:
            c_proj = self.perspective_projection(center)
            a_proj = [self.perspective_projection(p) for p in axes_pts]

        colors = ['red', 'green', 'blue']
        labels = ['X', 'Y', 'Z']
        for i in range(3):
            x1, y1 = c_proj
            x2, y2 = a_proj[i]
            self.canvas.create_line(x1, y1, x2, y2, fill=colors[i], width=2,
                                    arrow=tk.LAST, arrowshape=(8, 10, 5))
            self.canvas.create_text(x2 + 10, y2 + 10, text=labels[i],
                                    fill=colors[i], font=('Arial', 12, 'bold'))

    def run(self):
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        ww, wh = self.width + 320, self.height + 50
        x = (sw - ww) // 2
        y = (sh - wh) // 2
        self.root.geometry(f"{ww}x{wh}+{x}+{y}")
        self.root.mainloop()


def main():
    app = ProjectionViewer(800, 600)
    app.run()


if __name__ == "__main__":
    main()
