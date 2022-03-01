# Auto Projection Matching 2
 
 Auto projection matching refers to a method that can give the illusion of seeing a 3D object even when viewing an image through a 2D monitor screen.
 
In a [previous project](https://github.com/unknownpgr/auto-projection-matching), we studied a projection method that can be used when viewing the screen from any arbitrary angle.
However, since the method studied in the last project requires a calibration process, correct projection cannot be obtained when the observer moves.
In general, when watching a video or playing a game, the observer moves frequently. Therefore, this method is difficult to apply in reality.
 
In this project, calibration is performed by attaching a camera to the screen and recognizing the observer's position.
A marker is attached to the observer, and the position of the marker is tracked by a camera attached to the screen, and the position of the observer is estimated.
Based on this estimate, the projection from the observer's point of view is calculated.

## Demo Video
<center>
  <a href="https://youtu.be/77tAkzMEDdw">
    <img src="https://i9.ytimg.com/vi_webp/77tAkzMEDdw/mqdefault.webp?time=1621596600000&sqp=CLiznoUG&rs=AOn4CLAAa6I0g9t4jDn3_D0eaovxC-pXZw">
  </a>
</center>
