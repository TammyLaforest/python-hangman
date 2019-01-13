from PIL import Image
import random

def get_image():
	cat1 = ('static','media/cat1.jpg')
	cat2 = ('static','media/cat2.jpg')
	images = [cat1, cat2]
	return random.choice(images)


