from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.recorder import RecorderService
import numpy as np

FONT = "Noto Sans CJK SC"


class CalculusCircleAreaScene(VoiceoverScene, MovingCameraScene):
    """Introduce calculus through the area of a circle."""

    def construct(self):
        self.set_speech_service(RecorderService())
        config.frame_rate = 30
        config.pixel_width = 1920
        config.pixel_height = 1080
        self.camera.background_color = "#1a1a1a"

        title = Text(
            "从圆面积认识微积分", font=FONT, weight=BOLD, color=YELLOW
        )
        title.to_edge(UP)
        subtitle = Text("积分 · 微分 · 互为逆运算", font=FONT, color=GRAY_B)
        subtitle.next_to(title, DOWN, buff=0.3)

        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            background_line_style={"stroke_opacity": 0.2, "stroke_width": 1},
        )
        circle = Circle(radius=2, color=PURE_BLUE, stroke_width=6)
        radius_line = Line(ORIGIN, 2 * RIGHT, color=PURE_GREEN, stroke_width=4)
        radius_label = MathTex("r", color=PURE_GREEN).next_to(radius_line, DOWN * 0.5)
        VGroup(plane, circle, radius_line, radius_label).move_to(
            LEFT * 3 + DOWN * 0.5
        )

        # Segment 1: 引入问题
        question = Text(
            "一个圆的面积究竟是怎么来的?",
            font=FONT,
            color=WHITE,
        ).scale(0.9)
        question.to_edge(RIGHT)

        with self.voiceover(
            text="我们常常背圆的面积是π乘以半径的平方, 可你想过这个公式从哪里来吗?"
        ):
            self.play(FadeIn(title, shift=UP), FadeIn(subtitle, shift=UP))
            self.play(
                FadeIn(plane, shift=DOWN),
                GrowFromCenter(circle),
                GrowFromCenter(radius_line),
                FadeIn(radius_label),
                FadeIn(question, shift=LEFT),
            )
            self.wait(0.5)

        highlight_circle = circle.copy().set_stroke(color=PURE_RED, width=8)
        with self.voiceover(
            text="今天我们从一个圆开始, 把它拆开来重新认识积分和微分。"
        ):
            self.play(ShowPassingFlash(highlight_circle, run_time=2))
            self.play(Circumscribe(question, color=PURE_RED, fade_out=True))

        # Segment 2: 基础概念
        wedges = self.create_wedges(circle, n_slices=12)
        wedges.set_fill(color=BLUE, opacity=0.4)
        wedges.set_stroke(color=PURE_BLUE, width=2, opacity=0.6)
        wedge_group = VGroup(*wedges)

        with self.voiceover(
            text="把圆切成许多细薄的扇形, 每一块都像一个小三角形。"
        ):
            self.play(LaggedStart(*[FadeIn(w) for w in wedge_group], lag_ratio=0.1))
            self.wait(0.3)

        strip_layout = self.rearrange_wedges(wedges)
        strip_layout.scale(0.9)
        strip_layout.to_edge(RIGHT, buff=1.5)

        with self.voiceover(
            text="把这些扇形交错摆放, 圆就渐渐变成一个长条。"
        ):
            self.play(
                LaggedStart(
                    *[
                        w.animate.move_to(strip_layout[i].get_center())
                        for i, w in enumerate(wedge_group)
                    ],
                    lag_ratio=0.06,
                )
            )
            self.wait(0.3)

        # Segment 3: 机制原理
        top_text = Text(
            "微分: 边长变化率", font=FONT, color=PURE_GREEN
        ).scale(0.7)
        top_text.next_to(strip_layout, UP, buff=0.5)
        bottom_text = Text(
            "积分: 小面积累加", font=FONT, color=PURE_BLUE
        ).scale(0.7)
        bottom_text.next_to(strip_layout, DOWN, buff=0.5)

        perimeter_line = Line(
            strip_layout[0].get_left(), strip_layout[-1].get_right(),
            stroke_width=6,
            color=PURE_GREEN,
        )
        height_brace = BraceBetweenPoints(
            strip_layout[0].get_top(), strip_layout[0].get_bottom(),
            color=PURE_BLUE,
        )
        height_label = height_brace.get_text("r", font=FONT, color=PURE_BLUE)

        with self.voiceover(
            text="长条的上底像圆周, 它的长度就是二πr; 高度就是半径 r。"
        ):
            self.play(Write(top_text), Write(bottom_text))
            self.play(Create(perimeter_line))
            self.play(GrowFromCenter(height_brace), FadeIn(height_label, shift=LEFT))
            self.wait(0.3)

        slope_arrow = Arrow(
            strip_layout.get_right() + UP * 0.3,
            strip_layout.get_right() + UP + RIGHT * 0.8,
            color=PURE_GREEN,
            buff=0.1,
        )
        slope_text = Text(
            "dA/dr = 2πr", font=FONT, color=PURE_GREEN
        ).scale(0.65)
        slope_text.next_to(slope_arrow, RIGHT)

        with self.voiceover(
            text="微分告诉我们面积随半径增长的速率, 也就是圆周长。"
        ):
            self.play(GrowArrow(slope_arrow))
            self.play(Write(slope_text))
            self.wait(0.3)

        # Segment 4: 数学表达
        formula_group = VGroup(
            MathTex(r"A(r) = \int_0^r 2\pi x\,dx", color=PURE_BLUE),
            MathTex(r"A(r) = \pi r^2", color=YELLOW),
            MathTex(r"\frac{d}{dr}A(r) = 2\pi r", color=PURE_GREEN),
        )
        formula_group.arrange(DOWN, buff=0.4)
        formula_group.scale(0.85)
        formula_group.to_edge(LEFT, buff=0.8)

        with self.voiceover(
            text="把所有小面积加起来就是积分, 所以 A(r) 等于从零到 r 的二πx dx。"
        ):
            self.play(Write(formula_group[0]))
            self.wait(0.2)

        with self.voiceover(
            text="计算结果是熟悉的πr平方, 再微分就回到圆周长。"
        ):
            self.play(Write(formula_group[1]))
            self.play(Write(formula_group[2]))
            self.wait(0.4)

        # Segment 5: 系统整合
        rectified = self.rectify_circle(circle)
        rectified.scale(0.8)
        rectified.next_to(strip_layout, LEFT, buff=1.5)

        with self.voiceover(
            text="想象把扇形继续变细, 圆最终铺成一个长方形, 底是πr, 高是r。"
        ):
            self.play(FadeIn(rectified, shift=DOWN))
            self.play(
                LaggedStart(
                    *[ShowPassingFlash(edge.copy().set_stroke(width=5)) for edge in rectified[1]],
                    lag_ratio=0.1,
                    run_time=2,
                )
            )
            self.wait(0.3)

        inverse_arrow = CurvedArrow(
            formula_group[0].get_right(),
            formula_group[2].get_right() + RIGHT * 0.5,
            color=PURE_RED,
        )
        inverse_text = Text(
            "积分与微分互逆", font=FONT, color=PURE_RED
        ).scale(0.7)
        inverse_text.next_to(inverse_arrow, RIGHT)

        with self.voiceover(
            text="积分和微分就像拆和装, 一个把变化累积成总量, 一个再把总量拆回变化。"
        ):
            self.play(Create(inverse_arrow))
            self.play(Write(inverse_text))
            self.wait(0.3)

        # Segment 6: 学习过程
        axes = Axes(
            x_range=[0, 4.5, 1],
            y_range=[0, 16, 4],
            x_length=5,
            y_length=3.2,
            axis_config={"include_numbers": True, "font": FONT, "color": GRAY_B},
            tips=False,
        )
        axes.to_corner(DR, buff=1)
        area_graph = axes.plot(lambda x: np.pi * x**2, color=PURE_BLUE)
        slope_graph = axes.plot(lambda x: 2 * np.pi * x, color=PURE_GREEN)
        area_label = axes.get_graph_label(
            area_graph, MathTex("A(r)", color=PURE_BLUE)
        )
        slope_label = axes.get_graph_label(
            slope_graph,
            MathTex("A'(r)", color=PURE_GREEN),
            x_val=3.5,
        )

        tracker = ValueTracker(1.0)
        moving_radius = always_redraw(
            lambda: DashedLine(
                ORIGIN,
                tracker.get_value() * RIGHT,
                dash_length=0.1,
                color=PURE_GREEN,
            ).move_to(circle.get_center()),
        )
        moving_point_area = always_redraw(
            lambda: Dot(
                axes.c2p(
                    tracker.get_value(),
                    np.pi * tracker.get_value() ** 2,
                ),
                color=PURE_BLUE,
                radius=0.08,
            )
        )
        moving_point_slope = always_redraw(
            lambda: Dot(
                axes.c2p(
                    tracker.get_value(),
                    2 * np.pi * tracker.get_value(),
                ),
                color=PURE_GREEN,
                radius=0.08,
            )
        )

        with self.voiceover(
            text="随着半径慢慢变化, 面积曲线和变化率曲线一起滑动, 像在观察学习的过程。"
        ):
            self.play(FadeIn(axes, shift=UP))
            self.play(Create(area_graph), Create(slope_graph))
            self.play(FadeIn(area_label), FadeIn(slope_label))
            self.add(moving_radius, moving_point_area, moving_point_slope)
            self.play(tracker.animate.set_value(3.5), run_time=4, rate_func=smooth)
            self.wait(0.3)

        # Segment 7: 总结应用
        summary = VGroup(
            Text(
                "积分: 累加小块得到整体", font=FONT, color=PURE_BLUE
            ).scale(0.65),
            Text(
                "微分: 衡量变化的瞬时速度", font=FONT, color=PURE_GREEN
            ).scale(0.65),
            Text(
                "互逆: 让我们在物理、工程中自由切换视角",
                font=FONT,
                color=PURE_RED,
            ).scale(0.65),
        ).arrange(DOWN, buff=0.3)
        summary.to_edge(RIGHT, buff=1)

        with self.voiceover(
            text="微积分让我们在面积与变化之间自由切换, 也帮助理解物理和工程里的复杂系统。"
        ):
            self.play(FadeIn(summary, shift=LEFT))
            self.play(Circumscribe(summary, color=YELLOW, fade_out=True))
            self.wait(0.5)

        closing = Text(
            "下次看到πr平方, 记得它藏着一个微积分的故事。",
            font=FONT,
            color=WHITE,
        ).scale(0.7)
        closing.next_to(subtitle, DOWN, buff=0.8)

        with self.voiceover(
            text="下次遇到圆面积公式, 别忘了其中藏着一个关于积分与微分的故事。"
        ):
            self.play(FadeIn(closing, shift=UP))
            self.wait(1.0)

    def create_wedges(self, circle, n_slices=12):
        center = circle.get_center()
        radius = circle.radius
        wedges = []
        for i in range(n_slices):
            angle_start = TAU * i / n_slices
            angle_end = TAU * (i + 1) / n_slices
            wedge = Sector(
                outer_radius=radius,
                angle=angle_end - angle_start,
                start_angle=angle_start,
                arc_center=center,
                fill_opacity=0.4,
            )
            wedges.append(wedge)
        return wedges

    def rearrange_wedges(self, wedges):
        arranged = VGroup()
        for i, wedge in enumerate(wedges):
            copy = wedge.copy()
            direction = 1 if i % 2 == 0 else -1
            copy.rotate(-copy.start_angle - copy.angle / 2)
            copy.shift(RIGHT * i * 0.22)
            copy.shift(UP * direction * copy.outer_radius * 0.2)
            arranged.add(copy)
        return arranged

    def rectify_circle(self, circle):
        width = np.pi * circle.radius
        height = circle.radius
        rectangle = Rectangle(
            width=width,
            height=height,
            color=PURE_BLUE,
            fill_opacity=0.25,
        )
        edges = VGroup(*rectangle.get_lines())
        return VGroup(rectangle, edges)
