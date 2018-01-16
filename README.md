1. Prerequisites.
 - OS: tested on Linux Fedora 24;
 - Python 3.5.3 or higher;
 - Redis 3.2.8 or higher;
 - Py-redis 2.10.3 or higher;
 - Python RQ 0.10.0 or higher;

Clone the repository to some local directory (/path/to/application/).
Execute the next step from repo directory (/path/to/application/).

2. Deploy platform and application.
 - Make sure that all prerequisites are satisfied.
 - Start Redis server.
    E.g. for RH-like:
      sudo service redis start

 - Start RQ workers.
    RQ is a simple Python library for queueing jobs and processing them in the background with workers.
    Each worker will process a single job at a time. If you want to perform jobs concurrently, simply start more workers.

    It is recommended to use background mode and nohup logging to start RQ workers.

    RQ workers startup using default settings (run it twice to have two running jobs at the same time):

    nohup rq worker &

    Check nohup log for any issues.

 - Start the application.
    It is recommended to use background mode and nohup logging to start RQ workers.

    nohup ./app.py &

    Check nohup log for any issues.
    If anything is OK you will see something like

    22:48:00 RQ worker 'rq:worker:numenor.6023' started, version 0.10.0
22:48:00 *** Listening on default...
22:48:00 Cleaning registries for queue: default
22:48:02 RQ worker 'rq:worker:numenor.6038' started, version 0.10.0
22:48:02 *** Listening on default...
22:48:02 Cleaning registries for queue: default
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 523-202-160

3. Usage.

  - Counter job.

    The service supports GET and POST requests. You can use curl utility to send necessary requests to the service.

    E.g.
    To create the new job:

    request:
    curl -i -H "Content-Type: application/json" -X POST -d '{"url":"http://yandex.ru"}' http://127.0.0.1:5000/v1/task

    response:

    HTTP/1.0 201 CREATED
    Content-Type: application/json
    Content-Length: 57
    Server: Werkzeug/0.14.1 Python/3.5.3
    Date: Tue, 16 Jan 2018 19:52:16 GMT

    {
      "task_uuid": "740b0acc-1d1f-4ce2-81a0-23c70dce897d"
    }

    To show result:

    Use Job_UUID from previous point to get job:

    request:
    [isilme@numenor py_tags_counter]$ curl -i -H "Content-Type: application/json" -X GET -d '{"task_uuid":"740b0acc-1d1f-4ce2-81a0-23c70dce897d"}' http://127.0.0.1:5000/v1/task

    response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 625
    Server: Werkzeug/0.14.1 Python/3.5.3
    Date: Tue, 16 Jan 2018 19:55:04 GMT

    {
      "Result": {
        "a": 129,
        "aqwf": 26,
        "body": 1,
        "button": 3,
        "dbgrsae": 20,
        "dhtaq": 19,
        "div": 245,
        "dqs": 21,
        "edvrt": 27,
        "eflll": 24,
        "fdpprt": 21,
        "fgn": 20,
        "form": 2,
        "ftgr": 15,
        "fwap": 17,
        "h1": 11,
        "head": 1,
        "html": 1,
        "i": 13,
        "img": 7,
        "input": 6,
        "label": 3,
        "li": 55,
        "link": 12,
        "meta": 15,
        "noscript": 4,
        "ol": 4,
        "path": 1,
        "pjtr": 24,
        "script": 19,
        "span": 111,
        "style": 2,
        "svg": 1,
        "title": 1,
        "ul": 9
      },
      "Status": "done"
    }

4. Queued jobs.

    Usually job works not too long to have 'QUEUED' status for a long time.
    Please use test API '/v1/test_task' to check it.

    Create:
    request:
    [isilme@numenor py_tags_counter]$ curl -i -X POST  http://127.0.0.1:5000/v1/test_task

    response:
    HTTP/1.0 201 CREATED
    Content-Type: application/json
    Content-Length: 58
    Server: Werkzeug/0.14.1 Python/3.5.3
    Date: Tue, 16 Jan 2018 20:07:38 GMT

    {
      "task_uuid": "e36ac7aa-f34c-4e87-a4d1-bfd7ff00abcc"
    }

    Get result:
    request:
    [isilme@numenor py_tags_counter]$ curl -i -H "Content-Type: application/json" -X GET -d '{"task_uuid":"e36ac7aa-f34c-4e87-a4d1-bfd7ff00abcc"}' http://127.0.0.1:5000/v1/test_task

    response:
      HTTP/1.0 200 OK
      Content-Type: application/json
      Content-Length: 53
      Server: Werkzeug/0.14.1 Python/3.5.3
      Date: Tue, 16 Jan 2018 20:07:48 GMT

      {
        "Result": "",
        "Status": [
          "running"
        ]
      }

      Create:

      request:
      [isilme@numenor py_tags_counter]$ curl -i -X POST  http://127.0.0.1:5000/v1/test_task

      response:
      HTTP/1.0 201 CREATED
      Content-Type: application/json
      Content-Length: 58
      Server: Werkzeug/0.14.1 Python/3.5.3
      Date: Tue, 16 Jan 2018 20:07:58 GMT

      {
        "task_uuid": "dca567a5-ae90-42e0-8127-64fbcdd50251"
      }

      Get result:

      request:
      [isilme@numenor py_tags_counter]$ curl -i -H "Content-Type: application/json" -X GET -d '{"task_uuid":"dca567a5-ae90-42e0-8127-64fbcdd50251"}' http://127.0.0.1:5000/v1/test_task

      response:
      HTTP/1.0 200 OK
      Content-Type: application/json
      Content-Length: 52
      Server: Werkzeug/0.14.1 Python/3.5.3
      Date: Tue, 16 Jan 2018 20:08:12 GMT

      {
        "Result": "",
        "Status": [
          "queued"
        ]
      }
