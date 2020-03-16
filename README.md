# message-wordcloud

Wordcloud from messages in all the popular social media messaging platform.
Right now it supports:

- Facebook
- Whatsapp
- Instagram
- Hike

#### Sample Result:

You can find the result [here](http://tusharmakkar08.github.io/wordcloud.html). 

Sample screenshot: 
![alt text](wc_images/wordcloud.png)

#### Running code instructions

    python message_wordcloud.py --folder sample_data/ --ig_names "a" "b"

Help:

    usage: message_wordcloud.py [-h] --ig_names IG_NAMES IG_NAMES --folder FOLDER
    
    Argument parser for wordcloud
    
    optional arguments:
      -h, --help            show this help message and exit
      --ig_names IG_NAMES IG_NAMES
                            Instagram name list
      --folder FOLDER       Folder where files are present

Currently, we are expecting file names as follows:
* Facebook - `fb.json`
* Hike - `hike.txt`
* Instagram - `ig.json`
* Whatsapp - `wp.txt`

#### Downloading data instructions

###### Facebook:
* Go to settings 
![alt text](wc_images/fb1.png)
* Click on your facebook information and then click on download your information.
![alt text](wc_images/fb2.png)
* Select format as Json and select the message field from the list.
![alt text](wc_images/fb3.png)

###### Instagram:
* Go to settings > privacy and security 
![alt text](wc_images/ig1.png)
![alt text](wc_images/ig2.png)
* Then click on download data.
![alt text](wc_images/ig3.png)

###### Whatsapp:
* Go to more from the whatsapp chat
![alt text](wc_images/wp1.jpg)
* Click on export. 
![alt text](wc_images/wp2.jpg)

###### Hike:
* Go to profile of the chat and click on export.
![alt text](wc_images/hike1.jpg)


#### References

* [Anycloud](https://github.com/AnyChart/AnyChart)
