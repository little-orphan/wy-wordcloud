import jieba
from os import path
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 创建停用词列表
def stopwordslist():
    stopwords = [line.strip() for line in open('chinsesstoptxt.txt',encoding='utf8').readlines()]
    return stopwords

# 对句子进行中文分词
def seg_depart(sentence):
    # 对文档中的每一行进行中文分词
    print("正在分词")
    sentence_depart = jieba.cut(sentence.strip())
    # 创建一个停用词列表
    stopwords = stopwordslist()
    # 输出结果为outstr
    outstr = ''
    # 去停用词
    for word in sentence_depart:
        if word not in stopwords:
            if word != '\t':
                outstr += word
                outstr += " "
    return outstr

# 给出文档路径
filename = "1.txt"
outfilename = "out.txt"
inputs = open(filename, 'r', encoding='utf8')
outputs = open(outfilename, 'w', encoding='utf8')

# 将输出结果写入ou.txt中
for line in inputs:
    line_seg = seg_depart(line)
    outputs.write(line_seg + '\n')
    print("-------------------正在分词和去停用词-----------")
outputs.close()
inputs.close()
print("删除停用词和分词成功！！！")

d=path.dirname(__file__)
text=open(path.join(d, outfilename), encoding='utf8').read()

# 步骤3-2：设置一张词云图对象
wordcloud = WordCloud(font_path="./simsun.ttf", background_color="white", width=800,
                      height=600, max_font_size=50, max_words=1000).generate(text)

# 步骤4-1：创建一个图表画布
plt.figure()
# 步骤4-2：设置图片
plt.imshow(wordcloud, interpolation="bilinear")
# 步骤4-3：取消图表x、y轴
plt.axis("off")
# 显示图片
plt.show()
