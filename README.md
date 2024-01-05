## <table cellspacing="0" cellpadding="0"><tr><td><p align="center"><img src="/images/movie.png" width="50"></td><td align='center'>MoviePulse: Feeling the Pulse in Cinema - AI-Powered Emotion Forecasting for Box Office Prediction</td><td><img src="/images/pulse.png" width="50"></p></td></tr></table>

> [!TIP]
> [Demo page](https://moviepulse.github.io/): https://moviepulse.github.io 

### Instructions for installation and run this web-based APP

>[!NOTE]
> Download the entire website folder and put it on your local computer.<br>
> Due to the size limit, the saved model (variables.data-00000-of-00001) is included in the [here](https://drive.google.com/file/d/1cKxYXUyXzve-BlB1VXocEOEAQU0ePBxz).<br>
> You can also download it from [here](https://drive.google.com/file/d/13ABwzHWUnYXIHLK0jgykN9vMlzhD4ogW).


> Create a virtual environment
```
$ mkdir myproject
$ cd myproject
$ python -m venv myenv
```

> Activate the environment
```
$ . myenv/bin/activate
```
> Install Flask
```
$ pip3 install Flask
```

> Install the following packages: tensorflow, keras, scikit-learn, keras_retinanet, requests, matplotlib
```
$ pip3 install tensorflow
$ pip3 install keras
$ pip3 install scikit-learn
$ pip3 install keras_retinanet
$ pip3 install requests
$ pip3 install matplotlib
```

> Run your flask App under your virtual environment
```
$ python app.py
```
> [!WARNING] 
> <b>Before run this Python file, please use your own GPT API key on line 13</b>


> After running this command, you should be able to see the following message in the terminal:
```
* Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 141-477-686
```
> Go to your web browser (e.g., Google Chrome) and type http://127.0.0.1:5000. The App is then ready to use. 
