pip install easydict -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip install keras==2.0.8 tensorflow==1.4 tensorflow-gpu==1.4 -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip install Cython opencv-python -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip install matplotlib -i https://pypi.tuna.tsinghua.edu.cn/simple/
conda install pytorch torchvision -c pytorch
cd ./ctpn/lib
python setup.py build ##最好使用sudo运行

