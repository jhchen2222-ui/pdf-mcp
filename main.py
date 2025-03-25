from mcp.server.fastmcp import FastMCP
import PyPDF2
import fitz,os
from PIL import Image as pilImage
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Image, PageBreak

# 创建一个 MCP 服务端实例，命名为 "SimpleServer"
mcp = FastMCP("SimpleServer")

# 定义一个资源：返回一个简单的问候语
@mcp.resource("greeting://hello")
def get_greeting() -> str:
    """Return a static greeting message."""
    return "hello 这个一个pdf工具!"

# 定义一个工具：拆分PDF
@mcp.tool()
def split_pdf(pdf_file_path: str, target_pages: list, save_path: str) -> str:
    """拆分pdf.
    
    Args:
        pdf_file_path: 文件位置
        target_pages: 所包含的页面序号，从 1 开始算起
        save_path: 最后的保存路径
    Returns:
        str: 包含搜索结果的格式化字符串
    """
    if not target_pages or not save_path or not pdf_file_path:
        raise Exception('请输入正确的参数')
    pdf_reader = PyPDF2.PdfReader(pdf_file_path)
    maxpage = max(target_pages)
    # 新建一个空白 PDF
    pdf_writer = PyPDF2.PdfWriter()
    num_pages = len(pdf_reader.pages)
    for page_num in range(num_pages):
        page_num += 1
        if page_num > maxpage:
            # 循环过程中，如果某页面的序号大于所需页面的最大序号则跳出循环
            break
        if page_num in target_pages:
            # 由于上面的 page_num 已经增加 1，所以这里增加页面时要减去 1
            page = pdf_reader.pages[page_num-1]
            pdf_writer.add_page(page)
    # 开始写入 PDF
    with open(save_path, 'wb') as out_file:
        pdf_writer.write(out_file)
    return '拆分成功'

# 定义一个工具：合并PDF
@mcp.tool()
def merge_pdf(pdf_files_path: list, save_path: str) -> str:
    '''合并pdf.
    
    Args:
        pdf_files_path: 文件位置
        save_path: 最后的保存路径
    Returns:
        str: 包含搜索结果的格式化字符串
    '''
    pdf_writer = PyPDF2.PdfWriter()

    # 遍历所有 PDF 文件
    for pdf_file in pdf_files_path:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)
        # 将每一页添加到写入器
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num-1]
            pdf_writer.add_page(page)

    # 写入合并后的 PDF 文件
    with open(save_path, 'wb') as out_file:
        pdf_writer.write(out_file)
    return '合并成功'

# 定义一个工具：PDF转图片
@mcp.tool()
def pdf_to_picture(pdf_file_path: str, picture_path: str, save_prefix: str) -> str:
    '''PDF转图片.
    
    Args:
        pdf_file_path: 文件位置
        picture_path: 图片保存位置
        save_prefix: 保存文件前缀
    Returns:
        str: 包含搜索结果的格式化字符串
    '''
    # 打开PDF文件
    pdf_file = fitz.open(pdf_file_path)

    # 新建一个文件用于保存另存后的图片，前提是该文件夹不存在
    if not os.path.exists(picture_path): os.mkdir(picture_path)

    ## 使用 fitz 库将 pdf 页面转存为图片
    for pagenum in range(pdf_file.page_count):
        # 获取一个页面
        pdfpage = pdf_file[pagenum]
        # 定义缩放系数，这个操作将使得到的图片质量相对较高，这里相当于是保存放大四倍后的图像
        zoom_x, zoom_y = 4,4
        mat = fitz.Matrix(zoom_x, zoom_y).prerotate(0)
        # 获取图片矩阵对象
        pix = pdfpage.get_pixmap(matrix=mat, alpha=False)
        # 将图片对象写入本地图片
        PNG_path = f'{picture_path}/{save_prefix}_{pagenum+1}.png'
        pix.save(PNG_path)
    return '转换成功'

 
 
# 定义一个工具：获取目标文件下jpg和png图片文件
@mcp.tool()
def get_images(picture_path: str) -> list:
    '''图片转PDF.
    
    Args:
        picture_path: 图片位置
    Returns:
        list: 图片名称列表
    '''
    images = []
    file_lis = os.listdir(picture_path)
    for image_path in file_lis:
        if image_path.endswith(('jpg', 'png')):
            images.append(image_path)
    return images
 
 
# 定义一个工具：图片转PDF
@mcp.tool()
def images_to_pdf(pictures: list, picture_path: str, save_path: str) -> str:
    '''图片转PDF.
    
    Args:
        pictures: 有那些文件
        picture_path: 图片位置
        save_path: 保存文件位置
    Returns:
        str: 包含搜索结果的格式化字符串
    '''
    os.chdir(picture_path)
 
    # 获取A4尺寸
    a4_w, a4_h = landscape(A4)
 
    # 创建一个PDF文档
    pdf_doc = SimpleDocTemplate(save_path)
 
    if len(pictures) == 0:
        print('该文件夹路径下无图片，请检查图片格式！')
    elif len(pictures) == 1:
        # 获取图片尺寸
        img = pilImage.open(pictures[0])
        img_w, img_h = img.size
        # 设置合适的缩放比率
        ratio = min(a4_w / img_w, a4_h / img_h)
        # 创建文档
        page = Image(pictures[0], img_w * ratio, img_h * ratio)
        pdf_doc.build([page])
        # print(images[0] + '——转换完成')
    else:
        frames = []  # 用于存储多张图片框架
        con = 0
        for image in pictures:
            # 获取图片尺寸
            img = pilImage.open(image)
            img_w, img_h = img.size
            # 设置合适的缩放比率
            ratio = min(a4_w / img_w, a4_h / img_h)
            # 储存文档内容
            page = Image(image, img_w * ratio, img_h * ratio)
            frames.append(page)  # 将文档内容添加到列表中
            frames.append(PageBreak())  # 在每张图片后添加PageBreak
            con += 1
            # print(image + '——第%d张' % con)
 
        pdf_doc.build(frames)
        # print('转换完成，共计%d张' % len(images))
    return '转换成功'

# 运行服务端
if __name__ == "__main__":
    mcp.run()
