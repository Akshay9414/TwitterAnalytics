# Online News streaming

## Step by step setup

* Create a free account on [streamdata.io](https://portal.streamdata.io/#/register) and [NewsApi](https://newsapi.org/) to get their App token

```bash
> cd Read\ News\ Stream
> pip3 install -r requirements.txt
```

* Edit ``streaming.py`` and replace ``[STREAMDATAIO_APP_TOKEN]``,``[NEWSAPI_APP_TOKEN]`` with your App token

* Finally, run the python script

```python
> python3 streaming.py
```