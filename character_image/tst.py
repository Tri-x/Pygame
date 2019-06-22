from PIL import Image
txt,emperor='',Image.open('nmsl_small.png')
def get_character(R,G,B):
	return list('NM$L')[int((0.3*R+0.6*G+0.1*B)/(256/len(list('NM$L'))))]
for y_pixel in range(0,200):
	for x_pixel in range(0,168):
		txt+=get_character(*emperor.getpixel((x_pixel,y_pixel)))
	txt+='\n'
with open('emperor_txt.txt','w')as file:
	file.write(txt)