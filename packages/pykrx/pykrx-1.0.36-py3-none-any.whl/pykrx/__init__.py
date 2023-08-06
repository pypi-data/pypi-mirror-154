import platform
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


os = platform.system()

if os == "Darwin":
    family = "AppleGothic"
    install_url = "https://www.download-free-fonts.com/details/89379/" \
                  "applegothic-regular"

else:
    path = "./NanumBarunGothic.ttf"
    fe = fm.FontEntry(
        fname="NanumBarunGothic.ttf",
        name='NanumBarunGothic'
    )
    fm.fontManager.ttflist.insert(0, fe)
    plt.rc('font', family=fe.name)

plt.rcParams['axes.unicode_minus'] = False
