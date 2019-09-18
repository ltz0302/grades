# -*- coding: UTF-8 -*-
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter, PDFPageAggregator
from pdfminer.layout import LAParams
from pdfminer.pdfdevice import PDFDevice
from pdfminer.pdfparser import PDFParser, PDFDocument
import matplotlib.pyplot as plt 

#读取文档
fp=open("Grades_StudIP.pdf","rb")

#创建一个与文档相关联的解释器
parser=PDFParser(fp)
#PDF文档对象
doc=PDFDocument(parser)
#链接解释器和文档对象
parser.set_document(doc)
doc.set_parser(parser)
#初始化文档
doc.initialize("")
#创建PDF资源管理器
resource=PDFResourceManager()
#参数分析器
laparam=LAParams()
#创建一个聚合器
device=PDFPageAggregator(resource,laparams=laparam)
#创建PDF页面解释器
interpreter=PDFPageInterpreter(resource,device)

#新建一个文档来写入数据
grades=open('grades.txt','w')
for page in doc.get_pages():
	#使用页面解释器来读取
	interpreter.process_page(page)
	#使用聚合器来获得内容
	layout=device.get_result()
	for out in layout:
		if hasattr(out, 'get_text'):  # 需要注意的是在PDF文档中不只有 text 还可能有图片等等，为了确保不出错先判断对象是否具有 get_text()方法 
			grades.write(out.get_text())		
grades.close()	
fp.close()


fp=open('grades.txt','r')
#将所有文本读入列表
grades=fp.read().splitlines() 
grades_list=[]
#需要统计的字符串，此处为成绩
Note=['1','1.3','1.7','2','2.3','2.7','3','3.3','3.7','4','5']
#将要统计的字符串加入列表
for i in grades:
	if i in Note:
		grades_list.append(i)		
fp.close()

ax = plt.subplot()
xlabel_grades_list=Note
ylabel_number_list=[]
#计算纵坐标的值
for i in xlabel_grades_list:
	ylabel_number_list.append(grades_list.count(i))
plt.title('The total number of students is '+str(len(grades_list)))
#设置X轴Y轴名称  
plt.xlabel("grades")  
plt.ylabel("number") 
#绘制柱状图
rectangles = ax.bar(range(len(xlabel_grades_list)),ylabel_number_list, width=1, color='blue', edgecolor='white', linewidth=5)
ax.set_xticks(range(len(xlabel_grades_list)))  # 设置x轴坐标数量
ax.set_xticklabels(xlabel_grades_list)  # 设置X轴坐标名称
for r in rectangles:
	ax.text(r.get_x()+r.get_width()/2,r.get_height(),'%d'%r.get_height(),ha='center')  # 添加文本标注
ax.set_ylim(0, 100) #设置纵轴范围
plt.show()

