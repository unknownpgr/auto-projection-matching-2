# Auto-projection-matching 2
 
[저번 프로젝트](https://github.com/unknownpgr/auto-projection-matching)에서는 어떤 관측 각도에서도 사용가능한 3차원 정보의 2차원 표현방법을 연구하여 구현하였다. 그런데 저번 프로젝트의 구현에서는 관찰자가 화면을 인식하므로, 화면이 표출되는 동안에는 캘리브레이션이 불가능하여 카메라의 위치가 고정되어있는 경우에만 사용가능하였다. 그러나 실제로 영상을 시청하거나 게임을 할 때에는 관찰자가 화면에 대해 상대적으로 움직이는 경우가 잦다. 따라서 이 방법은 현실에 적용이 어렵다.

이번 프로젝트에서는 이러한 단점을 극복하고자, 반대로 화면에 카메라를 달아 관찰자의 위치를 인식하는 방법을 통해 켈리브레이션을 수행하도록 한다. 먼저 관찰자는 특수한 마커를 부착하고, 이 마커의 위치를 화면에 달린 카메라가 추적, 화면 중심을 기준으로 관찰자의 위치를 추정한다. 이를 바탕으로 관찰자의 시점에서 볼 때 똑바로 보이는 화면을 계산하여 재생한다.

## Demo Video
<center>
  <a href="https://youtu.be/77tAkzMEDdw">
    <img src="https://i9.ytimg.com/vi_webp/77tAkzMEDdw/mqdefault.webp?time=1621596600000&sqp=CLiznoUG&rs=AOn4CLAAa6I0g9t4jDn3_D0eaovxC-pXZw">
  </a>
</center>
