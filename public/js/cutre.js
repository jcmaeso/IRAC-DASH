const protData = {"org.w3.clearkey": {"clearkeys": {"oW5AK5BW43HzbTSKpiu3S": "hyN9IKGfWKdAwFaE5pm0qg"}}};
document.addEventListener("DOMContentLoaded", function () {
  init();
});
  
function init()
{
  //var video,player,mpd_url = "./output_enc/stream.mpd";
  var video,player,mpd_url = "./data/{{items[0]}}/stream.mpd";
  video = document.querySelector("video");
  player = dashjs.MediaPlayer().create();
  player.initialize(video, mpd_url, true);
 // player.setProtectionData(protData);
  player.on(dashjs.MediaPlayer.events["PLAYBACK_ENDED"], function() {
    clearInterval(eventPoller);});
  var eventPoller = setInterval(
    function() {
      var streamInfo = player.getActiveStream().getStreamInfo();
      var dashMetrics = player.getDashMetrics();
      var dashAdapter = player.getDashAdapter();
      if (dashMetrics && streamInfo) 
      {
        const periodIdx = streamInfo.index;
        var repSwitch = dashMetrics.getCurrentRepresentationSwitch('video', true);
        var bufferLevel = dashMetrics.getCurrentBufferLevel('video', true);
        var bitrate = repSwitch ? Math.round(dashAdapter.getBandwidthForRepresentation(repSwitch.to,periodIdx) / 1000) : NaN;
        document.getElementById('buffer').innerText = bufferLevel + " secs";document.getElementById('bitrate').innerText = bitrate + " Kbps";document.getElementById('representation').innerText = repSwitch.to;
      }
    }, 500);

    document.querySelector("video").volume = 0.1;
  }
