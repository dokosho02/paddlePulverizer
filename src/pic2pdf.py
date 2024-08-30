from PIL import Image
import os

class image_to_pdf:
    def __init__(self,filepath):
        self.validFormats = (
            '.jpg',
            '.jpeg',
            '.png',
            '.JPG',
            '.PNG'
        )
        self.pictures = []

        folder = os.path.join(filepath.replace(".pdf", ""), "original")
        self.files = os.listdir( folder )
        for i in range( len(self.files) ):
            self.files[i] = os.path.join( folder, self.files[i] )

        self.mergedFilePath = filepath.replace(".pdf", "_box.pdf")
        self.convertPictures()
        print("Converted to PDF has been done.")

    
    def filter(self, item):
        return item.endswith(self.validFormats)


    def sortFiles(self):
        return sorted(self.files)

    
    def getPictures(self):
        pictures = list(filter(self.filter, self.sortFiles()))
        if self.isEmpty(pictures):
        	print("There are no pictrues in the directory !")
        	raise Exception("There are no pictrues in the directory !")
        print('Convert pictures are :')
        [ print(i) for i in pictures ]
        return pictures

    def isEmpty(self, items):
    	return True if len(items) == 0 else False


    def convertPictures(self):
        for picture in self.getPictures():
            self.pictures.append(Image.open(picture).convert('RGB'))
        self.save()




    def save(self):
        self.pictures[0].save(self.mergedFilePath, 
        save_all=True, append_images=self.pictures[1:])
    

# if __name__ == "__main__":
    # image_to_pdf()