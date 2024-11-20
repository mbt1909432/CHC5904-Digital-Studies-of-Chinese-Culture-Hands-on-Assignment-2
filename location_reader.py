import csv
import os
import re

import matplotlib.pyplot as plt
from matplotlib import font_manager

# set font
font_path = "C:/Windows/Fonts/simhei.ttf"
font_prop = font_manager.FontProperties(fname=font_path)

# set font
plt.rcParams['font.family'] = font_prop.get_name()


class LocationAnalysis:
    def __init__(self, chapters):
        self.chapters = chapters
        self.places = ["南京", "蘇州", "杭州", "北京", "揚州", "濟南", "湖州"]
        self.characters=["匡超人","馬二先生","馬靜","三公子","娄三公子",'楊執中',
                         '執中','景蘭江','蘭江','潘三','三哥','魯編修','編修公','編修','魯老先生','蓮公孫',
                         '陳和甫','魯老先生','鄭老爹','潘保正','浦墨卿','墨卿','支劍峰','宦成','衛先生','衛体善',
                         '魯小姐','王老六','權先生','權老爺','洪憨仙','匡太公','施美卿','鄔老爹']
        self.places_plus_characters=self.places+self.characters
        self.place_frequency = {place: [0] * len(self.chapters) for place in self.places_plus_characters}
        #初始化 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def analyze_frequencies(self):
        for i, chapter in enumerate(self.chapters):
            print(fr"-------------{i+1}----------------------------")
            print(chapter)
            for place in self.places_plus_characters:
                self.place_frequency[place][i] = chapter.count(place)

    def display_results(self):
        for place, frequency in self.place_frequency.items():
            print(f"{place}: {frequency}")



    def export_to_csv(self, filename='place_frequency.csv'):
        """
        导出为CSV文件。
        """
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Place'] + [f'Chapter {i + 1}' for i in range(len(self.chapters))]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for place, frequency in self.place_frequency.items():
                row = {'Place': place}
                row.update({f'Chapter {i + 1}': freq for i, freq in enumerate(frequency)})
                writer.writerow(row)

def natural_sort_key(s):
    # 使用正则表达式将字符串中的数字部分转换为整数，这样可以进行自然排序
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def get_txt_filenames(directory):#没有排序。。。。
    txt_filenames = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                txt_filenames.append(os.path.join(root, file))
    txt_filenames.sort(key=lambda f: natural_sort_key(os.path.basename(f)))
    return txt_filenames

def chapter_reader()->list:
    txt_filenames=get_txt_filenames("raw_data")
    chapter_data=list()

    for filename in txt_filenames:
        with open(rf'{filename}','r',encoding='utf-8') as file:
            chapter_data.append(file.read())

    return chapter_data

def calculate_totals(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # 获取表头

        # 在表头末尾添加“Total”
        header.append('Total')

        rows_with_totals = []
        for row in reader:
            # 将非数值列（如地点名称）跳过，仅对数字部分求和
            place_name = row[0]
            counts = list(map(int, row[1:]))
            total_count = sum(counts)
            row_with_total = row + [total_count]
            rows_with_totals.append(row_with_total)

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)  # 写入修改后的表头
        writer.writerows(rows_with_totals)  # 写入有总计数的行



def read_totals_from_csv(filename):
    totals = {}

    with open(filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            place = row['Place']
            total = int(row['Total'])
            totals[place] = total

    return totals


def plot_totals_bar_chart(totals):
    places = list(totals.keys())
    counts = list(totals.values())

    plt.figure(figsize=(10, 6))  # 设置图形大小
    plt.bar(places, counts, color='skyblue')

    plt.xlabel('Place/Character')
    plt.ylabel('Total Count')
    plt.title('Total Occurrences of Places and Characters')
    plt.xticks(rotation=45, ha='right')  # 旋转x轴标签以提高可读性
    plt.tight_layout()  # 自动调整布局以防止标签重叠

    plt.show()




input_csv = 'place_frequency.csv'
output_csv = 'place_frequency_with_totals.csv'

chapters_data =chapter_reader()
analysis = LocationAnalysis(chapters_data)
analysis.analyze_frequencies()
analysis.display_results()

analysis.export_to_csv(input_csv)
calculate_totals(input_csv, output_csv)

totals = read_totals_from_csv(output_csv)



place_total=dict()
character_total=dict()
for data in analysis.places:
    place_total[data]=totals[data]

for data in analysis.characters:
    character_total[data]=totals[data]


plot_totals_bar_chart(place_total)
plot_totals_bar_chart(character_total)


