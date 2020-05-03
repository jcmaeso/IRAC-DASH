document.addEventListener("DOMContentLoaded", function () {
  init();
});
  
let layout1 = {
  title: {
    text:'Bitrate',
    font: {
      family: 'Courier New, monospace',
      size: 24
    },
    xref: 'paper',
    x: 0.05,
  },
  xaxis: {
    title: {
      text: 'ticks',
      font: {
        family: 'Courier New, monospace',
        size: 18,
        color: '#7f7f7f'
      }
    },
  },
  hovermode: false,
  yaxis: {
    title: {
      text: 'Kbps',
      font: {
        family: 'Courier New, monospace',
        size: 18,
        color: '#7f7f7f'
      }
    }
  }
}

let layout2 = {
  title: {
    text:'Video Buffer',
    font: {
      family: 'Courier New, monospace',
      size: 24
    },
    xref: 'paper',
    x: 0.05,
  },
  xaxis: {
    title: {
      text: 'ticks',
      font: {
        family: 'Courier New, monospace',
        size: 18,
        color: '#7f7f7f'
      }
    },
  },
  hovermode: false,
  yaxis: {
    title: {
      text: 'Buffer (s)',
      font: {
        family: 'Courier New, monospace',
        size: 18,
        color: '#7f7f7f'
      }
    }
  }
}

function init()
{
  //var video,player,mpd_url = "./output_enc/stream.mpd";
  var video,player,mpd_url = document.getElementById('player').getAttribute('src');
  video = document.querySelector("video");
  player = dashjs.MediaPlayer().create();
  

  Plotly.plot('chartBR',[{
      y:[0],
      type:'line',
  }],layout1);

  Plotly.plot('chartBF',[{
    y:[0],
    type:'line',
  }],layout2);

  //Get js
    console.log("1");
    player.initialize(video, mpd_url, true);
    player.setProtectionData({"org.w3.clearkey": { "serverURL" : '/drm'} });
    console.log("2")
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
          if (!video.paused){
            updatePlots(bitrate,bufferLevel)
          }
          document.getElementById('buffer').innerText = bufferLevel + " secs";document.getElementById('bitrate').innerText = bitrate + " Kbps";document.getElementById('representation').innerText = repSwitch.to;
        }
      }, 500);
  
      document.querySelector("video").volume = 0.1;
  }

  let cnt = 0;

  let updatePlots = (bitrate,bufferLevel) => {
    Plotly.extendTraces('chartBR', { y: [[bitrate]] }, [0]);
    Plotly.extendTraces('chartBF', { y: [[bufferLevel]] }, [0]);
    cnt++;
    if(cnt > 10) {
      Plotly.relayout('chartBR',{
           xaxis: {
                     range: [cnt-10,cnt]
                  }
      });
      Plotly.relayout('chartBF',{
        xaxis: {
                  range: [cnt-10,cnt]
               }
   });
   }
  }

  let drmPetition = (id) => {
    const fetchPromise = fetch("http://70.37.52.23:8080/drm?id="+'encoded');
    return fetchPromise.then(response => {
      return response.json();
    });
  }
