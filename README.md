## Live Cam Object Identifier

Version: **0.0.1**

Receives a live camera URL input and return a screen with the live broadcast image and overlay it with identification for some objects

<p>
  <a href="#">
    <img 
      alt="identified_cars" 
      src="https://raw.githubusercontent.com/natanaelfneto/live_cam_object_identifier/master/assets/identified_cars.png" 
      width="240"/>
  </a>
</p>

#### Dependencies:

Actual version:
```JSON
{
    "imutils": "0.5.1",
    "numpy": "1.15.4",
    "opencv-python": "3.4.3.18",
    "pypiwin32": "223",
    "pywin32": "224"
}
```

Future implementations:
-- not defined --

Future deprecations:
```JSON
{
    "pywin32": "224"
}
```

#### Live Example:
*Not available yet*

#### Simple Local Run:
_creates virtual env_
```Shell
pip install -r requiremetns.txt
python src/streamer.py "http://semobrn.sytes.net:1935/live/21.stream/playlist.m3u8"
```
**OBS**: _this example url is a public security camera from Natal, Brazil_

| Field     | Obrigatory    | Description                       | Input type        | Default value
| ---       | ---           | ---                               | ---               | ---
| sources   | yes           | source to have objects identified | Array of Strings  | None
| queues    | no            | set queue maximum size for frames | Integer           | 60
| help      | no            | show this help message and exit   | --                | --
| debug     | no            | process debug flag                | --                | --
| version   | no            | output software version           | --                | --

#### TODO:

- Get video from an URL and retrieve its frames [OK]
- Implement a thread for video buffering like function [OK]
- **Split code on stream, identifier and main in spearated files for better use of python module structure** [PENDING]
- **Set function for identify array size and fix frame shapes for better visualize multi video input** [PENDING]
- **Add a multithread to avoid server problems on delay  for its video stream** [PENDING]
- **Identify simple objects like car or cats to verify specific case of use** [PENDING]
- **Generalize object identification as modules to be passed within command lines or arument on function calls** [PENDING]