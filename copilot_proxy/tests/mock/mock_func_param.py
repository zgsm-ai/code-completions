

MOCK_NOT_REPETITIVE_CONTENT = [
    {
        "content": "12345678",
        "label": "12345678"
    },
    {
        "content": """
        def funca(data, is_single_completion):
            if is_single_completion:
                if isinstance(data["stop"], list):
                    data["stop"].append("\n")
                elif isinstance(data["stop"], str):
                    data["stop"] += "\n"
            # 获取返回值
            # 返回返回值
            # 获取请求参数
            # 验证参数
            # 验证通过，调用函数
            # 验证不通过，返回错信息""",
        "label": """
        def funca(data, is_single_completion):
            if is_single_completion:
                if isinstance(data["stop"], list):
                    data["stop"].append("\n")
                elif isinstance(data["stop"], str):
                    data["stop"] += "\n"
            # 获取返回值
            # 返回返回值
            # 获取请求参数
            # 验证参数
            # 验证通过，调用函数
            # 验证不通过，返回错信息"""
    },
    {
        "content": """
    def funca(data, is_single_completion):
        if is_single_completion:
            if isinstance(data["stop"], list):
                data["stop"].append("\n")
            elif isinstance(data["stop"], str):
                data["stop"] += "\n"
        # 获取返回值
        # 获取返回值
        # 获取返回值""",
        "label": """
    def funca(data, is_single_completion):
        if is_single_completion:
            if isinstance(data["stop"], list):
                data["stop"].append("\n")
            elif isinstance(data["stop"], str):
                data["stop"] += "\n"
        # 获取返回值
        # 获取返回值
        # 获取返回值"""
    },
]

MOCK_REPETITIVE_CONTENT = [
    {
        # 其禄提出的问题
        "content": """
        def funca(data, is_single_completion):
            if is_single_completion:
                if isinstance(data["stop"], list):
                    data["stop"].append("\n")
                elif isinstance(data["stop"], str):
                    data["stop"] += "\n"
            # 获取返回值
            # 返回返回值
            # 获取请求参数
            # 验证参数
            # 验证通过，调用函数
            # 验证不通过，返回错信息
            # 获取返回值
            # 返回返回值
            # 获取请求参数
            # 验证参数
            # 验证通过，调用函数
            # 验证不通过，返回错信息""",
        "label": """
        def funca(data, is_single_completion):
            if is_single_completion:
                if isinstance(data["stop"], list):
                    data["stop"].append("\n")
                elif isinstance(data["stop"], str):
                    data["stop"] += "\n"
            # 获取返回值
            # 返回返回值
            # 获取请求参数
            # 验证参数
            # 验证通过，调用函数
            # 验证不通过，返回错信息"""
    },
    {
        "content": """
        def funca(data, is_single_completion):
            if is_single_completion:
                if isinstance(data["stop"], list):
                    data["stop"].append("\n")
                elif isinstance(data["stop"], str):
                    data["stop"] += "\n"
        def funca(data, is_single_completion):
            if is_single_completion:
                if isinstance(data["stop"], list):
                    data["stop"].append("\n")
                elif isinstance(data["stop"], str):
                    data["stop"] += "\n"
""",
        "label": """
        def funca(data, is_single_completion):
            if is_single_completion:
                if isinstance(data["stop"], list):
                    data["stop"].append("\n")
                elif isinstance(data["stop"], str):
                    data["stop"] += "\n"
"""
    },
    {
        "content": """
        @classmethod
        def get_ongoing_count_by_id(cls, pipeline):
            # 获取流水线正在执行的流水线数量
            #  查询历史表，根据流水线配置和存在正在执行的流水线
            #  查询历史表，根据流水线配置和存在正在执行的流水线
            #  查询历史表，根据流水线配置和存在正在执行的流水线
            #  查询历史表，根据流水线配置和存在正在执行的流水线
            #  查询历史表，根据流水线配置和存在正在执行的流水线
""",
        "label": """
        @classmethod
        def get_ongoing_count_by_id(cls, pipeline):
            # 获取流水线正在执行的流水线数量
            #  查询历史表，根据流水线配置和存在正在执行的流水线
"""
    },
    {
        "content": """
        def funca(data, is_single_completion):
            if is_single_completion:
                if isinstance(data["stop"], list):
                    data["stop"].append("\n")
                elif isinstance(data["stop"], str):
                    data["stop"] += "\n"
            # 获取返回值
            # 获取返回值
            # 获取返回值
            # 获取返回值
            # 获取返回值
            # 获取返回值
            # 获取返回值""",
        "label": """
        def funca(data, is_single_completion):
            if is_single_completion:
                if isinstance(data["stop"], list):
                    data["stop"].append("\n")
                elif isinstance(data["stop"], str):
                    data["stop"] += "\n"
            # 获取返回值"""
    },
    {
        # 重复内容过多，因超过500Token 或 因超时被截断
        "content": """print("hello")
        print("hello")
        print("hello")
        print("hello")
        print("hello")
        print("hello")
        print("hello")
        print("hello")
        print("hello")
        print("hello")
        print("hello")
        print("hello")
        print("hello")
        print("hello")
        print("hello")
        print("hello")
        print("hello")
        print("hello")
        print("hello")
        print("hello")
        print("hello")
        print("hello")
        print("hello")
        print("hello")
        print("hello")
        pri""",

        "label": """print("hello")
        """
    },
    {
        # 洋哥群里反馈的问题
        "content": """
        if($sum>0){
            $profit_loss_release=round($profit_loss_release, 2);
            $profit_loss_release=abs($profit_loss_release);
            $profit_loss_release=number_format($profit_loss_release, 2);
            $profit_loss_release=floatval($profit_loss_release);
            $profit_loss_release=round($profit_loss_release, 2);
            $profit_loss_release=abs($profit_loss_release);
            $profit_loss_release=number_format($profit_loss_release, 2);
            $profit_loss_release=floatval($profit_loss_release);
            $profit_loss_release=round($profit_loss_release, 2);
            $profit_loss_release=abs($profit_loss_release);
            $profit_loss_release=number_format($profit_loss_release, 2);
            $profit_loss_release=floatval($profit_loss_release);
            $profit_loss_release=round($profit_loss_release, 2);
            $profit_loss_release=abs($profit_loss_release);
            $profit_loss_release=number_format($profit_loss_release, 2);
            $profit_loss_release=floatval($profit_loss_release);
            $profit_loss_release=round($profit_loss_release, 2);
            $profit_loss_release=abs($profit_loss_release);
            $profit_loss_release=number_format($profit_loss_release, 2);
            $profit_loss_release=floatval($profit_loss_release);
            $profit_loss_release=round($profit_loss_release, 2);
            $profit_loss_release=abs($profit_loss_release);
            $profit_loss_release=number_
            """,
        "label": """
        if($sum>0){
            $profit_loss_release=round($profit_loss_release, 2);
            $profit_loss_release=abs($profit_loss_release);
            $profit_loss_release=number_format($profit_loss_release, 2);
            $profit_loss_release=floatval($profit_loss_release);"""
    }

]

MOCK_CUT_SUFFIX_OVERLAP_CONTENT = [
    {
        "text": "result_map[handler.get_metric_name()] = cur_val",
        "suffix": "all_val.append(cur_val)",
        "label": "result_map[handler.get_metric_name()] = cur_val"
    },
    {
        "text": "result_map[handler.get_metric_name()] = cur_val",
        "suffix": "result_map[handler.get_metric_name()] = cur_val \n"
                  "all_val.append(cur_val)",
        "label": "result_map[handler.get_metric_name()] = cur_val"
    },
    {
        "text": "result_map[handler.get_metric_name()] = cur_val",
        "suffix": "result_map[handler.get_metric_name()] = cur_val",
        "label": ""
    },
    {
        "text": "result_map[handler.get_metric_name0()] = cur_val0\n"
                "result_map[handler.get_metric_name()] = cur_val\n"
                "result_map[handler.get_metric_name2()] = cur_val2",
        "suffix": "result_map[handler.get_metric_name()] = cur_val\n"
                  "result_map[handler.get_metric_name2()] = cur_val2\n"
                  "result_map[handler.get_metric_name3()] = cur_val3",
        "label": "result_map[handler.get_metric_name0()] = cur_val0\n"
    },
    # 苏德利反馈的问题
    {
        "text": """
        ans = []
        for key, value in data.items():
            for sample in value:
                ans.append(BaseDatasetType(
                    prefix=sample['prefix'],
                    suffix=sample['suffix'],
                    additional_data={
                        'language': sample['language'],
                        'feature': sample['feature'],
                        'reference_answer': sample['reference_answer'],
                        'file_path': sample.get("path", "")
                    }
                ))
        """,
        "suffix": """        ans = ["尝试阻止cut_suffix_overlap"]
        ans = ["又尝试阻止cut_suffix_overlap"]
        for key, value in data.items():
            for sample in value:
                ans.append(BaseDatasetType(
                    prefix=sample['prefix'],
                    suffix=sample['suffix'],
                    additional_data={
                        'language': sample['language'],
                        'feature': sample['feature'],
                        'reference_answer': sample['reference_answer'],
                        'file_path': sample.get("path", "")
                    }
                ))
        """,
        "label": """
        ans = []
"""
    },
]

MOCK_CUT_TEXT_BY_TREE_SITTER = [
    {
        "language": "python",
        "text": "lines, bilingual))",
        "prefix": "return _parse_srt_lines(",
        "suffix": ")",
        "label": "lines, bilingual"
    },
    {
        "language": "python",
        "text": "   lines = srtstrs.split('\n')\n   return _parse_srt_lines(lines, bilingual):",
        "prefix": "def _parse_srt_string(srtstrs, bilingual=False):\n",
        "suffix": "",
        "label": "   lines = srtstrs.split('\n')\n   return _parse_srt_lines(lines, bilingual)"
    }
]

MOCK_FIND_NEAREST_BLOCK = [
    {
        "code": """
    def get_node_text1(self, source_code, node):
        return source_code[node.start_byte:node.end_byte].decode('utf-8')
    def get_node_text2(self, source_code, node):
        print("hello")
        print("hello")
        print("hello")
        print("hello")
        print("hello")
        print("hello")
        print("hello")
        return source_code[node.start_byte:node.end_byte].decode('utf-8')

    """,
        "language": "python",
        "start_number": 4,
        "end_number": 7,
        "label": """print("hello")
        print("hello")
        print("hello")
        print("hello")
        print("hello")
        print("hello")
        print("hello")
        return source_code[node.start_byte:node.end_byte].decode('utf-8')"""
    },

    {
        "code": """
    def get_node_text1(self, source_code, node):
        return source_code[node.start_byte:node.end_byte].decode('utf-8')
    def get_node_text2(self, source_code, node):
        print("hello")
        print("hello")
        print("hello")
        print("hello")
        print("hello")
        print("hello")
        print("hello")
        return source_code[node.start_byte:node.end_byte].decode('utf-8')

    """,
        "language": "python",
        "start_number": 2,
        "end_number": 2,
        "label": """return source_code[node.start_byte:node.end_byte].decode('utf-8')"""
    },

    {
        "code": """
class DataHandlerStrategy:
    def __init__(self, handler: AbstractDataHandler):
        self._handler = handler

    def handle(self, data) -> List[BaseDatasetType]:
        return self._handler.handle(data)

    def load_data(self, path):
        return self._handler.load_data(path)
    """,
        "language": "python",
        "start_number": 3,
        "end_number": 3,
        "label": """def __init__(self, handler: AbstractDataHandler):
        self._handler = handler

    def handle(self, data) -> List[BaseDatasetType]:
        return self._handler.handle(data)

    def load_data(self, path):
        return self._handler.load_data(path)"""
    },
    # 上下文不完整时，抽取函数级别block
    {
        "code": """
f __init__(self, handler: AbstractDataHandler):
        self._handler = handler

    def handle(self, data) -> List[BaseDatasetType]:
        return self._handler.handle(data)

    def load_data(self, path):
        return self._handler.load_dat
    """,
        "language": "python",
        "start_number": 5,
        "end_number": 5,
        "label": """def handle(self, data) -> List[BaseDatasetType]:
        return self._handler.handle(data)"""
    },
    # 上下文不完整时，抽取函数级别block
    {
        "code": """
f __init__(self, handler: AbstractDataHandler):
        self._handler = handler

    def handle(self, data) -> List[BaseDatasetType]:
        return self._handler.handle(data)

    def load_data(self, path):
        return self._handler.load_dat
    """,
        "language": "python",
        "start_number": 4,
        "end_number": 5,
        "label": """def handle(self, data) -> List[BaseDatasetType]:
        return self._handler.handle(data)"""
    },
]

MOCK_FIND_SECOND_LEVEL_NODE_BY_LINE_NUM = [
    {
        "code": """
import os
import json
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
import matplotlib.ticker as ticker
from matplotlib.font_manager import FontProperties


def get_font():
    # 加载字体文件
    font_path = '../fonts/SimHei.ttf'  # 替换为你的字体文件路径
    font_prop = FontProperties(fname=font_path)
    return font_prop


# 加载当前路径所有文件夹下同名文件json数据
def load_data():
    # 获取result目录下的所有文件夹
    folders = [f for f in os.listdir('.') if os.path.isdir(f) and "show" not in f]

    # 遍历这些文件夹，找到所有.json文件，放入set中
    data_set = set()
    for folder in folders:
        for file in os.listdir(folder):
            if file.endswith('.json'):
                data_set.add(file)
    # 统计
    stat_map = {}
    for stat_file in data_set:
        stat_map[stat_file] = {}
        for folder in folders:
            file_path = os.path.join(folder, stat_file)
            if os.path.exists(file_path):
                stat_map[stat_file][folder] = {}
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for item in data:
                        for metric, metric_score in item['valuation'].items():
                            if metric.endswith('percentage'):
                                # 如果stat_map[stat_file][folder][metric]不存在，则创建一个空列表
                                if metric not in stat_map[stat_file][folder]:
                                    stat_map[stat_file][folder][metric] = []
                                stat_map[stat_file][folder][metric].append(metric_score)
                        for name, value in item["additional_data"].items():
                            if name == "feature":
                                if name not in stat_map[stat_file][folder]:
                                    stat_map[stat_file][folder][name] = []
                                stat_map[stat_file][folder][name].append(value)
    # 统计数据输出到文件 stat.json中
    with open('stat.json', 'w', encoding='utf-8') as f:
        json.dump(stat_map, f, ensure_ascii=False, indent=4)
    return stat_map


# 展示模型在不同评价指标下的每个样本的表现
def show_all(stat_map):
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    # 确保保存图片的目录存在
    os.makedirs('show', exist_ok=True)

    # 遍历stat_map中的每个键
    for scenario, models in stat_map.items():
        # 获取所有的评价指标
        metrics = set()
        for model_name, values in models.items():
            metrics.update(values.keys())
        # 移除不包含percentage后缀的指标
        metrics = [metric for metric in metrics if metric.endswith('percentage')]
        # 如果metrics为空，则跳过这个scenario
        if not metrics:
            continue

        # 创建一个新的图形，包含多个子图
        num_metrics = len(metrics)
        fig, axes = plt.subplots(num_metrics, 1, figsize=(10, 5 * num_metrics))  # 根据评价指标数量创建子图

        if num_metrics == 1:
            axes = [axes]  # 如果只有一个子图，确保axes是一个列表

        # 为每个评价指标创建一个子图
        for ax, metric in zip(axes, metrics):
            bar_width = 0.2  # 设置每个柱状图的宽度
            index = range(len(next(iter(models.values()))[metric]))  # 样本索引
            for i, (model_name, values) in enumerate(models.items()):
                if metric in values and values[metric]:  # 忽略空列表
                    ax.bar([x + i * bar_width for x in index], values[metric], bar_width, label=model_name)
            ax.set_title(f"{metric}", fontproperties=get_font())
            ax.set_xlabel('样本索引', fontproperties=get_font())
            ax.set_ylabel(f'{metric}（百分数）', fontproperties=get_font())
            ax.grid(True)
            ax.xaxis.set_major_locator(MaxNLocator(integer=True))  # 设置x轴标签为整数
            ax.legend()  # 显示图例

        plt.tight_layout()
        plt.savefig(f"show/show_all_{scenario}.png")  # 保存图片
        plt.show()  # 显示图形


# 展示模型在所有样本及评价指标上的平均表现
def show_final(stat_map):
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    # 确保保存图片的目录存在
    os.makedirs('show', exist_ok=True)

    for scenario, models in stat_map.items():
        final_model_val_result = {}
        for model_name, values in models.items():
            avg_percentage = values.get('avg_percentage', [])
            if not avg_percentage:
                continue
            final_avg_percentage = sum(avg_percentage) / len(avg_percentage)
            final_model_val_result[model_name] = final_avg_percentage

        if not final_model_val_result:
            continue

        # 按照结果进行排序
        final_model_val_result = dict(sorted(final_model_val_result.items(), key=lambda item: item[1], reverse=True))

        # 展示不同模型的最终结果，放在一个柱状图中
        model_names = list(final_model_val_result.keys())
        avg_percentages = list(final_model_val_result.values())

        # 生成颜色列表
        colors = plt.cm.tab20(np.linspace(0, 1, len(model_names)))

        plt.figure(figsize=(10, 6))
        bars = plt.bar(model_names, avg_percentages, color=colors, width=0.5)

        # 在柱状图上方显示数值
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.2f}', ha='center', va='bottom')

        plt.xlabel('模型名称', fontproperties=get_font())
        plt.ylabel('平均评价指标', fontproperties=get_font())
        plt.title(f'{scenario} 数据集下不同模型的最终结果', fontproperties=get_font())
        plt.xticks(rotation=45, fontproperties=get_font())
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()

        # 保存图像
        plt.savefig(f'show/show_final_{scenario}.png')
        plt.show()


# 展示模型在不同feature组下的平均表现（例如：行级or块级）
def show_group_by_feature(stat_map):

    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    # 确保保存图片的目录存在
    os.makedirs('show', exist_ok=True)

    for scenario, models in stat_map.items():
        model_group_score = {}
        for model_name, values in models.items():
            # 收集数据
            each_sample_score_and_feature = {}
            for metric, metric_value in values.items():
                if metric == "avg_percentage" or metric == "feature":
                    each_sample_score_and_feature[metric] = metric_value

            # 分组
            feature_sums = {}
            feature_counts = {}
            if not each_sample_score_and_feature:
                continue
            for feature, percentage in zip(each_sample_score_and_feature["feature"],
                    each_sample_score_and_feature["avg_percentage"]):
                if feature not in feature_sums:
                    feature_sums[feature] = 0
                    feature_counts[feature] = 0
                feature_sums[feature] += percentage
                feature_counts[feature] += 1
            feature_averages = {feature: feature_sums[feature] / feature_counts[feature] for feature in feature_sums}

            model_group_score[model_name] = feature_averages

        # 创建子图
        fig, axes = plt.subplots(nrows=len(model_group_score), ncols=1, figsize=(20, 10 * len(models)))  # 调整图表宽度

        # 如果只有一个模型，axes不会是数组
        if len(model_group_score) == 1:
            axes = [axes]

        # 绘制每个模型的数据
        for ax, (model, values) in zip(axes, model_group_score.items()):
            categories = list(values.keys())
            # 仅展示category中前10个字其余用...代替
            categories = [category.split("-")[0][:10] + '...' + category.split("-")[1]
                          if len(category.split("-")[0]) > 10 else category for category in categories]
            scores = list(values.values())

            # 使用颜色映射
            colors = plt.cm.rainbow(np.linspace(0, 1, len(categories)))

            bars = ax.barh(categories, scores, color=colors)
            ax.set_title(f'{model} 数据', fontproperties=get_font())
            ax.set_xlabel('分数', fontproperties=get_font())
            ax.set_ylabel('类别', fontproperties=get_font())
            ax.set_xlim(0, 100)  # 设置x轴范围
            # 设置固定的刻度
            ax.set_yticks(range(len(categories)))
            # 使用 FixedLocator
            ax.yaxis.set_major_locator(ticker.FixedLocator(range(len(categories))))
            # 设置y轴标签的字体大小
            ax.set_yticklabels(categories, fontsize=10, fontproperties=get_font())

            # 在每个柱子上方添加数值标签
            for bar in bars:
                width = bar.get_width()
                ax.text(width, bar.get_y() + bar.get_height() / 2, f'{width:.2f}', va='center', ha='left', fontsize=8)

        # 调整布局
        plt.tight_layout()

        plt.savefig(f"show/show_group_by_feature_{scenario}.png")  # 保存图片

        # 显示图表
        plt.show()


def start():
    stat_map = load_data()
    show_all(stat_map)
    show_final(stat_map)
    show_group_by_feature(stat_map)


if __name__ == '__main__':
    start()
    """,
        "language": "python",
    },
    {
        "code": """
package main

//正常导入（import "go-project/utils/date"）用于需要使用包中的功能时。
//匿名导入（import _ "go-project/utils/date"）用于只需要执行包的初始化逻辑，而不需要直接使用包中的功能时。
import (
    ts "go-project/utils/typestruct"
)
import f "fmt"
import (
    "fmt"
    "go-project/utils/constant"
    error "go-project/utils/dataflow-error"
    "go-project/utils/date"
    _ "go-project/utils/date"
    demo "go-project/utils/func/manyfunc"
    "go-project/utils/myfor"
    "go-project/utils/string"
    stringutils "go-project/utils/string"
)

func TestMyFour() {
    myfor.TestFor()
    error.PatchServiceHandler(nil)
}

func TestConstant() (float64, float64, int) {
    numbers := constant.MyList
    for _, number := range numbers {
        fmt.Println(number)
    }

    var calculator []*demo.Calculator
    calculator = append(calculator, &demo.Calculator{Brand: "Casio"})
    calculator = append(calculator, &demo.Calculator{Brand: "Icasio"})
    calculator = append(calculator, &demo.Calculator{Brand: "Ifasio"})
    for _, calculator := range calculator {
        f.Println(calculator.Brand)
    }
    demo.FunctionName("ddd", "sss")
    fmt.Println(demo.FunctionName("first", "second"))
    fmt.Println(demo.Calculator{
        Brand: stringutils.GetAlpha("1234567890"),
    }.Add(1, 2))
    demo.Greet("Alice")
    employee := ts.Employee{
        Name:    "John",
        Age:     30,
        Address: ts.Address{City: "New York", Country: "USA"},
    }
    employee.Address.City = "New York"

    const (
        x = constant.Pi
        y = constant.E
        z = constant.Zero
    )

    return x, y, z
}

func PrintAddress(address ts.Address) {
    f.Println(address)
    demo.FunctionName("ddd", "sss")
    fmt.Printf("姓名：%s，年龄：%d", demo.FunctionName("first", "second"), demo.Calculator{
        Brand: stringutils.GetAlpha("1234567890"),
    }.Add(1, 2))
    for i := 0; i < 10; i++ {
        fmt.Println(i)
        fmt.Println(i)
    }
    demo.Greet("Alice")
}

func main() {
    TestConstant()
    s := "Hello, world. 12123123"
    f.Println(s)

    fmt.Println(date.GetDate(s))
    fmt.Println(date.DateFormat(s))
    fmt.Println(string.GetDigits(s))
    fmt.Println(stringutils.GetChars(s))
    fmt.Println(demo.FunctionName("ddd", "sss"))
    fmt.Println("1. 标准声明形式:")
    ts.TestStruct()
    employee := ts.Employee{
        Name:    "John",
        Age:     30,
        Address: ts.Address{City: "New York", Country: "USA"},
    }
    employee.Age = 35
    f.Println("Employee:", employee)

    var area = ts.Rectangle{Width: 5, Height: 10}
    ts.Dog{Animal: ts.Animal{}}.Bark()
    ts.Rectangle{Width: 5, Height: 10}.Area()
    fmt.Println("圆的面积：", constant.Pi*constant.Pi)

    area.Height = 10
    PrintAddress(ts.Address{})
    fmt.Println(area)
    fmt.Println(constant.Pi)
    fmt.Println(constant.Pi)

}

func PrintAddress2(address ts.Address) {
    f.Println(address)
    demo.FunctionName("ddd", "sss")
    fmt.Printf("姓名：%s，年龄：%d", demo.FunctionName("first", "second"), demo.Calculator{
        Brand: stringutils.GetAlpha("1234567890"),
    }.Add(1, 2))
    for i := 0; i < 10; i++ {
        fmt.Println(i)
        fmt.Println(i)
    }
    demo.Greet("Alice")
}

// ApplyOperation 函数用于对两个整数应用给定的数学操作，并返回结果和操作实例
//
// 参数：
//
//	numberA:      第一个整数
//	numberB:      第二个整数
//	operations:   要应用的数学操作实例
//
// 返回值：
//
//	operation_return: 执行操作后的结果
//	mathOperations:   数学操作实例
func ApplyOperation(numberA int, numberB int, operations demo.MathOperations) (operation_return int, mathOperations [][]**demo.MathOperations) {
    var p = constant.Person{
        Name: "John",
        Age:  30,
    }
    fmt.Println(p.Name)
    return operations.Sum(numberA, numberB), mathOperations
}

// 二分查找
func binarySearch(arr []int, target int) int {
    left, right := 0, len(arr)-1
    for left <= right {
        mid := (left + right) / 2
        if arr[mid] == target {
            return mid
        } else if arr[mid] < target {
            left = mid + 1
        } else {
            right = mid - 1
        }
    }
    return -1
}

// 堆排序
func heapSort(arr []int) {
    n := len(arr)
    for i := n/2 - 1; i >= 0; i-- {
        heapify(arr, n, i)
    }
    for i := n - 1; i > 0; i-- {
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)
    }
}

func heapify(arr []int, n, i int) {
    largest := i
    left := 2*i + 1
    right := 2*i + 2
    if left < n && arr[left] > arr[largest] {
        largest = left
    }
    if right < n && arr[right] > arr[largest] {
        largest = right
    }
}

// 快速排序
func quickSort(arr []int) {
    if len(arr) <= 1 {
        return
    }
    pivot := arr[0]
    var left, right []int
    for _, v := range arr[1:] {
        if v <= pivot {
            left = append(left, v)
        } else {
            right = append(right, v)
        }
    }
    quickSort(left)
    quickSort(right)
    copy(arr, append(append(left, pivot), right...))
}
        """,
        "language": "go"
    }
]

MOCK_IS_CURSOR_IN_PARENTHESES = [
    {
        "prefix": "def funca(data, ",
        "suffix": ")",
        "label": True
    },
    {
        "prefix": "def funca(data) ",
        "suffix": "\n",
        "label": False
    },
    {
        "prefix": "def funca(funcb(), ",
        "suffix": ")",
        "label": True
    },
    {
        "prefix": "return [i for i in range(10) if i % 2 == 0",
        "suffix": "]",
        "label": True
    },
    {
        "prefix": "return [i for i in range(",
        "suffix": ")]",
        "label": True
    },
]

MOCK_IS_CURSOR_IN_STRING = [
    {
        "prefix": "print('hello",
        "suffix": " world')",
        "label": True
    },
    {
        "prefix": "const s = 'Hello '",
        "suffix": "+ 'World';",
        "label": False
    },
    {
        "prefix": "const s = 'It\\'s a ",
        "suffix": "nice day';",
        "label": True
    },
    {
        "prefix": "const s = 'It\\'s a nice day';",
        "suffix": "",
        "label": False
    },
    {
        "prefix": "const s = 'Hello " + '"quotes',
        "suffix": '"' + "+ 'World';",
        "label": True
    },
]

MOCK_CUT_CSS_STYLE = [
    {
        "language": "vue",
        "content": """
            width: 100%;
            margin: 10px 0;
            background: linear-gradient(
                to right,  /*to结束的方向*/
                transparent 0%,
                transparent 50%,
                #ccc 50%,
                #ccc 100%
            );
            }
        """,
        "label": True
    },

    {
        "language": "vue",
        "content": """
            justify-content: space-between;
            align-items: center;
            padding-top: 20px;
            .send{
              width: 100%;
              height: 40px;
              background: #0078d4;
              border-radius: 4px;
              color: #fff;
              font-size: 16px;
              font-weight: 400;
              line-height: 40px;
              text-align: center;
              cursor: pointer;
            }
            .send:hover{
              background: #0067b8;
            }
            .send:active{
              background: #005c9e;
            }
            .send:disabled{
              background: #d9d9d9;
              cursor: not-allowed;
            }
            .send:disabled:hover{
              background: #d9d9d9;
            }
            .send:disabled:active{
        """,
        "label": True
    },
    # 非css样式
    {
        "language": "vue",
        "content": """
            model_handler_map = {
                "default": ModelHandlerStrategy(OpenAIModelHandler()),
                "DeepSeek-Coder-V2-Lite-Base": ModelHandlerStrategy(OpenAIModelHandler()),
                "codegeex4-all-9b": ModelHandlerStrategy(OpenAIModelHandler()),
            }
        """,
        "label": False
    },
    {
        "language": "vue",
        "content": """
            width: 100%;
            height: 40px;
            background: #0078d4;
            border-radius: 4px;
            color: #fff;
            font-size: 16px;
            font-weight: 400;
        """,
        "label": True
    },
    # 非css样式
    {
        "language": "java",
        "content": """
            sendactive = {
              background: "#005c9e",
            }
        """,
        "label": False
    },
    {
        "language": "vue",
        "content": """
            .send:active{
              background: #005c9e;
            }
        """,
        "label": True
    },
    {
        "language": "vue",
        "content": """background: #005c9e;""",
        "label": False
    },
    {
        "language": "vue",
        "content": """
            background: linear-gradient(
                to right,  /*to结束的方向*/
                transparent 0%,
                transparent 50%,
                #ccc 50%,
                #ccc 100%
            );
        """,
        "label": True
    },
    {
        "language": "html",
        "content": """
            const Button = styled.button`
              background: blue;
              color: white;
              font-size: 16px;
            `;
        """,
        "label": True
    },
    {
        "language": "vue",
        "content": """
            &:hover {
                color: rgb(255,255,255);
            }
        """,
        "label": True
    }

]

MOCK_IS_VALID_CONTEXT = [
    {
        "text": " ",
        "label": False
    },
    {
        "text": "     \n    \n      \t",
        "label": False
    },
    {
        "text": "\n\n",
        "label": False
    }, {
        "text": "",
        "label": False
    }, {
        "text": "1",
        "label": True
    }, {
        "text": " \\ ",
        "label": True
    }, {
        "text": "               \\\n",
        "label": True
    }, {
        "text": " \r",
        "label": False
    }, {
        "text": " \r\n",
        "label": False
    },
]

MOCK_CUT_PREFIX_OVERLAP = [
    # 与前缀完全重叠
    {
        "text": """
    for true {
        result := monitoringAgent(agentName)
        if result == false {
            break
        }
        monitor.MonitoringCd(agentName)
        time.Sleep(time.Second * 5)
    }
        """,
        "prefix": """
    xxx
    xxx
    xxx
    xxx
    for true {
        result := monitoringAgent(agentName)
        if result == false {
            break
        }
        monitor.MonitoringCd(agentName)
        time.Sleep(time.Second * 5)
    }
        """,
        "label": ""
    },
    # 与较前的前缀完全重叠
    {
        "text": """
    for true {
        result := monitoringAgent(agentName)
        if result == false {
            break
        }
        monitor.MonitoringCd(agentName)
        time.Sleep(time.Second * 5)
    }
        """,
        "prefix": """
    xxx
    xxx
    xxx
    xxx
    for true {
        result := monitoringAgent(agentName)
        if result == false {
            break
        }
        monitor.MonitoringCd(agentName)
        time.Sleep(time.Second * 5)
    }
    xxx
    xxx
        """,
        "label": ""
    },
    # 与前缀部分重叠
    {
        "text": """
    if text:
        return True
    else:
        return False
        """,
        "prefix": """
    if text:
        return False
    else:
        return False
        """,
        "label": ""
    },
    # 与前缀部分连续3行重叠
    {
        "text": """
    for true {
        result := monitoringAgent(agentName)
        if result == false {
            return
        }
        monitor2.MonitoringCd(agentName)
        time.Sleep(time.Second * 6)
    }
        """,
        "prefix": """
    xxx
    xxx
    xxx
    xxx
    for true {
        result := monitoringAgent(agentName)
        if result == false {
            break
        }
        monitor.MonitoringCd(agentName)
        time.Sleep(time.Second * 5)
    }
    """,
        "label": ""
    },
    # 与前缀部分连续2行重叠
    {
        "text": """
    for true {
        result := monitoringAgent(agentName)
        if result == true {
            return
        }
        monitor2.MonitoringCd(agentName)
        time.Sleep(time.Second * 6)
    }
        """,
        "prefix": """
    xxx
    xxx
    xxx
    xxx
    for true {
        result := monitoringAgent(agentName)
        if result == false {
            break
        }
        monitor.MonitoringCd(agentName)
        time.Sleep(time.Second * 5)
    }
        """,
        "label": """
    for true {
        result := monitoringAgent(agentName)
        if result == true {
            return
        }
        monitor2.MonitoringCd(agentName)
        time.Sleep(time.Second * 6)
    }
        """,
    },
]


MOCK_LONGEST_COMMON_SUBSTRING = [
    {
        "str1": "abc",
        "str2": "abc",
        "label": "abc"
    },
    {
        "str1": "abcdadsdssszz",
        "str2": "adsds",
        "label": "adsds"
    },
    {
        "str1": "zxw",
        "str2": "abn",
        "label": ""
    },
    {
        "str1": "abc",
        "str2": "acc",
        "label": "a"
    }
]

MOCK_IS_EXTREME_REPETITION = [
    {
        "code": """
            def func():
                print("Hello, world!")
                print("Hello, world!2")
                print("Hello, world!3")
                print("Hello, world!4")
                print("Hello, world!5")
                print("Hello, world!6")
                print("Hello, world!7")
                print("Hello, world!8")
                print("Hello, world!9")
            """,
        "label": True
    },
    {
        "code": """
            def func():
                print("
                print("Hello, world!2")
                print("Hello, world!3")
                print("Hello, world!4")
                print(
                print("Hello, world!6")
                print("Hello, world!7")
                print("Hello, world!8")
                print("Hello, world!9")
                print("Hello, world!10")
            """,
        "label": True
    },
    {
        "code": """
            for i in range(10):
                if i % 2 == 0:
                    print(i)
                else:
                    print(i)
            for i in range(10):
                if i % 2 == 0:
                    print(i)
                else:
                    print(i)
        """,
        "label": False
    },
    {
        "code": """
            for i in range(10):
                if i % 2 == 0:
                    print(i)
                else:
                    print(i)
            # 1. 恢复管理员密码
            # 2. 恢复管理员密码
            # 3. 恢复管理员密码
            # 4. 恢复管理员密码
            # 5. 恢复管理员密码
            # 6. 恢复管理员密码
            # 7. 恢复管理员密码
            # 8. 恢复管理员密码
        """,
        "label": True
    },
    {
        "code": """
            def heapify(arr, n, i):
                largest = i
                left = 2 * i + 1
                right = 2 * i + 2
                if left < n and arr[left] > arr[largest]:
                    largest = left
                if right < n and arr[right] > arr[largest]:
                    largest = right
                if largest != i:
                    arr[i], arr[largest] = arr[largest], arr[i]
                    heapify(arr, n, largest)
        """,
        "label": False
    }
]
