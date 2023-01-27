import streamlit as st
import streamlit.components.v1 as components
from content import *

st.set_page_config(layout="wide", page_title="Low Light Image Enhancement")

components.html(f'<h1 style="text-align:center; font-size: 27px; font-weight: bold"> {title} </h1>', height=60)

for i, col in enumerate(st.columns(4)):
    col.image(f'pictures/output/output_{i+1}.gif')

components.html(f"""
<span style="font-size: 25px; font-weight: bold" >Abstract</span>
<div style="text-align: justify">
    <p> {abstract} </p>
    <p> {keywords} </p>
</div>

<br/>
<span style="font-size: 25px; font-weight: bold" >Network Architecture</span>
<div style="text-align: justify">
    <p> {network_architecture} </p>
    <img src="https://github.com/LobbeyTan/FYP_LLIE_APP/blob/main/pictures/res/network_architecture.png?raw=true" 
    alt="Generative Network Architecture" style="width: 100%">
</div>

<br/>
<br/>
<span style="font-size: 25px; font-weight: bold" >Low-light Image Enhancement Results</span>
<div style="text-align: justify">
    <p> {enhanced_result_desc} </p>
    <img src="https://github.com/LobbeyTan/FYP_LLIE_APP/blob/main/pictures/res/enhancement_result.png?raw=true" 
    alt="Low-Light Enhanced Results" style="width: 100%">
</div>

<br/>
<br/>
<span style="font-size: 25px; font-weight: bold" >Low-light Object Detection Results (After Enhanced)</span>
<div style="text-align: justify">
    <p> {detection_result_desc} </p>
    <img src="https://github.com/LobbeyTan/FYP_LLIE_APP/blob/main/pictures/res/detection_result.png?raw=true" 
    alt="Low-Light Enhanced Results" style="width: 100%">
</div>

<br/>
<br/>
<span style="font-size: 25px; font-weight: bold; margin-bottom: 25px;" >Viva Presentation Slide</span>
<iframe src={powerpoint_embed_link} width="100%" height="600px" frameborder="0">This is an embedded <a target="_blank" href="https://office.com">Microsoft Office</a> presentation, powered by <a target="_blank" href="https://office.com/webapps">Office</a>.</iframe>

<br/>
<br/>
<span style="font-size: 25px; font-weight: bold;" >References</span>
<div style="text-align: justify">
    <p> [1] Fu, X., Zeng, D., Huang, Y., Zhang, X.-P., &amp; Ding, X. (2016). A weighted variational model for simultaneous reflectance and illumination estimation. 2016 IEEE Conference on Computer Vision and Pattern Recognition (CVPR). https://doi.org/10.1109/cvpr.2016.304  </p>
    <p> [2] Guo, C., Li, C., Guo, J., Loy, C. C., Hou, J., Kwong, S., &amp; Cong, R. (2020). Zero-reference deep curve estimation for low-light image enhancement. 2020 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR). https://doi.org/10.1109/cvpr42600.2020.00185 </p>
    <p> [3] Guo, X., Li, Y., &amp; Ling, H. (2017). Lime: Low-light image enhancement via Illumination Map Estimation. IEEE Transactions on Image Processing, 26(2), 982–993. https://doi.org/10.1109/tip.2016.2639450 </p>
    <p> [4] Jiang, Y., Gong, X., Liu, D., Cheng, Y., Fang, C., Shen, X., Yang, J., Zhou, P., &amp; Wang, Z. (2021). Enlightengan: Deep light enhancement without paired supervision. IEEE Transactions on Image Processing, 30, 2340–2349. https://doi.org/10.1109/tip.2021.3051462 </p>
    <p> [5] Loh, Y. P., &amp; Chan, C. S. (2019). Getting to know low-light images with the exclusively Dark Dataset. Computer Vision and Image Understanding, 178, 30–42. https://doi.org/10.1016/j.cviu.2018.10.010 </p>
    <p> [6] Wei, C., Wang, W., Yang, W., &amp; Liu, J. (2018, August 14). Deep RETINEX decomposition for low-light enhancement. arXiv.org. Retrieved from https://arxiv.org/abs/1808.04560 </p>
    <p> [7] Zhang, Y., Zhang, J., &amp; Guo, X. (2019). Kindling the darkness. Proceedings of the 27th ACM International Conference on Multimedia. https://doi.org/10.1145/3343031.3350926 </p>
</div>
""", height=3700)
