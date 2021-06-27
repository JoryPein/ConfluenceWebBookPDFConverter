from PyPDF2 import  PdfFileReader, PdfFileWriter
import os

def resort_files(files, root):
    dir_ = []
    fil_ = []
    for item in files:
        x = os.path.join(root,item)
        if os.path.isdir(x):
            dir_.append(item)
        else:
            fil_.append(item)
    new_list = []
    for item in fil_:
        new_list.append(item)
        k = item.strip('.pdf')
        if k in dir_:
            dir_.pop(dir_.index(k))
            new_list.append(k)
    new_list.extend(dir_)
    return new_list

def read_list(root='./pdf/'):
    files = os.listdir(root)
    files = resort_files(files, root)
    for item in files:
        fullpath = os.path.join(root, item)
        if os.path.isdir(fullpath):
            for item in read_list(root=fullpath):
                yield item
        else:
            yield fullpath

d = dict()
def get_parent(filename):
    parent_key = os.path.dirname(filename)
    if parent_key == './pdf':
        result = None
    else:
        result = d[parent_key.strip('.')]
    return result

def set_bookmark_node(filename, bookmark):
    key = filename.strip('.pdf')
    d[key] = bookmark

file_writer = PdfFileWriter()
offset = 0

for filename in read_list():
    file_reader = PdfFileReader(filename)
    title = filename.split('\\')[-1].strip('.pdf').split(".")[-1]

    for page in range(file_reader.getNumPages()):
        file_writer.addPage(file_reader.getPage(page))

    boomark = file_writer.addBookmark(title, offset, parent=get_parent(filename))
    set_bookmark_node(filename, boomark)

    offset += file_reader.getNumPages()

with open("book.pdf",'wb') as fp:
    file_writer.write(fp)           
