import matplotlib.pyplot as plt 
from matplotlib.font_manager import FontProperties

y = [12312312,4123124,4123421,4213212,64541221,3124643,6878655,123534534]
x = [1,2,3,4,5,6,7,8]

font = FontProperties(fname=r"./FZHTJW.TTF", size=14)

plt.title('聊天条数/月',fontproperties=font)
plt.xlabel('月份',fontproperties=font)
plt.ylabel('万条',fontproperties=font)
plt.plot(x,y)
plt.show()