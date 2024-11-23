import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sympy as sp
import ctypes
from matplotlib.backend_bases import MouseButton
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk

class DraggableText:
    def __init__(self, ax, text):
        self.ax = ax
        self.text = self.ax.text(0.5, 0.5, text, ha='center', va='center')
        self.press = None
        self.cur_xlim = ax.get_xlim()
        self.cur_ylim = ax.get_ylim()
        self.ax.set_picker(True)  # 启用鼠标点击事件

    def on_press(self, event):
        if event.inaxes != self.ax:
            return
        if event.button == MouseButton.LEFT:
            self.press = (event.xdata, event.ydata)
            self.text.set_animated(True)

    def on_release(self, event):
        if event.button != MouseButton.LEFT:
            return
        self.press = None
        self.text.set_animated(False)

    def on_motion(self, event):
        if self.press is None:
            return
        if event.inaxes != self.ax:
            return
        dx = event.xdata - self.press[0]
        dy = event.ydata - self.press[1]
        self.text.set_position((self.press[0] + dx, self.press[1] + dy))
        self.press = (event.xdata, event.ydata)
#告诉操作系统使用程序自身的dpi适配
ctypes.windll.shcore.SetProcessDpiAwareness(1)
#获取屏幕的缩放因子
ScaleFactor=ctypes.windll.shcore.GetScaleFactorForDevice(0)
class SymbolKeyboard(tk.Toplevel):
    def __init__(self, master, symbols):
        super().__init__(master)
        self.title("符号键盘")
        self.geometry("600x300")
        self.attributes('-topmost', True)  # 确保窗口置顶

        self.symbols_frame = ttk.Frame(self)
        self.symbols_frame.pack(pady=10)

        for i, (symbol_text, symbol_value) in enumerate(symbols):
            button = ttk.Button(self.symbols_frame, text=symbol_text, command=lambda v=symbol_value: self.insert_symbol(v))
            button.grid(row=i // 5, column=i % 5, padx=5, pady=5)

    def insert_symbol(self, symbol):
        cursor_position = self.master.input_entry.index(tk.INSERT)  # 获取光标位置
        self.master.input_entry.insert(cursor_position, symbol)  # 在光标位置插入符号
        self.master.input_entry.focus_set()  # 将焦点重新设置到输入框
        self.master.update_preview()  # 更新预览


class MathEditor(tk.Toplevel):
    def __init__(self, master=None, callback=None):
        super().__init__(master)
        
        self.title("高等数学公式编辑器")
        self.geometry("800x800")

        self.callback = callback  # 用于返回公式到主窗口

        # 输入框
        self.input_label = ttk.Label(self, text="请输入数学公式 (使用变量 x, y, z 等):")
        self.input_label.pack(pady=10)

        self.input_entry = ttk.Entry(self, width=70)
        self.input_entry.pack(pady=10)

        # 符号键盘按钮
        self.open_basic_keyboard_button = ttk.Button(self, text="打开基本符号键盘", command=self.open_basic_keyboard)
        self.open_basic_keyboard_button.pack(pady=5)

        self.open_trigonometric_keyboard_button = ttk.Button(self, text="打开三角函数键盘", command=self.open_trigonometric_keyboard)
        self.open_trigonometric_keyboard_button.pack(pady=5)

        self.open_linear_algebra_keyboard_button = ttk.Button(self, text="打开线性代数符号键盘", command=self.open_linear_algebra_keyboard)
        self.open_linear_algebra_keyboard_button.pack(pady=5)

        self.open_abstract_algebra_keyboard_button = ttk.Button(self, text="打开抽象代数符号键盘", command=self.open_abstract_algebra_keyboard)
        self.open_abstract_algebra_keyboard_button.pack(pady=5)

        self.open_logic_symbols_keyboard_button = ttk.Button(self, text="打开逻辑符号键盘", command=self.open_logic_symbols_keyboard)
        self.open_logic_symbols_keyboard_button.pack(pady=5)

        self.open_xyz_keyboard_botton = ttk.Button(self,text='打开字母键盘（测试）',command=self.open_xyz_keyboard)
        self.open_xyz_keyboard_botton.pack(pady=5)

        # 完成按钮
        self.finish_button = ttk.Button(self, text="完成", command=self.finish_editing)
        self.finish_button.pack(pady=20)

        # 预览区域
        self.preview_frame = ttk.Frame(self)
        self.preview_frame.pack(pady=10)

        # Matplotlib 图形
        self.figure, self.ax = plt.subplots(figsize=(5, 2))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.preview_frame)
        self.canvas.get_tk_widget().pack()
        toolbar = NavigationToolbar2Tk(self.canvas, self.preview_frame)  # 创建导航工具栏
        toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        # 初始化预览
        self.input_entry.bind("<KeyRelease>", lambda event: self.update_preview())
        self.update_preview()

    def finish_editing(self):
        # 获取输入框中的公式
        formula_text = self.input_entry.get()
        if self.callback:
            self.callback(formula_text)  # 调用父窗口的回调方法，传递公式
        self.destroy()  # 关闭编辑器窗口

    def open_basic_keyboard(self):
        basic_symbols = [
            ('+', ' + '), 
            ('-', ' - '), 
            ('*', ' * '), 
            ('/', ' / '),
            ('^', ' ** '), 
            ('(', '('), 
            (')', ')'), 
            ('=', ' = '),
            ('>', ' > '),      # 大于
            ('<', ' < '),      # 小于
            ('≥', ' >= '),     # 大于等于
            ('≤', ' <= '),     # 小于等于
            ('≠', ' != '),     # 不等于
            ('&&', ' and '),   # 逻辑与
            ('||', ' or '),    # 逻辑或
            ('!', ' not '),    # 逻辑非
            ('%', ' % '),      # 百分比
            ('abs', 'abs(')    # 绝对值
        ]
        SymbolKeyboard(self, basic_symbols)
    def open_xyz_keyboard(self):
        greek_letters = [
        ('α', 'alpha'),               # Alpha
        ('δ', 'delta'),               # Delta
        ('ε', 'epsilon'),             # Epsilon
        ('ζ', 'zeta'),                # Zeta
        ('η', 'eta'),                 # Eta
        ('θ', 'theta'),               # Theta
        ('ι', 'iota'),                # Iota
        ('κ', 'kappa'),               # Kappa
        ('λ', 'lambda'),              # Lambda
        ('μ', 'mu'),                  # Mu
        ('ν', 'nu'),                  # Nu
        ('ξ', 'xi'),                  # Xi
        ('ο', 'omicron'),             # Omicron
        ('π', 'pi'),                  # Pi
        ('ρ', 'rho'),                 # Rho
        ('σ', 'sigma'),               # Sigma
        ('τ', 'tau'),                 # Tau
        ('υ', 'upsilon'),             # Upsilon
        ('φ', 'phi'),                 # Phi
        ('χ', 'chi'),                 # Chi
        ('ψ', 'psi'),                 # Psi
        ('ω', 'omega'),                # Omega
        ('x','x'),
        ('y','y'),
        ('z','z'),
        ('p','p'),
        ('q','q'),
        ('r','r'),
        ('s','s'),
        ('k','k'),
        ('t','t'),
    ]
        SymbolKeyboard(self,greek_letters)

    def open_trigonometric_keyboard(self):
        trigonometric_symbols = [
            ('sin', 'sin('), 
            ('cos', 'cos('), 
            ('tan', 'tan('),
            ('arcsin', 'asin('), 
            ('arccos', 'acos('), 
            ('arctan', 'atan('),
            ('sec', 'sec('),      # 正割
            ('csc', 'csc('),      # 余割
            ('cot', 'cot('),      # 余切
            ('sinh', 'sinh('),    # 双曲正弦
            ('cosh', 'cosh('),    # 双曲余弦
            ('tanh', 'tanh('),     # 双曲正切
            ('arcsinh', 'asinh('), # 反双曲正弦
            ('arccosh', 'acosh('), # 反双曲余弦
            ('arctanh', 'atanh(')  # 反双曲正切
        ]
        SymbolKeyboard(self, trigonometric_symbols)


    def open_calculus_keyboard(self):
        calculus_symbols = [
            ('∫', 'integrate('),          # 积分
            ('lim', 'limit('),            # 极限
            ('d/dx', 'diff('),            # 导数
            ('!', 'factorial('),          # 阶乘
            ('√', 'sqrt('),               # 平方根
            ('log', 'log('),              # 对数
            ('exp', 'exp(')               # 指数函数
        ]
        SymbolKeyboard(self, calculus_symbols)

    def open_linear_algebra_keyboard(self):
        linear_algebra_symbols = [
            ('∑', 'Sum('),               # 求和
            ('det', 'det('),             # 行列式
            ('tr', 'trace('),            # 矩阵迹
            ('rank', 'rank('),           # 矩阵秩
            ('⊕', 'direct_sum('),        # 直和
            ('⊗', 'tensor_product('),    # 张量积
            ('||', 'norm('),             # 范数
            ('M', 'matrix('),            # 矩阵
            ('V', 'vector(')             # 向量
        ]
        SymbolKeyboard(self, linear_algebra_symbols)

    def open_abstract_algebra_keyboard(self):
        abstract_algebra_symbols = [
            ('ℤ', 'integers'),           # 整数集
            ('ℚ', 'rationals'),          # 有理数集
            ('ℝ', 'reals'),              # 实数集
            ('ℂ', 'complexes'),          # 复数集
            ('P', 'polynomial(')         # 多项式
        ]
        SymbolKeyboard(self, abstract_algebra_symbols)

    def open_logic_symbols_keyboard(self):
        logic_symbols = [
            ('∧', 'and('),                # 与
            ('∨', 'or('),                 # 或
            ('¬', 'not('),                # 非
            ('→', 'implies('),            # 蕴含
            ('↔', 'iff(')                 # 当且仅当
        ]
        SymbolKeyboard(self, logic_symbols)
    
    def update_preview(self):
        # 清空当前图形
        self.ax.clear()
        
        # 获取输入内容
        formula_text = self.input_entry.get()

        try:
            # 检查是否包含等号，若有，则处理为方程
            if '=' in formula_text:
                # 使用 SymPy 解析公式并构造一个 Eq 对象
                left_expr, right_expr = formula_text.split('=', 1)  # 将等式两边分开
                expr = sp.Eq(sp.sympify(left_expr), sp.sympify(right_expr))  # 创建方程
            else:
                expr = sp.sympify(formula_text)  # 否则直接解析表达式

            # 使用 LaTeX 格式化公式
            latex_str = sp.latex(expr)

            # 清除图形并添加 LaTeX 文本
            self.ax.text(0.5, 0.5, f"${latex_str}$", fontsize=20, ha='center', va='center')
            self.ax.axis('off')  # 关闭坐标轴
        except Exception as e:
            self.ax.text(0.5, 0.5, f"错误: {str(e)}", fontsize=12, ha='center', va='center')
            self.ax.axis('off')  # 关闭坐标轴

        # 更新画布
        self.canvas.draw()

# 在 MainApp 类中添加编辑、删除和联合求解功能

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("表达式管理程序")
        self.geometry("1000x500")
        self.tk.call('tk', 'scaling', ScaleFactor / 75)
        
        # 初始化标志，判断编辑器是否打开
        self.is_editor_open = False
        self.formulas = []  # 存储所有的公式

        # 创建一个顶层框架用作主界面
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 主窗口的 Canvas 和滚动条
        self.canvas = tk.Canvas(main_frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.main_preview_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.main_preview_frame, anchor="nw")

        # 打开数学公式编辑器按钮
        self.open_editor_button = ttk.Button(self, text="打开数学公式编辑器", command=self.open_math_editor)
        self.open_editor_button.pack(pady=10)

        #更新按钮
        self.update_button = ttk.Button(self,text="更新列表", command=self.update_scrollregion)
        self.update_button.pack(padx=10)

        # 联合求解按钮
        self.solve_button = ttk.Button(self, text="联合求解", command=self.solve_equations)
        self.solve_button.pack(pady=10)

    def open_math_editor(self):
        # 打开 MathEditor 编辑器窗口，并传递回调函数以接收返回的公式
        MathEditor(self, callback=self.add_formula)
        self.update_main_preview()  # 更新预览显示所有公式

    def add_formula(self, formula_text):
        # 添加新的公式到公式列表
        self.formulas.append(formula_text)
        self.update_main_preview()  # 更新预览

    def update_main_preview(self):
        # 清空当前的预览框架
        for widget in self.main_preview_frame.winfo_children():
            widget.destroy()

        # 显示每一个公式
        for i, formula in enumerate(self.formulas):
            frame = ttk.Frame(self.main_preview_frame)
            frame.pack(pady=5, fill=tk.X)

            label = ttk.Label(frame, text=f"公式 {i + 1}: {formula}", wraplength=300)
            label.pack(fill=tk.X)  # 确保标签填充整个宽度

            # 添加编辑按钮
            edit_button = ttk.Button(frame, text="编辑", command=lambda idx=i: self.edit_formula(idx))
            edit_button.pack(side=tk.LEFT, padx=5)

            # 添加删除按钮
            delete_button = ttk.Button(frame, text="删除", command=lambda idx=i: self.delete_formula(idx))
            delete_button.pack(side=tk.LEFT)

            # 计算公式并绘制
            self.display_formula_in_canvas(formula, frame)

        # 更新 Canvas 的滚动区域
        self.update_scrollregion()

    def display_formula_in_canvas(self, formula_text, frame):
        # 使用 SymPy 解析公式并生成 LaTeX 字符串
        try:
            if '=' in formula_text:
                left_expr, right_expr = formula_text.split('=', 1)
                expr = sp.Eq(sp.sympify(left_expr), sp.sympify(right_expr))
            else:
                expr = sp.sympify(formula_text)
        except Exception as e:
            latex_str = f"错误: {str(e)}"
        latex_str = sp.latex(expr)
        
        # 创建 Matplotlib 图形来显示公式
        fig, ax = plt.subplots(figsize=(5, 1))
        ax.text(0.5, 0.5, f"${latex_str}$", fontsize=12, ha='center', va='center')
        ax.axis('off')

        # 将图形嵌入到 Tkinter 窗口中
        #canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas_fig = FigureCanvasTkAgg(fig, master=frame)
        canvas_fig.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # 添加matplotlib导航工具栏
        toolbar = NavigationToolbar2Tk(canvas_fig, frame)  # 创建导航工具栏
        toolbar.update()

        # 绘制图形
        canvas_fig.draw()
        canvas_fig.get_tk_widget().pack(fill=tk.X)
        
        canvas_fig.draw()

    def update_scrollregion(self):
        # 更新 canvas 滚动区域
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def edit_formula(self, idx):
        # 编辑公式功能
        formula_text = self.formulas[idx]
        editor = MathEditor(self, callback=lambda new_formula: self.save_edited_formula(idx, new_formula))
        editor.input_entry.delete(0, tk.END)
        editor.input_entry.insert(0, formula_text)
        editor.update_preview()

    def save_edited_formula(self, idx, new_formula):
        # 保存编辑后的公式
        self.formulas[idx] = new_formula
        self.update_main_preview()

    def delete_formula(self, idx):
        # 删除公式功能
        del self.formulas[idx]
        self.update_main_preview()

    def solve_equations(self):
        # 联合求解功能
        if len(self.formulas) < 2:
            tk.messagebox.showerror("错误", "至少需要两个公式进行联合求解！")
            return

        # 询问用户选择求解的变量
        variable = tk.simpledialog.askstring("选择变量", "请输入要求解的变量（如x, y, z等）:")
        if not variable:
            return
        symbols = sp.symbols(variable)  # 将变量名列表转换为符号

        # 将公式转换为 SymPy 方程
        equations = []
        for formula in self.formulas:
            try:
                if '=' in formula:
                    left_expr, right_expr = formula.split('=', 1)
                    eq = sp.Eq(sp.sympify(left_expr), sp.sympify(right_expr))
                else:
                    eq = sp.sympify(formula)
            except Exception as e:
                tk.messagebox.showerror("错误", f"公式解析错误: {str(e)}")
                return
            equations.append(eq)

        # 使用 SymPy 求解
        solutions = sp.solve(equations, symbols)

        # 创建新窗口显示结果
        result_window = tk.Toplevel()
        result_window.title("求解结果")

        # 创建一个可滚动的画布和框架
        canvas = tk.Canvas(result_window)
        scroll_y = tk.Scrollbar(result_window, orient="vertical", command=canvas.yview)
        scroll_x = tk.Scrollbar(result_window, orient="horizontal", command=canvas.xview)

        # 创建一个框架来放置公式文本
        frame = tk.Frame(canvas)

        # 使用 SymPy 生成 LaTeX 字符串
        latex_str = sp.latex(sp.sympify(solutions))

        # 创建 Matplotlib 图形来显示公式
        fig, ax = plt.subplots(figsize=(5, 1))
        ax.text(0.5, 0.5, f"${latex_str}$", fontsize=12, ha='center', va='center')
        ax.axis('off')

        # 将图形嵌入到 Tkinter 窗口中
        canvas_fig = FigureCanvasTkAgg(fig, master=frame)
        canvas_fig.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        # 添加matplotlib导航工具栏
        toolbar = NavigationToolbar2Tk(canvas_fig, frame)  # 创建导航工具栏
        toolbar.update()

        # 绘制图形
        canvas_fig.draw()

        # 将框架放入画布中
        canvas.create_window((0, 0), window=frame, anchor='nw')

        # 更新画布的视图范围
        frame.update_idletasks()  # 更新画布以获得框架的大小
        canvas.config(scrollregion=canvas.bbox("all"), width=500, height=200)
        canvas.configure(xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        # 放置画布和滚动条
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        # 使matplotlib窗口居中
        frame.pack(fill=tk.BOTH, expand=True)

def _quit():
    app.quit()
    app.destroy()
if __name__ == "__main__":
    app = MainApp()
    app.protocol("WM_DELETE_WINDOW", _quit)
    app.mainloop()
