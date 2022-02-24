
# PDF Render API

Web API used to upload a PDF file. From this file are asynchronously rendered PNG images with size 1200x1600px and 600dpi. API accepted file and verifies it, then save him to local disk and database after that return id from database. The file is then processed in the background using combination of [Dramatiq](https://dramatiq.io/) library and [RabbitMQ](https://www.rabbitmq.com/) as message broker for worker queue. When all images(pages from PDF) are processed update status about PDF(save status to processed). At all times, information about the progress of the PDF file is available at the relevant link and document id. This is retrieved as a response when the file is successfully uploaded.The individual processed images can then be downloaded using the relevant link and image id. which is available in the information about the processed document.


# How to use
In first to download project

```
git clone https://github.com/DireFael/PDF-render-api.git
```

In folder ``PDF-render-api`` run:
```
docker-compose up
```

# Tests
They are not implemented in docker-composer. I find it better to put them in ``git-lab-ci`` for example. However, there is a sample pytest for all modules in the ``tests`` folder and it can be run manually.

# Extensions
There is a large possibility to extend its functionality, mentioned in comments. However, this would imply the need to develop a larger and more robust application/code. Thus, I have tried to keep some features as simple as possible even at the cost of not having a more efficient or clear solution.