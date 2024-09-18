# tekken8_oneshot_replays
This is a pipeline of tekken8 replays' auto recorder and video processor.
Support Tekken8 on Steam (This game only support Windows).
Default recorder is Nvidia Shadow Play in Nvidia Experience.


## Navigate 🌍

  | [Recorde](#Recorde)
  | [Make Replays](#Make-Replays)


## Recorde

In Tekken 8 Online replay interface search for your replays and download them to your local stock. Go to the replay you downloaded then
````
.\script\Tekken8\recorder_t8.py
````

This will download video files in ./video/TK8/


## Make-Replays


Check hyper parameters in 
````
.\configure\Tekken8.yml
````
Then

````
.\script\Tekken8\one_shot_replays_t8.py
````

This will concatenate videos and draw scoreboard when who wins.
