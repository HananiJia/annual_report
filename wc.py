import json
import jieba
from wordcloud import WordCloud

with open('report.json','r') as f:
    report = json.load(f)
    msg = report['receive']['all_msg']
    msg += report['send']['all_msg']
    seg_list = jieba.lcut(msg, cut_all=False)
    results = ' '.join(seg_list)
    wc = WordCloud(
        font_path='FZHTJW.TTF',
        background_color='white',
        width=500,
        height=350,
        max_font_size=50,
        min_font_size=10,
        )
    wc.generate(results)
    wc.to_file('wc.png')
    