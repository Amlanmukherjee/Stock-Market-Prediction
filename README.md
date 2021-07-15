# Stock-Market-Prediction
Stock market prediction using FBprophet

<h3>What is Facebook Prophet?</h3>

Facebook Prophet is an open-source forecasting method implemented in Python and R. It provides automated forecasts. Prophet is used in many applications relating to time series data and to gather sample time forecast data. In the case of such models, getting exact future data is never possible, but we can somehow get the future trend.

<h3>Directory Tree Structure: </h3>

```
.
│
├── docker-compose.yml
├── flask
│   ├── Dockerfile
│   ├── app.ini
│   ├── app.py
│   ├── requirements.txt
│   ├── static
│   │   ├── background.png
│   │   ├── dygraph.css
│   │   ├── js
│   │   │   └── dygraph.js
│   │   ├── style.css
│   │   ├── style_result.css
│   │   └── video
│   │       └── video.mp4
│   └── templates
│       ├── index.html
│       ├── plot.html
│       └── result.html
└── nginx
    ├── Dockerfile
    └── nginx.conf

6 directories, 18 files

```

<h3>Requirements for this project: </h3>
- flask
- nginx
- gunicorn
- docker
- fbprophet
